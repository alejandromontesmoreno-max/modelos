"""
PASO 0 - El problema: el modelo no conoce tus documentos.

El modelo aprendió de textos públicos hasta cierta fecha. No ha visto el
reglamento del laboratorio, así que no puede responder sobre él.

Qué observar:
    El modelo inventará una respuesta que suena convincente, o dirá que no
    lo sabe. En ningún caso responde con lo que dice el documento
    (la respuesta correcta es: tres días hábiles, renovable una vez).

Ese es el problema que resuelve RAG (Retrieval-Augmented Generation):
buscar la información relevante en tus documentos y dársela al modelo
junto con la pregunta.
"""
from langchain_ollama import ChatOllama

from config import MODELO_CHAT

modelo = ChatOllama(model=MODELO_CHAT, temperature=0.1)

pregunta = "¿Cuántos días puedo tener prestada una laptop del Laboratorio de Inteligencia Artificial?"

print("Pregunta:", pregunta)
respuesta = modelo.invoke(pregunta)
print("\nRespuesta del modelo SIN acceso al documento:\n")
print(respuesta.content)
