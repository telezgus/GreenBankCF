import csv
from cards.models import Card
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def load_all():
    create_admin_group()
    create_client_group()
    load_users()
    load_cards()


def create_admin_group():
    """Creates admin group and assigns permissions
    """
    # Obtener o crear el grupo "admin"
    admin_group, created = Group.objects.get_or_create(name='admin')

    # Definir los permisos con sus respectivos nombres de modelo y codenames
    permissions = [
        ('accounts', 'profile', ['add_profile', 'change_profile', 'delete_profile', 'view_profile']),
        ('auth', 'group', ['add_group', 'change_group', 'delete_group', 'view_group']),
        ('auth', 'user', ['add_user', 'change_user', 'delete_user', 'view_user']),
        ('cards', 'card', ['add_card', 'change_card', 'delete_card', 'view_card'])
    ]

    # Asignar los permisos al grupo "admin"
    for app, model, codenames in permissions:
        content_type = ContentType.objects.get(app_label=app, model=model)
        for codename in codenames:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            admin_group.permissions.add(permission)



def create_client_group():
    """Creates client group and assigns permissions
    """
    # Obtener o crear el grupo "client"
    client_group, created = Group.objects.get_or_create(name='client')

    # Definir los permisos con sus respectivos nombres de modelo y codenames
    permissions = [
        ('accounts', 'profile', ['change_profile', 'view_profile']),
        ('cards', 'card', ['change_card', 'view_card']),
        ('cards', 'transaction', ['add_transaction', 'view_transaction'])
    ]

    # Asignar los permisos al grupo "client"
    for app, model, codenames in permissions:
        content_type = ContentType.objects.get(app_label=app, model=model)
        for codename in codenames:
            permission = Permission.objects.get(codename=codename, content_type=content_type)
            client_group.permissions.add(permission)



def load_users():
    """Loads cards from csv
    """
    group_client = Group.objects.get(name='client')
    group_admin = Group.objects.get(name='admin')
    with open('listado_tarjetas/listado_de_usuarios.csv', newline='') as file_csv:
        read_csv = csv.reader(file_csv)
        for row in read_csv:
            username, password, first_name, last_name, email, dni, group  = row
            user = User.objects.create(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       email=email)
            user.set_password(password)
            profile = Profile.objects.create(user=user,dni=dni)
            if group == 'client':    
                user.groups.add(group_client)
            else:
                user.groups.add(group_admin)
            user.save()


def load_cards():
    """Loads cards from csv
    """
    with open('listado_tarjetas/listado_de_tarjetas.csv', newline='') as file_csv:
        read_csv = csv.reader(file_csv)
        for row in read_csv:
            user, card_number, pin, total_amount  = row
            card_number=int(card_number.replace("-",""))
            Card.objects.create(user=User.objects.get(username=user), card_number=card_number, pin=pin, total_amount=total_amount)




load_all()

