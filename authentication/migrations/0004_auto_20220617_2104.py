# Generated by Django 3.2 on 2022-06-17 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_consultant_working_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultant',
            name='working_period',
        ),
        migrations.AlterField(
            model_name='consultant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='consultant', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='visitor', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='WorkingPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='working_period', to='authentication.consultant')),
            ],
        ),
    ]