import typer
import json
from agent.parsing.collector import collect_functions

app = typer.Typer()

@app.command("review")
def review_cmd(path: str):
    """
    Analyze Python files in a directory and print collected functions.
    """
    results = collect_functions(path)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    app()
