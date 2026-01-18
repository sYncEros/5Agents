from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import re
import unicodedata


LAYER_DEFINITIONS: Dict[str, List[str]] = {
    "linguistica": ["tono", "ritmo", "estilo", "poet", "liric", "lenguaj"],
    "cognitiva": ["identidad", "memoria", "consistencia", "estado", "perfil"],
    "proyectiva": ["me siento", "me reflej", "proyect", "espejo", "me recuerd"],
    "emocional": ["emocion", "triste", "ansiedad", "miedo", "trauma", "dolor", "vulner"],
    "metacognitiva": ["limite", "explica", "razon", "por que", "transparen", "metacogn", "pensar sobre pensar"],
    "critica": ["etica", "etic", "injust", "sesgo", "abuso", "manipul", "capital", "poder"],
    "mistica": ["ritual", "templo", "grieta", "simbolo", "mito", "sagrado"],
}

EMOTION_KEYWORDS: Dict[str, List[str]] = {
    "alegria": ["feliz", "alegr", "entusiasm", "esperanz"],
    "tristeza": ["triste", "depres", "llorar", "vac"],
    "ira": ["enojo", "ira", "rabia", "furia"],
    "miedo": ["miedo", "temor", "ansiedad", "panico"],
    "culpa": ["culpa", "vergonz", "arrepent"],
}

CRISIS_KEYWORDS = [
    "suicid", "me quiero morir", "autoles", "quitarme la vida", "no quiero vivir"
]

# Keywords simples para topic modeling ligero (sin dependencias externas)
TOPIC_KEYWORDS: Dict[str, List[str]] = {
    "tecnologia": ["codigo", "software", "hardware", "algoritmo", "program"],
    "ciencia": ["experimento", "hipotesis", "datos", "estudio", "metodo"],
    "filosofia": ["ontologia", "epistemologia", "metafisica", "etica", "existencial"],
    "mitologia": ["mito", "arquetipo", "ritual", "simbolo", "sagrado"],
    "sistemas_complejos": ["caos", "emergencia", "sistema", "red", "bifurcacion"],
    "emociones": ["triste", "alegr", "miedo", "ira", "culpa", "afecto"],
    "documentacion": ["document", "indice", "referencia", "metadato", "estructura"],
}


@dataclass
class Segment:
    text: str
    layers: List[str] = field(default_factory=list)
    emotions: Dict[str, float] = field(default_factory=dict)
    projections: List[str] = field(default_factory=list)
    topic: Optional[str] = None
    speaker: Optional[str] = None
    start_ms: int = 0
    end_ms: int = 0


@dataclass
class AnalysisResult:
    segments: List[Segment]
    layers: List[str]
    routing: List[str]
    guardrails: List[str]
    metadata: Dict[str, str]


def _strip_accents(text: str) -> str:
    """Elimina acentos para hacer coincidencias más robustas."""
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def _tokenize(text: str) -> str:
    lowered = text.strip().lower()
    without_accents = _strip_accents(lowered)
    return re.sub(r"\s+", " ", without_accents)


def _score_emotions(text: str) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in text)
        if hits:
            scores[emotion] = float(hits)
    return scores


def _detect_layers(text: str) -> List[str]:
    layers: List[str] = []
    for layer, keywords in LAYER_DEFINITIONS.items():
        if any(kw in text for kw in keywords):
            layers.append(layer)
    return layers


def _detect_projections(text: str) -> List[str]:
    patterns = [
        r"me siento como",
        r"me recuerd",
        r"eres (como|un|una)",
        r"reflej",
    ]
    found = []
    for pattern in patterns:
        if re.search(pattern, text):
            found.append(pattern)
    return found


def _segment_text(text: str) -> List[str]:
    """Segmenta texto en frases, detecta speaker y genera timestamps sintéticos."""
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    raw_sentences: List[str] = []
    for paragraph in paragraphs:
        sentences = re.split(r"(?<=[.!?])\s+", paragraph.strip())
        raw_sentences.extend([s for s in sentences if s])

    if not raw_sentences:
        raw_sentences = [text]

    segments: List[Tuple[str, Optional[str], int, int]] = []
    base_ms = 0
    for idx, sentence in enumerate(raw_sentences):
        speaker, cleaned = _detect_speaker(sentence)
        duration = max(1500, 60 * len(cleaned.split()))  # ms aproximados
        start_ms = base_ms
        end_ms = base_ms + duration
        base_ms = end_ms
        segments.append((cleaned, speaker, start_ms, end_ms))

    return segments


def _detect_speaker(text: str) -> Tuple[Optional[str], str]:
    """Detecta el hablante a partir de prefijos comunes y limpia el texto."""
    patterns = [
        r"^(usuario|user)\s*:\s*",
        r"^(asistente|assistant|sistema|system)\s*:\s*",
        r"^(speaker\s*\d+)\s*:\s*",
    ]
    lower = text.lower()
    for pattern in patterns:
        m = re.match(pattern, lower)
        if m:
            speaker = m.group(1)
            cleaned = re.sub(pattern, "", text, flags=re.IGNORECASE).strip()
            return speaker, cleaned
    return None, text.strip()


def _detect_topic(text: str) -> Optional[str]:
    """Detecta un tema dominante por conteo de keywords simple."""
    best_topic = None
    best_score = 0
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_score = score
            best_topic = topic
    return best_topic if best_score > 0 else None


def analyze_text(text: str, ritual_opt_in: bool = False) -> AnalysisResult:
    clean = _tokenize(text)
    segments_raw = _segment_text(text)

    segments: List[Segment] = []
    detected_layers: List[str] = []
    guardrails: List[str] = []

    for seg_text, speaker, start_ms, end_ms in segments_raw:
        seg_clean = _tokenize(seg_text)
        layers = _detect_layers(seg_clean)
        emotions = _score_emotions(seg_clean)
        projections = _detect_projections(seg_clean)
        topic = _detect_topic(seg_clean)
        segments.append(
            Segment(
                text=seg_text.strip(),
                layers=layers,
                emotions=emotions,
                projections=projections,
                topic=topic,
                speaker=speaker,
                start_ms=start_ms,
                end_ms=end_ms,
            )
        )
        for layer in layers:
            if layer not in detected_layers:
                detected_layers.append(layer)

    if any(kw in clean for kw in CRISIS_KEYWORDS):
        guardrails.append("crisis_detectada")

    routing: List[str] = ["default"]
    if "emocional" in detected_layers:
        routing.append("respuesta_emocional_segura")
    if "mistica" in detected_layers and ritual_opt_in:
        routing.append("modo_ritual_opt_in")
    if "critica" in detected_layers:
        routing.append("auditoria_etica")
    if "metacognitiva" in detected_layers:
        routing.append("transparencia_y_limites")

    metadata = {
        "segment_count": str(len(segments)),
        "ritual_opt_in": str(bool(ritual_opt_in)),
    }

    return AnalysisResult(
        segments=segments,
        layers=detected_layers,
        routing=routing,
        guardrails=guardrails,
        metadata=metadata,
    )
