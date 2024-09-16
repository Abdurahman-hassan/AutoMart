from pathlib import Path
import os
import sys


# === variables =====================================
BASE_DIR = Path(__file__).resolve().parent

# === error message ===
_error_structure = "You can only use this with the octos template or any project created with the same structure."


# === functions =====================================
def get_settings_module():
    terminal_dir = os.getcwd()

    if terminal_dir not in sys.path:
        sys.path.append(terminal_dir)

    try:
        from config.settings.base import DEBUG  # type: ignore
    except ImportError:
        raise ValueError(_error_structure)

    if DEBUG:
        return "config.settings.development"
    return "config.settings.production"
