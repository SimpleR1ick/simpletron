import json
from pathlib import Path
from typing import Any

def load_json(filepath: Path, default: Any = None) -> Any:
    """Lê um arquivo JSON de forma segura, retornando um valor padrão se não existir."""
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Storage] Erro ao carregar {filepath}: {e}")
            return default if default is not None else []
    return default if default is not None else []

def save_json(filepath: Path, data: Any) -> None:
    """Salva dados em formato JSON com indentação e formatação legível."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Storage] Erro ao salvar {filepath}: {e}")
