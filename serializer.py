class Serializer:
    @staticmethod
    def article(
        article,
        publication=None,
        signature=None,
        section=None,
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
    def publication(publication) -> dict | None:
        if publication is None:
            return publication

        return {
            "pk": publication.pk,
            "cover": str(publication.cover),
            "file": str(publication.file),
            "number": publication.number,
            "date": publication.date,
        }

    @staticmethod
    def section(section) -> dict | None:
        if section is None:
            return section

        return {"pk": section.pk, "name": section.name}

    @staticmethod
    def signature(signature) -> dict | None:
        if signature is None:
            return signature

        return {
            "pk": signature.pk,
            "name": signature.name,
            "portrait": str(signature.portrait),
        }
