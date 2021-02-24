from pathlib import Path
from typing import Optional

import typer


def main(connect_zip: Optional[Path] = typer.Argument(default=None, exists=True, file_okay=True, dir_okay=False, writable=False,
                                                    readable=True,
                                                    resolve_path=True)):
    if not connect_zip:
        typer.secho("Please provide a zip file obtained from Adobe Connect", fg=typer.colors.RED)
    else:
        typer.secho(f"You provided the file: {connect_zip}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    typer.run(main)
