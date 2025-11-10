import subprocess
from pathlib import Path

import typer

app = typer.Typer()


def parse_gs_output(gs_output: str):
    return [
        tuple(float(x) for x in line.split()[1:])
        for line in gs_output.splitlines()[1::2]
    ]


@app.command()
def main(pdf_path: Path):
    try:
        gs_result = subprocess.run(
            ["gs", "-dSAFER", "-dNOPAUSE", "-dBATCH", "-sDEVICE=bbox", pdf_path],
            capture_output=True,
            check=True,
            encoding="utf-8",
        )
    except FileNotFoundError as e:
        print("The ghostscript executable `gs` could not be found.")
        raise e

    bounding_boxes = parse_gs_output(gs_result.stderr)
    print(bounding_boxes)


if __name__ == "__main__":
    app()
