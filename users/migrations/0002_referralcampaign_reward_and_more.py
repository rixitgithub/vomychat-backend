# Generated by Django 4.2.7 on 2025-02-27 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('multiplier', models.FloatField(default=1.0)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField(default=0)),
                ('unlocked_tiers', models.JSONField(default=list)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='referral',
            old_name='date_referred',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='referral',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='referral',
            name='tier',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Direct'), (2, 'Level 2'), (3, 'Level 3')], default=1),
        ),
        migrations.AddIndex(
            model_name='referral',
            index=models.Index(fields=['referrer', 'tier'], name='users_refer_referre_7af483_idx'),
        ),
        migrations.AddIndex(
            model_name='referral',
            index=models.Index(fields=['created_at'], name='users_refer_created_bffbb8_idx'),
        ),
        migrations.AddField(
            model_name='reward',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rewards', to=settings.AUTH_USER_MODEL),
        ),
    ]
