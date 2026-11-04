"""
PASO 5 - RAG completo: recuperar + generar.

Clase: ModeloRAGBasico (usa BuscadorDocumentos del paso 4)

Se agrega el modelo de chat a la búsqueda del paso 4:
    1. Recuperar los fragmentos más parecidos a la pregunta (paso 4).
    2. Insertarlos como contexto en una plantilla.
    3. Pedir al modelo que responda usando solo ese contexto.
    4. Mostrar las páginas de origen para poder verificar.

Qué observar:
    - Hacer la misma pregunta del paso 0 y comparar las respuestas.
    - Las fuentes permiten comprobar la respuesta en el PDF.

Experimentos:
    - Preguntar algo que NO está en el documento
      ("¿Cuánto cuesta la inscripción?"). El modelo debería decir que no
      lo encuentra. Con un modelo pequeño no siempre obedece: buen tema
      para discutir las limitaciones de RAG.
    - Escribir "contexto" antes de una pregunta para ver exactamente
      qué fragmentos recibió el modelo.

La versión completa para el menú, con reindexación automática y manejo
de errores, está en modelo_rag.py.
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from config import MODELO_CHAT
from paso4_buscar import BuscadorDocumentos


class ModeloRAGBasico:
    def __init__(self):
        self.modelo = ChatOllama(model=MODELO_CHAT, temperature=0.1)

        # Composición: la búsqueda la hace el buscador del paso 4
        self.buscador = BuscadorDocumentos()

        # El contexto recuperado se inyecta en el mensaje de sistema
        self.plantilla = ChatPromptTemplate.from_messages([
            ("system",
             "Eres un asistente que responde en español. "
             "Responde únicamente con la información del contexto. "
             "Si la respuesta no está en el contexto, di que no la "
             "encuentras en el documento.\n\nContexto:\n{contexto}"),
            ("human", "{pregunta}"),
        ])
        self.cadena = self.plantilla | self.modelo

    def recuperar(self, pregunta):
        # El buscador devuelve (fragmento, similitud); aquí solo se necesita el fragmento
        return [fragmento for fragmento, _ in self.buscador.buscar(pregunta)]

    @staticmethod
    def paginas_de_origen(fragmentos):
        # PyPDFLoader numera las páginas desde 0
        paginas = sorted({f.metadata.get("page", 0) + 1 for f in fragmentos})
        return ", ".join(map(str, paginas))

    def generar_respuesta(self):
        try:
            self.buscador.preparar_indice()
        except Exception as error:
            print(f"No se pudo preparar el índice: {error}")
            return

        while True:
            pregunta = input("\nUsuario: ").strip()

            if pregunta.lower() == "salir":
                break
            if not pregunta:
                continue

            # Modo de depuración: "contexto <pregunta>" muestra lo que recibe el modelo
            mostrar_contexto = pregunta.lower().startswith("contexto ")
            if mostrar_contexto:
                pregunta = pregunta[len("contexto "):]

            try:
                # 1. Recuperar
                fragmentos = self.recuperar(pregunta)
                contexto = "\n\n".join(f.page_content for f in fragmentos)

                if mostrar_contexto:
                    print("\n--- Contexto enviado al modelo ---")
                    print(contexto)
                    print("--- Fin del contexto ---\n")

                # 2 y 3. Generar con el contexto
                respuesta = self.cadena.invoke({"contexto": contexto, "pregunta": pregunta})
            except Exception as error:
                print(f"Error al consultar el modelo: {error}")
                continue

            print("IA:", respuesta.content)

            # 4. Fuentes
            print("Fuentes: páginas", self.paginas_de_origen(fragmentos))


if __name__ == "__main__":
    ModeloRAGBasico().generar_respuesta()
