from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

ALLOWED_TEXT_EXTENSIONS = {"txt", "md", "markdown"}
ALLOWED_DOC_EXTENSIONS = {"docx"}
ALLOWED_PDF_EXTENSIONS = {"pdf"}
ALLOWED_ARCHIVE_EXTENSIONS = {"zip"}


def _decode_text(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("latin-1")
        except Exception:
            return data.decode("utf-8", errors="ignore")


def _extract_txt(data: bytes) -> str:
    return _decode_text(data)


def _extract_docx(data: bytes) -> str:
    try:
        from docx import Document  # type: ignore
    except Exception as e:
        raise RuntimeError("Falta dependencia 'python-docx' para leer .docx") from e
    doc = Document(BytesIO(data))
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return "\n".join(paragraphs)


def _extract_pdf(data: bytes) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as e:
        raise RuntimeError("Falta dependencia 'pypdf' para leer .pdf") from e
    reader = PdfReader(BytesIO(data))
    texts: List[str] = []
    for page in reader.pages:
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        if txt:
            texts.append(txt)
    return "\n".join(texts)


def _extract_from_zip(data: bytes, depth: int = 0, max_depth: int = 2) -> List[Tuple[str, str]]:
    if depth > max_depth:
        return [("<zip:depth_exceeded>", "")] 
    out: List[Tuple[str, str]] = []
    with zipfile.ZipFile(BytesIO(data)) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = info.filename
            try:
                file_bytes = zf.read(info)
            except Exception:
                continue
            ext = name.lower().rsplit(".", 1)[-1] if "." in name else ""
            if ext in ALLOWED_TEXT_EXTENSIONS:
                out.append((name, _extract_txt(file_bytes)))
            elif ext in ALLOWED_DOC_EXTENSIONS:
                out.append((name, _extract_docx(file_bytes)))
            elif ext in ALLOWED_PDF_EXTENSIONS:
                out.append((name, _extract_pdf(file_bytes)))
            elif ext in ALLOWED_ARCHIVE_EXTENSIONS:
                nested = _extract_from_zip(file_bytes, depth=depth + 1, max_depth=max_depth)
                out.extend([(f"{name}/{n}", t) for (n, t) in nested])
            else:
                # Ignorar tipos no soportados
                continue
    return out


def cargar_entradas(files: Iterable, max_files: int = 1000, max_total_text_mb: int = 1000, 
                   usar_limites: bool = True) -> Tuple[str, List[str]]:
    """
    Acepta una colección de archivos (Streamlit UploadedFile o similares) y
    retorna un único texto concatenado y una lista de nombres procesados.
    
    Args:
        files: Colección de archivos a procesar
        max_files: Máximo número de archivos a procesar (si usar_limites=True)
        max_total_text_mb: Límite de texto total en MB (si usar_limites=True)
        usar_limites: Si False, procesa todos los archivos sin límites
    """
    if not files:
        return "", []

    corpus_parts: List[str] = []
    processed_names: List[str] = []
    total_text_bytes = 0
    processed_count = 0

    def within_limits() -> bool:
        if not usar_limites:
            return True
        if processed_count >= max_files:
            return False
        if (total_text_bytes / (1024 * 1024)) >= max_total_text_mb:
            return False
        return True

    for f in files:
        if not within_limits():
            break
            
        # Compatibilidad con Streamlit UploadedFile
        name = getattr(f, "name", "<archivo>")
        try:
            data: bytes = f.read() if hasattr(f, "read") else bytes(f)
        except Exception:
            # Streamlit puede requerir getvalue()
            data = f.getvalue() if hasattr(f, "getvalue") else b""

        ext = name.lower().rsplit(".", 1)[-1] if "." in name else ""

        try:
            if ext in ALLOWED_TEXT_EXTENSIONS:
                text = _extract_txt(data)
                corpus_parts.append(f"\n\n--- {name} ---\n\n{text}")
                processed_names.append(name)
                total_text_bytes += len(text.encode('utf-8', errors='ignore'))
            elif ext in ALLOWED_DOC_EXTENSIONS:
                text = _extract_docx(data)
                corpus_parts.append(f"\n\n--- {name} ---\n\n{text}")
                processed_names.append(name)
                total_text_bytes += len(text.encode('utf-8', errors='ignore'))
            elif ext in ALLOWED_PDF_EXTENSIONS:
                text = _extract_pdf(data)
                corpus_parts.append(f"\n\n--- {name} ---\n\n{text}")
                processed_names.append(name)
                total_text_bytes += len(text.encode('utf-8', errors='ignore'))
            elif ext in ALLOWED_ARCHIVE_EXTENSIONS:
                extracted = _extract_from_zip(data)
                for child_name, child_text in extracted:
                    if not within_limits():
                        break
                    corpus_parts.append(f"\n\n--- {child_name} ---\n\n{child_text}")
                    processed_names.append(child_name)
                    total_text_bytes += len(child_text.encode('utf-8', errors='ignore'))
                    processed_count += 1
            else:
                # Tratar como texto crudo por si acaso
                text = _extract_txt(data)
                if text.strip():
                    corpus_parts.append(f"\n\n--- {name} ---\n\n{text}")
                    processed_names.append(name)
                    total_text_bytes += len(text.encode('utf-8', errors='ignore'))
                    
            processed_count += 1
        finally:
            # Si el objeto soporta seek, reseteamos para no interferir con otros usos
            if hasattr(f, "seek"):
                try:
                    f.seek(0)
                except Exception:
                    pass

    return ("\n\n".join(corpus_parts).strip(), processed_names)


def _extract_from_zip_path(zip_path: Path, max_members: Optional[int] = None, max_depth: int = 2,
                           sample: bool = False, sample_max_files: int = 200,
                           max_total_text_mb: Optional[int] = 300) -> List[Tuple[str, str]]:
    """Extrae texto de un ZIP en disco sin cargar todo en memoria.
    - sample: si True, procesa solo los primeros sample_max_files miembros legibles.
    - max_total_text_mb: tope de texto acumulado para evitar consumo excesivo.
    """
    out: List[Tuple[str, str]] = []
    total_text_bytes = 0
    processed = 0
    def allowed_ext(name: str) -> str:
        return name.lower().rsplit(".", 1)[-1] if "." in name else ""

    def within_limits() -> bool:
        if sample and processed >= sample_max_files:
            return False
        if max_total_text_mb is not None and (total_text_bytes / (1024 * 1024)) >= max_total_text_mb:
            return False
        return True

    with zipfile.ZipFile(str(zip_path), 'r') as zf:
        for info in zf.infolist():
            if not within_limits():
                break
            if info.is_dir():
                continue
            name = info.filename
            ext = allowed_ext(name)
            try:
                file_bytes = zf.read(info)
            except Exception:
                continue
            text = ""
            if ext in ALLOWED_TEXT_EXTENSIONS:
                text = _extract_txt(file_bytes)
            elif ext in ALLOWED_DOC_EXTENSIONS:
                text = _extract_docx(file_bytes)
            elif ext in ALLOWED_PDF_EXTENSIONS:
                text = _extract_pdf(file_bytes)
            elif ext in ALLOWED_ARCHIVE_EXTENSIONS and max_depth > 0:
                try:
                    nested_pairs = _extract_from_zip(file_bytes, depth=1, max_depth=max_depth)
                except Exception:
                    nested_pairs = []
                for child_name, child_text in nested_pairs:
                    if not within_limits():
                        break
                    out.append((f"{name}/{child_name}", child_text))
                    total_text_bytes += len(child_text.encode('utf-8', errors='ignore'))
                    processed += 1
                continue
            else:
                continue
            out.append((name, text))
            total_text_bytes += len(text.encode('utf-8', errors='ignore'))
            processed += 1
            if max_members is not None and processed >= max_members:
                break
    return out


def cargar_entradas_desde_ruta(path_str: str, sample: bool = False, sample_max_files: int = 200,
                               max_total_text_mb: Optional[int] = 300) -> Tuple[str, List[str]]:
    """Carga entradas desde una ruta local (archivo .txt/.md/.docx/.pdf/.zip).
    Para ZIP grandes usa lectura en streaming con opciones de muestreo.
    """
    p = Path(path_str)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"No existe el archivo: {path_str}")
    ext = p.suffix.lower().lstrip('.')
    corpus_parts: List[str] = []
    processed_names: List[str] = []

    if ext in ALLOWED_TEXT_EXTENSIONS:
        text = _extract_txt(p.read_bytes())
        corpus_parts.append(f"\n\n--- {p.name} ---\n\n{text}")
        processed_names.append(p.name)
    elif ext in ALLOWED_DOC_EXTENSIONS:
        text = _extract_docx(p.read_bytes())
        corpus_parts.append(f"\n\n--- {p.name} ---\n\n{text}")
        processed_names.append(p.name)
    elif ext in ALLOWED_PDF_EXTENSIONS:
        text = _extract_pdf(p.read_bytes())
        corpus_parts.append(f"\n\n--- {p.name} ---\n\n{text}")
        processed_names.append(p.name)
    elif ext in ALLOWED_ARCHIVE_EXTENSIONS:
        pairs = _extract_from_zip_path(p, sample=sample, sample_max_files=sample_max_files,
                                       max_total_text_mb=max_total_text_mb)
        for name, text in pairs:
            corpus_parts.append(f"\n\n--- {name} ---\n\n{text}")
            processed_names.append(name)
    else:
        raise ValueError(f"Extensión no soportada: .{ext}")

    return ("\n\n".join(corpus_parts).strip(), processed_names)
