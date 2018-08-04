from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class Report_item(models.Model):
    item_name = models.CharField(max_length=20)
    location = models.CharField(max_length=60)
    city = models.CharField(default="city option", max_length=20)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=20)
    Description = models.TextField(default="lost item desciption")

    def __str__(self):
        return self.item_name + " " + self.location

    def get_absolute_url(self):
        return reverse('feed:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["-date"]

# Create your models here.
