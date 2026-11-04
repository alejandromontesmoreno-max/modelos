from langchain_ollama import ChatOllama
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

class ModeloConMemoria:
    def __init__(self):
        self.modelo = ChatOllama(model="qwen2.5:3b", 
                                 temperature=0.1)
        # 2. Crear historial de mensajes
        self.historial = [
                    SystemMessage(
                    content="Eres un asistente que responde en español."
                    )]
        
    def generar_respuesta(self):
        while True:
            pregunta = input("\nUsuario: ")

            if pregunta.lower() == "salir":
                break

            # 3. Agregar la pregunta del usuario al historial
            self.historial.append(HumanMessage(content=pregunta))
            # 4. Enviar conversación completa al modelo
            respuesta = self.modelo.invoke(self.historial)
            # 5. Mostrar respuesta
            print("IA:", respuesta.content)
            # 7. Guardar respuesta en el historial
            self.historial.append(respuesta)




    

    