from src.modelos.modelo_google import ModeloGoogle
from src.modelos.modelo_groq import ModeloGroq
from src.modelos.modelo_local import ModeloLocal
from src.modelos.modelo_local2 import ModeloLocal2
from src.modelos.prompt_01 import Prompt01
from src.modelos.prompt_02 import Prompt_02
from src.modelos.modelo_roles import Prompt_Roles
from src.modelos.modelo_sinmemoria import ModeloSinMemoria
from src.modelos.modelo_conmemoria import ModeloConMemoria
from src.modelos.modelo_conpersistencia import ModeloConPersistencia

import os
from rich.console import Console
from rich.markdown import Markdown

class MenuPrincipal():
    def __init__(self):
        self.console = Console()
        self.opcion = ""

    @staticmethod
    def limpiar_pantalla():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pausar():
        input("Presione Enter para continuar...")

    def mostrar_menu(self):
        print("=== Menú Principal ===")
        print("1. Modelo Google API KEY")
        print("2. Modelo Groq API KEY")
        print("3. Modelo Local")
        print("4. Modelo Local 2")
        print("5. Prompt básico")
        print("6. Prompt template")
        print("7. Modelo Roles")
        print("8. Modelo sin memoria")
        print("9. Modelo con memoria")
        print("10. Modelo con memoria y persistencia")
        print("0. Salir")

    def ejecutar_opcion(self):
        while True:
            self.limpiar_pantalla()
            self.mostrar_menu()
            self.opcion = input("Seleccione una opción: ")

            if self.opcion == "1":
                modelo_google = ModeloGoogle()
                prompt = input("Ingrese su prompt: ")
                respuesta = modelo_google.generar_respuesta(prompt)
                print("Respuesta del modelo Google:", respuesta, "\n")
                self.console.print(Markdown(respuesta))


            elif self.opcion == "2":
                modelo_groq = ModeloGroq()
                prompt = input("Ingrese su prompt: ")
                respuesta = modelo_groq.generar_respuesta(prompt)
                print("Respuesta del modelo Groq:", respuesta, "\n")
                self.console.print(Markdown(respuesta))

            elif self.opcion == "3":
                modelo_local = ModeloLocal()
                prompt = input("Ingrese su prompt: ")
                respuesta = modelo_local.generar_respuestas(prompt)
                print("Respuesta del modelo local:", respuesta, "\n")
                self.console.print(Markdown(respuesta))
            
            elif self.opcion == "4":
                modelo_local = ModeloLocal2()
                prompt = input("Ingrese su prompt: ")
                respuesta = modelo_local.generar_respuestas(prompt)
                print("Respuesta del modelo local:", respuesta, "\n")
                self.console.print(Markdown(respuesta))

            elif self.opcion == "5":
                prompt_01 = Prompt01()
                respuesta = prompt_01.generar_respuestas()
                print("Respuesta del prompt básico:")
                self.console.print(Markdown(respuesta))
            
            elif self.opcion == "6":
                prompt_02 = Prompt_02()
                respuesta = prompt_02.generar_respuestas()
                print("Respuesta del prompt template:")
                self.console.print(Markdown(respuesta))

            elif self.opcion == "7":
                prompt_roles = Prompt_Roles()
                respuesta = prompt_roles.generar_respuesta()
                print("Respuesta del modelo Roles:")
                self.console.print(Markdown(respuesta))    
            
            elif self.opcion == "8":
                modelo_sin_memoria = ModeloSinMemoria()
                modelo_sin_memoria.generar_respuesta()

            elif self.opcion == "9":
                modelo_con_memoria = ModeloConMemoria()
                modelo_con_memoria.generar_respuesta()

            elif self.opcion == "10":
                modelo_con_persistencia = ModeloConPersistencia()
                modelo_con_persistencia.generar_respuesta()    

            elif self.opcion == "0":
                print("Saliendo del programa...")
                break

            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
            self.pausar()