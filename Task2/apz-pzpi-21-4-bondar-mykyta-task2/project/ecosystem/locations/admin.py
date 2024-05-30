from django.contrib import admin

# Register your models here.
from locations.models import Location, LocationType, MonitoringData, Parameter

admin.site.register(Location)
admin.site.register(LocationType)
admin.site.register(MonitoringData)
admin.site.register(Parameter)