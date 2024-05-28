from django.db import models


class Publication(models.Model):
    cover = models.ImageField(
        upload_to="static/hemeroteca/uploads/covers/",
        default="hemeroteca/cover-placeholder.png",
        name="cover",
        verbose_name="portada",
        help_text="Portada del número en format png o jpg. <strong>Opcional</strong>",
        blank=True,
        null=True,
    )
    number = models.IntegerField(
        primary_key=True,
        name="number",
        verbose_name="Número",
        help_text="Numeració serial de les publicacions",
    )
    date = models.DateField(
        name="date",
        verbose_name="Data",
        help_text="Data en que es va publicar el número",
    )
    file = models.FileField(
        upload_to="static/hemeroteca/uploads/documents/",
        name="file",
        verbose_name="Document PDF",
        help_text="Arxiu PDF amb la publicació",
    )
    is_vector = models.BooleanField(
        default=True,
        name="is_vector",
        verbose_name="PDF vectorial",
        help_text="L'arxiu font és un PDF de tipus vectorial",
    )

    class Meta:
        verbose_name = "Publicació"
        verbose_name_plural = "Publicacions"
        ordering = ["-number"]

    def __str__(self) -> str:
        return str(self.number)


class Section(models.Model):
    name = models.CharField(
        max_length=100,
        name="name",
        verbose_name="Nom de la secció",
    )

    class Meta:
        verbose_name = "Secció"
        verbose_name_plural = "Seccions"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class Signature(models.Model):
    name = models.CharField(
        max_length=100,
        name="name",
        verbose_name="Nom de la persona redactora",
    )
    portrait = models.ImageField(
        upload_to="hemeroteca/uploads/portraits/",
        default="hemeroteca/portrait-placeholder.png",
        name="portrait",
        verbose_name="Foto de perfil",
        help_text="Imatge en format png o jpg de mida petita. <strong>Opcional</strong>",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmes"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class Article(models.Model):
    title = models.CharField(
        max_length=200,
        name="title",
        verbose_name="Títol",
        help_text="Títol i subtítol si s'escau",
    )
    publication = models.ForeignKey(
        Publication,
        name="publication",
        verbose_name="Número",
        help_text="Número en que es va publicar l'article",
        on_delete=models.CASCADE,
    )
    section = models.ForeignKey(
        Section,
        name="section",
        verbose_name="Secció",
        help_text="Secció on es va publicar l'article. <strong>Opcional</strong>",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )
    signatures = models.ManyToManyField(
        Signature,
        name="signatures",
        verbose_name="Firma",
        help_text="Firma de l'autoria de l'article. <strong>Opcional</strong>",
        default=None,
        blank=True,
    )
    page = models.IntegerField(
        name="page",
        verbose_name="Pàgina",
        help_text="Pàgina on apareix l'article",
        default=1,
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self) -> str:
        return str(self.title)


class Content(models.Model):
    text = models.TextField()
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    page = models.IntegerField(
        name="page",
        verbose_name="Pàgina",
        help_text="Pàgina on apareix l'article",
        default=1,
    )

    class Meta:
        verbose_name = "Contingut"
        verbose_name_plural = "Continguts"

    def __str__(self) -> str:
        return str(self.publication.number)
