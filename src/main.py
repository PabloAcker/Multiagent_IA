import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import PDFSearchTool, CodeDocsSearchTool


## NOTA: es necesario iniciar Docker para ejecutar el codigo


# Cargar variables de entorno
load_dotenv()

# Inicializar el modelo LLM
llm = LLM(model="gpt-4o-mini")
current_dir = os.path.dirname(os.path.abspath(__file__))

# Herramientas que el analyzer utilizará
pdf_tool = PDFSearchTool(pdf="../papers/PaperInformatica.pdf")
fastapi_docs_tool = CodeDocsSearchTool(docs_url="https://fastapi.tiangolo.com")
scipy_docs_tool = CodeDocsSearchTool(docs_url="https://docs.scipy.org/doc/scipy/")

# Agente encargado de analizar la documentación
analyzer_agent = Agent(
    role="Senior Python Developer and Documentation Analyzer",
    goal="Analyze documentation to extract relevant insights for creating FastAPI services.",
    backstory="""You are a senior developer with strong analytical skills, capable of understanding complex documentation 
    and extracting the relevant information to guide the implementation of FastAPI services.""",
    llm=llm,
    tools=[pdf_tool, fastapi_docs_tool, scipy_docs_tool]
)

# Agente encargado de generar el servicio en FastAPI
coder_agent = Agent(
    role="Senior Python Developer",
    goal="Develop a FastAPI service based on the analysis provided.",
    backstory="""You are a senior Python developer tasked with creating robust, well-structured FastAPI services.""",
    llm=llm,
    allow_code_execution=True
)

# Tarea de análisis de documentos por parte del analyzer
analyze_docs_task = Task(
    description="""Analyze the provided PDF, FastAPI documentation, and SciPy documentation. Extract necessary insights 
    and suggestions for implementing a FastAPI service.""",
    expected_output="""A detailed analysis of the documents, extracting key insights and suggestions to guide the FastAPI service implementation.""",
    agent=analyzer_agent,
    output_file="document_analysis.md"
)

# Tarea del coder para implementar el servicio FastAPI
generate_fastapi_service_task = Task(
    description="""Based on the analysis of the provided documents, generate a FastAPI service. 
    The service should expose endpoints that utilize data processing features described in the documents.""",
    expected_output="""A FastAPI service implemented in Python with endpoints that reflect the insights and analysis provided. 
    The service should follow best practices and be thoroughly documented.""",
    agent=coder_agent,
    output_file="fastapi_service.py"
)

# Definición del equipo de agentes (Crew)
dev_crew = Crew(
    agents=[analyzer_agent, coder_agent],
    tasks=[analyze_docs_task, generate_fastapi_service_task],
    verbose=True
)

# Iniciar el proceso del crew
result = dev_crew.kickoff()

# Imprimir los resultados
print(result)
