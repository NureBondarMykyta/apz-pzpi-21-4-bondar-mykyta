from django.db import models

from django.db import models

from users.models import User


class LocationType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='location_types/')

    def __str__(self):
        return self.name

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    created_date = models.DateField(auto_now_add=True)
    location_type = models.ForeignKey(LocationType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Внешний ключ на модель User

    def __str__(self):
        return f"{self.name} owner {self.user}"
class Parameter(models.Model):
    id = models.AutoField(primary_key=True)
    parameter_name = models.CharField(max_length=100)
    min_value = models.FloatField()
    max_value = models.FloatField()
    unit = models.CharField(max_length=50)
    weight = models.FloatField()

    def __str__(self):
        return f"Parameter {self.parameter_name}"

class MonitoringData(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    value = models.FloatField()
    update_time = models.DateTimeField(auto_now=True)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)

    def __str__(self):
        return f"Monitoring Data for {self.location.name} - Parameter {self.parameter.parameter_name}"