# PDF Reader MCP Server

An MCP server for reading PDF files and extracting text content. (PDF 파일을 읽고 텍스트를 추출하는 MCP 서버)

## Installation (설치 방법)

```bash
cd /path/to/pdfreaderMCP
pip install -r requirements.txt
```

## MCP Configuration (MCP 설정)

Add the following to your `~/.cursor/mcp.json` or `/root/.cursor/mcp.json`:

(`~/.cursor/mcp.json` 또는 `/root/.cursor/mcp.json`에 다음을 추가하세요)

```json
{
  "mcpServers": {
    "pdf-reader": {
      "command": "python3",
      "args": [
        "/absolute/path/to/server.py"
      ]
    }
  }
}
```

**Note:** Replace `/absolute/path/to/server.py` with the actual path to your `server.py` file.

(경로를 실제 `server.py` 파일 위치로 변경하세요)

## Available Tools (사용 가능한 도구)

### 1. read_pdf
Reads a PDF file and extracts text content. (PDF 파일을 읽고 텍스트 내용을 추출합니다)

**Parameters (파라미터):**
- `file_path` (required/필수): Path to the PDF file to read (읽을 PDF 파일의 경로)
- `page_range` (optional/선택): Page range to read (읽을 페이지 범위)
  - `"all"`: All pages (default) (모든 페이지, 기본값)
  - `"1-5"`: Pages 1 to 5 (1페이지부터 5페이지까지)
  - `"1,3,5"`: Pages 1, 3, and 5 only (1, 3, 5 페이지만)
  - `"1-3,7,10-12"`: Mixed range (복합 범위)

**Example (예시):**
```python
# Read all pages (모든 페이지 읽기)
read_pdf(file_path="/path/to/document.pdf")

# Read specific pages (특정 페이지만 읽기)
read_pdf(file_path="/path/to/document.pdf", page_range="1-10")
```

### 2. get_pdf_info
Retrieves PDF metadata information. (PDF 파일의 메타데이터 정보를 가져옵니다)

**Parameters (파라미터):**
- `file_path` (required/필수): Path to the PDF file (정보를 얻을 PDF 파일의 경로)

**Example (예시):**
```python
get_pdf_info(file_path="/path/to/document.pdf")
```

## Features (기능)

- ✅ PDF text extraction (PDF 텍스트 추출)
- ✅ Page range specification (페이지 범위 지정)
- ✅ PDF metadata retrieval (title, author, dates, etc.) (메타데이터 조회: 제목, 저자, 생성일 등)
- ✅ Unicode support (Korean, Chinese, Japanese, etc.) (유니코드 지원: 한글, 중국어, 일본어 등)

## Dependencies (의존성)

- `mcp>=1.0.0`: Model Context Protocol server library (MCP 서버 라이브러리)
- `pymupdf>=1.24.0`: PDF processing library (PyMuPDF) (PDF 처리 라이브러리)

## Troubleshooting (문제 해결)

### ImportError: mcp package not found
```bash
pip install mcp
```

### ImportError: fitz (PyMuPDF) not found
```bash
pip install pymupdf
```

## Restart Cursor (Cursor 재시작)

After configuration changes, restart Cursor to activate the new MCP server.

(설정 변경 후 Cursor를 재시작하면 새로운 MCP 서버가 활성화됩니다)

## License

MIT License - Free to use, modify, and distribute. (자유롭게 사용, 수정, 배포 가능합니다)

See the [LICENSE](LICENSE) file for details. (자세한 내용은 LICENSE 파일을 참고하세요)

