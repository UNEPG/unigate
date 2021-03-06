# Generated by Django 3.2.9 on 2021-11-06 10:15

import azt_connect.storage_backends
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BmeDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unisat_id', models.IntegerField()),
                ('temperature', models.FloatField()),
                ('pressure', models.FloatField()),
                ('humidity', models.FloatField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Bme DataBase',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='BnoDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unisat_id', models.IntegerField()),
                ('temperature', models.FloatField()),
                ('acceleration', models.CharField(max_length=200)),
                ('magnetic', models.CharField(max_length=200)),
                ('gyro', models.CharField(max_length=200)),
                ('euler', models.CharField(max_length=200)),
                ('quaternion', models.CharField(max_length=200)),
                ('linear_acceleration', models.CharField(max_length=200)),
                ('gravity', models.CharField(max_length=200)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Bno DataBase',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='CameraDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unisat_id', models.IntegerField()),
                ('updated', models.DateTimeField()),
                ('cam_num', models.IntegerField()),
                ('path', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Camera Data Base',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SiDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unisat_id', models.IntegerField()),
                ('updated', models.DateTimeField()),
                ('vis', models.IntegerField()),
                ('ir', models.IntegerField()),
                ('uv', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Si DataBase',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='VcmdSchemaBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unisat_id', models.IntegerField()),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('cam_supported', models.PositiveIntegerField()),
                ('cam_detected', models.PositiveIntegerField()),
                ('state', models.CharField(max_length=10)),
                ('temperature', models.FloatField()),
                ('arm_clock', models.IntegerField()),
                ('core_clock', models.IntegerField()),
                ('serial_clock', models.IntegerField()),
                ('storage_clock', models.IntegerField()),
                ('voltage', models.FloatField()),
                ('otp', models.CharField(max_length=2000)),
                ('cpu_memory', models.PositiveIntegerField()),
                ('gpu_memory', models.PositiveIntegerField()),
                ('config', models.CharField(max_length=1000)),
                ('space', models.CharField(max_length=200)),
                ('memory', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'Vcmd SchemaBase',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SystemData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_expired', models.BooleanField(default=False)),
                ('expire_date', models.DateTimeField(blank=True, null=True)),
                ('date_of_update', models.DateTimeField(auto_now=True)),
                ('date_of_add', models.DateTimeField(auto_now_add=True)),
                ('unisat_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='system_data', to='adapter.vcmdschemabase')),
            ],
            options={
                'verbose_name_plural': 'System Data',
                'ordering': ['-date_of_update'],
            },
        ),
        migrations.CreateModel(
            name='SiData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_expired', models.BooleanField(default=False)),
                ('expire_date', models.DateTimeField(blank=True, null=True)),
                ('date_of_update', models.DateTimeField(auto_now=True)),
                ('date_of_add', models.DateTimeField(auto_now_add=True)),
                ('unisat_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='si_data', to='adapter.sidatabase')),
            ],
            options={
                'verbose_name_plural': 'Si Data',
                'ordering': ['-date_of_update'],
            },
        ),
        migrations.CreateModel(
            name='CameraData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_expired', models.BooleanField(default=False)),
                ('expire_date', models.DateTimeField(blank=True, null=True)),
                ('date_of_update', models.DateTimeField(auto_now=True)),
                ('date_of_add', models.DateTimeField(auto_now_add=True)),
                ('unisat_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='camera_data', to='adapter.cameradatabase')),
            ],
            options={
                'verbose_name_plural': 'Camera Data',
                'ordering': ['-date_of_update'],
            },
        ),
        migrations.CreateModel(
            name='BnoData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_expired', models.BooleanField(default=False)),
                ('expire_date', models.DateTimeField(blank=True, null=True)),
                ('date_of_update', models.DateTimeField(auto_now=True)),
                ('date_of_add', models.DateTimeField(auto_now_add=True)),
                ('unisat_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bno_data', to='adapter.bnodatabase')),
            ],
            options={
                'verbose_name_plural': 'Bno Data',
                'ordering': ['-date_of_add'],
            },
        ),
        migrations.CreateModel(
            name='BmeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_expired', models.BooleanField(default=False)),
                ('expire_date', models.DateTimeField(blank=True, null=True)),
                ('date_of_update', models.DateTimeField(auto_now=True)),
                ('date_of_add', models.DateTimeField(auto_now_add=True)),
                ('unisat_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bme_data', to='adapter.bmedatabase')),
            ],
            options={
                'verbose_name_plural': 'Bme Data',
                'ordering': ['-date_of_update'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='AzatAI ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, verbose_name='Full name')),
                ('image', models.ImageField(blank=True, default='', storage=azt_connect.storage_backends.PublicMediaStorage(), upload_to='images/avatars/', verbose_name='Avatar')),
                ('birthday', models.DateField(blank=True, default=django.utils.timezone.localdate, verbose_name='Birthdate')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Contact phone number', max_length=128, region=None, verbose_name='Phone Number')),
                ('locale', models.CharField(default='en', max_length=2, verbose_name='Locale (ISO 639-1)')),
                ('theme', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark')], default='light', max_length=5, verbose_name='Perefered Color Theme')),
                ('date_of_update', models.DateTimeField(auto_now=True)),
                ('date_of_add', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'User',
                'ordering': ['-date_of_update'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
