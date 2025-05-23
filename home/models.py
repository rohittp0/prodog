from django.db import models

from home.constants import RequestType, Status


# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MaintenanceRequest(models.Model):
    request_type = models.CharField(max_length=RequestType.length(), choices=RequestType.choices())
    description = models.TextField()
    status = models.CharField(max_length=Status.length(), choices=Status.choices(), default=Status.default())
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_type} - {self.status}"


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
