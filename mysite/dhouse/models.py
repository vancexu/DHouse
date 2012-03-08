from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    photo = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    remains = models.IntegerField()
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    name = models.CharField(max_length=200, default='')
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default='M')
    addr = models.CharField('address', max_length=200, null=True)
    money = models.FloatField(default=0.0)
    level = models.IntegerField(default=0)
    state = models.BooleanField(default=False)
    now = datetime.now()
    expire_date = models.DateTimeField('date expired', default=now.replace(year=now.year+1))
    products = models.ManyToManyField(Product, through='SalesRecord', null=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class SalesRecord(models.Model):
    user = models.ForeignKey(UserProfile)
    product = models.ForeignKey(Product)
    num = models.IntegerField('number of product')
    time = models.DateTimeField('record time', default=datetime.now())
    
    def __unicode__(self):
        return self.product.name

@receiver(post_save, sender=User)
def create_userProfile(sender, instance, created, **kwargs):
    print "Save a User"
    if created:
        up = UserProfile.objects.create(user=instance)
        # print "Save a UserProfile"

