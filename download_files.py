import shutil
import requests
from pathlib import Path
from joblib import Parallel, delayed

import click
from rich.progress import Progress


def download_files(url: str, output_directory: Path, progress: Progress, task: int):
    """ """
    if not isinstance(url, str):
        raise TypeError("Expected type str for url!")

    filename = Path(url.split("/")[-1])
    filename = output_directory / filename

    if filename.is_file():
        return

    with requests.get(url, stream=True) as r:
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    progress.update(task, advance=1)


@click.command()
@click.option(
    "--input-url-list",
    "-i",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        path_type=Path,
    ),
    default="url_list.txt",
)
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default="data",
)
def main(input_url_list: str or Path, output_directory: str or Path):
    with open(input_url_list, "r") as f:
        urls = f.read().splitlines()

    output_directory.mkdir(parents=True, exist_ok=True)

    with Progress() as progress:
        dl = progress.add_task("[red]Downloading...", total=len(urls))

        Parallel(backend="threading", n_jobs=16)(
            delayed(download_files)(url, output_directory, progress, dl) for url in urls
        )


if __name__ == "__main__":
    main()
