"""
Document Converter MCP Server
Converts PDFs and Office files to Markdown for academic research.
"""

from fastmcp import FastMCP
from pathlib import Path
from typing import Optional
import subprocess
import sys
import shutil
import tempfile
import platform

mcp = FastMCP("document-converter")

# File type mappings
OFFICE_EXTS = {'.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.odt', '.odp', '.ods', '.rtf'}
PDF_EXT = '.pdf'
SUPPORTED_EXTS = OFFICE_EXTS | {PDF_EXT}


def find_soffice() -> Optional[str]:
    """Find LibreOffice soffice executable."""
    path = shutil.which('soffice')
    if path:
        return path
    
    system = platform.system()
    if system == 'Windows':
        candidates = [
            r'C:\Program Files\LibreOffice\program\soffice.exe',
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
        ]
        for c in candidates:
            if Path(c).exists():
                return c
    elif system == 'Darwin':
        candidate = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
        if Path(candidate).exists():
            return candidate
    return None


@mcp.tool()
async def convert_to_markdown(
    input_path: str,
    output_path: Optional[str] = None,
    fallback_to_markitdown: bool = True
) -> dict:
    """
    Convert a PDF or Office document to Markdown.
    
    Supported formats:
    - PDF: Direct conversion via pymupdf4llm
    - Office: docx, doc, pptx, ppt, xlsx, xls, odt, odp, ods, rtf
      (Converts to PDF first via LibreOffice, then to Markdown)
    
    Args:
        input_path: Path to input file
        output_path: Path for output .md file (optional, defaults to input name + .md)
        fallback_to_markitdown: Use markitdown CLI as fallback
    
    Returns:
        Dictionary with conversion result
    """
    input_file = Path(input_path).resolve()
    
    if not input_file.exists():
        return {"success": False, "error": f"File not found: {input_path}"}
    
    if not input_file.is_file():
        return {"success": False, "error": f"Not a file: {input_path}"}
    
    ext = input_file.suffix.lower()
    if ext not in SUPPORTED_EXTS:
        return {
            "success": False,
            "error": f"Unsupported format: {ext}. Supported: {', '.join(sorted(SUPPORTED_EXTS))}"
        }
    
    # Determine output path
    if output_path:
        output_file = Path(output_path).resolve()
    else:
        output_file = input_file.with_suffix('.md')
    
    try:
        if ext == PDF_EXT:
            # PDF conversion
            result = _convert_pdf_to_markdown(input_file, output_file)
        elif ext in OFFICE_EXTS:
            # Office conversion
            result = _convert_office_to_markdown(input_file, output_file, fallback_to_markitdown)
        else:
            return {"success": False, "error": f"Unsupported extension: {ext}"}
        
        if result["success"]:
            content = output_file.read_text(encoding='utf-8')
            return {
                "success": True,
                "output_path": str(output_file),
                "content_length": len(content),
                "content_preview": content[:500] + "..." if len(content) > 500 else content
            }
        else:
            return result
            
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
async def get_supported_formats() -> dict:
    """
    Get list of supported document formats.
    
    Returns:
        Dictionary with supported formats
    """
    return {
        "pdf": [".pdf"],
        "office": sorted(OFFICE_EXTS),
        "all": sorted(SUPPORTED_EXTS)
    }


@mcp.tool()
async def batch_convert(
    input_directory: str,
    output_directory: Optional[str] = None,
    file_pattern: str = "*"
) -> dict:
    """
    Convert all supported documents in a directory.
    
    Args:
        input_directory: Path to directory containing documents
        output_directory: Path for output directory (optional, defaults to input_directory)
        file_pattern: Glob pattern for file selection (default: all files)
    
    Returns:
        Dictionary with batch conversion results
    """
    input_dir = Path(input_directory).resolve()
    
    if not input_dir.exists() or not input_dir.is_dir():
        return {"success": False, "error": f"Directory not found: {input_directory}"}
    
    # Determine output directory
    if output_directory:
        output_dir = Path(output_directory).resolve()
    else:
        output_dir = input_dir
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find matching files
    files = [f for f in input_dir.glob(file_pattern) if f.suffix.lower() in SUPPORTED_EXTS]
    
    if not files:
        return {"success": True, "message": "No supported files found", "converted": 0, "failed": 0}
    
    results = {"success": True, "converted": 0, "failed": 0, "errors": []}
    
    for file in files:
        output_file = output_dir / file.with_suffix('.md').name
        result = await convert_to_markdown(str(file), str(output_file))
        
        if result["success"]:
            results["converted"] += 1
        else:
            results["failed"] += 1
            results["errors"].append({"file": str(file), "error": result.get("error", "Unknown error")})
    
    return results


def _convert_pdf_to_markdown(input_file: Path, output_file: Path) -> dict:
    """Convert PDF to Markdown using pymupdf4llm."""
    try:
        import pymupdf4llm
        md_text = pymupdf4llm.to_markdown(str(input_file))
        output_file.write_text(md_text, encoding='utf-8')
        return {"success": True}
    except ImportError:
        return {"success": False, "error": "pymupdf4llm not installed. Run: pip install pymupdf4llm"}
    except Exception as e:
        return {"success": False, "error": f"PDF conversion failed: {str(e)}"}


def _convert_office_to_markdown(input_file: Path, output_file: Path, fallback: bool) -> dict:
    """Convert Office file to Markdown via PDF intermediate."""
    soffice = find_soffice()
    
    if not soffice:
        if fallback:
            return _convert_with_markitdown(input_file, output_file)
        return {"success": False, "error": "LibreOffice not found. Install LibreOffice or enable fallback."}
    
    # Create temp directory for intermediate PDF
    tmp_dir = Path(tempfile.mkdtemp(prefix="office2md_"))
    
    try:
        # Convert Office to PDF
        expected_pdf = tmp_dir / (input_file.stem + '.pdf')
        cmd = [soffice, '--headless', '--convert-to', 'pdf', '--outdir', str(tmp_dir), str(input_file)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if not expected_pdf.exists():
            if fallback:
                return _convert_with_markitdown(input_file, output_file)
            err = result.stderr.strip()[:200] if result.stderr else 'unknown error'
            return {"success": False, "error": f"LibreOffice conversion failed: {err}"}
        
        # Convert PDF to Markdown
        pdf_result = _convert_pdf_to_markdown(expected_pdf, output_file)
        
        if pdf_result["success"]:
            return {"success": True}
        elif fallback:
            return _convert_with_markitdown(input_file, output_file)
        else:
            return pdf_result
            
    except subprocess.TimeoutExpired:
        if fallback:
            return _convert_with_markitdown(input_file, output_file)
        return {"success": False, "error": "LibreOffice conversion timed out"}
    except Exception as e:
        if fallback:
            return _convert_with_markitdown(input_file, output_file)
        return {"success": False, "error": str(e)}
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _convert_with_markitdown(input_file: Path, output_file: Path) -> dict:
    """Convert using markitdown CLI as fallback."""
    try:
        result = subprocess.run(
            ['markitdown', str(input_file), '-o', str(output_file)],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and output_file.exists():
            return {"success": True}
        else:
            err = result.stderr.strip()[:200] if result.stderr else f"markitdown exit code {result.returncode}"
            return {"success": False, "error": f"markitdown failed: {err}"}
    except FileNotFoundError:
        return {"success": False, "error": "markitdown not installed. Run: pip install markitdown"}
    except Exception as e:
        return {"success": False, "error": f"markitdown failed: {str(e)}"}


if __name__ == "__main__":
    mcp.run()
