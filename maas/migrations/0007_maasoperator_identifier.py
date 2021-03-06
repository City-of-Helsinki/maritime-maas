# Generated by Django 3.1.7 on 2021-05-03 11:45

from django.db import migrations, models


def initialize_identifier(apps, schema_editor):
    MaasOperator = apps.get_model("maas", "MaasOperator")

    MaasOperator.objects.all().update(identifier=models.F("name"))


class Migration(migrations.Migration):

    dependencies = [
        ("maas", "0006_remove_permission_expires_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="maasoperator",
            name="identifier",
            field=models.CharField(
                blank=True,
                help_text="Value is sent in an API call to a ticketing system. Identifies the MaaS operator in a ticketing system.",
                max_length=64,
                verbose_name="identifier",
            ),
        ),
        migrations.RunPython(initialize_identifier, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="maasoperator",
            name="identifier",
            field=models.CharField(
                help_text="Value is sent in an API call to a ticketing system. Identifies the MaaS operator in a ticketing system.",
                max_length=64,
                unique=True,
                verbose_name="identifier",
            ),
        ),
    ]
