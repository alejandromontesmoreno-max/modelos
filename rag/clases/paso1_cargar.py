"""
PASO 1 - Cargar el documento.

Clase: CargadorPDF

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


class CargadorPDF:
    def __init__(self, ruta_pdf=RUTA_PDF):
        self.ruta_pdf = ruta_pdf

    def cargar(self):
        return PyPDFLoader(str(self.ruta_pdf)).load()

    @staticmethod
    def mostrar_resumen(documentos):
        print(f"Se cargaron {len(documentos)} documentos (uno por página).\n")

        for doc in documentos:
            print("-" * 60)
            print("Metadata:", doc.metadata)
            print(f"Caracteres: {len(doc.page_content)}")
            print("Inicio del texto:")
            print(doc.page_content[:200], "...")


if __name__ == "__main__":
    cargador = CargadorPDF()
    documentos = cargador.cargar()
    cargador.mostrar_resumen(documentos)
