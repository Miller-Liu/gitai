import subprocess
from pathlib import Path

from langchain.tools import tool

MAX_FILE_SIZE = 100_000

def get_repo_path() -> Path:
    return Path.cwd()

def get_tracked_files() -> list[str]:
    """Returns all files git is tracking (respects .gitignore automatically)."""
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True, text=True,
        cwd=get_repo_path()
    )
    return result.stdout.strip().split('\n') if result.stdout.strip() else []

def read_file(path: str) -> str:
    full_path = get_repo_path() / path
    if not full_path.exists():
        return f"File not found: {path}"
    if full_path.stat().st_size > MAX_FILE_SIZE:
        return f"File too large: {path}"
    return full_path.read_text(errors='ignore')

def list_directory(path: str = ".") -> list[str]:
    """List only git-tracked files under a given path."""
    tracked = get_tracked_files()
    prefix = path.rstrip("/") + "/"
    if path == ".":
        return tracked
    return [f for f in tracked if f.startswith(prefix)]

def search_code(query: str) -> list[str]:
    """Search across tracked files only."""
    result = subprocess.run(
        ["git", "grep", "-l", query],
        capture_output=True, text=True,
        cwd=get_repo_path()
    )
    return result.stdout.strip().split('\n') if result.stdout.strip() else []

def get_file_tree() -> str:
    """Compact tree of tracked files."""
    tracked = get_tracked_files()
    lines = []
    for path in tracked:
        parts = Path(path).parts
        depth = len(parts) - 1
        lines.append("  " * depth + path)  # full path, not just filename
    return '\n'.join(lines)

#-------------------------------------------------------------------------------------------------#

@tool
def tool_read_file(path: str) -> str:
    """Read the contents of a file in the repo."""
    return read_file(path)

@tool
def tool_list_directory(path: str) -> str:
    """List files and folders at a path in the repo."""
    return "\n".join(list_directory(path))

@tool
def tool_search_code(query: str) -> str:
    """Search for a string across the repo."""
    results = search_code(query)
    return "\n".join(results) if results else "No results found."

@tool
def tool_get_file_tree() -> str:
    """Get a full file tree of the repo."""
    return get_file_tree()

# reusable tool sets
FILESYSTEM_TOOLS = [tool_read_file, tool_list_directory, tool_search_code, tool_get_file_tree]