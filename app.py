import importlib.util
from pathlib import Path

# Load Flask app from a filename that is not a valid module name.
_module_path = Path(__file__).with_name("3_api_pokemon.py")
_spec = importlib.util.spec_from_file_location("api_pokemon_module", _module_path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

app = _module.app
