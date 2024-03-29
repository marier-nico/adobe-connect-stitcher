# Adobe Connect Stitcher

**Requirements**

- Make `ffmpeg` available in your system path (usually, installing it with the system package manager works).
- Install dependencies listed in `pyproject.toml` (either with `pip` or `poetry`). See below for details.

**Dependency Management**

To install packages, you can either use `pip` with a virtualenv that you create yourself (i.e. with
`python -m venv my-venv`), or you can use [Poetry](https://python-poetry.org/). When using poetry, you can simply run
`poetry install`, followed by `poetry shell` to install all dependencies and use the virtual environment.

**Usage**

```shell
Usage: python -m stitcher [OPTIONS] [CONNECT_DIR]

Arguments:
  [CONNECT_DIR]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.
```

The value for `CONNECT_DIR` should be the directory where you unzipped the contents of the meeting downloaded from
Adobe Connect.

To download the data for a given meeting, you'll need to know the URL you used to access the meeting when it was live.
The URL will look something like `https://<adobe-connect-domain>/<meeting-id>`, where `<adobe-connect-domain>` will be
the domain for your Adobe Connect instance, and `<meeting-id>` is the ID of the meeting (for example `pzc5v85utuyx`).

For the download, visit the following URL: `https://<adobe-connect-domain>/<meeting-id>/output/filename.zip?download=zip`,
and replace `<adobe-connect-domain>` and `<meeting-id>` with the values for the meeting you want to download. Doing this
will allow you to download a zip file containing all the files for a given meeting (all the videos, audio,chat
transcripts, etc.)

**Steps**

1. Download the meeting's zip file (see above)
2. Unzip it into a new directory
3. Execute the script and give it the path of the directory containing the meeting data.
4. Move (and rename, if you want) `final_output.mkv` elsewhere, and delete the meeting data.

Note that only audio and screen sharing are saved to the final output. Chat contents and the presenter's video will not
be saved.
