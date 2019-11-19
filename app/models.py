from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class User_data(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Account_Number=models.CharField(primary_key=True,max_length=10)
    Branch=models.CharField(max_length=40)
    profile_pic=models.ImageField(upload_to='user',blank=True)

    def __str__(self):
        self.user.username