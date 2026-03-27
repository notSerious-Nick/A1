from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class Owner(models.Model):
    name = models.CharField(max_length = 200)

    account = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return "Owner(name = " + self.name + ")"

class ShelterStaff(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )

    @classmethod
    def is_shelter_staff(cls, user):
        if not user or not user.is_authenticated:
            return False
        return cls.objects.filter(user=user).exists()
    
    def __str__(self):
        return "ShelterStaff(name = " + self.user.username + ")"

class Cat(models.Model):
    name = models.CharField(max_length = 200)
    age = models.IntegerField(default = 0)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    
    def can_edit(self, user):
        if not user or not user.is_authenticated:
            return False
        if ShelterStaff.is_shelter_staff(user):
            return True
        return self.owner.account == user
        

    def __str__(self):
        return "Cat(name = " + self.name + ", age = " + str(self.age) + ")"

class VetVisit(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    weight_lbs = models.DecimalField(max_digits=3, decimal_places=1)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"VetVisit(cat={self.cat.name}, reason={self.reason}, weight={self.weight_lbs})"
