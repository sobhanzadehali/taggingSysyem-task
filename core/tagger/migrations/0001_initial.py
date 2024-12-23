# Generated by Django 5.1.2 on 2024-10-31 14:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HasPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagger.dataset')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagger.operator')),
            ],
            options={
                'verbose_name': 'permission',
                'verbose_name_plural': 'permissions',
            },
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='body')),
                ('dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tagger.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagger.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='LabeledSentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagger.operator')),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagger.sentence')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tagger.tag')),
            ],
        ),
    ]
