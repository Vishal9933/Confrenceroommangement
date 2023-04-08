from django.db import models

# Create your models here.


class ConferenceRoom(models.Model):
    name = models.CharField(max_length=255,unique=True)
    capacity = models.IntegerField(default=1)


class BufferTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(ConferenceRoom,on_delete=models.CASCADE)
    


class Roombooking(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.ForeignKey(ConferenceRoom,on_delete=models.CASCADE)
    


