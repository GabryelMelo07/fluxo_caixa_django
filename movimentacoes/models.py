from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
import pytz

# Create your models here.
class Movimentacao(models.Model):

    TIPO_CHOICES = (
        ("Entrada", "ENTRADA"),
        ("Saída", "SAIDA")
    )

    valor = models.DecimalField (
        null=False,
        blank=False,
        validators=[MinValueValidator(1)],
        decimal_places=2,
        max_digits=10,
        verbose_name='Valor'
    )

    tipo = models.CharField (
        max_length=7,
        choices=TIPO_CHOICES,
        null=False,
        blank=False,
        verbose_name='Tipo'
    )

    descricao = models.TextField (
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Descrição'
    )

    data_hora = models.DateTimeField (
        default=timezone.localtime(),
        editable=False,
        verbose_name='Data e hora'
    )

    def __str__(self):
        return f'Movimentação {self.pk} - {self.descricao}'
    