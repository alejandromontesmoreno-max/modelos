"""
PASO 3 - Embeddings: convertir texto en números.

Un modelo de embeddings convierte un texto en un vector (una lista de
números). Textos con significado parecido producen vectores parecidos,
aunque no compartan palabras.

Para medir qué tan parecidos son dos vectores se usa la similitud coseno:
    cerca de 1 -> significado muy parecido
    cerca de 0 -> sin relación

Este paso no usa el PDF: solo muestra la idea con frases cortas.

Qué observar:
    - Todos los vectores tienen la misma longitud, sin importar el texto.
    - "devolver la laptop tarde" se parece más a la frase de sanciones
      que a la del horario, aunque no comparten las mismas palabras.

Experimento:
    Escribir otra pregunta y predecir, antes de ejecutar, qué frase
    quedará más arriba.
"""
import math

from langchain_ollama import OllamaEmbeddings

from config import MODELO_EMBEDDINGS


def similitud_coseno(a, b):
    producto = sum(x * y for x, y in zip(a, b))
    norma_a = math.sqrt(sum(x * x for x in a))
    norma_b = math.sqrt(sum(y * y for y in b))
    return producto / (norma_a * norma_b)


if __name__ == "__main__":
    embeddings = OllamaEmbeddings(model=MODELO_EMBEDDINGS)

    frases = [
        "El retraso en la entrega de un equipo se castiga con suspensión.",
        "El laboratorio abre de lunes a viernes de 8 a 20 horas.",
        "El servidor de GPU se reserva con 48 horas de anticipación.",
        "La receta lleva harina, huevo y azúcar.",
    ]
    pregunta = "¿Qué pasa si devuelvo la laptop tarde?"

    vectores = embeddings.embed_documents(frases)
    vector_pregunta = embeddings.embed_query(pregunta)

    print(f"Cada texto se convierte en un vector de {len(vector_pregunta)} números.")
    print("Primeros 5 valores del vector de la pregunta:")
    print([round(v, 4) for v in vector_pregunta[:5]])

    print(f"\nPregunta: {pregunta}\n")
    print("Similitud con cada frase (de mayor a menor):")

    resultados = [
        (similitud_coseno(vector_pregunta, vector), frase)
        for vector, frase in zip(vectores, frases)
    ]
    for similitud, frase in sorted(resultados, reverse=True):
        print(f"  {similitud:.3f}  {frase}")
