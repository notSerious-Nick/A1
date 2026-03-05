from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Owner(name={self.name})"


class Cat(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cat(name={self.name}, age={self.age})"


class VetVisit(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    visit_time = models.DateTimeField()
    reason = models.CharField(max_length=200)

    # Typical cat weights are single/double digits with one decimal.
    # max_digits=4 allows up to 999.9, max_digits=3 allows up to 99.9.
    weight_lbs = models.DecimalField(max_digits=4, decimal_places=1)

    paid = models.BooleanField(default=False)

    # Currency stored as decimal with cents precision
    cost_usd = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return (
            f"VetVisit(cat={self.cat.name}, time={self.visit_time}, "
            f"reason={self.reason}, weight={self.weight_lbs}, paid={self.paid}, cost={self.cost_usd})"
        )
