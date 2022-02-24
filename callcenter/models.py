from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Caller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile/', blank=True, null=True)
    ph_number = models.CharField(max_length=15)
    details = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    at_reception = models.BooleanField(default=False)
    at_counselor = models.BooleanField(default=False)
    at_operations = models.BooleanField(default=False)
    branch_assign = models.CharField(max_length=255, blank=True, null=True)
    assign_date = models.DateField(null=True, blank=True)
    assign_time = models.CharField(max_length=255, blank=True, null=True)
    isCallDiscard = models.BooleanField(default=False)
    needsToFollow = models.BooleanField(default=False)
    isRegistered = models.BooleanField(default=False)
    isDocumentMissing = models.BooleanField(default=False)
    remark = models.TextField(blank=True, null=True)


class Uploades(models.Model):
    fid = models.AutoField(primary_key=True)
    document_title = models.CharField(max_length=255)
    document = models.FileField(upload_to="upload/")
    caller = models.ForeignKey(Caller, on_delete=models.CASCADE)


# class Vendor(models.Model):
#     vid = models.AutoField(primary_key=True)

