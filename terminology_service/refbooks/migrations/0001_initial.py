# Generated by Django 5.0.7 on 2024-07-17 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Refbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
        migrations.CreateModel(
            name='RefbookVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50, verbose_name='Версия')),
                ('start_date', models.DateField(verbose_name='Дата начала действия')),
                ('refbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='refbooks.refbook', verbose_name='Справочник')),
            ],
            options={
                'verbose_name': 'Версия справочника',
                'verbose_name_plural': 'Версии справочников',
                'unique_together': {('refbook', 'version', 'start_date')},
            },
        ),
        migrations.CreateModel(
            name='RefbookElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, verbose_name='Код элемента')),
                ('value', models.CharField(max_length=300, verbose_name='Значение элемента')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='refbooks.refbookversion', verbose_name='Версия справочника')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочников',
                'unique_together': {('version', 'code')},
            },
        ),
    ]