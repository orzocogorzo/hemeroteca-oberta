from django.forms import ModelForm

from .models import Publication, Section, Signature, Article


class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        fields = ["number", "date", "cover", "file"]


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ["name"]


class SignatureForm(ModelForm):
    class Meta:
        model = Signature
        fields = ["name"]


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "publication", "section", "signature"]
