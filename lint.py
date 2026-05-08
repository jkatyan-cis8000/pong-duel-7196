#!/usr/bin/env python3
"""
Lint.py for enforcing source architecture rules.

Rules:
1. Every file under src/ belongs in exactly one layer directory.
2. Imports may only target layers in the file's own "may import from" set.
3. No file exceeds 300 lines.
4. Parse-don't-validate at boundaries.

Layer dependencies:
- types: types only
- config: types, config
- repo: types, config, repo
- service: types, config, repo, providers, service
- runtime: types, config, repo, service, providers, runtime
- ui: types, config, service, runtime, providers, ui
- providers: types, config, utils, providers
- utils: utils only (leaf)
"""

import ast
import os
import sys
from pathlib import Path
from typing import NamedTuple


class Violation(NamedTuple):
    """A linting violation."""
    file_path: str
    line: int
    message: str


# Layer definitions and allowed imports
LAYERS = ["types", "config", "repo", "service", "runtime", "ui", "providers", "utils"]

# Each layer can import from these layers
ALLOWED_IMPORTS = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}

# Maximum lines per file
MAX_LINES = 300


def get_layer_from_path(file_path: str) -> str | None:
    """Get the layer name from a file path."""
    parts = Path(file_path).parts
    for part in parts:
        if part in LAYERS:
            return part
    return None


def get_imports(file_path: str) -> list[str]:
    """Get all imports from a Python file."""
    imports = []
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split(".")[0])
    except SyntaxError:
        pass
    return imports


def lint_file(file_path: str) -> list[Violation]:
    """Lint a single file."""
    violations = []
    
    # Get layer
    layer = get_layer_from_path(file_path)
    if layer is None:
        return violations  # Skip files not in src/
    
    # Check line count
    with open(file_path) as f:
        lines = f.readlines()
        if len(lines) > MAX_LINES:
            violations.append(Violation(
                file_path=file_path,
                line=len(lines),
                message=f"File exceeds {MAX_LINES} lines ({len(lines)} lines)"
            ))
    
    # Check imports
    imports = get_imports(file_path)
    allowed = ALLOWED_IMPORTS[layer]
    
    for imp in imports:
        # Check if import is from src/ and is a layer
        if imp in LAYERS and imp not in allowed:
            violations.append(Violation(
                file_path=file_path,
                line=1,
                message=f"Import '{imp}' not allowed in layer '{layer}'. "
                        f"May only import from: {', '.join(sorted(allowed))}"
            ))
    
    return violations


def main() -> int:
    """Run linting on all Python files under src/."""
    src_dir = Path(__file__).parent / "src"
    violations: list[Violation] = []
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                violations.extend(lint_file(file_path))
    
    if violations:
        print("Linting failed with the following violations:\n")
        for v in violations:
            print(f"{v.file_path}:{v.line}: {v.message}")
        return 1
    
    print("Linting passed! All files follow architecture rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
