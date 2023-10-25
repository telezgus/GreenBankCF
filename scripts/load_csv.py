import csv
from cards.models import Card
from django.contrib.auth.models import User

def load_csv():
    with open('listado_tarjetas/listado_de_tarjetas.csv', newline='') as file_csv:
        read_csv = csv.reader(file_csv)
        for row in read_csv:
            user, card_number, pin, total_amount  = row
            card_number=int(card_number.replace("-",""))
            Card.objects.create(user=User.objects.get(id=user), card_number=card_number, pin=pin, total_amount=total_amount)

load_csv()