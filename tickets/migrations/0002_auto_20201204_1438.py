# Generated by Django 3.1.4 on 2020-12-04 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ticketpassinganswer',
            unique_together={('ticket_passing', 'answer')},
        ),
    ]