import ast
from pathlib import Path
from radon.complexity import cc_visit

def collect_functions(repo_path: str):
    repo = Path(repo_path)
    py_files = repo.rglob("*.py")
    functions = []

    for file in py_files:
        if "venv" in str(file) or "tests" in str(file):
            continue
        try:
            source = file.read_text()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    sig = f"{node.name}({', '.join([a.arg for a in node.args.args])})"
                    complexity = cc_visit(source)
                    functions.append({
                        "file": str(file),
                        "name": node.name,
                        "signature": sig,
                        "lineno": node.lineno,
                        "docstring": ast.get_docstring(node),
                        "complexity": complexity[0].complexity if complexity else None,
                        "source": ast.get_source_segment(source, node),
                    })
        except Exception as e:
            print(f"Skipping {file}: {e}")
    return functions
