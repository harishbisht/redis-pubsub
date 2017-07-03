from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from .models import TransactionHistory, Wallet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from wallet.helpers import get_new_transaction_id, get_unique_username
from django.db.models import Q
from redishelp.config import check_redis_connection, update_the_cache


@login_required(login_url='/login')
@csrf_exempt
def dashboard_view(request):
    try:
        wallet_obj = Wallet.objects.get(user=request.user)
        context = {"balance": wallet_obj.balance,
                   "email_id": wallet_obj.email}
        return render(request, "dashboard.html", context=context)
    except Exception, e:
        return render(request, "login.html", context={"error": str(e)})


@csrf_exempt
def signup_view(request):
    logout(request)
    if request.method == 'POST':
        email_id = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'signup.html', {'error': "Password Not Matching"})
        try:
            User.objects.get(email=email_id)
            return render(request, 'signup.html', {'error': "Email Id Already Exists"})
        except User.DoesNotExist:
            pass
        username = get_unique_username()
        user = User.objects.create_user(username, email_id, password1)
        user.is_active = True
        user.save()
        user = authenticate(username=username, password=password1)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html', {'error': None})


@csrf_exempt
def login_view(request):
    logout(request)
    if request.method == 'POST':
        email_id = request.POST['email']
        password = request.POST['password']
        try:
            user_obj = User.objects.get(email=email_id)
            username = user_obj.username
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email is wrong'})
        except:
            return render(request, 'login.html', {'error': 'Email id password is wrong'})
    return render(request, 'login.html', {'error': None})


@csrf_exempt
@login_required(login_url='/login')
def add_money_to_wallet(request):
    if request.method == 'POST':
        try:
            user = request.user
            wallet_obj = Wallet.objects.get(user=user)
            amount = request.POST['amount']
            transactionhistoryobj = TransactionHistory()
            transactionhistoryobj.user_wallet = wallet_obj
            transactionhistoryobj.transation_type = 'Add To Wallet'
            transactionhistoryobj.transaction_id = get_new_transaction_id()
            transactionhistoryobj.transaction_amount = int(amount)
            transactionhistoryobj.is_success = True
            transactionhistoryobj.is_completed = True
            transactionhistoryobj.save()
            wallet_obj.balance = int(wallet_obj.balance) + int(amount)
            wallet_obj.save()
            return redirect('home')
        except Exception, e:
            return render(request, 'addmoney.html', {'error': str(e)})
    return render(request, 'addmoney.html', {'error': None})


@csrf_exempt
@login_required(login_url='/login')
def transfer(request):
    if request.method == 'POST':
        try:
            wallet_obj = Wallet.objects.get(user=request.user)
            amount = request.POST['amount']
            send_to_email = request.POST['email_id']
            if int(amount) > int(wallet_obj.balance) or send_to_email == request.user.email:
                return render(request, 'transfer.html', {'error': 'Not Sufficient balance or cannot send to same account'})
            transactionhistoryobj = TransactionHistory()
            transactionhistoryobj.user_wallet = wallet_obj
            transactionhistoryobj.transation_type = 'Transfer'
            transactionhistoryobj.transaction_id = get_new_transaction_id()
            transactionhistoryobj.transaction_amount = int(amount)

            obj, created = Wallet.objects.get_or_create(email=send_to_email)
            obj.balance = int(obj.balance) + int(amount)
            if obj and obj.user:
                transactionhistoryobj.is_success = True
                transactionhistoryobj.is_completed = True
            else:
                transactionhistoryobj.is_success = False
                # send to redis
                if check_redis_connection():
                    transactionhistoryobj.save()
                    update_the_cache(transactionhistoryobj.pk, "history")
                else:
                    pass
            transactionhistoryobj.to_wallet = obj
            obj.save()
            transactionhistoryobj.save()
            wallet_obj.balance = int(wallet_obj.balance) - int(amount)
            wallet_obj.save()
            return redirect('home')
        except Exception, e:
            return render(request, 'transfer.html', {'error': str(e)})
    return render(request, 'transfer.html', {'error': None})


@login_required(login_url='/login')
def passbook(request):
    try:
        transactions = TransactionHistory.objects.filter(Q(user_wallet__user=request.user) |
                                                         Q(to_wallet__user=request.user)
                                                         ).values_list('transation_type',
                                                                       'transaction_id',
                                                                       'user_wallet__email',
                                                                       'to_wallet__email',
                                                                       'transaction_amount',
                                                                       'created_on',
                                                                       'is_success',
                                                                       'is_completed')
        return render(request, 'passbook.html', {'error': None, 'transactions': transactions})
    except Exception, e:
        return render(request, 'passbook.html', {'error': str(e)})
