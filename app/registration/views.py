# -*- coding: utf-8 -*-
# app/asset/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, session
from flask_login import login_required, current_user

from .. import db, log
from . import registration
from ..models import  Registration

from ..base import build_filter, get_ajax_table
from ..tables_config import  tables_configuration

import cStringIO, csv, re, datetime

from sqlalchemy.exc import IntegrityError

#This route is called by an ajax call on the assets-page to populate the table.
@registration.route('/registration/data', methods=['GET', 'POST'])
@login_required
def source_data():
    return get_ajax_table(tables_configuration['registration'])

#show a list of registrations
@registration.route('/registration/registrations', methods=['GET', 'POST'])
@login_required
def registrations():
    #The following line is required only to build the filter-fields on the page.
    _filter, _filter_form, a,b, c = build_filter(tables_configuration['registration'])
    return render_template('base_multiple_items.html',
                           title='registraties',
                           filter=_filter, filter_form=_filter_form,
                           config = tables_configuration['registration'])


#show a list of registrations
@registration.route('/registration', methods=['GET', 'POST'])
@login_required
def register():
    student_name = ''
    computer_code = ''
    classgroup = ''
    registration_id = -1
    new_registration = False
    barcode = ''
    try:
        if 'code' in request.form:
            code = request.form['code'].upper()
            if 'add_student' in request.form:
                if request.form['add_student']=='Bewaar': #save new student
                    first_name = request.form['new_first_name']
                    last_name = request.form['new_last_name']
                    classgroup = request.form['new_classgroup']
                    if last_name=='' or first_name=='':
                        flash('Naam is niet volledig, probeer opnieuw')
                        log.info('add student : bad name')
                    else:
                        registration = Registration(first_name=first_name, last_name=last_name, student_code=code, classgroup=classgroup)
                        db.session.add(registration)
                        db.session.commit()
                        flash(u'Nieuwe student: {} {} {} met code {}'.format(last_name, first_name, classgroup, code))
                        log.info(u'added student : {} {} {} with code {}'.format(last_name, first_name, classgroup, code))
            else:
                registration_id = int(request.form['registration_id'])
                if code[:2] == 'LL':    #student code
                    registration = Registration.query.filter(Registration.student_code==code).first()
                    if registration:
                        student_name = u'{} {}'.format(registration.last_name, registration.first_name)
                        classgroup = registration.classgroup
                        computer_code = ''
                        registration_id = registration.id
                    else: #student code not present : new entry
                        new_registration = True
                        barcode = code
                elif code[:3] == 'URS' and registration_id > -1:
                    #add a computer code.  Old computer code will be overwritten
                    registration = Registration.query.get(registration_id)
                    if registration:
                        registration.computer_code = None if code == u'URSDELETE' else code
                        registration.timestamp = datetime.datetime.now()
                        registration.user_id = current_user.id
                        db.session.commit()
                        log.info(u'assigned pc {} to student code {}'.format(code, registration.student_code))
                        registration_id = -1
                else:
                    flash(u'Onbekende code.  Code moet beginnen met LL of URS')
                    log.info(u'unknown code (does not start with LL or URS)')
                    registration_id = -1

    except IntegrityError as e: #computer code already present
        db.session.rollback()
        r = Registration.query.filter(Registration.computer_code==code).first()
        flash(u'Deze computer code is reeds toegewezen aan {} {}'.format(r.last_name, r.first_name))
        log.warning(u'PC {} is already assigned to {}.  error {}'.format(code, r.student_code, e))
        student_name = ''
        computer_code = ''
        registration_id = -1
        barcode = ''
    except Exception as e:
        db.session.rollback()
        flash(u'Onbekende fout, probeer opnieuw')
        log.warning(u'unknow error : {}'.format(e))
        student_name = ''
        computer_code = ''
        registration_id = -1
        barcode = ''

    registrations = Registration.query.filter(Registration.computer_code<>'', Registration.user_id==current_user.id).order_by(Registration.timestamp.desc()).all()
    return render_template('registration/registration.html', student_name=student_name,
                           barcode=barcode,
                           computer_code=computer_code,
                           registration_id=registration_id,
                           new_registration=new_registration,
                           classgroup=classgroup,
                           registrations=registrations)

