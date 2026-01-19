from __future__ import annotations

import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.core.agents_manager import get_agents_manager
from backend.core.layer_detector import analyze_text
from backend.core.statistics_manager import get_stats_manager

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify({"ok": True})


@app.post("/api/process")
def process():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()
    ritual_opt_in = bool(payload.get("ritual_opt_in", False))

    if not text:
        return jsonify({"error": "text is required"}), 400

    agents_manager = get_agents_manager()
    stats_manager = get_stats_manager()

    agent_responses = agents_manager.process_idea(text)
    process_id = stats_manager.record_processing(text, agent_responses)

    analysis = analyze_text(text, ritual_opt_in=ritual_opt_in)

    return jsonify(
        {
            "process_id": process_id,
            "agents": agent_responses,
            "analysis": {
                "layers": analysis.layers,
                "routing": analysis.routing,
                "guardrails": analysis.guardrails,
                "segments": [
                    {
                        "text": segment.text,
                        "layers": segment.layers,
                        "emotions": segment.emotions,
                        "projections": segment.projections,
                        "topic": segment.topic,
                        "speaker": segment.speaker,
                        "start_ms": segment.start_ms,
                        "end_ms": segment.end_ms,
                    }
                    for segment in analysis.segments
                ],
                "metadata": analysis.metadata,
            },
        }
    )


@app.get("/api/stats")
def stats():
    stats_manager = get_stats_manager()
    return jsonify(stats_manager.get_all_stats())


@app.get("/api/history")
def history():
    limit_raw = request.args.get("limit", "10")
    try:
        limit = max(1, min(100, int(limit_raw)))
    except ValueError:
        return jsonify({"error": "limit must be an integer"}), 400

    stats_manager = get_stats_manager()
    return jsonify(stats_manager.get_processing_history(limit=limit))


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    debug = os.environ.get("DEBUG", "1").strip() not in {"0", "false", "False"}

    app.run(host=host, port=port, debug=debug)
