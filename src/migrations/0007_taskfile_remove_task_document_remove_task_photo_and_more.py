# Generated by Django 5.0.6 on 2024-07-17 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0006_alter_task_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('Taskfile', models.FileField(blank=True, null=True, upload_to='documents/')),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='document',
        ),
        migrations.RemoveField(
            model_name='task',
            name='photo',
        ),
        migrations.AddField(
            model_name='task',
            name='document',
            field=models.ManyToManyField(blank=True, related_name='document', to='src.taskfile'),
        ),
        migrations.AddField(
            model_name='task',
            name='photo',
            field=models.ManyToManyField(blank=True, related_name='photo', to='src.taskfile'),
        ),
    ]
