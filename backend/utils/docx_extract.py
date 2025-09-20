from fastapi import HTTPException
import mammoth
from io import BytesIO
from pdf2docx import Converter
import tempfile, os, asyncio, docx2txt, re


def docx_to_markdown(docx_bytes: bytes) -> str:
    result = mammoth.convert_to_markdown(BytesIO(docx_bytes))
    md = result.value.strip()
    return md
    
async def docx_to_txt(data: bytes) -> str:
    if not data:
        raise HTTPException(status_code=400, detail="Файл пустой")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    try:
        tmp.write(data)
        tmp.flush()
        tmp.close()
        text = await asyncio.to_thread(docx2txt.process, tmp.name)
        text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
        return _clean_text(text)
    finally:
        try:
            os.remove(tmp.name)
        except OSError:
            pass
        
async def pdf_to_docx(pdf_bytes: bytes, start: int = 0, end: int | None = None) -> bytes:
    """
    Принимает PDF в байтах и возвращает готовый DOCX в байтах
    """
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Файл пустой")

    pdf_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    docx_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    try:
        pdf_tmp.write(pdf_bytes)
        pdf_tmp.flush()
        pdf_tmp.close()
        docx_tmp.close()

        # отдельный поток для конвертации
        await asyncio.to_thread(_convert_pdf_path_to_docx_path, pdf_tmp.name, docx_tmp.name, start, end)

        with open(docx_tmp.name, "rb") as f:
            docx_bytes = f.read()
        if not docx_bytes:
            raise HTTPException(status_code=500, detail="Не удалось сконвертировать PDF в DOCX")
        return docx_bytes
    finally:
        for p in (pdf_tmp.name, docx_tmp.name):
            try:
                os.remove(p)
            except OSError:
                pass
            
async def pdf_to_txt_via_docx(pdf_bytes: bytes, start: int = 0, end: int | None = None) -> str:
    """
    Конвертирует PDF в DOCX и затем переиспользует docx_to_txt
    """
    docx_bytes = await pdf_to_docx(pdf_bytes, start=start, end=end)
    return await docx_to_txt(docx_bytes)
            
def _convert_pdf_path_to_docx_path(pdf_path: str, docx_path: str, start: int = 0, end: int | None = None) -> None:
    """
    Конвертирует PDF-файл (по пути) в DOCX-файл (по пути).
    end=None -> до конца PDF. Нумерация страниц как в pdf2docx (0-based).
    """
    cv = Converter(pdf_path)
    try:
        cv.convert(docx_path, start=start, end=end)
    finally:
        cv.close()

def _clean_text(text: str) -> str:
  
    # нормализуем переводы строк и неразрывные пробелы
    text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\u00A0', ' ')

    # email, телефоны, URLs
    text = re.sub(r'\bhttps?://\S+|www\.\S+\b', '', text)

    # номера страниц и мусор
    text = re.sub(r'(?i)Page\s+\d+\s+of\s+\d+', '', text)
    text = re.sub(r'(?i)Страница\s+\d+\s+из\s+\d+', '', text)

    # спецсимволы (оставляем буквы/цифры, пробел, таб, перевод строки и базовую пунктуацию)
    text = re.sub(r'[^\w \t\n.,!?;:()\-+@]', '', text)

    # множественные пробелы
    text = re.sub(r'[ \u00A0]{2,}', ' ', text)

    # убрать пустые строки
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()