from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.core.exceptions import NON_FIELD_ERRORS


# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	profile_pic = models.ImageField(default = "default_img.jpg", null=True, blank=True)
	
	def __str__(self):
		return self.name 


class Service(models.Model):
	name = models.CharField(max_length = 200, null = True)
	description = models.CharField(max_length = 200, null = True)
	price = models.FloatField(null = True) 
	seller = models.ForeignKey(Customer, null=True, on_delete = models.CASCADE)
	
	def __str__(self):
		return self.name 


class Booking(models.Model):
	service = models.ForeignKey(Service,  null=True, on_delete = models.SET_NULL) 
	date=models.DateField(default=date.today, auto_now=False, auto_now_add=False)
	time=models.TimeField(default=timezone.now, auto_now=False, auto_now_add=False)
	buyer = models.ForeignKey(Customer, null=True, on_delete = models.CASCADE)

	def __str__(self):
		return self.service.name 
		
	class Meta:
		unique_together = ('service', 'date', 'time',)
        
	

def customer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='customer')
		instance.groups.add(group)
		Customer.objects.create(
			user=instance,
			name=instance.username,
			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User) 





