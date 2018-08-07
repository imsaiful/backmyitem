from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django import forms


class Report_item(models.Model):
    item_name = models.CharField(max_length=50,help_text='*Enter the item name you found e.g. Marksheet,key,wallet')
    location = models.CharField(max_length=60, help_text='*Enter the address/street where you find this item')
    city = models.CharField(default="city option", max_length=20, help_text='*Enter the city name')
    date = models.DateTimeField(default=timezone.now)
    Description = models.TextField(help_text='*Enter full description about item')
    category= models.CharField(max_length=50)
    publish = models.BooleanField(default=False)

    image = models.FileField(default="add Item image",help_text='*Please uplocad a item image to identify by the owner')

    def __str__(self):
        return self.item_name+"      "+str(self.publish)



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
