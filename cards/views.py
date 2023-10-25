from django.shortcuts import render, redirect
from .models import Card, Transaction
from accounts.models import Profile
from django.contrib.auth.decorators import login_required, permission_required
from .forms import TransactionForm, NewCardForm, DeleteCardForm, ChangeAlias
from django.db.models import Q
from datetime import datetime
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from random_word import RandomWords
from accounts.forms import UserCreationFormWithProfile


def new_transaction_render(request,form,card,message=''):
    return render(request,'cards/new_transaction.html', {'form':form,'card':card,'message':message})

def sort_by_date(e):
    return e.date

@login_required
def cards(request):
    cards = Card.objects.filter(user = request.user)
    return render(request,'cards/cards.html', {'cards':cards})
    
@login_required   
def transactions(request,id):
    card = get_object_or_404(Card, id=id)
    if card.user == request.user:
        actual_month = datetime.now().month
        transactions = Transaction.objects.filter(Q(sender_card=card) | Q(receiver_card=card), date__month=actual_month).order_by('-date')
        
        return render(request,'cards/transactions.html', {'transactions':transactions, 'card':card})
    else:
        return redirect('forbidden')
    
@login_required   
def new_transaction(request,id):
    card = get_object_or_404(Card,id=id)
    if card.user == request.user:
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                alias = form.cleaned_data['alias']
                amount = form.cleaned_data['amount']
                pin = form.cleaned_data['pin']
                if card.pin == pin:
                    if amount <= card.total_amount:
                        try:
                            receiver_card = Card.objects.get(alias=alias)
                            new_transaction = Transaction.objects.create(
                                                                        sender_card=card,
                                                                        receiver_card=receiver_card,
                                                                        amount=amount
                                                                        )
                            card.total_amount -= amount
                            receiver_card.total_amount += amount
                            receiver_card.save()
                            card.save()
                            return render(request,'cards/transaction_ok.html', {'new_transaction':new_transaction})                            
                        except:
                            message = "Alias not valid"
                            return new_transaction_render(request,form,card,message)
                    else:
                        message = "Insufficient funds"
                        return new_transaction_render(request,form,card,message)
                else:
                    message = "Pin not valid"
                    return new_transaction_render(request,form,card,message)
            else:
                message = "Not valid data"
                return new_transaction_render(request,form,card,message)   
        else:
            form = TransactionForm()
            return new_transaction_render(request,form,card)
    else:
        return redirect('forbidden')   
    

def random_alias():
    r = RandomWords()
    a = r.get_random_word() 
    b = r.get_random_word()
    c = r.get_random_word()
    return f'{a}.{b}.{c}'

def check_alias_uniqueness(alias):
    if Card.objects.filter(alias=alias).exists():
        alias = random_alias()
        return check_alias_uniqueness(alias)
    else:
        return alias
        
        

@login_required
@permission_required('auth.add_user',raise_exception=True)
def new_card(request):
    if request.method == 'POST':
        form = NewCardForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                user_profile = Profile.objects.get(dni=dni)
                alias = check_alias_uniqueness(random_alias())
                last_card_number = Card.objects.order_by('card_number').last()
                card = Card.objects.create(user=user_profile.user,card_number= last_card_number.card_number+1,alias=alias)
                return render(request,'cards/new_card_ok.html', {'card':card})
            except:
                form = UserCreationFormWithProfile()
                message = f"User with DNI {dni} doesn't exist. Please create user first"
                return render(request, 'accounts/signup.html', {'form' : form, 'message':message})
        else: 
            return render(request,'cards/new_card.html', {'form':form})
    else:
        form = NewCardForm()
        return render(request,'cards/new_card.html', {'form':form})




@login_required
@permission_required('auth.add_user',raise_exception=True)
def delete_card(request):
    if request.method == 'POST':
        form = DeleteCardForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            card_number = form.cleaned_data['card_number']
            try:
                user_profile = Profile.objects.get(dni=dni)
                card = Card.objects.get(card_number=card_number, user=user_profile.user)
                card.delete()
                return render(request,'cards/deleted_card_ok.html', {'card':card})
            except:
                form = DeleteCardForm()
                message = f"Card Number and User doesn't match."
                return render(request, 'cards/delete_card.html', {'form' : form, 'message':message})
        else: 
            return render(request,'cards/delete_card.html', {'form':form})
    else:
        form = DeleteCardForm()
        return render(request,'cards/delete_card.html', {'form':form})

def check_card_user(card,request):
    if card.user == request.user:
        pass
    else:
        return redirect('forbidden')


    
        
@login_required       
def change_alias(request,id):
    card = get_object_or_404(Card,id=id)
    check_card_user(card,request)
    if request.method == 'POST':
        form = ChangeAlias(request.POST)
        if form.is_valid():
            alias = form.cleaned_data['alias']           
            if Card.objects.filter(alias=alias).exists():
                message = "Alias already used. Please try a new one"
                return render(request,'cards/change_alias.html', {'form':form,'card':card,'message':message})
            else:
                card.alias = alias
                card.save()
                return render(request,'cards/alias_ok.html', {'card':card})
        else:
            message = "Not valid Alias"
            return render(request,'cards/change_alias.html', {'form':form,'card':card,'message':message})
    else:
        form = ChangeAlias()
        return render(request,'cards/change_alias.html', {'form':form,'card':card})
       
    
    
            
def forbidden(request):
    return render(request,'cards/forbidden.html', status=403)


def error_404(request, exception):
    return render(request, 'cards/404.html', status=404)

def error_403(request, exception):
    return render(request, 'cards/forbidden.html', status=403)



