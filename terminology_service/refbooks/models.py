from django.db import models


class Refbook(models.Model):
    code = models.CharField(max_length=100, unique=True, null=False, verbose_name="Код")
    name = models.CharField(max_length=300, null=False, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return self.name

class RefbookVersion(models.Model):
    refbook = models.ForeignKey(Refbook, related_name='versions', on_delete=models.CASCADE, verbose_name="Справочник")
    version = models.CharField(max_length=50, null=False, verbose_name="Версия")
    start_date = models.DateField(verbose_name="Дата начала действия")

    class Meta:
        unique_together = ('refbook', 'version', 'start_date')
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочников"

    def __str__(self):
        return f"{self.refbook.name} - {self.version}"

class RefbookElement(models.Model):
    version = models.ForeignKey(RefbookVersion, related_name='elements', on_delete=models.CASCADE, verbose_name="Версия справочника")
    code = models.CharField(max_length=100, null=False, verbose_name="Код элемента")
    value = models.CharField(max_length=300, null=False, verbose_name="Значение элемента")

    class Meta:
        unique_together = ('version', 'code')
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочников"

    def __str__(self):
        return self.value
