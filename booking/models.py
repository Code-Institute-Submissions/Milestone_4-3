from django.db import models
from django.contrib.auth.models import User
from properties.models import Property

# Create your models here.
class Booking(models.Model):
    
    book_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    book_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    book_check_in = models.DateTimeField()
    book_check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.book_user} booked {self.book_check_in.strftime("%d-%b-%Y %H:%M")} To = {self.book_check_out.strftime("%d-%b-%Y %H:%M")}'


