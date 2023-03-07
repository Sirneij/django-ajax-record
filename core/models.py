import uuid

from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.db import models
from django.urls.base import reverse


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voice_record = models.FileField(upload_to="records")
    language = models.CharField(max_length=50, null=True, blank=True)
    result = models.TextField(null=True)
    transcript = models.TextField(null=True)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("core:record_detail", kwargs={"id": str(self.id)})
