from crew_config import get_crew

if __name__ == "__main__":
    crew = get_crew()

    # Ejecutar las tareas del crew
    result = crew.kickoff()
    print(result)

    print("Process completed successfully!")
