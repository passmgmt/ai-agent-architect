from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def generate_architecture_doc(project_name: str, repo_path: str | Path) -> Dict[str, Any]:
    """Generate a markdown architecture document for a repository."""
    repo = Path(repo_path)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    output_dir = repo / "workflows" / "architecture"
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / "architecture-overview.md"

    content = f'''# {project_name} Architecture Overview

Date: {timestamp}

## Purpose
This document captures the system architecture for the AI Agent Architect project and highlights the repository structure, workflow boundaries, and extensibility points.

## High-Level Components
- VS Code / Copilot client
- Local MCP server
- Repository analysis tools
- Architecture generation workflows
- ADR generation support

## Workflow
```mermaid
flowchart LR
    A[Developer Prompt] --> B[AI Agent Server]
    B --> C[Repository Scan]
    B --> D[Architecture Generation]
    D --> E[Architecture Docs]
    D --> F[ADR Drafts]
```

## Repository Layout
- `server.py` hosts the MCP server entry point.
- `tools/` contains repository and documentation utilities.
- `workflows/` contains architecture and ADR outputs.
- `skills/` stores reusable reasoning or task-specific guidance.
- `examples/` captures prompts and generated outputs.
'''

    filename.write_text(content, encoding="utf-8")
    return {
        "status": "created",
        "path": str(filename),
        "content": content,
    }


def generate_adr(title: str, status: str, repo_path: str | Path) -> Dict[str, Any]:
    """Create a markdown ADR file with a consistent structure."""
    repo = Path(repo_path)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    adr_dir = repo / "workflows" / "adr"
    adr_dir.mkdir(parents=True, exist_ok=True)

    slug = title.lower().replace(" ", "-")
    filename = adr_dir / f"ADR-{timestamp}-{slug}.md"

    content = f'''# {title}

- Status: {status}
- Date: {timestamp}

## Context
This ADR documents the design decision for the {title} topic and sets the rationale for future implementation decisions.

## Decision
The project will adopt a modular, tool-driven architecture that keeps AI reasoning, repository analysis, and documentation generation separate, enabling future extension without coupling workflow logic to the MCP server itself.

## Consequences
- Easier to extend with additional tools and skills.
- Better separation of concerns between analysis, generation, and repository utilities.
- Keeps architecture decisions easy to review and evolve over time.
'''

    filename.write_text(content, encoding="utf-8")
    return {
        "status": "created",
        "path": str(filename),
        "content": content,
    }
