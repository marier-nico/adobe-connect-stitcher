from pathlib import Path

import typer

from extract_content_info import get_all_content
from stitch_content import stitch

CONNECT_DIR_OPTION = typer.Argument(
    default=None,
    exists=True,
    file_okay=False,
    dir_okay=True,
    writable=False,
    readable=True,
    resolve_path=True,
)


def main(connect_dir: Path = CONNECT_DIR_OPTION):
    content = get_all_content(connect_dir)
    result = stitch(content, connect_dir)
    typer.secho(f"Access the stitched output at {result}")


try:
    typer.run(main)
except Exception as e:
    typer.secho(f"Uncaught exception: {str(e)}", fg=typer.colors.RED)
