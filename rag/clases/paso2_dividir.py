"""
PASO 2 - Dividir en fragmentos (chunks).

Clase: DivisorDocumentos (usa CargadorPDF del paso 1)

Las páginas son demasiado grandes para buscar con precisión: una página
habla de varios temas. Si la dividimos en fragmentos pequeños, cada uno
trata (idealmente) un solo tema, y la búsqueda encuentra justo lo necesario.

RecursiveCharacterTextSplitter corta intentando respetar, en este orden,
párrafos, líneas, palabras y finalmente caracteres.

El traslape (chunk_overlap) repite el final de un fragmento al inicio del
siguiente, para no partir una idea a la mitad.

Qué observar:
    - Cada fragmento conserva la metadata de su página.
    - Parte del final de un fragmento se repite al inicio del siguiente
      (traslape). No siempre son exactamente TRASLAPE caracteres, porque
      el divisor corta en espacios para no partir palabras.

Experimento:
    Cambiar TAMANO_FRAGMENTO en config.py a 200 y a 1500.
    Muy pequeño: fragmentos sin contexto suficiente.
    Muy grande: fragmentos que mezclan temas y la búsqueda se vuelve imprecisa.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import TAMANO_FRAGMENTO, TRASLAPE
from paso1_cargar import CargadorPDF


class DivisorDocumentos:
    def __init__(self, tamano=TAMANO_FRAGMENTO, traslape=TRASLAPE):
        self.traslape = traslape
        self.divisor = RecursiveCharacterTextSplitter(
            chunk_size=tamano,
            chunk_overlap=traslape,
        )

    def dividir(self, documentos):
        return self.divisor.split_documents(documentos)

    def mostrar_resumen(self, documentos, fragmentos):
        print(f"{len(documentos)} páginas -> {len(fragmentos)} fragmentos\n")

        for i, fragmento in enumerate(fragmentos):
            pagina = fragmento.metadata.get("page", 0) + 1
            print(f"Fragmento {i} | página {pagina} | {len(fragmento.page_content)} caracteres")

        # Mostrar dos fragmentos consecutivos para ver el traslape
        if len(fragmentos) > 1:
            print("\n" + "=" * 60)
            print("FINAL del fragmento 0:")
            print("..." + fragmentos[0].page_content[-self.traslape:])
            print("\nINICIO del fragmento 1:")
            print(fragmentos[1].page_content[:self.traslape] + "...")


if __name__ == "__main__":
    cargador = CargadorPDF()
    divisor = DivisorDocumentos()

    documentos = cargador.cargar()
    fragmentos = divisor.dividir(documentos)
    divisor.mostrar_resumen(documentos, fragmentos)
