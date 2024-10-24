from dotenv import load_dotenv
from crewai import Agent, Crew, LLM
from tasks import (
    analyze_paper_task,
    read_fastapi_docs_task,
    read_scipy_docs_task,
    combine_analysis_task,
    generate_service_task
)

load_dotenv()

llm = LLM(model="gpt-4o-mini")

analyzer_agent = Agent(
    role="Analyzer Agent",
    goal="Analyze papers and documentation to extract actionable insights.",
    backstory="An expert in academic analysis and technical documentation.",
    llm=llm,
    allow_code_execution=True
)

coder_agent = Agent(
    role="Python Developer",
    goal="Generate Python code based on the insights provided by the Analyzer.",
    backstory="Expert in Python development, FastAPI, and SciPy.",
    llm=llm,
    allow_code_execution=True
)


def get_crew():
    return Crew(
        agents=[analyzer_agent, coder_agent],
        tasks=[
            analyze_paper_task,
            read_fastapi_docs_task,
            read_scipy_docs_task,
            combine_analysis_task,
            generate_service_task
        ],
        verbose=True
    )
