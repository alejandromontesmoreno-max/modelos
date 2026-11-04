from langchain_ollama import ChatOllama
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    message_to_dict,
    messages_from_dict
)
#Path para el manejo de memoria en el modelo de lenguaje
from pathlib import Path
import json



class ModeloConPersistencia:
    def __init__(self):
        self.modelo = ChatOllama(model="qwen2.5:3b", 
                                 temperature=0.1)
        
        # Archivo donde se almacenará el historial
        self.archivo = Path("historial.json")
        
       # Mensaje inicial del sistema
        self.mensaje_sistema = SystemMessage(
            content="Eres un asistente que responde en español."
        )
        
        # Cargar historial existente o iniciar uno nuevo
        self.historial = self.cargar_historial()
        
    def generar_respuesta(self):
        while True:
            pregunta = input("\nUsuario: ")

            if pregunta.lower() == "salir":
                break

            # 3. Agregar la pregunta del usuario al historial
            self.historial.append(HumanMessage(content=pregunta))
            # Guardar pregunta en JSON
            self.guardar_historial()
            
            # 4. Enviar conversación completa al modelo
            respuesta = self.modelo.invoke(self.historial)
            # 5. Mostrar respuesta
            print("IA:", respuesta.content)
            # 7. Guardar respuesta en el historial
            self.historial.append(respuesta)
            # Guardar respuesta en JSON
            self.guardar_historial()

    def cargar_historial(self):

        if self.archivo.exists():

            with open(self.archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            # Reconstruir los mensajes de LangChain
            historial = messages_from_dict(datos)

            print("Historial recuperado desde JSON.")

            return historial

        # Si no existe el archivo, iniciar historial
        print("Iniciando nueva conversación.")

        return [self.mensaje_sistema]
    
    def guardar_historial(self):

        # Convertir mensajes de LangChain a diccionarios
        datos = [
            message_to_dict(mensaje)
            for mensaje in self.historial
        ]

        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                ensure_ascii=False,
                indent=4
            )