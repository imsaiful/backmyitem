from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django import forms


class Report_item(models.Model):
    item_name = models.CharField(max_length=20)
    location = models.CharField(max_length=60)
    city = models.CharField(default="city option", max_length=20)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=20)
    Description = models.TextField()
    publish=models.BooleanField(default=False)
    image=models.FileField(default="add Item image")

    def __str__(self):
        return self.item_name + " " + self.location

    def get_absolute_url(self):
        return reverse('feed:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["-date"]


class ClaimForm(models.Model):
    Your_name = models.CharField(max_length=50)
    Your_mobile_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    Detail_proof = models.TextField()

    def __str__(self):
        return self.Your_name + " " + self.Detail_of_proof



# Create your models here.
