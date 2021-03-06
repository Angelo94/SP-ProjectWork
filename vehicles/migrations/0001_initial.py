# Generated by Django 2.0.5 on 2018-06-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('bookid', models.AutoField(primary_key=True, serialize=False)),
                ('userid', models.IntegerField()),
                ('vehiclesid', models.IntegerField()),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('place', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('vehiclesid', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('model', models.CharField(max_length=100)),
            ],
        ),
    ]
