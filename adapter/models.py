import datetime

from azt_connect.storage_backends import PublicMediaStorage
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone
from django.db import models
import transliterate
import uuid
# Create your models here.


class User(AbstractUser):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name="AzatAI ID",
        db_index=True,
    )
    name = models.CharField(
        verbose_name="Full name", max_length=255, blank=True, default=""
    )
    image = models.ImageField(
        verbose_name="Avatar", storage=PublicMediaStorage(), default="", blank=True, upload_to="images/avatars/"
    )
    birthday = models.DateField(
        verbose_name="Birthdate", blank=True, editable=True, default=timezone.localdate
    )
    phonenumber = PhoneNumberField(
        verbose_name="Phone Number", blank=True, help_text="Contact phone number"
    )
    locale = models.CharField(
        verbose_name="Locale (ISO 639-1)", blank=False, default="en", editable=True, max_length=2
    )
    theme = models.CharField(
        verbose_name='Perefered Color Theme', blank=False, default='light', choices=THEME_CHOICES, max_length=5
    )
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + " " + self.username

    def save(self, *args, **kwargs):

        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "User"
        ordering = ['-date_of_update']

''' Satellite API's '''


class VcmdSchemaBase(models.Model):
    unisat_id = models.IntegerField()
    updated = models.DateTimeField(auto_now_add=True)
    cam_supported = models.PositiveIntegerField()
    cam_detected = models.PositiveIntegerField()
    state = models.CharField(max_length=10,)
    temperature = models.FloatField()
    arm_clock = models.IntegerField()
    core_clock = models.IntegerField()
    serial_clock = models.IntegerField()
    storage_clock = models.IntegerField()
    voltage = models.FloatField()
    otp = models.CharField(max_length=2000)
    cpu_memory = models.PositiveIntegerField()
    gpu_memory = models.PositiveIntegerField()
    config = models.CharField(max_length=1000)
    space = models.CharField(max_length=200)
    memory = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.unisat_id}- {self.updated}"

    class Meta:
        verbose_name_plural = "Vcmd SchemaBase"
        ordering = ['-id']


class SystemData(models.Model):
    unisat_data = models.OneToOneField(VcmdSchemaBase, on_delete=models.CASCADE, related_name="system_data")
    is_expired = models.BooleanField(default=False)
    expire_date = models.DateTimeField(blank=True, null=True)
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_of_add)

    def save(self, *args, **kwargs):
        super(SystemData, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "System Data"
        ordering = ['-date_of_update']


class BmeDataBase(models.Model):
    unisat_id = models.IntegerField()
    temperature = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    updated = models.DateTimeField()

    def __str__(self):
        return str(self.updated)

    class Meta:
        verbose_name_plural = "Bme DataBase"
        ordering = ['-id']


class BmeData(models.Model):
    unisat_data = models.OneToOneField(BmeDataBase, on_delete=models.CASCADE, related_name="bme_data")
    is_expired = models.BooleanField(default=False)
    expire_date = models.DateTimeField(blank=True, null=True)
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_of_add)

    def save(self, *args, **kwargs):
        super(BmeData, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Bme Data"
        ordering = ['-date_of_update']


class BnoDataBase(models.Model):
    unisat_id = models.IntegerField()
    temperature = models.FloatField()
    acceleration = models.CharField(max_length=200)
    magnetic = models.CharField(max_length=200)
    gyro = models.CharField(max_length=200)
    euler = models.CharField(max_length=200)
    quaternion = models.CharField(max_length=200)
    linear_acceleration = models.CharField(max_length=200)
    gravity = models.CharField(max_length=200)
    updated = models.DateTimeField()

    def __str__(self):
        return str(self.unisat_id)

    class Meta:
        verbose_name_plural = "Bno DataBase"
        ordering = ['-id']


class BnoData(models.Model):
    unisat_data = models.OneToOneField(BnoDataBase, on_delete=models.CASCADE, related_name="bno_data")
    is_expired = models.BooleanField(default=False)
    expire_date = models.DateTimeField(blank=True, null=True)
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_of_add)

    def save(self, *args, **kwargs):
        super(BnoData, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Bno Data"
        ordering = ['-date_of_add']


class SiDataBase(models.Model):
    unisat_id = models.IntegerField()
    updated = models.DateTimeField()
    vis = models.IntegerField()
    ir = models.IntegerField()
    uv = models.IntegerField()

    def __str__(self):
        return str(self.unisat_id)

    class Meta:
        verbose_name_plural = "Si DataBase"
        ordering = ('-id', )


class SiData(models.Model):
    unisat_data = models.OneToOneField(SiDataBase, on_delete=models.CASCADE, related_name="si_data")
    is_expired = models.BooleanField(default=False)
    expire_date = models.DateTimeField(blank=True, null=True)
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_of_add)

    def save(self, *args, **kwargs):
        super(SiData, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Si Data"
        ordering = ['-date_of_update']


class CameraDataBase(models.Model):
    unisat_id = models.IntegerField()
    updated = models.DateTimeField()
    cam_num = models.IntegerField()
    path = models.CharField(max_length=200)

    def __str__(self):
        return str(self.unisat_id)

    class Meta:
        verbose_name_plural = "Camera Data Base"
        ordering = ['-id']


class CameraData(models.Model):
    unisat_data = models.OneToOneField(CameraDataBase, on_delete=models.CASCADE, related_name="camera_data")
    is_expired = models.BooleanField(default=False)
    expire_date = models.DateTimeField(blank=True, null=True)
    date_of_update = models.DateTimeField(auto_now=True)
    date_of_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_of_add)

    def save(self, *args, **kwargs):
        super(CameraData, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Camera Data"
        ordering = ['-date_of_update']
