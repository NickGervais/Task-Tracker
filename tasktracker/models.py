from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    slot_size = models.IntegerField(default=30)
    start_day = models.IntegerField(default=8)
    end_day = models.IntegerField(default=22)
    def __str__(self):
        return self.name

class Task(models.Model):
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    completion_state = models.IntegerField(default=0)
    date_created = models.DateField('date created')
    time_scheduled = models.IntegerField(default=-1)
    time_length = models.IntegerField(default=30)
    def __str__(self):
        return self.title
    def is_completed(self):
        return completion_state >= 2
    



