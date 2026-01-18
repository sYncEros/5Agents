#!/usr/bin/env python3
"""
run_pipeline.py
Orquesta pipeline: TopicsDetector -> ContextBuilder -> AgentsActivation -> Synthesis
Mejorado: CLI, debug, force, export JSONs por paso, reporte de agentes no activados con razón.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Intentar importar componentes usando los nombres que has usado en el repo.
try:
    from domain.analysis.TopicsDetector import TopicsDetector
except Exception as e:
    print("[ERROR] No pude importar TopicsDetector:", e)
    raise

# Agents system puede llamarse AgentsActivationSystem o SistemaActivacionAgentes según tu repo.
_agents_mod = None
try:
    from domain.analysis.AgentsSystem import AgentsActivationSystem as _agents_mod
except Exception:
    try:
        from domain.analysis.AgentsSystem import AgentsActivationSystem as _agents_mod
    except Exception as e:
        print("[ERROR] No pude importar AgentsActivationSystem / SistemaActivacionAgentes:", e)
        raise

try:
    from domain.analysis.SynthesisMotor import SynthesisMotor
except Exception as e:
    print("[ERROR] No pude importar SynthesisMotor:", e)
    raise

# Context builder (suele estar en pipelines/context_builder.py según conversación)
try:
    from pipelines.context_builder import build_activation_context, enriquecer_contexto, detectar_faltantes
except Exception:
    # Fallback: si no existe, construiremos el contexto de forma directa
    def build_activation_context(analisis_temas: Dict[str, Any], niveles=None, guia_sistema: str | None = None):
        niveles = niveles or {}
        planos = [p.value if hasattr(p, "value") else str(p) for p in analisis_temas.get("planos_activos", [])]
        temas = [t.nombre if hasattr(t, "nombre") else str(t) for t in analisis_temas.get("temas_explícitos", [])]
        contradicciones = analisis_temas.get("contradicciones_emergentes", []) or []
        bifurcaciones = analisis_temas.get("bifurcaciones_detectadas", []) or []
        from domain.analysis.ActivationContext import ActivationContext
        return ActivationContext(
            planos_detectados=planos,
            temas_principales=temas,
            contradicciones=contradicciones,
            bifurcaciones=bifurcaciones,
            nivel_abstraccion=float(niveles.get("abstraccion", 0.5)) if niveles else 0.5,
            nivel_especulacion=float(niveles.get("especulacion", 0.5)) if niveles else 0.5,
            nivel_tecnico=float(niveles.get("tecnico", 0.5)) if niveles else 0.5,
            guia_sistema=guia_sistema or ""
        )
    def enriquecer_contexto(ctx, analisis_temas): return ctx
    def detectar_faltantes(ctx): return []

# Utilities
def safe_mkdir(p: Path):
    try:
        p.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

def save_json(obj: Any, path: Path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[WARN] No se pudo guardar {path}: {e}")

def infer_reason_not_activated(agent, contexto):
    """
    Reproduce la heurística básica de activación para dar una razón
    (basada en AgentsSystem._es_relevante_para_contexto de tu código).
    """
    dominios_fuente = getattr(agent, 'dominios', None) or getattr(agent, 'fields', None) or []
    if isinstance(dominios_fuente, str):
        dominios_fuente = [dominios_fuente]
    agente_dominios = [str(d).lower() for d in dominios_fuente]

    temas = [str(t).lower() for t in getattr(contexto, 'temas_principales', [])]
    planos = [str(p).lower() for p in getattr(contexto, 'planos_detectados', [])]

    if not agente_dominios:
        return "Se activa por defecto (no declara dominios) — debería haberse activado"
    score = 0
    for t in temas:
        if any(t in d for d in agente_dominios):
            score += 1
    for p in planos:
        if any(p in d for d in agente_dominios):
            score += 1

    if score <= 0:
        # buscar faltantes específicos: plano técnico ausente
        if "tecnico" not in planos and any("tech" in d or "tecni" in d for d in agente_dominios):
            return "No se activó: faltó plano técnico detectado en el texto (requisito para este agente)"
        if not temas:
            return "No se activó: no hay temas principales detectados que coincidan con los dominios del agente"
        return "No se activó: coincidencia baja entre temas/plano y dominios del agente"
    return "No se activó por motivo desconocido (score>0 pero no en resultados)"

def pretty_plural(n):
    return f"{n}" if n == 1 else f"{n}"

def main(argv=None):
    p = argparse.ArgumentParser(prog="run_pipeline.py", description="Ejecuta pipeline: TopicsDetector -> Agents -> Synthesis")
    p.add_argument("--text", "-t", help="Texto para analizar (si se proporciona, ignora --file).", default=None)
    p.add_argument("--file", "-f", help="Archivo de texto a analizar (UTF-8).", default=None)
    p.add_argument("--force", "-F", help="Forzar activación de todos los agentes", action="store_true")
    p.add_argument("--debug", "-d", help="Habilitar debug en AgentsSystem / TopicsDetector si procede", action="store_true")
    p.add_argument("--slowdown", "-s", help="Ralentizar pasos de agentes (ms)", type=int, default=0)
    p.add_argument("--export-dir", "-o", help="Directorio donde guardar outputs (JSONs)", default="pipeline_outputs")
    p.add_argument("--show-reasons", help="Mostrar razones por las que agentes NO se activaron", action="store_true")
    p.add_argument("--no-enrich", help="No ejecutar enriquecer_contexto (si está disponible)", action="store_true")
    args = p.parse_args(argv)

    # Leer texto
    if args.text:
        texto = args.text.strip()
    elif args.file:
        fp = Path(args.file)
        if not fp.exists():
            print("[ERROR] Archivo no encontrado:", args.file); sys.exit(2)
        texto = fp.read_text(encoding="utf-8")
    else:
        print("Provee --text o --file (ej: python run_pipeline.py --text \"mi texto...\")")
        sys.exit(1)

    export_dir = Path(args.export_dir)
    safe_mkdir(export_dir)

    print("🚀 Pipeline transdisciplinario - inicio")
    t_all_start = time.perf_counter()

    # Paso 1: TopicsDetector
    t0 = time.perf_counter()
    detector = TopicsDetector(debug=bool(args.debug)) if "debug" in detector_init_args(detector_cls := TopicsDetector) else TopicsDetector()
    # Nota: si tu TopicsDetector acepta debug kwarg lo pasamos; helper detector_init_args gestiona eso.
    try:
        analisis_inicial = detector.analizar_conversacion(texto)
    except Exception as e:
        print("[ERROR] TopicsDetector falló:", e)
        raise
    dt = time.perf_counter() - t0
    print(f"✅ Paso 1 completado en {int(dt*1000)} ms — temas detectados: {len(analisis_inicial.get('temas_explícitos', []))}")

    # Guardar paso1
    paso1_path = export_dir / "paso1_deteccion.json"
    # serializar dataclasses/enums si existen: intentar usar método exportador del detector si lo tiene
    try:
        if hasattr(detector, "exportar_analisis"):
            detector.exportar_analisis(analisis_inicial, str(paso1_path))
        else:
            save_json(analisis_inicial, paso1_path)
    except Exception:
        save_json(analisis_inicial, paso1_path)

    # Construir ActivationContext (usando builder si existe)
    niveles = {"abstraccion": 0.7, "especulacion": 0.6, "tecnico": 0.5}
    try:
        contexto = build_activation_context(analisis_inicial, niveles=niveles, guia_sistema=None)
    except Exception as e:
        print("[WARN] build_activation_context falló, construyendo contexto directo:", e)
        from domain.analysis.ActivationContext import ActivationContext
        planes = [p.value if hasattr(p, "value") else str(p) for p in analisis_inicial.get("planos_activos", [])]
        temas = [t.nombre if hasattr(t, "nombre") else str(t) for t in analisis_inicial.get("temas_explícitos", [])]
        contexto = ActivationContext(planes, temas, analisis_inicial.get("contradicciones_emergentes", []),
                                     analisis_inicial.get("bifurcaciones_detectadas", []),
                                     niveles["abstraccion"], niveles["especulacion"], niveles["tecnico"])

    # Enriquecer contexto opcional
    if not args.no_enrich and 'enriquecer_contexto' in globals():
        try:
            contexto = enriquecer_contexto(contexto, {**analisis_inicial, "texto_original": texto})
        except Exception as e:
            print("[WARN] enriquecer_contexto falló:", e)

    # Guardar contexto resumido
    try:
        save_json(contexto.resumen(), export_dir / "paso1_contexto_resumen.json")
    except Exception:
        pass

    # Paso 2: Activación de agentes
    t0 = time.perf_counter()
    # Crear factory para hooks si el sistema lo acepta (mostrar logs en consola simple)
    def step_hook_factory(ag):
        def hook(step: dict):
            name = getattr(ag, 'nombre', getattr(ag, 'name', ag.__class__.__name__))
            ts = time.strftime("%H:%M:%S")
            title = step.get("title") or step.get("type") or "paso"
            # imprimir un mensaje conciso
            print(f"[{ts}] {name} — {title}")
        return hook

    # Instanciar sistema de agentes respetando la clase importada
    try:
        # la variable _agents_mod apunta a la clase importada
        SistemaClase = _agents_mod
        if SistemaClase is None:
            raise ImportError("No se pudo importar AgentsActivationSystem. Verifica el nombre del módulo y la ruta.")
        # Intentar detectar signature para pasar debug y slowdown_ms y step_hook_factory
        kwargs = {}
        try:
            params = detector_init_args(SistemaClase)
            if "debug" in params:
                kwargs["debug"] = bool(args.debug)
            if "slowdown_ms" in params:
                kwargs["slowdown_ms"] = int(args.slowdown)
            if "step_hook_factory" in params:
                kwargs["step_hook_factory"] = step_hook_factory
        except Exception:
            pass
        sistema = SistemaClase(**kwargs) if kwargs else SistemaClase()
    except Exception as e:
        print("[ERROR] No pude instanciar el sistema de agentes:", e)
        raise

    try:
        analisis_agentes = sistema.analizar_con_agentes(texto, contexto, forzar_todos=bool(args.force))
    except TypeError:
        # intentar sin forzar si la firma es otra
        analisis_agentes = sistema.analizar_con_agentes(texto, contexto)

    dt = time.perf_counter() - t0
    print(f"✅ Paso 2 completado en {int(dt*1000)} ms — agentes con salida: {len(analisis_agentes)}")

    # Guardar paso2 (serializar posibles objetos dentro)
    paso2_path = export_dir / "paso2_agentes.json"
    try:
        save_json(analisis_agentes, paso2_path)
    except Exception:
        # intentar serializar manualmente truncando objetos extraños
        serial = {}
        for k, v in (analisis_agentes or {}).items():
            try:
                serial[k] = v
            except Exception:
                try:
                    serial[k] = str(v)
                except Exception:
                    serial[k] = {"repr": repr(v)}
        save_json(serial, paso2_path)

    # Diagnóstico: listar agentes disponibles y los que no se activaron con razones
    agentes_totales = []
    try:
        agentes_totales = getattr(sistema, "agentes", []) or getattr(sistema, "agente", []) or []
    except Exception:
        agentes_totales = []

    activados_ids = set(analisis_agentes.keys() if isinstance(analisis_agentes, dict) else [])
    no_activados_report = []
    for ag in agentes_totales:
        try:
            ident = getattr(ag, 'identificador_tecnico', None) or getattr(ag, 'id', None) or getattr(ag, 'name', None) or ag.__class__.__name__
            if ident not in activados_ids:
                reason = infer_reason_not_activated(ag, contexto)
                no_activados_report.append({"id": ident, "nombre": getattr(ag, 'nombre', getattr(ag, 'name', ag.__class__.__name__)), "razon": reason})
        except Exception:
            continue

    if no_activados_report:
        print("ℹ️ Agentes que NO se activaron (motivos estimados):")
        for r in no_activados_report:
            print(f" - {r['nombre']} ({r['id']}): {r['razon']}")
    else:
        print("ℹ️ Todos los agentes cargados generaron salida (o forzados).")

    # Paso 3: Síntesis con SynthesisMotor
    t0 = time.perf_counter()
    motor = SynthesisMotor()
    try:
        sintesis = motor.sintetizar_analisis_agentes(analisis_agentes)
    except Exception as e:
        print("[ERROR] Motor de síntesis falló:", e)
        raise
    dt = time.perf_counter() - t0
    print(f"✅ Paso 3 completado en {int(dt*1000)} ms — madurez síntesis: {sintesis.nivel_madurez_sintesis:.3f}")

    # Guardar síntesis
    paso3_path = export_dir / "paso3_sintesis.json"
    try:
        motor.exportar_sintesis(sintesis, str(paso3_path))
    except Exception:
        try:
            save_json(sintesis.__dict__, paso3_path)
        except Exception:
            save_json({"nivel_madurez": getattr(sintesis, "nivel_madurez_sintesis", None)}, paso3_path)

    total_dt = time.perf_counter() - t_all_start
    print(f"\n🎉 Pipeline finalizado en {int(total_dt)} s")

    # Resumen para consola
    print("\n--- Resumen ---")
    print(f"Temas explícitos: {len(analisis_inicial.get('temas_explícitos', []))}")
    print(f"Agentes con resultado: {len(analisis_agentes)}")
    print(f"Agentes no activados (estim): {len(no_activados_report)}")
    print(f"Nivel madurez síntesis: {sintesis.nivel_madurez_sintesis:.3f}")

    # Guardar reporte final
    report = {
        "paso1": {"path": str(paso1_path), "tempo_ms": int(dt*1000)},
        "paso2": {"path": str(paso2_path)},
        "paso3": {"path": str(paso3_path)},
        "no_activados": no_activados_report,
        "madurez": getattr(sintesis, "nivel_madurez_sintesis", None)
    }
    save_json(report, export_dir / "pipeline_report.json")

    # Opcional: mostrar razones completas si requested
    if args.show_reasons and no_activados_report:
        print("\nDetalles (razones completas):")
        for r in no_activados_report:
            print(json.dumps(r, ensure_ascii=False, indent=2))

    return sintesis

# Helper que detecta si la clase acepta 'debug' o 'slowdown_ms' en su __init__
def detector_init_args(cls):
    try:
        import inspect
        sig = inspect.signature(cls.__init__)
        return sig.parameters
    except Exception:
        return {}

if __name__ == "__main__":
    main()

# API programático simple
def run_pipeline(texto: str,
                 force: bool = False,
                 debug: bool = False,
                 slowdown_ms: int = 0,
                 guia_sistema: str = "",
                 niveles: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Ejecuta el pipeline completo sobre un texto y devuelve un dict con temas y síntesis.

    Keys del resultado:
      - temas_explicitos: list[str]
      - temas_implicitos: list[str]
      - temas_emergentes: list[str]
      - sintesis: dict { nivel_madurez, hipotesis, paradigmas }
    """
    niveles = niveles or {"abstraccion": 0.7, "especulacion": 0.6, "tecnico": 0.5}

    # Paso 1: Detección
    detector = TopicsDetector(debug=bool(debug)) if "debug" in detector_init_args(TopicsDetector) else TopicsDetector()
    analisis_inicial = detector.analizar_conversacion(texto)

    # Fallback de temas para contexto
    def to_names(lst):
        out = []
        for t in lst or []:
            try:
                out.append(getattr(t, "nombre", str(t)))
            except Exception:
                out.append(str(t))
        return out

    temas_exp = analisis_inicial.get("temas_explícitos", [])
    temas_imp = analisis_inicial.get("temas_implícitos", [])
    temas_emg = analisis_inicial.get("temas_emergentes", [])

    temas_principales = to_names(temas_exp) or to_names(temas_imp) or to_names(temas_emg)
    planos = [getattr(p, "value", str(p)) for p in analisis_inicial.get("planos_activos", [])]

    # Construir ActivationContext directo para evitar dependencias del builder
    from domain.analysis.ActivationContext import ActivationContext
    contexto = ActivationContext(
        planos_detectados=planos,
        temas_principales=temas_principales,
        contradicciones=analisis_inicial.get("contradicciones_emergentes", []),
        bifurcaciones=analisis_inicial.get("bifurcaciones_detectadas", []),
        nivel_abstraccion=float(niveles.get("abstraccion", 0.5)),
        nivel_especulacion=float(niveles.get("especulacion", 0.5)),
        nivel_tecnico=float(niveles.get("tecnico", 0.5)),
        guia_sistema=(guia_sistema or "").strip()
    )

    # Paso 2: Agentes
    # Instanciar sistema de agentes con guardas
    SistemaClase = _agents_mod
    if SistemaClase is None:
        try:
            from domain.analysis.AgentsSystem import AgentsActivationSystem as SistemaClase
        except Exception as e:
            raise ImportError("No se pudo cargar AgentsActivationSystem para run_pipeline") from e
    kwargs = {}
    try:
        params = detector_init_args(SistemaClase)
        if "debug" in params:
            kwargs["debug"] = bool(debug)
        if "slowdown_ms" in params:
            kwargs["slowdown_ms"] = int(slowdown_ms)
    except Exception:
        pass
    sistema = SistemaClase(**kwargs) if kwargs else SistemaClase()
    try:
        analisis_agentes = sistema.analizar_con_agentes(texto, contexto, forzar_todos=bool(force))
    except TypeError:
        analisis_agentes = sistema.analizar_con_agentes(texto, contexto)

    # Paso 3: Síntesis
    motor = SynthesisMotor()
    sintesis = motor.sintetizar_analisis_agentes(analisis_agentes)

    # Resumen serializable de síntesis
    hipos = []
    try:
        for h in getattr(sintesis, "hipotesis_cruzadas", []) or []:
            en = getattr(h, "enunciado", None)
            if en:
                hipos.append(en)
    except Exception:
        pass
    res_sintesis = {
        "nivel_madurez": getattr(sintesis, "nivel_madurez_sintesis", None),
        "hipotesis": hipos,
        "paradigmas": getattr(sintesis, "paradigmas_emergentes", None)
    }

    return {
        "temas_explicitos": to_names(temas_exp),
        "temas_implicitos": to_names(temas_imp),
        "temas_emergentes": to_names(temas_emg),
        "sintesis": res_sintesis
    }
