from django.forms import ModelForm
from django.forms import DateInput, TimeInput, FileInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminSplitDateTime 
from .models import *



class DateInput(DateInput):
	input_type = 'date'	

class TimeInput(TimeInput):
	input_type = 'time'	



class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']
		widgets = {
            'profile_pic': FileInput(),
        }

class ServiceForm(ModelForm):
	class Meta():
		model = Service	
		fields = '__all__'	
		exclude = ['seller']
	

class BookingForm(ModelForm):
	class Meta():
		model = Booking		
		fields = ['date', 'time']
		widgets = {'date': DateInput(),
					'time': TimeInput(format = '%H:%M')}


# customise user creation form
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']



# if data < datetime.date.today():
#         raise ValidationError(_('Invalid date - reservation in past'), code='invalid')
#         messages.danger(request, "Reservation Created")