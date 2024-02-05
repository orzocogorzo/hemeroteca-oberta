# BUILT-INS
import os

# VENDOR
from PyPDF2 import PdfReader
from unidecode import unidecode

# SOURCE
from hemeroteca.parsers.image import ImageParser


class PdfParser(object):
    def __init__(self, file_path):
        if not file_path or type(file_path) != str:
            raise ValueError("file_path arguments is not a valid type")
        elif not os.path.isfile(file_path):
            raise FileExistsError("Can't find nothing at the end of the path")

        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.conn = open(file_path, "rb")
        self.parser = PdfReader(self.conn)
        self.pages = [self.parser.pages[i] for i in range(len(self.parser.pages))]

    @property
    def format(self):
        has_text = bool(self.pages[0].extract_text())
        if has_text:
            return "str"
        else:
            return "img"

    @property
    def text(self):
        if self.format == "str":
            text = ""
            for page in self.pages:
                text += "\n" + page.extract_text()

            return text
        else:
            return ImageParser(self.file_path).text

    @property
    def paged_text(self):
        if self.format == "str":
            pages = []
            for i, page in enumerate(self.pages):
                pages.append((i + 1, unidecode(page.extract_text())))

            return pages
        else:
            return ImageParser(self.file_path).paged_text

    def __str__(self):
        return self.text

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    directory = os.path.normpath(
        (
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "../static/hemeroteca/uploads",
            )
        )
    )
    for file_name in os.listdir(os.path.join(directory, "documents")):
        file_path = os.path.join(directory, "documents", file_name)
        parser = PdfParser(file_path)
        print(file_name.upper())
        print(parser.text)
        print()
