from django.db import models

class TimestampedModel(models.Model):
    """
        Abstract model to add timestamp fields for creation and update.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    """
        Abstract model to add soft delete functionality.
    """
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = models.DateTimeField(auto_now=True)
        self.save(update_fields=['deleted_at'])