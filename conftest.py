from pathlib import Path


def get_paths(file_name: str) -> list[str]:
    def normalize(path: str, name: str) -> str:
        return path.replace("/", ".").replace(f"{name}.py", name)

    return [
        normalize(str(path), file_name)
        for path in list(Path("src").rglob(f"**/{file_name}.py"))
        if not str(path).startswith(("venv", ".venv"))
    ]


pytest_plugins = get_paths("fixtures") + get_paths("factories")
