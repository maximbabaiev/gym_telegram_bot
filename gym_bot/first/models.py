from django.db import models


# Create your models here.

class User(models.Model):
    login_id = models.IntegerField()
    password = models.CharField(max_length=100)
    time_auto = models.FloatField(default=0.0)
    cash_account = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.password} {self.time_auto}"


class Trainer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Schedule_trainer(models.Model):
    weekday = models.CharField(max_length=100)
    trainer_name = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    time_training = models.CharField(max_length=100)
    clients = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.weekday}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class User_product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"
