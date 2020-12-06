""""""

# Standard library modules.
from pathlib import Path
import argparse
import itertools

# Third party modules.
import pdfminer.high_level
import PyPDF2

# Local modules.

# Globals and constants variables.


def crop(filepath, outfilepath, remove_first_page=False):
    pages = list(pdfminer.high_level.extract_pages(filepath))

    bboxs = []
    for page in pages:
        bboxs.append(page.groups[0].bbox)

    with open(filepath, "rb") as fp, open(outfilepath, "wb") as fpout:
        pdf = PyPDF2.PdfFileReader(fp)
        pdfout = PyPDF2.PdfFileWriter()

        start = 1 if remove_first_page else 0

        for page, bbox in itertools.islice(zip(pdf.pages, bboxs), start, None):
            page.cropBox = PyPDF2.generic.RectangleObject(bbox)
            pdfout.addPage(page)

        pdfout.write(fpout)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("file", nargs="+", type=Path, help="File to crop")
    parser.add_argument(
        "--remove-first-page", "-r", action="store_true", help="Remove first page"
    )

    args = parser.parse_args()

    for filepath in args.file:
        outfilepath = filepath.with_name(f"{filepath.stem}-cropped{filepath.suffix}")
        crop(filepath, outfilepath, args.remove_first_page)
        print(f"{filepath} -> {outfilepath}")


if __name__ == "__main__":
    main()
