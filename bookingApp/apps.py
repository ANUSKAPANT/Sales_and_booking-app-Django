from django.apps import AppConfig


class BookingappConfig(AppConfig):
    name = 'bookingApp'

    def ready(self):
    	import bookingApp.signals