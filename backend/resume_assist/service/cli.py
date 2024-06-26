import click
import uvicorn

from resume_assist.service.rest.factories import create_fastapi_application


@click.group()
def services():
    pass


@services.command()
@click.option("--host", default="0.0.0.0", type=str, show_default=True)
@click.option(
    "--port", default="10010", type=click.IntRange(0, 65536), show_default=True
)
def start(host, port):
    app = create_fastapi_application()
    uvicorn.run(app, host=host, port=port)
