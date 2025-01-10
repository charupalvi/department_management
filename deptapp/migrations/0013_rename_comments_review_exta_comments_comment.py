# Generated by Django 5.1.1 on 2025-01-10 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deptapp', '0012_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='comments',
            new_name='exta_comments',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='deptapp.review')),
            ],
        ),
    ]