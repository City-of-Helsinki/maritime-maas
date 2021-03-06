# Generated by Django 3.1.7 on 2021-04-22 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gtfs", "0019_add_shape"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trip",
            name="capacity_sales",
        ),
        migrations.AddField(
            model_name="route",
            name="capacity_sales",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Disabled"), (1, "Enabled"), (2, "Required")],
                default=0,
                verbose_name="capacity sales",
            ),
        ),
        migrations.AddField(
            model_name="trip",
            name="block_id",
            field=models.CharField(blank=True, max_length=255, verbose_name="block ID"),
        ),
    ]
