from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

class Prompt_02:
    def __init__(self):
        self.modelo=ChatOllama(model="qwen2.5:3b", temperature=0.1)

    def generar_respuestas(self):
        prompt_template = PromptTemplate.from_template(
            "Explica el concepto de {tema} "
            "para un estudiante de nivel {nivel}. "
            "Incluye un ejemplo sencillo."
        )

        prompt = prompt_template.format(
            tema="inteligencia artificial", 
            nivel="universitario"
        )
          
        print("Prompt generado:", prompt)
        respuesta = self.modelo.invoke(prompt)
        return respuesta.text