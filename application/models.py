from django.db import models

# Create your models here.
class Buff(models.Model):
    bid=models.AutoField(primary_key=True,null=False)
    appid = models.BigIntegerField(blank=True, null=True)
    bookmarked = models.IntegerField(blank=True, null=True)
    buy_max_price = models.FloatField(blank=True, null=True)
    buy_num = models.BigIntegerField(blank=True, null=True)
    can_bargain = models.IntegerField(blank=True, null=True)
    can_search_by_tournament = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    game = models.TextField(blank=True, null=True)
    has_buff_price_history = models.IntegerField(blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)
    market_hash_name = models.TextField(blank=True, null=True)
    market_min_price = models.FloatField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    quick_price = models.FloatField(blank=True, null=True)
    sell_min_price = models.FloatField(blank=True, null=True)
    sell_num = models.BigIntegerField(blank=True, null=True)
    sell_reference_price = models.FloatField(blank=True, null=True)
    short_name = models.TextField(blank=True, null=True)
    steam_market_url = models.TextField(blank=True, null=True)
    transacted_num = models.BigIntegerField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    fray = models.TextField(blank=True, null=True)
    quality = models.TextField(blank=True, null=True)
    rarity = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BUFF'