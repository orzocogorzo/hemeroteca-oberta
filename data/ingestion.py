# BUILT-IN
import os.path
from datetime import date, datetime as dt
import re
from typing import Any

# VENDOR
import pyexcel as pe
import fitz

# SOURCE
from hemeroteca.models import Publication, Section, Signature, Article, Content
from hemeroteca.parsers.pdf import PdfParser


src_dir = "hemeroteca/data"
uploads_dir = "hemeroteca/static/hemeroteca/uploads"


def parse_value(value: Any, field: str) -> Any:
    if value is None:
        return None

    elif field == "date":
        if type(value) is not date:
            try:
                return dt.strptime(value, "%m/%Y")
            except Exception:
                return None
        else:
            return value

    elif field == "number":
        try:
            return int(value)
        except:
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


# def get_intervieweds(
#     name: str, surname: str | None
# ) -> tuple[list[str], list[str] | list[None]]:
#     names = parse_name(name)
#     if surname:
#         surnames = parse_name(surname)
#     else:
#         surnames = [None] * len(names)

#     if len(names) > 1 and len(surnames) == 1:
#         surnames = surnames * len(names)
#     elif len(names) == 1 and len(surnames) > 1:
#         surnames = [" i ".join(surnames)]

#     if len(names) != len(surnames):
#         surnames = [None] * len(names)

#     return names, surnames


def load_data():
    book = pe.get_book(file_name=os.path.join(src_dir, "index.ods"))
    data = book.get_bookdict()["Sheet1"]
    headers = data[0]
    data = data[1:]

    return [val.strip() for val in headers], data


def get_cover(file_path: str) -> fitz.Pixmap:
    dpi = 300  # choose desired dpi here
    zoom = dpi / 72  # zoom factor, standard: 72 dpi
    magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
    doc = fitz.open(file_path)  # open document
    page = list(doc.pages())[0]
    return page.get_pixmap(matrix=magnify)  # render page to an image


def post_publication(columns: dict[str, int], row: list) -> Publication:
    schema = {
        "file": columns["Arxiu"],
        "number": columns["Número"],
        "date": columns["Data"],
        # "cover": None,
    }

    datum = {key: parse_value(row[index], key) for key, index in schema.items()}

    try:
        publication = Publication.objects.get(number=int(datum["number"]))
    except Publication.DoesNotExist:
        file_path = os.path.join(uploads_dir, "documents", datum["file"])
        with open(os.path.join(src_dir, "pdfs", datum["file"]), "rb") as rsock:
            with open(file_path, "wb") as wsock:
                wsock.write(rsock.read())

        cover_img = get_cover(os.path.join(src_dir, "pdfs", datum["file"]))
        cover_path = os.path.join(uploads_dir, "covers", str(datum["number"]) + ".png")
        cover_img.save(cover_path)
        datum["cover"] = cover_path

        publication = Publication(
            cover=re.sub(r"^hemeroteca\/static\/", "", datum["cover"]),
            file=re.sub(r"^hemeroteca\/static\/", "", os.path.join(file_path)),
            number=int(datum["number"]),
            date=datum["date"],
        )
        publication.save()

        post_content(columns, row, publication)

    return publication


def post_section(columns: dict[str, int], row: list) -> Section | None:
    schema = {"name": columns["Secció"]}
    datum = {key: parse_value(row[index], key) for key, index in schema.items()}

    if not datum["name"]:
        return None

    try:
        section = Section.objects.get(name=datum["name"])
    except Section.DoesNotExist:
        section = Section(name=datum["name"])
        section.save()

    return section


def post_signature(
    columns: dict[str, int], row: list, name: str | None = None
) -> Signature | list[Signature] | None:
    if name is None:
        schema = {"name": columns["Firma"]}
        datum = {key: parse_value(row[index], key) for key, index in schema.items()}

        if not datum["name"]:
            return None

        # elif len(datum["name"].split(",")) > 1:
        #     signatures = []
        #     for name in datum["name"].split(","):
        #         if not name:
        #             continue
        #         signature = post_signature(columns, row, name)
        #         signatures.append(signature)

        #     return signatures

        name = datum["name"]

    try:
        signature = Signature.objects.get(name=name)
    except Signature.DoesNotExist:
        signature = Signature(name=name)
        signature.save()

    return signature


def post_article(columns: dict[str, int], row: list) -> Article:
    schema = {
        "title": columns["Títol"],
        "publication": columns["Número"],
        "section": columns["Secció"],
        "signature": columns["Firma"],
        "number": columns["Número"],
        "page": columns["Pàgina"],
    }

    datum = {key: parse_value(row[index], key) for key, index in schema.items()}

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
        except Signature.DoesNotExist:
            import pdb

            pdb.set_trace()
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
    columns: dict[str, int], row: list, publication: Publication
) -> Content:
    file_path = os.path.join(src_dir, "pdfs", row[columns["Arxiu"]])
    parser = PdfParser(file_path)
    text = parser.text

    content = Content(text=text, publication=publication)
    content.save()
    return content


def ingest_data() -> list[dict]:
    headers, data = load_data()
    columns = {header: i for i, header in enumerate(headers)}

    output = []
    for row in data:
        publication = post_publication(columns, row)
        section = post_section(columns, row)
        signature = post_signature(columns, row)
        article = post_article(columns, row)

        print(
            {
                "publication": publication.number,
                "section": section.name if section else "",
                "article": article.title,
                "signature": signature.name if signature else "",
            }
        )

    return output


if __name__ == "__main__":
    ingestion = ingest_data()
