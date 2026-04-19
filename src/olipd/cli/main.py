import typer

app = typer.Typer(help="OLIPD: LLM Inference Optimization Toolkit")

@app.command()
def version():
    """Hiển thị phiên bản của OLIPD."""
    typer.echo("OLIPD version: 0.1.0")

@app.command()
def serve(
    host: str = "0.0.0.0",
    port: int = 8000,
):
    """Khởi chạy API Server."""
    typer.echo(f"Starting API Server on {host}:{port}...")
    # Sẽ tích hợp uvicorn.run("olipd.api.app:app") sau này

if __name__ == "__main__":
    app()
