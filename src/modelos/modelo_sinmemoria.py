from langchain_ollama import ChatOllama

class ModeloSinMemoria:
    def __init__(self):
        self.modelo = ChatOllama(model="qwen2.5:3b", 
                                 temperature=0.1)

    def generar_respuesta(self):
        respuesta1 = self.modelo.invoke("Mi nombre es Alejandro Montes")
        print("Respuesta a la primera pregunta:")
        print(respuesta1.text)
        print("--------------------------------------------------------------")

        print("Respuesta a la primera pregunta:")
        respuesta2 = self.modelo.invoke("¿Cuál es mi nombre?")
        print(respuesta2.text)
        print("--------------------------------------------------------------")