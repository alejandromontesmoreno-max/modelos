from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
import hashlib
import json


class ModeloRAG:
    def __init__(self, nombre_pdf="reglamento_laboratorio.pdf"):
        self.modelo = ChatOllama(model="qwen2.5:3b", temperature=0.1)

        # Modelo de embeddings: convierte texto en vectores
        self.nombre_modelo_embeddings = "qwen3-embedding:0.6b"
        self.embeddings = OllamaEmbeddings(model=self.nombre_modelo_embeddings)

        # Rutas junto al .py, sin depender de la carpeta desde donde se ejecuta
        carpeta = Path(__file__).parent
        self.archivo_pdf = carpeta / nombre_pdf
        self.archivo_indice = carpeta / "indice.json"
        # Huella del PDF y la configuración con que se creó el índice
        self.archivo_huella = carpeta / "indice_huella.json"

        # Parámetros de fragmentación y búsqueda
        self.tamano_fragmento = 500
        self.traslape = 100
        self.fragmentos_por_pregunta = 3

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

        # El índice se prepara al iniciar la conversación, no al crear el objeto,
        # para que un error (PDF faltante, Ollama apagado) no detenga el menú
        self.indice = None

    # ------------------------------------------------------------------
    # Conversación
    # ------------------------------------------------------------------
    def generar_respuesta(self):
        if not self.preparar_indice():
            return

        while True:
            pregunta = input("\nUsuario: ").strip()

            if pregunta.lower() == "salir":
                break
            if not pregunta:
                continue

            # Recuperar y generar pueden fallar si Ollama se detiene
            try:
                fragmentos = self.recuperar(pregunta)
                contexto = "\n\n".join(f.page_content for f in fragmentos)
                respuesta = self.cadena.invoke({"contexto": contexto, "pregunta": pregunta})
            except Exception as error:
                print(f"Error al consultar el modelo: {error}")
                continue

            print("IA:", respuesta.content)
            print("Fuentes: páginas", self.paginas_de_origen(fragmentos))

    def recuperar(self, pregunta):
        return self.indice.similarity_search(pregunta, k=self.fragmentos_por_pregunta)

    def paginas_de_origen(self, fragmentos):
        # PyPDFLoader numera las páginas desde 0
        paginas = sorted({f.metadata.get("page", 0) + 1 for f in fragmentos})
        return ", ".join(map(str, paginas))

    # ------------------------------------------------------------------
    # Índice vectorial (equivalente a cargar/guardar historial)
    # ------------------------------------------------------------------
    def preparar_indice(self):
        if not self.archivo_pdf.exists():
            print(f"No se encontró el documento: {self.archivo_pdf.name}")
            return False

        huella = self.calcular_huella()

        # Si el índice guardado corresponde al PDF y configuración actuales, se reutiliza
        if self.indice_vigente(huella):
            try:
                self.indice = InMemoryVectorStore.load(str(self.archivo_indice), self.embeddings)
                print("Índice recuperado desde JSON.")
                return True
            except Exception:
                print("El índice está dañado; se vuelve a crear.")

        try:
            self.indice = self.crear_indice(huella)
        except Exception as error:
            print(f"No se pudo crear el índice: {error}")
            return False

        return True

    def calcular_huella(self):
        # Si cambia el PDF o cualquiera de estos valores, el índice deja de ser válido
        return {
            "pdf_sha256": hashlib.sha256(self.archivo_pdf.read_bytes()).hexdigest(),
            "modelo_embeddings": self.nombre_modelo_embeddings,
            "tamano_fragmento": self.tamano_fragmento,
            "traslape": self.traslape,
        }

    def indice_vigente(self, huella):
        if not (self.archivo_indice.exists() and self.archivo_huella.exists()):
            return False
        try:
            with open(self.archivo_huella, "r", encoding="utf-8") as archivo:
                return json.load(archivo) == huella
        except (json.JSONDecodeError, OSError):
            return False

    def crear_indice(self, huella):
        print("Creando índice, puede tardar unos minutos...")

        documentos = self.cargar_documento()
        fragmentos = self.dividir(documentos)

        if not fragmentos:
            raise ValueError("el PDF no tiene texto seleccionable (¿es un escaneo?)")

        indice = InMemoryVectorStore(self.embeddings)
        indice.add_documents(fragmentos)
        self.guardar_indice(indice, huella)

        print(f"{len(documentos)} páginas, {len(fragmentos)} fragmentos indexados.")
        return indice

    def cargar_documento(self):
        # Un Document por página, con su número en metadata
        return PyPDFLoader(str(self.archivo_pdf)).load()

    def dividir(self, documentos):
        divisor = RecursiveCharacterTextSplitter(
            chunk_size=self.tamano_fragmento,
            chunk_overlap=self.traslape,
        )
        return divisor.split_documents(documentos)

    def guardar_indice(self, indice, huella):
        # Escribe en un temporal y luego reemplaza: el original nunca queda a medias
        temporal = self.archivo_indice.with_suffix(".tmp")
        indice.dump(str(temporal))
        temporal.replace(self.archivo_indice)

        # La huella se guarda al final: si algo falla antes, el índice se recrea
        with open(self.archivo_huella, "w", encoding="utf-8") as archivo:
            json.dump(huella, archivo, ensure_ascii=False, indent=4)
