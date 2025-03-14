# Generated by Django 4.2.14 on 2025-03-07 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UranelDjangoServer', '0006_prescription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lunette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.DateField(auto_now_add=True)),
                ('sphere_vl_od', models.CharField(default='(vide)', max_length=30)),
                ('cylindre_vl_od', models.CharField(default='(vide)', max_length=30)),
                ('axe_vl_od', models.CharField(default='(vide)', max_length=30)),
                ('addition_vl_od', models.CharField(default='(vide)', max_length=30)),
                ('sphere_vp_od', models.CharField(default='(vide)', max_length=30)),
                ('cylindre_vp_od', models.CharField(default='(vide)', max_length=30)),
                ('axe_vp_od', models.CharField(default='(vide)', max_length=30)),
                ('addition_vp_od', models.CharField(default='(vide)', max_length=30)),
                ('sphere_vl_og', models.CharField(default='(vide)', max_length=30)),
                ('cylindre_vl_og', models.CharField(default='(vide)', max_length=30)),
                ('axe_vl_og', models.CharField(default='(vide)', max_length=30)),
                ('addition_vl_og', models.CharField(default='(vide)', max_length=30)),
                ('sphere_vp_og', models.CharField(default='(vide)', max_length=30)),
                ('cylindre_vp_og', models.CharField(default='(vide)', max_length=30)),
                ('axe_vp_og', models.CharField(default='(vide)', max_length=30)),
                ('addition_vp_og', models.CharField(default='(vide)', max_length=30)),
                ('focal', models.CharField(default='(vide)', max_length=30)),
                ('filter', models.CharField(default='(vide)', max_length=30)),
                ('teinte', models.CharField(default='(vide)', max_length=30)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UranelDjangoServer.customer')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UranelDjangoServer.site')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'lunette',
                'verbose_name_plural': 'lunettes',
            },
        ),
    ]
