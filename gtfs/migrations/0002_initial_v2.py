# Generated by Django 3.1.7 on 2021-03-22 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gtfs", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agency",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="agency",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="calendar",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="calendar",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="calendardate",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="calendardate",
            name="source_id",
        ),
        migrations.RemoveField(
            model_name="calendardate",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="fare",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="fare",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="farerule",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="farerule",
            name="source_id",
        ),
        migrations.RemoveField(
            model_name="farerule",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="route",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="route",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="stop",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="stop",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="stoptime",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="stoptime",
            name="source_id",
        ),
        migrations.RemoveField(
            model_name="stoptime",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="trip",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="trip",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="agency",
            name="source_id",
            field=models.CharField(max_length=255, verbose_name="source ID"),
        ),
        migrations.AlterField(
            model_name="calendar",
            name="source_id",
            field=models.CharField(max_length=255, verbose_name="source ID"),
        ),
        migrations.AlterField(
            model_name="calendardate",
            name="exception_type",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "Added"), (2, "Removed")], verbose_name="exception type"
            ),
        ),
        migrations.AlterField(
            model_name="fare",
            name="source_id",
            field=models.CharField(max_length=255, verbose_name="source ID"),
        ),
        migrations.AlterField(
            model_name="farerule",
            name="route",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fare_rules",
                to="gtfs.route",
                verbose_name="route",
            ),
        ),
        migrations.AlterField(
            model_name="route",
            name="source_id",
            field=models.CharField(max_length=255, verbose_name="source ID"),
        ),
        migrations.AlterField(
            model_name="stop",
            name="source_id",
            field=models.CharField(max_length=255, verbose_name="source ID"),
        ),
        migrations.AlterField(
            model_name="stoptime",
            name="stop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stop_times",
                to="gtfs.stop",
                verbose_name="stop",
            ),
        ),
        migrations.AlterField(
            model_name="trip",
            name="source_id",
            field=models.CharField(max_length=255, verbose_name="source ID"),
        ),
    ]
