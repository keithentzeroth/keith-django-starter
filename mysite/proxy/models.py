from django.db import models
import datetime

# Create your models here.
class Invite(models.Model):
    granter_id  = models.CharField(max_length=200)
    granter_name = models.CharField(max_length=200)
    invited_email = models.CharField(max_length=200)
    date     = models.DateTimeField('date invited')

class Relation(models.Model):
    invitation_id = models.ForeignKey(Invite)      
    acceptor_id = models.CharField(max_length=200)
    acceptor_name = models.CharField(max_length=200)
    granter_id  = models.CharField(max_length=200)
    granter_name = models.CharField(max_length=200)
    date     = models.DateTimeField('date accepted')

