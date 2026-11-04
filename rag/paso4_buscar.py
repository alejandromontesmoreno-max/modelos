"""
PASO 4 - Almacén vectorial y búsqueda semántica.

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
from paso1_cargar import cargar_pdf
from paso2_dividir import dividir


def obtener_indice():
    embeddings = OllamaEmbeddings(model=MODELO_EMBEDDINGS)

    if ARCHIVO_INDICE.exists():
        print("Índice recuperado desde JSON.")
        return InMemoryVectorStore.load(str(ARCHIVO_INDICE), embeddings)

    print("Creando índice, puede tardar unos minutos...")
    fragmentos = dividir(cargar_pdf())

    indice = InMemoryVectorStore(embeddings)
    indice.add_documents(fragmentos)
    indice.dump(str(ARCHIVO_INDICE))

    print(f"{len(fragmentos)} fragmentos indexados y guardados.")
    return indice


if __name__ == "__main__":
    indice = obtener_indice()

    while True:
        pregunta = input("\nBuscar (o 'salir'): ").strip()
        if pregunta.lower() == "salir":
            break
        if not pregunta:
            continue

        resultados = indice.similarity_search_with_score(pregunta, k=FRAGMENTOS_POR_PREGUNTA)

        for posicion, (fragmento, puntaje) in enumerate(resultados, start=1):
            pagina = fragmento.metadata.get("page", 0) + 1
            print(f"\n#{posicion} | similitud {puntaje:.3f} | página {pagina}")
            print(fragmento.page_content[:300], "...")
