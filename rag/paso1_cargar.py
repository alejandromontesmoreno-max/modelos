"""
PASO 1 - Cargar el documento.

Un "loader" lee un archivo y lo convierte en objetos Document de LangChain.
Cada Document tiene dos partes:
    page_content -> el texto
    metadata     -> datos sobre el texto (archivo de origen, número de página...)

PyPDFLoader crea un Document por cada página del PDF.

Qué observar:
    - Cuántos Document se crearon (uno por página).
    - Qué guarda la metadata: la usaremos en el paso 5 para citar la página.

Experimento:
    Probar con un PDF escaneado (una imagen sin texto seleccionable):
    page_content queda vacío, porque el loader extrae texto, no lee imágenes.
"""
from langchain_community.document_loaders import PyPDFLoader

from config import RUTA_PDF


def cargar_pdf():
    return PyPDFLoader(str(RUTA_PDF)).load()


if __name__ == "__main__":
    documentos = cargar_pdf()

    print(f"Se cargaron {len(documentos)} documentos (uno por página).\n")

    for doc in documentos:
        print("-" * 60)
        print("Metadata:", doc.metadata)
        print(f"Caracteres: {len(doc.page_content)}")
        print("Inicio del texto:")
        print(doc.page_content[:200], "...")
