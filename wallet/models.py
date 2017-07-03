from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from redishelp.config import check_redis_connection, check_in_cache, delete_from_cache


class Wallet(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    email = models.EmailField(verbose_name="Email Address")
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        obj, c = Wallet.objects.get_or_create(email=instance.email)
        obj.user = instance
        obj.save()
        transactionhistoryobj = TransactionHistory.objects.filter(to_wallet__email=instance.email,
                                                                  is_success=False,
                                                                  is_completed=False)
        for t in transactionhistoryobj:
            if check_redis_connection() and check_in_cache(t.pk):
                delete_from_cache(t.pk)
            t.is_success = True
            t.is_completed = True
            t.save()
    # instance.wallet.save()


class TransactionHistory(models.Model):
    user_wallet = models.ForeignKey(Wallet, blank=True, null=True, related_name="Owner")
    Type = (
        ('Add To Wallet', 'Add To Wallet'),
        ('Transfer', 'Transfer'),
    )
    transation_type = models.CharField(choices=Type, max_length=64, blank=True, null=True)
    transaction_id = models.CharField(max_length=64, blank=True, null=True)
    to_wallet = models.ForeignKey(Wallet, blank=True, null=True, related_name="Send_To")
    transaction_amount = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=False)  # True when money received and transfered success
    is_completed = models.BooleanField(default=False)
