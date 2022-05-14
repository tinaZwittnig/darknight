from django.db import models

choices = [('display', 'display window'),
           ('street', 'street light')]


class Location(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    city = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=100, decimal_places=10)
    latitude = models.DecimalField(max_digits=100, decimal_places=10)

    def __str__(self):
        return str(self.city)


class Type(models.Model):
    type = models.CharField(choices=choices, max_length=100)

    def __str__(self):
        return self.type


class Light(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    mesh_id = models.PositiveIntegerField()
    power = models.PositiveIntegerField(verbose_name='Power in watts')

    def __str__(self):
        return str(self.type) + " "+str(self.location)


class Passes(models.Model):
    light = models.ForeignKey(Light, on_delete=models.PROTECT)
    time_of_pass = models.DateTimeField()
    temperature = models.IntegerField(blank=True, null=True)
    duration = models.PositiveIntegerField(verbose_name='Duration in seconds', blank=True, null=True)
    brightness = models.DecimalField(max_digits=100, decimal_places=10, blank=True, null=True)
    pressure = models.DecimalField(max_digits=100, decimal_places=10, blank=True, null=True)
    humidity = models.DecimalField(max_digits=100, decimal_places=10, blank=True, null=True)
    air_quality = models.DecimalField(max_digits=100, decimal_places=10,blank=True, null=True)

    def __str__(self):
        return str(self.time_of_pass) + " " + str(self.light)





