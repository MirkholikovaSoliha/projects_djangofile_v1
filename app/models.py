from django.db import models

class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    project = models.FileField(upload_to='projects/')

    def __str__(self):
        return f"{self.full_name} ({self.age})"
