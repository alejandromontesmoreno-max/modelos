"""
Configuración compartida por todos los pasos.
Cambiar un valor aquí lo cambia en todos los scripts.
"""
from pathlib import Path

CARPETA = Path(__file__).parent

# Documento que se va a consultar
RUTA_PDF = CARPETA / "reglamento_laboratorio.pdf"

# Índice vectorial guardado en disco (se crea en el paso 4)
ARCHIVO_INDICE = CARPETA / "indice.json"

# Modelos de Ollama (descargar antes con "ollama pull <nombre>")
MODELO_CHAT = "qwen2.5:3b"
MODELO_EMBEDDINGS = "qwen3-embedding:0.6b"

# Tamaño de cada fragmento y traslape entre fragmentos, en caracteres
TAMANO_FRAGMENTO = 500
TRASLAPE = 100

# Cuántos fragmentos se recuperan por pregunta
FRAGMENTOS_POR_PREGUNTA = 3
