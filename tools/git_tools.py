from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List


def list_repo_summary(repo_path: str | Path) -> Dict[str, Any]:
    """Summarize a repository tree for architecture analysis."""
    repo = Path(repo_path)
    summary: Dict[str, Any] = {
        "root": str(repo),
        "files": [],
        "directories": [],
        "total_files": 0,
        "total_directories": 0,
    }

    if not repo.exists():
        return summary

    for root, dirs, files in os.walk(repo):
        rel_root = Path(root).relative_to(repo)
        if rel_root != Path("."):
            summary["directories"].append(str(rel_root))
        for file_name in sorted(files):
            rel_file = Path(root, file_name).relative_to(repo)
            summary["files"].append(str(rel_file))

    summary["total_files"] = len(summary["files"])
    summary["total_directories"] = len(summary["directories"])
    return summary
