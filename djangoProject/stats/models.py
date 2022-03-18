from django.db import models


class Population(models.Model):
    id = models.IntegerField(primary_key=True)
    data = models.DateField()
    population = models.IntegerField()
    class Meta:
        db_table = "population"