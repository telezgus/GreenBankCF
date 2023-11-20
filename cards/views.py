from django.shortcuts import render, redirect
from .models import Card, Transaction
from accounts.models import Profile
from django.contrib.auth.decorators import login_required, permission_required
from .forms import TransactionForm, NewCardForm, DeleteCardForm, ChangeAlias
from django.db.models import Q
from datetime import datetime
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from accounts.forms import UserCreationFormWithProfile
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
from .models import random_alias
from django.views.decorators.cache import never_cache




load_dotenv()

# Encoding key
cipher_suite = Fernet(os.getenv("ENCODED_KEY").encode('utf-8'))




def encrypt_id(id):
    """Encrypts card Id.

    Args:
        id (int): Id

    Returns:
        str: Id encripted
    """
    try:
        id_encoded = str(id).encode()  # Convertir el entero a una cadena
        id_encrypted = cipher_suite.encrypt(id_encoded)
        return id_encrypted.decode()
    except:
        return None
    
    
    

def decrypt_id(id):
    """Decrypts card Id.

    Args:
        id (str): encrypted Id

    Returns:
        int: decrypted Id
    """
    try:
        id_bytes = id.encode()  # Convertir la cadena en bytes
        id_decrypted = cipher_suite.decrypt(id_bytes)
        return int(id_decrypted.decode())
    except:
        return None





def new_transaction_render(request,form,card,id,message=''):
    """Renders new transactions
    """
    return render(request,'cards/new_transaction.html', {'form':form,'card':card,'message':message,'id':id})




@login_required
def cards(request):
    """Renders user cards
    """
    cards = Card.objects.filter(user=request.user)
    if cards.exists():
        encripted_ids = []
        for card in cards:
            id= card.id
            encripted_ids.append(encrypt_id(id))
        cards = zip(cards, encripted_ids)
        return render(request, 'cards/cards.html', {'cards': cards})
    else:
        return render(request, 'cards/cards.html', {'cards': cards})




@login_required
def transactions(request, id):
    """Renders card transactions
    """
    id_decrypted = decrypt_id(id)  # Convertir los datos desencriptados en un entero
    card = get_object_or_404(Card, id=id_decrypted)
    if card.user == request.user:
        actual_month = datetime.now().month
        transactions = Transaction.objects.filter(
            Q(sender_card=card) | Q(receiver_card=card), date__month=actual_month
        ).order_by('-date')

        return render(request, 'cards/transactions.html', {'transactions': transactions, 'card': card,'id':id})
    else:
        return redirect('forbidden')
    
    
    
    
@login_required   
def new_transaction(request,id):
    """Creates a new transaction
    """
    id_decrypted = decrypt_id(id)
    card = get_object_or_404(Card,id=id_decrypted)
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
                            transaction_id_encrypted = encrypt_id(new_transaction.id)
                            return render(request, 'cards/confirm_transaction.html', {'new_transaction':new_transaction, 'transaction_id_encrypted':transaction_id_encrypted })                            
                        except:                            
                            message = "Alias not valid"
                            return new_transaction_render(request,form,card,id,message)
                    else:
                        message = "Insufficient funds"
                        return new_transaction_render(request,form,card,id,message)
                else:
                    message = "Pin not valid"
                    return new_transaction_render(request,form,card,id,message)
            else:
                message = "Not valid data"
                return new_transaction_render(request,form,card,id,message)   
        else:
            form = TransactionForm()
            return new_transaction_render(request,form,card,id)
    else:
        return redirect('forbidden')   
    

@never_cache
@login_required
def confirm_transaction(request, id):
    """Renders tansaction confimation page

    Args:
        request (request): 
        id (str): encrypted id

    Returns:
        HTTPResponse
    """
    transaction_id = decrypt_id(id)
    new_transaction = get_object_or_404(Transaction,id=transaction_id)
    if new_transaction.confirmed == True:
        message = 'Transaction already made'
        return render(request,'errors/forbidden.html',{'message':message}, status=403)
    else:
        if new_transaction.sender_card.user == request.user:
            #sender_card = get_object_or_404(Card,id=transaction.sender_card.id)
            #receiver_card = get_object_or_404(Card, id=transaction.receiver_card.id)
            new_transaction.sender_card.total_amount-= new_transaction.amount
            new_transaction.sender_card.save()
            new_transaction.receiver_card.total_amount+= new_transaction.amount
            new_transaction.receiver_card.save()
            new_transaction.confirmed = True
            new_transaction.save()
            return render(request,'cards/transaction_ok.html', {'new_transaction':new_transaction})
        else:
            return redirect('forbidden')

        

@login_required
@permission_required('auth.add_user',raise_exception=True)
def new_card(request):
    """Creates a new card
    """
    if request.method == 'POST':
        form = NewCardForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                user_profile = Profile.objects.get(dni=dni)
                alias = random_alias()
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
    """Deletes a card
    """
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
    """Changes alias

    Args:
        request (request): request
        id (str): encripted card id

    """
    id_decrypted = decrypt_id(id)
    card = get_object_or_404(Card,id=id_decrypted)
    check_card_user(card,request)
    if request.method == 'POST':
        form = ChangeAlias(request.POST)
        if form.is_valid():
            alias = form.cleaned_data['alias']           
            if Card.objects.filter(alias=alias).exists():
                message = "Alias already used. Please try a new one"
                return render(request,'cards/change_alias.html', {'form':form,'card':card,'message':message,'id':id})
            else:
                card.alias = alias
                card.save()
                return render(request,'cards/alias_ok.html', {'card':card})
        else:
            message = "Not valid Alias"
            return render(request,'cards/change_alias.html', {'form':form,'card':card,'message':message,'id':id})
    else:
        form = ChangeAlias()
        return render(request,'cards/change_alias.html', {'form':form,'card':card,'id':id})
       
    
    
            
def forbidden(request):
    """Renders forbidden page (403)
    """
    return render(request,'errors/forbidden.html', status=403)


def error_404(request, exception):
    """Renders not found page (404)
    """    
    return render(request, 'errors/404.html', status=404)

def error_403(request, exception):
    """Renders forbidden page (403) with exception argument
    """
    return render(request, 'errors/forbidden.html', status=403)



