from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "Owner(name = "+ self.name + ")"
    
class Cat(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)