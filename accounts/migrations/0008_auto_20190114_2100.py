# Generated by Django 2.1.2 on 2019-01-14 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190110_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='universityYear',
            field=models.CharField(choices=[('1', '1st year'), ('2', '2nd year'), ('3', '3rd year')], default='', max_length=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='module',
            field=models.ManyToManyField(to='accounts.Module'),
        ),
    ]
