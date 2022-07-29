import email
from email import message
from MySQLdb import Timestamp
from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    suggest = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    Timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return 'Message from ' + self.name
    
class Reply(models.Model):
    name = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    
    def __str__(self):
        return 'Message from ' + self.name
    