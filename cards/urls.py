"""Exports cards related urls to main urls (.banco_cf.urls)
"""

from django.contrib import admin
from django.urls import path

from .views import cards, transactions, new_transaction, forbidden, new_card, delete_card, change_alias,confirm_transaction

urlpatterns = [
    path('', cards , name = 'cards'),
    path('transactions/<str:id>', transactions , name = 'transactions'),
    path('forbidden', forbidden , name = 'forbidden'),
    path('new_transaction/<str:id>', new_transaction , name = 'new_transaction'),
    path('new_card', new_card , name = 'new_card'),
    path('delete_card', delete_card , name = 'delete_card'),
    path('change_alias/<str:id>', change_alias , name = 'change_alias'),
    path('transaction_confirmed/<str:id>', confirm_transaction , name = 'transaction_confirmed'),   
    
]
