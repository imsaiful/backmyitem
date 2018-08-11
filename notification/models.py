from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserNotification(models.Model):
    Name = models.CharField(max_length=250)
    Mobile_No = models.IntegerField(validators=[MaxValueValidator(9999999999)])
    Proof = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.Name



@receiver(post_save, sender=User)
def create_welcome_page(sender, **kwargs):
    if kwargs.get("created", False):
        UserNotification.objects.create(user=kwargs.get('instance'), title="Welcome to BackMYItem",
                                        message="Thanks for signin")

# Create your models here.
