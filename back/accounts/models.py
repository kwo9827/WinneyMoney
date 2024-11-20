from django.db import models
from django.contrib.auth.models import AbstractUser
from finlife.models import DepositProducts

class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    favorite_products = models.ManyToManyField('finlife.DepositProducts', related_name='favorited_users', blank=True)

    def __str__(self):
        return self.username

    def add_favorite_product(self, product):
        self.favorite_products.add(product)

    def remove_favorite_product(self, product):
        self.favorite_products.remove(product)

    def is_favorite_product(self, product):
        return self.favorite_products.filter(id=product.id).exists()