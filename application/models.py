from django.db import models

# Create your models here.
class Buff(models.Model):
    id = models.BigIntegerField(primary_key=True,blank=True)
    name = models.TextField(blank=True, null=True)
    market_hash_name = models.TextField(blank=True, null=True)
    sell_min_price = models.IntegerField(blank=True, null=True)
    sell_num = models.BigIntegerField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    fray = models.TextField(blank=True, null=True)
    quality = models.TextField(blank=True, null=True)
    rarity = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BUFF'