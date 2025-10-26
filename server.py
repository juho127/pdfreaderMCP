#!/usr/bin/env python3
"""
PDF Reader MCP Server
PDF 파일을 읽고 텍스트를 추출하는 MCP 서버입니다.
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent, INVALID_PARAMS, INTERNAL_ERROR
    import mcp.server.stdio
except ImportError:
    print("Error: mcp package not found. Please install it with: pip install mcp", file=sys.stderr)
    sys.exit(1)


# MCP 서버 초기화
server = Server("pdf-reader")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록을 반환합니다."""
    return [
        Tool(
            name="read_pdf",
            description="PDF 파일을 읽고 텍스트 내용을 추출합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "읽을 PDF 파일의 경로"
                    },
                    "page_range": {
                        "type": "string",
                        "description": "읽을 페이지 범위 (예: '1-5', '1,3,5', 'all'). 기본값: 'all'",
                        "default": "all"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="get_pdf_info",
            description="PDF 파일의 메타데이터 정보를 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "정보를 얻을 PDF 파일의 경로"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]


def parse_page_range(page_range_str: str, total_pages: int) -> list[int]:
    """페이지 범위 문자열을 파싱하여 페이지 번호 리스트를 반환합니다."""
    if page_range_str == "all":
        return list(range(total_pages))
    
    pages = set()
    parts = page_range_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            start_page = int(start) - 1  # 0-based index
            end_page = int(end)
            pages.update(range(max(0, start_page), min(total_pages, end_page)))
        else:
            page_num = int(part) - 1  # 0-based index
            if 0 <= page_num < total_pages:
                pages.add(page_num)
    
    return sorted(list(pages))


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """도구 호출을 처리합니다."""
    
    if not fitz:
        return [TextContent(
            type="text",
            text="Error: PyMuPDF (fitz) is not installed. Please install it with: pip install pymupdf"
        )]
    
    try:
        if name == "read_pdf":
            file_path = arguments.get("file_path")
            page_range = arguments.get("page_range", "all")
            
            if not file_path:
                raise ValueError("file_path is required")
            
            path = Path(file_path)
            if not path.exists():
                return [TextContent(
                    type="text",
                    text=f"Error: File not found: {file_path}"
                )]
            
            if not path.suffix.lower() == '.pdf':
                return [TextContent(
                    type="text",
                    text=f"Error: File is not a PDF: {file_path}"
                )]
            
            # PDF 열기
            doc = fitz.open(file_path)
            total_pages = len(doc)
            
            # 페이지 범위 파싱
            pages_to_read = parse_page_range(page_range, total_pages)
            
            # 텍스트 추출
            text_content = []
            for page_num in pages_to_read:
                page = doc[page_num]
                text = page.get_text()
                text_content.append(f"=== Page {page_num + 1} ===\n{text}\n")
            
            doc.close()
            
            result = "\n".join(text_content)
            return [TextContent(
                type="text",
                text=f"PDF: {file_path}\nTotal pages: {total_pages}\nPages read: {len(pages_to_read)}\n\n{result}"
            )]
        
        elif name == "get_pdf_info":
            file_path = arguments.get("file_path")
            
            if not file_path:
                raise ValueError("file_path is required")
            
            path = Path(file_path)
            if not path.exists():
                return [TextContent(
                    type="text",
                    text=f"Error: File not found: {file_path}"
                )]
            
            # PDF 열기
            doc = fitz.open(file_path)
            
            # 메타데이터 수집
            metadata = doc.metadata
            info = {
                "file_path": str(path.absolute()),
                "total_pages": len(doc),
                "title": metadata.get("title", "N/A"),
                "author": metadata.get("author", "N/A"),
                "subject": metadata.get("subject", "N/A"),
                "creator": metadata.get("creator", "N/A"),
                "producer": metadata.get("producer", "N/A"),
                "creation_date": metadata.get("creationDate", "N/A"),
                "modification_date": metadata.get("modDate", "N/A")
            }
            
            doc.close()
            
            result = json.dumps(info, indent=2, ensure_ascii=False)
            return [TextContent(
                type="text",
                text=f"PDF Information:\n{result}"
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """서버를 시작합니다."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

