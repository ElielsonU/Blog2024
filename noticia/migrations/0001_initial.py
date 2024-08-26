# Generated by Django 5.1 on 2024-08-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_publicacao', models.DateField(auto_created=True)),
                ('titulo', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField()),
                ('texto', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='noticias/')),
                ('autor', models.CharField(max_length=100)),
            ],
        ),
    ]
