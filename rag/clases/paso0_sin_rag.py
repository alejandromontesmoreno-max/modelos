"""
PASO 0 - El problema: el modelo no conoce tus documentos.

Clase: ModeloSinRAG

El modelo aprendió de textos públicos hasta cierta fecha. No ha visto el
reglamento del laboratorio, así que no puede responder sobre él.

Qué observar:
    Preguntar "¿Cuántos días puedo tener prestada una laptop del
    laboratorio?". El modelo inventará una respuesta que suena
    convincente, o dirá que no lo sabe. En el reglamento la respuesta es:
    tres días hábiles, renovable una vez.

Ese es el problema que resuelve RAG (Retrieval-Augmented Generation):
buscar la información relevante en tus documentos y dársela al modelo
junto con la pregunta.
"""
from langchain_ollama import ChatOllama

from config import MODELO_CHAT


class ModeloSinRAG:
    def __init__(self):
        self.modelo = ChatOllama(model=MODELO_CHAT, temperature=0.1)

    def generar_respuesta(self):
        print("Modelo SIN acceso al documento. Escribe 'salir' para terminar.")

        while True:
            pregunta = input("\nUsuario: ").strip()

            if pregunta.lower() == "salir":
                break
            if not pregunta:
                continue

            try:
                respuesta = self.modelo.invoke(pregunta)
            except Exception as error:
                print(f"Error al consultar el modelo: {error}")
                continue

            print("IA:", respuesta.content)


if __name__ == "__main__":
    ModeloSinRAG().generar_respuesta()
