from django.db import models


class Memory(models.Model):
    title = models.CharField(max_length=100)
    comment = models.TextField()


    def __str__(self):
        return f'{self.title} - {self.comment}'

