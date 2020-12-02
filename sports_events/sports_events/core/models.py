from django.db import models

# Create your models here.


class Sports(models.Model):
	objects = models.Manager()

	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=250)
	added_at = models.DateTimeField(auto_now=True)
	num_teams = models.IntegerField(default=2)


class Events(models.Model):	
	objects = models.Manager()

	id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length=250)
	startTime = models.DateTimeField()
	sport = models.ForeignKey(Sports, on_delete=models.DO_NOTHING, )
	
	

class Markets(models.Model):
	objects = models.Manager()

	id = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length=250)	
	added_at = models.DateTimeField(auto_now=True)

	# delete event
	# event = models.ForeignKey(Events, on_delete=models.CASCADE)

	sport = models.ForeignKey(Sports, on_delete=models.CASCADE,related_name="markets")


class Selection(models.Model):
	objects = models.Manager()

	id = models.BigIntegerField(primary_key=True)	
	name = models.CharField(max_length=250)
	odds = models.FloatField()
	market = models.ForeignKey(Markets, on_delete= models.CASCADE )
	event = models.ForeignKey(Events, on_delete=models.DO_NOTHING ,related_name="selEnv")
	updated_at = models.DateTimeField(auto_now=True)

