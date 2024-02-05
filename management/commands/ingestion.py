import os.path
import re
import warnings
import csv
from datetime import date, datetime as dt
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import pyexcel as pe
import fitz

from hemeroteca.models import Publication, Section, Signature, Article, Content
from hemeroteca.parsers.pdf import PdfParser


def parse_value(value: Any, field: str) -> Any:
    if value is None:
        return None

    elif field == "date":
        if type(value) is not date:
            try:
                return dt.strptime(value, "%m/%Y")
            except Exception as e:
                warnings.warn("Error parsing {field} with value {value}")
                print(e)
                return None

        return value

    elif field == "number":
        try:
            return int(value)
        except Exception as e:
            warnings.warn("Error parsing {field} with value {value}")
            print(e)
            return None

    value = str(value).strip()
    if value.lower() == "x" or value == "" or value == "-":
        return None
    else:
        return re.sub(r" *\n *", ", ", value)


def parse_name(name: str) -> list[str]:
    names = []
    for n0 in name.strip().split("/"):
        for n1 in re.split(r" i ", n0.strip(), 0, re.IGNORECASE):
            for n2 in re.split(r" *, +", n1.strip()):
                for n3 in n2.strip().split("\n"):
                    names.append(n3)

    return [name for name in names if name]


def get_cover(file_path: str) -> fitz.Pixmap:
    dpi = 300  # choose desired dpi here
    zoom = dpi / 72  # zoom factor, standard: 72 dpi
    magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
    doc = fitz.open(file_path)  # open document
    page = list(doc.pages())[0]
    return page.get_pixmap(matrix=magnify)  # render page to an image


class CatalogFields:
    _file: int = 0
    _number: int = 1
    _date: int = 2
    _section: int = 3
    _title: int = 4
    _signature: int = 5
    _page: int = 6

    @property
    def publication(self):
        return {
            "file": self._file,
            "number": self._number,
            "date": self._date,
        }

    @property
    def section(self):
        return {"name": self._section}

    @property
    def signature(self):
        return {"name": self._signature}

    @property
    def article(self):
        return {
            "title": self._title,
            "publication": self._number,
            "section": self._section,
            "signature": self._signature,
            "number": self._number,
            "page": self._page,
        }

    @property
    def content(self):
        return {"file": self._file}

    def datum(self, field, row):
        schema = getattr(self, field)
        return {key: parse_value(row[index], key) for key, index in schema.items()}

    @staticmethod
    def validate(headers: list) -> bool:
        return len(headers) == 7


class Command(BaseCommand):
    help: str = "Ingest your pdf catalog"
    catalog: str = ""
    uploads: str = "hemeroteca/static/hemeroteca/uploads"
    headers: dict[str, int] = {}
    fields: CatalogFields = CatalogFields()

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "catalog",
            type=os.path.abspath,
            help="Path to the catalog folder",
        )

        parser.add_argument(
            "--flush",
            action="store_true",
            help="Flush database before ingestion",
        )

    def handle(self, *args, **options) -> str:
        self.catalog = options["catalog"]
        if not self.catalog:
            raise CommandError("Catalog argument is required")

        if os.path.isdir(self.catalog):
            raise CommandError("Catalog file is a directory")

        if not os.path.exists(self.catalog):
            raise CommandError("Catalog file does not exists")

        if options["flush"]:
            self.flush_data()

        headers, data = self.load_data()
        if self.fields.validate(headers) is False:
            raise CommandError("Invalid table structure")

        count = 0
        for row in data:
            if not row[0]:
                continue

            publication = self.post_publication(row)
            section = self.post_section(row)
            signature = self.post_signature(row)
            article = self.post_article(row)

            doc = {
                "publication": publication.number,
                "section": section.name if section else "",
                "article": article.title,
                "signature": signature.name if signature else "",
            }

            if options["verbosity"] > 0:
                print(doc)

            count += 1

        return f"Ingestion completed with {count} inserts"

    def flush_data(self) -> None:
        Content.objects.all().delete()
        Article.objects.all().delete()
        Signature.objects.all().delete()
        Section.objects.all().delete()
        Publication.objects.all().delete()

    def load_data(self) -> tuple[list, list]:
        file_ext = os.path.splitext(self.catalog)[1]
        if file_ext == ".ods":
            book = pe.get_book(file_name=self.catalog)
            data = book.get_bookdict()["Sheet1"]
            headers = data[0]
            data = data[1:]
        elif file_ext == ".csv":
            reader = csv.reader(self.catalog)
            data = [row for row in reader]
            headers = data[0]
            data = data[1:]
        else:
            raise CommandError(
                f"Format not supported for file {os.path.basename(self.catalog)}"
            )

        return [val.strip() for val in headers], data

    def post_publication(self, row: list) -> Publication:
        datum = self.fields.datum("publication", row)

        try:
            publication = Publication.objects.get(number=int(datum["number"]))
        except Publication.DoesNotExist:
            file_path = os.path.abspath(
                os.path.join(os.path.dirname(self.catalog), datum["file"])
            )
            store_path = os.path.join(
                self.uploads,
                "documents",
                os.path.basename(file_path),
            )

            with open(file_path, "rb") as rfp:
                with open(store_path, "wb") as wfp:
                    wfp.write(rfp.read())

            cover_img = get_cover(file_path)
            cover_path = os.path.join(
                self.uploads,
                "covers",
                str(datum["number"]) + ".png",
            )
            cover_img.save(cover_path)
            datum["cover"] = cover_path

            publication = Publication(
                cover=re.sub(r"^hemeroteca\/static\/", "", datum["cover"]),
                file=re.sub(r"^hemeroteca\/static\/", "", os.path.join(store_path)),
                number=int(datum["number"]),
                date=datum["date"],
            )
            publication.save()

            fmt_handle = {"is_vector": True}
            if (
                hasattr(settings, "HEMEROTECA_SEARCH_CONTENT")
                and settings.HEMEROTECA_SEARCH_CONTENT is True
            ):
                self.post_content(row, publication, fmt_handle)

            publication.is_vector = fmt_handle["is_vector"]
            publication.save()

        return publication

    def post_section(self, row: list) -> Section | None:
        datum = self.fields.datum("section", row)

        if not datum["name"]:
            return None

        try:
            section = Section.objects.get(name=datum["name"])
        except Section.DoesNotExist:
            section = Section(name=datum["name"])
            section.save()

        return section

    def post_signature(
        self, row: list, name: str | None = None
    ) -> Signature | list[Signature] | None:
        if name is None:
            datum = self.fields.datum("signature", row)

            if not datum["name"]:
                return None

            name = datum["name"]

        try:
            signature = Signature.objects.get(name=name)
        except Signature.DoesNotExist:
            signature = Signature(name=name)
            signature.save()

        return signature

    def post_article(self, row: list) -> Article:
        datum = self.fields.datum("article", row)

        publication = Publication.objects.get(number=datum["number"])

        if not datum["section"]:
            section = None
        else:
            section = Section.objects.get(name=datum["section"])

        if not datum["signature"]:
            signature = None
        else:
            try:
                signature = Signature.objects.get(name=datum["signature"])
            except Signature.DoesNotExist as e:
                print(e)
                signature = None

        article = Article(
            title=datum["title"],
            publication=publication,
            section=section,
            signature=signature,
            page=datum["page"],
        )

        article.save()
        return article

    def post_content(
        self, row: list, publication: Publication, fmt_handle: dict
    ) -> list[Content]:
        datum = self.fields.datum("content", row)
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(self.catalog), datum["file"])
        )
        parser = PdfParser(file_path)
        fmt_handle["is_vector"] = parser.format == "str"

        pages = []
        for page, text in parser.paged_text:
            content = Content(text=text.lower(), page=page, publication=publication)
            content.save()
            pages.append(content)

        return pages
