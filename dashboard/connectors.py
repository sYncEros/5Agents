"""Conectores simples para Node-RED y Neo4j.

Diseñados para funcionar incluso si los servicios no están activos,
retornando datos de ejemplo para que la UI cargue en modo demo.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)


class NodeRedConnector:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str, default: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            # Merge to guarantee expected keys exist
            return {**default, **data}
        except Exception as exc:  # noqa: BLE001
            logger.warning("Node-RED GET %s falló: %s", url, exc)
            return {**default, "status": "offline", "error": str(exc)}

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Node-RED POST %s falló: %s", url, exc)
            return {"status": "error", "message": str(exc)}

    def get_synthesis_data(self) -> Dict[str, Any]:
        default = {
            "total_files_processed": 0,
            "processing_rate": 0,
            "clusters_detected": 0,
            "potential_papers": 0,
        }
        return self._get("/synthesis", default)

    def trigger_batch_processing(self, batch_size: int = 50) -> Dict[str, Any]:
        payload = {"batch_size": batch_size}
        result = self._post("/process", payload)
        if result.get("status") != "success":
            # Fallback demo response
            return {
                "status": "success",
                "message": f"Procesamiento simulado: {batch_size} items (modo demo)",
            }
        return result

    def get_processing_stats(self) -> Dict[str, Any]:
        default = {
            "cpu_usage": 0,
            "memory_usage": 0,
            "queue_size": 0,
        }
        return self._get("/stats", default)


class Neo4jConnector:
    def __init__(self, uri: str, user: str, password: str) -> None:
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self.last_error: Optional[str] = None
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as exc:  # noqa: BLE001
            self.last_error = str(exc)
            logger.warning("Neo4j driver no inicializado: %s", exc)

    def _run(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[List[Dict[str, Any]]]:
        if not self.driver:
            return None
        try:
            with self.driver.session() as session:
                return session.run(query, params or {}).data()
        except Exception as exc:  # noqa: BLE001
            self.last_error = str(exc)
            logger.warning("Query Neo4j falló: %s", exc)
            return None

    def get_knowledge_graph(self) -> Dict[str, List[Dict[str, Any]]]:
        records = self._run(
            """
            MATCH (a)-[r]->(b)
            RETURN id(a) AS source, id(b) AS target, coalesce(r.weight,1.0) AS weight,
                   coalesce(a.name, a.id, toString(id(a))) AS source_label,
                   coalesce(b.name, b.id, toString(id(b))) AS target_label
            LIMIT 200
            """
        )
        if records is None:
            return self._demo_graph()

        nodes = {}
        edges = []
        for rec in records:
            src_id = str(rec.get("source"))
            tgt_id = str(rec.get("target"))
            nodes[src_id] = {"id": src_id, "label": rec.get("source_label", src_id)}
            nodes[tgt_id] = {"id": tgt_id, "label": rec.get("target_label", tgt_id)}
            edges.append({
                "source": src_id,
                "target": tgt_id,
                "weight": rec.get("weight", 1.0),
            })
        return {"nodes": list(nodes.values()), "edges": edges}

    def get_strongest_connections(self, limit: int = 10) -> pd.DataFrame:
        records = self._run(
            """
            MATCH (a)-[r]->(b)
            RETURN coalesce(a.name, toString(id(a))) AS source,
                   coalesce(b.name, toString(id(b))) AS target,
                   coalesce(r.weight, 1.0) AS weight
            ORDER BY weight DESC
            LIMIT $limit
            """,
            {"limit": limit},
        )
        if records is None:
            data = [
                {"source": "A", "target": "B", "weight": 0.8},
                {"source": "B", "target": "C", "weight": 0.6},
            ]
        else:
            data = records
        return pd.DataFrame(data)

    def get_clusters(self) -> List[Dict[str, Any]]:
        records = self._run(
            """
            MATCH (c:Cluster)
            RETURN c.name AS name, c.size AS size, c.coherence AS coherence,
                   c.sample_docs AS sample_docs
            LIMIT 25
            """
        )
        if records is None:
            return [
                {
                    "name": "demo_cluster",
                    "size": 12,
                    "coherence": 0.72,
                    "sample_docs": ["doc_1", "doc_2", "doc_3"],
                }
            ]
        return records

    def get_recent_insights(self, limit: int = 20) -> List[Dict[str, Any]]:
        records = self._run(
            """
            MATCH (i:Insight)
            RETURN i.cluster AS cluster, i.description AS description,
                   coalesce(i.importance,0.5) AS importance,
                   coalesce(i.type,"connection") AS type,
                   coalesce(i.timestamp, datetime()) AS timestamp
            ORDER BY timestamp DESC
            LIMIT $limit
            """,
            {"limit": limit},
        )
        if records is None:
            now = datetime.utcnow()
            return [
                {
                    "cluster": "demo_cluster",
                    "description": "Insight de ejemplo (modo demo)",
                    "importance": 0.65,
                    "type": "synthesis",
                    "timestamp": now - timedelta(minutes=idx * 5),
                }
                for idx in range(min(limit, 3))
            ]
        # Asegurar que timestamp sea datetime para usar strftime
        for rec in records:
            ts = rec.get("timestamp")
            if isinstance(ts, str):
                try:
                    rec["timestamp"] = datetime.fromisoformat(ts)
                except ValueError:
                    rec["timestamp"] = datetime.utcnow()
        return records

    def _demo_graph(self) -> Dict[str, List[Dict[str, Any]]]:
        nodes = [
            {"id": "A", "label": "AI"},
            {"id": "B", "label": "Science"},
            {"id": "C", "label": "Health"},
        ]
        edges = [
            {"source": "A", "target": "B", "weight": 0.7},
            {"source": "B", "target": "C", "weight": 0.5},
            {"source": "A", "target": "C", "weight": 0.4},
        ]
        return {"nodes": nodes, "edges": edges}
