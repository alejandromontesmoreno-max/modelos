"""
PASO 4 - Almacén vectorial y búsqueda semántica.

Clase: BuscadorDocumentos (usa CargadorPDF del paso 1 y
DivisorDocumentos del paso 2)

Se juntan los pasos 1 a 3: cada fragmento del PDF se convierte en vector y
se guarda en un almacén vectorial (vector store). Al preguntar, la pregunta
también se convierte en vector y se buscan los fragmentos más parecidos.

Generar embeddings toma tiempo, así que el índice se guarda en
indice.json y se reutiliza en las siguientes ejecuciones (la misma idea que
historial.json en el ejemplo de memoria).

IMPORTANTE: si cambias el PDF o los valores de config.py, borra indice.json
para que se vuelva a generar.

Qué observar:
    - Todavía NO hay modelo de chat: esto es solo búsqueda.
    - El puntaje es la similitud coseno del paso 3.
    - Preguntar con otras palabras ("¿me castigan si entrego tarde?")
      encuentra el mismo fragmento: la búsqueda es por significado.

Preguntas sugeridas:
    ¿Cuántos días puedo tener una laptop?
    ¿Con cuánta anticipación reservo la GPU?
    ¿Puedo ir el domingo?
"""
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings

from config import ARCHIVO_INDICE, MODELO_EMBEDDINGS, FRAGMENTOS_POR_PREGUNTA
from paso1_cargar import CargadorPDF
from paso2_dividir import DivisorDocumentos


class BuscadorDocumentos:
    def __init__(self):
        # Composición: el buscador usa las clases de los pasos anteriores
        self.cargador = CargadorPDF()
        self.divisor = DivisorDocumentos()

        self.embeddings = OllamaEmbeddings(model=MODELO_EMBEDDINGS)
        self.archivo_indice = ARCHIVO_INDICE
        self.indice = None

    def preparar_indice(self):
        if self.archivo_indice.exists():
            self.indice = InMemoryVectorStore.load(str(self.archivo_indice), self.embeddings)
            print("Índice recuperado desde JSON.")
            return

        print("Creando índice, puede tardar unos minutos...")
        documentos = self.cargador.cargar()
        fragmentos = self.divisor.dividir(documentos)

        self.indice = InMemoryVectorStore(self.embeddings)
        self.indice.add_documents(fragmentos)
        self.indice.dump(str(self.archivo_indice))

        print(f"{len(fragmentos)} fragmentos indexados y guardados.")

    def buscar(self, pregunta, k=FRAGMENTOS_POR_PREGUNTA):
        # Devuelve pares (fragmento, similitud)
        return self.indice.similarity_search_with_score(pregunta, k=k)

    def ejecutar(self):
        self.preparar_indice()

        while True:
            pregunta = input("\nBuscar (o 'salir'): ").strip()

            if pregunta.lower() == "salir":
                break
            if not pregunta:
                continue

            for posicion, (fragmento, puntaje) in enumerate(self.buscar(pregunta), start=1):
                pagina = fragmento.metadata.get("page", 0) + 1
                print(f"\n#{posicion} | similitud {puntaje:.3f} | página {pagina}")
                print(fragmento.page_content[:300], "...")


if __name__ == "__main__":
    BuscadorDocumentos().ejecutar()
