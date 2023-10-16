from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.urls import reverse

from .models import Publication, Section, Signature, Article, Content
from .serializer import Serializer


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

        # page = str(request.GET.get("page", "1"))
        # per_page = str(request.GET.get("per_page", "10"))
        # try:
        #     page = max(0, int(page) - 1)
        #     per_page = int(per_page)
        # except ValueError:
        #     raise BadRequest

        # start = per_page * page
        # end = start + per_page
        limit = request.GET.get("limit")
        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                limit = None

        articles = Article.objects.all().order_by("title")
        if limit:
            articles = articles[:limit]
        return JsonResponse(
            [Serializer.article(article) for article in articles],
            safe=False,
            json_dumps_params={
                "indent": 0,
                "sort_keys": False,
                "separators": (",", ":"),
            },
        )

    @staticmethod
    def search(request: HttpRequest) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest

        search_text = request.GET.get("text")
        if not search_text:
            raise BadRequest

        matches = Content.objects.filter(text__icontains=search_text)
        publications = [Serializer.publication(match.publication) for match in matches]
        return JsonResponse(publications, safe=False)


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
                return render(
                    request,
                    "hemeroteca/publication.html",
                    {"publication": publication, "articles": articles},
                )
            else:
                publications = Publication.objects.all()
                return render(
                    request,
                    "hemeroteca/publications.html",
                    {"publications": publications},
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
                    {"section": section, "articles": articles},
                )
            else:
                sections = Section.objects.all()
                return render(
                    request,
                    "hemeroteca/sections.html",
                    {"sections": sections},
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
                    Serializer.article(article, signature=signature)
                    for article in signature.article_set.all()
                ]
                return render(
                    request,
                    "hemeroteca/signature.html",
                    {"signature": signature, "articles": articles},
                )
            else:
                signatures = Signature.objects.all()
                return render(
                    request,
                    "hemeroteca/signatures.html",
                    {"signatures": signatures},
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
                    {"article": datum},
                )
            else:
                # articles = []
                # for article in Article.objects.all():
                #     datum = Serializer.article(article)
                #     articles.append(datum)

                return render(
                    request,
                    "hemeroteca/articles.html",
                    # {"articles": articles},
                )

        elif request.method == "POST":
            form = ArticleForm(request.POST)
            article = form.save()
            return redirect(reverse("hemeroteca:article", args=(article.pk,)))

        else:
            raise BadRequest

    @staticmethod
    def search(request: HttpRequest) -> HttpResponse:
        return render(request, "hemeroteca/search.html")
