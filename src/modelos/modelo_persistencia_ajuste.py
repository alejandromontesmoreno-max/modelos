from langchain_ollama import ChatOllama
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    message_to_dict,
    messages_from_dict
)
from pathlib import Path
import json


class ModeloConPersistenciaAjuste:
    def __init__(self):
        self.modelo = ChatOllama(model="qwen2.5:3b", temperature=0.1)

        # Ruta junto al .py, sin depender de la carpeta desde donde se ejecuta
        self.archivo = Path(__file__).parent / "historial.json"

        self.mensaje_sistema = SystemMessage(
            content="Eres un asistente que responde en español."
        )

        # Máximo de mensajes recientes que se envían al modelo
        self.max_mensajes = 3

        self.historial = self.cargar_historial()

    def generar_respuesta(self):
        while True:
            pregunta = input("\nUsuario: ").strip()  # quita espacios sobrantes

            if pregunta.lower() == "salir":
                break
            if not pregunta:  # ignora entradas vacías
                continue

            self.historial.append(HumanMessage(content=pregunta))

            # Si el modelo falla, se retira la pregunta y la conversación continúa
            try:
                respuesta = self.modelo.invoke(self.ventana_contexto())
            except Exception as error:
                self.historial.pop()
                print(f"Error al consultar el modelo: {error}")
                continue

            print("IA:", respuesta.content)
            self.historial.append(respuesta)

            # Una sola escritura por turno, con pregunta y respuesta completas
            self.guardar_historial()

    def ventana_contexto(self):
        conversacion = [m for m in self.historial if not isinstance(m, SystemMessage)]
        return [self.mensaje_sistema] + conversacion[-self.max_mensajes:]

    def cargar_historial(self):
        if self.archivo.exists():
            # Si el archivo está dañado, se avisa y se inicia una conversación nueva
            try:
                with open(self.archivo, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)
                historial = messages_from_dict(datos)
                print("Historial recuperado desde JSON.")
                return historial
            except (json.JSONDecodeError, KeyError, ValueError):
                print("El historial está dañado; se inicia una conversación nueva.")

        print("Iniciando nueva conversación.")
        return [self.mensaje_sistema]

    def guardar_historial(self):
        datos = [message_to_dict(mensaje) for mensaje in self.historial]

        # Escribe en un temporal y luego reemplaza: el original nunca queda a medias
        temporal = self.archivo.with_suffix(".tmp")
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        temporal.replace(self.archivo)