# Generated by Django 3.1.7 on 2021-04-26 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gtfs", "0020_add_block_id_relocate_capacity_sales"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stoptime",
            name="arrival_time",
            field=models.DurationField(
                blank=True, null=True, verbose_name="arrival time"
            ),
        ),
        migrations.AlterField(
            model_name="stoptime",
            name="departure_time",
            field=models.DurationField(
                blank=True, null=True, verbose_name="departure time"
            ),
        ),
    ]