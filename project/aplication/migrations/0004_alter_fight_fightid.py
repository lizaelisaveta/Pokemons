# Generated by Django 4.2.5 on 2023-10-17 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0003_alter_fight_fightid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fight',
            name='fightid',
            field=models.AutoField(auto_created=True, db_column='FightId', primary_key=True, serialize=False),
        ),
    ]
