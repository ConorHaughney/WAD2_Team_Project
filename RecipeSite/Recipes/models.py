from django.db import models

class Category(models.Model):
    NAME_MAX_LENGTH = 25

    NAME = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name
    
class Difficulty(models.model):
    DIFFICULTY_MAX_LENGTH = 15

    difficulty = models.CharField(max_length=DIFFICULTY_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

