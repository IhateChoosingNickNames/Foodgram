from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractModel(models.Model):
    """Модель для наследования."""

    name = models.CharField(_("Название"), max_length=128)
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("дата публикации"), db_index=True
    )

    class Meta:
        abstract = True
