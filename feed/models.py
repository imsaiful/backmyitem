from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
import sys


def get_uplaod_file_name(image, filename):
    return u'photos/%s/%s_%s' % (str(image.owner),
                                 str(timezone.now()).replace('.', '_'),
                                 filename)


class Report_item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255, help_text='*Title for the post e.g. item identity')
    item_type = models.CharField(default="", max_length=100,
                                 help_text='*Enter the item name you found e.g. Marksheet,key,wallet')
    location = models.CharField(max_length=255, help_text='*Enter the address and city where you found this item')
    date = models.DateTimeField(default=timezone.now)
    Description = models.TextField(blank=True, null=True, help_text='*Enter full description about item')
    publish = models.BooleanField(default=False)

    image = models.ImageField(default="add Item image",
                              upload_to=get_uplaod_file_name)

    def save(self):
        # Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((500, 500))

        # after modifications, save it to the output

        im.save(output, format='JPEG', optimize=True, quality=95)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                          sys.getsizeof(output), None)

        super(Report_item, self).save()

    def __str__(self):
        return self.title + "      " + str(self.publish)

    def get_absolute_url(self):
        return reverse('feed:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["-date"]



class UserNotification(models.Model):
    Name = models.CharField(max_length=250)
    Mobile_No = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    Proof = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ["-date"]


class ContactHelp(models.Model):
    Name = models.CharField(max_length=250)
    Email = models.EmailField(blank=False, null=False)
    query = models.TextField(blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.query

# Create your models here.
