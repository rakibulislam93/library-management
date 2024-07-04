from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAccountModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='account')
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    balance_after_transaction = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    amount = models.DecimalField(max_digits=12,decimal_places=2,default=0)

    def deposite(self,amount):
        self.balance += amount
        self.balance_after_transaction = self.balance
        self.save()
    
    def __str__(self) -> str:
        return self.user.username