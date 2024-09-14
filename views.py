# built-ins
import os
from functools import reduce

# vendor
from django.conf import settings
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from unidecode import unidecode

# source
from .models import Publication, Section, Signature, Article, Content
from .serializer import Serializer


def get_react_statics() -> dict:
    app_statics = os.path.join(
        os.path.dirname(__file__), "static/hemeroteca/js/pdf-reader/build/static"
    )
    scripts = os.path.join(app_statics, "js")
    styles = os.path.join(app_statics, "css")

    script = [
        os.path.join(scripts, file)
        for file in os.listdir(scripts)
        if file[-3:] == ".js"
    ]
    style = [
        os.path.join(styles, file) for file in os.listdir(styles) if file[-4:] == ".css"
    ]

    if len(script) == 0 or len(style) == 0:
        raise Exception("React scripts not found")

    start_path = os.path.join(os.path.dirname(__file__), "static")
    return {
        "script": os.path.relpath(script[0], start_path),
        "style": os.path.relpath(style[0], start_path),
    }


def fill_context(context: dict) -> dict:
    statics = get_react_statics()
    return {
        "site_base_url": os.getenv("VDV_BASE_URL"),
        "site_title": settings.HEMEROTECA_TITLE,
        "site_description": settings.HEMEROTECA_DESCRIPTION,
        "statics": statics,
        **context,
    }


class API:
    @staticmethod
    def signatures(request: HttpRequest) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest

        signatures = Signature.objects.all()
        return JsonResponse(
            [Serializer.signature(signature) for signature in signatures],
            safe=False,
        )

    @staticmethod
    def sections(request: HttpRequest) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest

        sections = Section.objects.all()
        return JsonResponse(
            [Serializer.section(section) for section in sections],
            safe=False,
        )

    @staticmethod
    def publications(request: HttpRequest) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest

        publications = Publication.objects.all()
        return JsonResponse(
            [Serializer.publication(publication) for publication in publications],
            safe=False,
        )

    @staticmethod
    def articles(request: HttpRequest) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest

        start = int(request.GET.get("start"))
        length = int(request.GET.get("length"))
        end = start + length
        search = request.GET.get("search[value]")

        if search:
            articles = Article.objects.filter(
                Q(title__icontains=search)
                | Q(signatures__name__icontains=search)
                | Q(publication__number__icontains=search)
                | Q(section__name__icontains=search)
            )
        else:
            articles = Article.objects.all()

        return JsonResponse(
            {
                "recordsTotal": Article.objects.count(),
                "recordsFiltered": articles.count(),
                "data": [
                    Serializer.article(article)
                    for article in articles.order_by("title")[start:end]
                ],
            },
            safe=False,
        )

    @staticmethod
    def search(request: HttpRequest) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest

        pattern = request.GET.get("pattern")
        if not pattern:
            raise BadRequest

        pattern = unidecode(pattern.lower())
        matches = Content.objects.filter(text__icontains=pattern)
        publications = [
            Serializer.publication(publication)
            for publication in set([match.publication for match in matches])
        ]

        return JsonResponse(publications, safe=False)

    @staticmethod
    def matches(request: HttpRequest, pk: int) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest

        pattern = request.GET.get("pattern")
        if not pattern:
            raise BadRequest

        pattern = unidecode(pattern.lower())
        matches = Content.objects.filter(publication=pk, text__icontains=pattern)
        if len(matches) == 0:
            return JsonResponse({"matches": []}, safe=False)

        def reducer(handle, content):
            handle[content.publication] = handle.get(content.publication, []) + [
                content
            ]
            return handle

        publication_found = reduce(reducer, matches, {})
        publications = [
            Serializer.publication_matches(publication, contents, pattern)
            for publication, contents in publication_found.items()
        ]

        return JsonResponse(publications[0], safe=False)

    @staticmethod
    def content(request: HttpRequest, pk: int, page: int) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest

        content = get_object_or_404(Content, publication_id=pk, page=page)
        return JsonResponse(Serializer.content(content), safe=False)


class Views:
    @staticmethod
    def index(request: HttpRequest) -> HttpResponse:
        return render(request, "hemeroteca/index.html")

    @staticmethod
    def publications(request: HttpRequest, pk: int | None = None) -> HttpResponse:
        if request.method == "GET":
            if pk is not None:
                publication = get_object_or_404(Publication, pk=pk)
                articles = [
                    Serializer.article(article, publication=publication)
                    for article in publication.article_set.all()
                ]
                statics = get_react_statics()
                return render(
                    request,
                    "hemeroteca/publication.html",
                    fill_context(
                        {
                            "publication": publication,
                            "articles": articles,
                            "statics": statics,
                        }
                    ),
                )
            else:
                publications = Publication.objects.all()
                return render(
                    request,
                    "hemeroteca/publications.html",
                    fill_context({"publications": publications}),
                )

        elif request.method == "POST":
            form = PublicationForm(request.POST)
            publication = form.save()
            return redirect(reverse("hemeroteca:publication", args=(publication.pk,)))
        else:
            raise BadRequest

    @staticmethod
    def sections(request: HttpRequest, pk: int | None = None) -> HttpResponse:
        if request.method == "GET":
            if pk is not None:
                section = get_object_or_404(Section, pk=pk)
                articles = [
                    Serializer.article(article, section=section)
                    for article in section.article_set.all()
                ]
                return render(
                    request,
                    "hemeroteca/section.html",
                    fill_context({"section": section, "articles": articles}),
                )
            else:
                sections = Section.objects.all()
                return render(
                    request,
                    "hemeroteca/sections.html",
                    fill_context({"sections": sections}),
                )

        elif request.method == "POST":
            form = SectionForm(request.POST)
            section = form.save()
            return redirect(reverse("hemeroteca:section", args=(section.pk,)))
        else:
            raise BadRequest

    @staticmethod
    def signatures(request: HttpRequest, pk: int | None = None) -> HttpResponse:
        if request.method == "GET":
            if pk is not None:
                signature = get_object_or_404(Signature, pk=pk)
                articles = [
                    Serializer.article(article)  # , signatures=[signature])
                    for article in signature.article_set.all()
                ]
                return render(
                    request,
                    "hemeroteca/signature.html",
                    fill_context({"signature": signature, "articles": articles}),
                )
            else:
                signatures = Signature.objects.all()
                return render(
                    request,
                    "hemeroteca/signatures.html",
                    fill_context({"signatures": signatures}),
                )

        elif request.method == "POST":
            form = SignatureForm(request.POST)
            signature = form.save()
            return redirect(reverse("hemeroteca:signature", args=(signature.pk,)))
        else:
            raise BadRequest

    @staticmethod
    def articles(request: HttpRequest, pk: int | None = None) -> HttpResponse:
        if request.method == "GET":
            if pk is not None:
                article = get_object_or_404(Article, pk=pk)
                datum = Serializer.article(article)
                return render(
                    request,
                    "hemeroteca/article.html",
                    fill_context({"article": datum}),
                )
            else:
                articles = Article.objects.all()
                return render(
                    request,
                    "hemeroteca/articles.html",
                    fill_context({"articles": articles}),
                )

        elif request.method == "POST":
            form = ArticleForm(request.POST)
            article = form.save()
            return redirect(reverse("hemeroteca:article", args=(article.pk,)))

        else:
            raise BadRequest

    @staticmethod
    def search(request: HttpRequest) -> HttpResponse:
        return render(request, "hemeroteca/search.html", fill_context({}))
