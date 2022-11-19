# Generated by Django 4.0.6 on 2022-11-19 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management_app', '0020_remove_leavereportstaff_staff_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('soilmoisture', models.CharField(max_length=255)),
                ('ph', models.CharField(max_length=255)),
                ('metal', models.CharField(max_length=255)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management_app.staffs')),
            ],
        ),
    ]