from crewai import Task
from crewai_tools import PDFSearchTool, CodeDocsSearchTool

pdf_tool = PDFSearchTool(pdf="../papers/Programacion_competitiva_Manual_para_concursantes_del_ICPC_y_la (1).pdf")
fastapi_docs_tool = CodeDocsSearchTool(docs_url="https://fastapi.tiangolo.com")
scipy_docs_tool = CodeDocsSearchTool(docs_url="https://docs.scipy.org/doc/scipy/")

analyze_paper_task = Task(
    description="Extract key insights from the academic paper.",
    expected_output="A summary of the key points relevant to the service.",
    agent="Analyzer Agent",
    tools=[pdf_tool],
    output_file="../artifacts/analysis_summary.txt"
)


read_fastapi_docs_task = Task(
    description="Extract relevant examples from FastAPI documentation.",
    expected_output="Examples or snippets relevant to the service from FastAPI.",
    agent="Analyzer Agent",
    tools=[fastapi_docs_tool]
)

read_scipy_docs_task = Task(
    description="Extract relevant examples from SciPy documentation.",
    expected_output="Examples or snippets relevant to the service from SciPy.",
    agent="Analyzer Agent",
    tools=[scipy_docs_tool]
)

combine_analysis_task = Task(
    description=(
        "Combine the insights from the paper and documentation into a cohesive plan "
        "for the FastAPI service."
    ),
    expected_output="A consolidated analysis with a plan for the service implementation.",
    agent="Analyzer Agent"
)


generate_service_task = Task(
    description=(
        "Generate a FastAPI service and additional modules based on the combined analysis."
    ),
    expected_output="A FastAPI service and helper modules saved as Python files.",
    agent="Python Developer",
    dependencies=[combine_analysis_task],
    output_file="../artifacts/fastapi_service.py"
)
