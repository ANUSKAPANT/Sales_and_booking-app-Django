from django.urls import path, include
from . import views
urlpatterns = [

    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

	path('', views.servicesView, name="services"),
	path('info/', views.infoView, name="info"),
	path('booking/<str:pk>', views.bookingView, name="booking"),
	path('delete-booking/<str:pk>', views.deleteBooking, name="delete-booking"),
	path('update-booking/<str:pk>', views.updateBooking, name="update-booking"),
	path('create-service/', views.createServiceView, name='create-service'),
	path('user-profile/', views.userProfile, name='user-profile'),
		
   
]