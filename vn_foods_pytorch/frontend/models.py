from django.db import models

class searchResult(models.Model):
    # ID is unique
    id=models.AutoField(primary_key=True,unique =  True)
    resultName=models.CharField(max_length=200)
    url=models.URLField(max_length=250)
    imageStatic=models.CharField(max_length=200)
    accuracy=models.FloatField()

    def __str__(self):
        return self.resultName
