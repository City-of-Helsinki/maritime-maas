# Generated by Django 3.1.7 on 2021-03-26 13:30
from uuid import uuid5

from django.db import migrations, models

from gtfs.models.base import API_ID_NAMESPACE


def populate_api_id(apps, schema_editor):
    for model_name in ("Agency", "Calendar", "Fare", "Route", "Stop", "Trip"):
        model = apps.get_model("gtfs", model_name)
        for obj in model.objects.all():
            obj.api_id = uuid5(
                API_ID_NAMESPACE,
                f"{model.__name__}:{obj.feed_id}:{obj.source_id}",
            )
            obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("gtfs", "0002_initial_v2"),
    ]

    operations = [
        migrations.AddField(
            model_name="agency",
            name="api_id",
            field=models.UUIDField(
                default="00000000-0000-0000-0000-000000000000", verbose_name="API ID"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="calendar",
            name="api_id",
            field=models.UUIDField(
                default="00000000-0000-0000-0000-000000000000", verbose_name="API ID"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="fare",
            name="api_id",
            field=models.UUIDField(
                default="00000000-0000-0000-0000-000000000000", verbose_name="API ID"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="route",
            name="api_id",
            field=models.UUIDField(
                default="00000000-0000-0000-0000-000000000000", verbose_name="API ID"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="stop",
            name="api_id",
            field=models.UUIDField(
                default="00000000-0000-0000-0000-000000000000", verbose_name="API ID"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="trip",
            name="api_id",
            field=models.UUIDField(
                default="00000000-0000-0000-0000-000000000000", verbose_name="API ID"
            ),
            preserve_default=False,
        ),
        migrations.RunPython(populate_api_id, migrations.RunPython.noop),
    ]