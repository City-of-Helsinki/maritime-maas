from django.db import models
from django.utils.translation import gettext_lazy as _


class BookingStatus(models.TextChoices):
    RESERVED = "RESERVED", _("Reserved")
    CONFIRMED = "CONFIRMED", _("Confirmed")


class LocaleChoices(models.TextChoices):
    FINNISH = "fi", _("Finnish")
    ENGLISH = "en", _("English")
    SWEDISH = "sv", _("Swedish")
