from django.db import models

class users(models.Model):
	uname=models.CharField(max_length=20)
	upass=models.CharField(max_length=50)
	ureqip=models.CharField(max_length=30)

class tools(models.Model):
	tname=models.CharField(max_length=20)

class user_coefficient(models.Model):
	ucuser = models.CharField(max_length=100)
	ucefficient = models.TextField()

class private_code(models.Model):
	pcuser = models.ForeignKey(users, related_name='user_id')
	pcfeature = models.TextField()
	pccode = models.TextField()

class asser_rec(models.Model):
	arcode = models.TextField()
	arasserflag = models.BooleanField(default=False)
	arasservar = models.CharField(max_length=20)
	arasserexpr = models.CharField(max_length=50)

class asser_count(models.Model):
	acnumber = models.CharField(max_length=20)

class fileassertion(models.Model):
	fapath = models.CharField(max_length=200)
	faneed = models.BooleanField(default=False)
	faexpr = models.CharField(max_length=50)
	faaccept = models.IntegerField()