# -*- coding: utf-8 -*-

from models import User, Offence, Teacher, Student, Classgroup, Lesson, Type, Measure, Registration
import user.extra_filtering
from floating_menu import default_menu_config, offence_menu_config

tables_configuration = {
    'registration' : {
        'model' : Registration,
        'title' : 'Registraties',
        'route' : 'registration.registrations',
        'subject' :'registration',
        'delete_message' : '',
        'template' : [{'name': 'Code', 'data':'student_code', 'order_by': Registration.student_code, 'width': '5%'},
                      {'name': 'Achternaam', 'data':'last_name', 'order_by': Registration.last_name, 'width': '10%'},
                      {'name': 'Voornaam', 'data':'first_name', 'order_by': Registration.first_name, 'width': '10%'},
                      {'name': 'Computer', 'data':'computer_code', 'order_by': Registration.computer_code, 'width': '10%'},
                      {'name': 'Tijd', 'data':'timestamp', 'order_by': Registration.timestamp, 'width': '10%'},
                      # {'name': 'Klas', 'data':'student.classgroup.name', 'order_by': Classgroup.name, 'width': '5%'},
                      # {'name': 'Les', 'data':'lesson.name', 'order_by': Lesson.name, 'width': '5%'},
                      # {'name': 'Opmerking', 'data':'types', 'order_by': lambda k: k['types'], 'width': '30%'},
                      # {'name': 'Maatregel', 'data':'measures', 'order_by': lambda k: k['measures'], 'width': '30%'},
                      ],
        'filter' :  [],
        'href': [],
        # 'href': [{'attribute': '["name"]', 'route': '"asset.view"', 'id': '["id"]'},
        #          {'attribute': '["purchase"]["since"]', 'route': '"purchase.view"', 'id': '["purchase"]["id"]'},
        #          {'attribute': '["purchase"]["supplier"]["name"]', 'route': '"supplier.view"', 'id': '["purchase"]["supplier"]["id"]'},
        #          {'attribute': '["purchase"]["device"]["brandtype"]', 'route': '"device.view"', 'id': '["purchase"]["device"]["id"]'}
        #          ],
        'floating_menu' : offence_menu_config,
        'disable_add_button' : True,
        #'export' : 'asset.exportcsv',
    },
    'user': {
        'model': User,
        'title' : 'gebruiker',
        'route' : 'user.users',
        'subject' :'user',
        'delete_message' : '',
        'template': [
            {'name': 'Gebruikersnaam', 'data': 'username', 'order_by': User.username},
            {'name': 'Voornaam', 'data': 'first_name', 'order_by': User.first_name},
            {'name': 'Naam', 'data': 'last_name', 'order_by': User.last_name},
            {'name': 'Email', 'data': 'email', 'order_by': User.email},
            {'name': 'Is admin', 'data': 'is_admin', 'order_by': User.is_admin},],
        'filter': [],
        'href': [{'attribute': '["username"]', 'route': '"user.view"', 'id': '["id"]'},
                 ],
        'floating_menu' : default_menu_config,
        'query_filter' : user.extra_filtering.filter,
    }
}

