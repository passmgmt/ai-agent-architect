#!/usr/bin/env python3
"""AI Agent Architect MCP server.

This server exposes a minimal local MCP-style interface for repository analysis,
architecture generation, and ADR workflow orchestration. It is intentionally
lightweight and easy to extend for real AI tool integrations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from tools.doc_generator import generate_architecture_doc, generate_adr
from tools.git_tools import list_repo_summary


def analyze_repository(path: str) -> Dict[str, Any]:
    """Analyze a repository path and return a summary payload."""
    repo_path = Path(path)
    return {
        "path": str(repo_path),
        "summary": list_repo_summary(repo_path),
    }


def generate_architecture(path: str, project_name: str = "AI Agent Architect") -> Dict[str, Any]:
    """Generate an architecture markdown document for a repository."""
    return generate_architecture_doc(project_name=project_name, repo_path=Path(path))


def create_adr(path: str, title: str, status: str = "Accepted") -> Dict[str, Any]:
    """Create a new ADR document under the workspace's ADR directory."""
    return generate_adr(title=title, status=status, repo_path=Path(path))


def main() -> None:
    """Entry point for local MCP server usage.

    This demo is intentionally simple: it exposes a JSON-driven command loop for
    manual testing and integration into VS Code MCP clients.
    """
    print("AI Agent Architect server started")
    while True:
        try:
            raw = input()
            if not raw.strip():
                continue
            command = json.loads(raw)
            action = command.get("action")
            payload = command.get("payload", {})

            if action == "analyze_repository":
                result = analyze_repository(payload.get("path", "."))
            elif action == "generate_architecture":
                result = generate_architecture(
                    payload.get("path", "."),
                    payload.get("project_name", "AI Agent Architect"),
                )
            elif action == "create_adr":
                result = create_adr(
                    payload.get("path", "."),
                    payload.get("title", "ADR"),
                    payload.get("status", "Accepted"),
                )
            else:
                result = {"error": f"Unknown action: {action}"}

            print(json.dumps(result))
        except EOFError:
            break
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON input"}))


if __name__ == "__main__":
    main()
