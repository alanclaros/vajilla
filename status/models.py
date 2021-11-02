from django.db import models


class Status(models.Model):
    status_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=150, blank=False)

    class Meta:
        db_table = 'status'
