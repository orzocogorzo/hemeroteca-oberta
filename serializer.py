# built-ins
import re

# source
from hemeroteca.models import Article, Content, Publication, Section, Signature


class Serializer:
    @staticmethod
    def article(
        article: Article,
        publication: Publication | None = None,
        signature: Signature | None = None,
        section: Section | None = None,
    ) -> dict:
        if publication is None:
            publication = article.publication

        if signature is None:
            signature = article.signature

        if section is None:
            section = article.section

        return {
            "pk": article.pk,
            "title": article.title,
            "page": article.page,
            "publication": Serializer.publication(publication),
            "section": Serializer.section(section),
            "signature": Serializer.signature(signature),
        }

    @staticmethod
    def publication(publication: Publication) -> dict | None:
        if publication is None:
            return publication

        return {
            "pk": publication.pk,
            "cover": str(publication.cover),
            "file": str(publication.file),
            "number": publication.number,
            "date": publication.date,
            "is_vector": publication.is_vector,
        }

    @staticmethod
    def publication_matches(
        publication: Publication, contents: list[Content], pattern: str
    ) -> dict | None:
        publication = Serializer.publication(publication)
        if publication is None:
            return Publication

        publication["matches"] = []
        for content in contents:
            match = re.search(pattern, content.text)
            if match is None:
                continue

            publication["matches"].append(
                {
                    "pageIndex": content.page,
                    "pageText": content.text,
                    "startIndex": match.start(),
                    "endIndex": match.end(),
                }
            )

        return publication

    @staticmethod
    def content(content: Content) -> dict | None:
        if content is None:
            return content

        return {"text": content.text, "page": content.page}

    @staticmethod
    def section(section: Section) -> dict | None:
        if section is None:
            return section

        return {"pk": section.pk, "name": section.name}

    @staticmethod
    def signature(signature: Signature) -> dict | None:
        if signature is None:
            return signature

        return {
            "pk": signature.pk,
            "name": signature.name,
            "portrait": str(signature.portrait),
        }
