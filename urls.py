from django.urls import path
from django.views.generic import RedirectView

from .views import API, Views

app_name = "hemeroteca"
urlpatterns = [
    path("", RedirectView.as_view(url="publications/", permanent=True), name="index"),
    path("publications/", Views.publications, name="publications"),
    path(
        "publications/<int:pk>/",
        Views.publications,
        name="publication",
    ),
    path("sections/", Views.sections, name="sections"),
    path(
        "sections/<int:pk>/",
        Views.sections,
        name="section",
    ),
    path("signatures/", Views.signatures, name="signatures"),
    path(
        "signatures/<int:pk>/",
        Views.signatures,
        name="signature",
    ),
    path("articles/", Views.articles, name="articles"),
    path(
        "articles/<int:pk>/",
        Views.articles,
        name="article",
    ),
    path("search/", Views.search, name="search"),
    path("api/publications/", API.publications, name="rs_publications"),
    path("api/sections/", API.sections, name="rs_sections"),
    path("api/signatures/", API.signatures, name="rs_signatures"),
    path("api/articles/", API.articles, name="rs_articles"),
    path("api/search/", API.search, name="rs_search"),
]
