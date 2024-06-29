import logging

import click

from resume_assist.service.cli import services

logger = logging.getLogger(__name__)


@click.group()
def cli():
    logging.basicConfig(
        level=logging.NOTSET,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


cli.add_command(services)


if __name__ == "__main__":
    cli()
