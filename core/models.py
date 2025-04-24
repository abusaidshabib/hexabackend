# pylint: disable=too-few-public-methods
""" core/models.py """

from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model with creation and update timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Avoid creating a table for this model in the database."""
        abstract = True
