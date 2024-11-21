from django.db import models
from django.contrib.auth.models import AbstractUser
from finlife.models import DepositProducts, SavingProducts

class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    favorite_deposits = models.ManyToManyField('finlife.DepositProducts', related_name='favorited_by_users', blank=True)
    favorite_savings = models.ManyToManyField('finlife.SavingProducts', related_name='favorited_by_users', blank=True)

    def __str__(self):
        return self.username

    def add_favorite_deposit(self, deposit):
        self.favorite_deposits.add(deposit)

    def remove_favorite_deposit(self, deposit):
        self.favorite_deposits.remove(deposit)

    def is_favorite_deposit(self, deposit):
        return self.favorite_deposits.filter(id=deposit.id).exists()

    def add_favorite_saving(self, saving):
        self.favorite_savings.add(saving)

    def remove_favorite_saving(self, saving):
        self.favorite_savings.remove(saving)

    def is_favorite_saving(self, saving):
        return self.favorite_savings.filter(id=saving.id).exists()