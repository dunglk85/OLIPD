import typer

app = typer.Typer(help="OLIPD: LLM Inference Optimization Toolkit")

@app.command()
def version():
    """Hiển thị phiên bản của OLIPD."""
    typer.echo("OLIPD version: 0.1.0")

if __name__ == "__main__":
    app()
