from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Cat(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    owner = models.ForeignKey(Owner, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class VetVisit(models.Model):
    cat = models.ForeignKey("Cat", on_delete=models.CASCADE)

    visit_time = models.DateTimeField()
    reason = models.CharField(max_length=200)
    weight_lbs = models.DecimalField(max_digits=4, decimal_places=1) 
    paid = models.BooleanField(default=False)
    cost_usd = models.DecimalField(max_digits=7, decimal_places=2) 

    def __str__(self):
        return f"VetVisit({self.cat.name} @ {self.visit_time:%Y-%m-%d %H:%M})"