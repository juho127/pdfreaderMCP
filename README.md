# PDF Reader MCP Server

PDF 파일을 읽고 텍스트를 추출하는 MCP 서버입니다.

## 설치 방법

```bash
cd /home/basecamp/SceneAware/mcp-servers/pdf-reader
pip install -r requirements.txt
```

## MCP 설정

`~/.cursor/mcp.json` 또는 `/root/.cursor/mcp.json`에 다음을 추가하세요:

```json
{
  "mcpServers": {
    "pdf-reader": {
      "command": "python3",
      "args": [
        "/home/basecamp/SceneAware/mcp-servers/pdf-reader/server.py"
      ]
    }
  }
}
```

## 사용 가능한 도구

### 1. read_pdf
PDF 파일을 읽고 텍스트 내용을 추출합니다.

**파라미터:**
- `file_path` (필수): 읽을 PDF 파일의 경로
- `page_range` (선택): 읽을 페이지 범위
  - `"all"`: 모든 페이지 (기본값)
  - `"1-5"`: 1페이지부터 5페이지까지
  - `"1,3,5"`: 1, 3, 5 페이지만
  - `"1-3,7,10-12"`: 복합 범위

**예시:**
```python
# 모든 페이지 읽기
read_pdf(file_path="/home/basecamp/SceneAware/paper/retry.pdf")

# 특정 페이지만 읽기
read_pdf(file_path="/home/basecamp/SceneAware/paper/retry.pdf", page_range="1-10")
```

### 2. get_pdf_info
PDF 파일의 메타데이터 정보를 가져옵니다.

**파라미터:**
- `file_path` (필수): 정보를 얻을 PDF 파일의 경로

**예시:**
```python
get_pdf_info(file_path="/home/basecamp/SceneAware/paper/retry.pdf")
```

## 기능

- ✅ PDF 텍스트 추출
- ✅ 페이지 범위 지정
- ✅ PDF 메타데이터 조회 (제목, 저자, 생성일 등)
- ✅ 한글 지원

## 의존성

- `mcp>=1.0.0`: Model Context Protocol 서버 라이브러리
- `pymupdf>=1.24.0`: PDF 처리 라이브러리 (PyMuPDF)

## 문제 해결

### ImportError: mcp package not found
```bash
pip install mcp
```

### ImportError: fitz (PyMuPDF) not found
```bash
pip install pymupdf
```

## Cursor 재시작

설정 변경 후 Cursor를 재시작하면 새로운 MCP 서버가 활성화됩니다.

## License

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

