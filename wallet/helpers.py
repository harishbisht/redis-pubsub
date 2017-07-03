import string


def random_word(size=6, chars=string.ascii_uppercase + string.digits):
    import random
    return ''.join(random.choice(chars) for _ in range(size))


def get_new_transaction_id():
    from wallet.models import TransactionHistory
    while 1:
        word = random_word()
        try:
            TransactionHistory.objects.get(transaction_id=word)
        except TransactionHistory.DoesNotExist:
            return word


def get_unique_username():
    from django.contrib.auth.models import User
    while 1:
        word = random_word()
        try:
            User.objects.get(username=word)
        except User.DoesNotExist:
            return word


def send_money_back_to_sender_account(id):
    try:
        from wallet.models import TransactionHistory
        transhistoryobj = TransactionHistory.objects.get(id=id)
        if not transhistoryobj.is_completed:
            transhistoryobj.is_completed = True
            transhistoryobj.is_success = False
            transhistoryobj.user_wallet.balance = (transhistoryobj.user_wallet.balance) + int(transhistoryobj.transaction_amount)
            transhistoryobj.to_wallet.balance = (transhistoryobj.to_wallet.balance) - int(transhistoryobj.transaction_amount)
            transhistoryobj.to_wallet.save()
            transhistoryobj.user_wallet.save()
            transhistoryobj.save()
        pass
    except TransactionHistory.DoesNotExist:
        pass
