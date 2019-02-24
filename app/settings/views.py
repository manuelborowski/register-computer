# -*- coding: utf-8 -*-
# app/settings/views.py

from flask import render_template, redirect, url_for, request, flash, send_file, abort, make_response
from flask_login import login_required
from ..base import get_global_setting_current_schoolyear, set_global_setting_current_schoolyear, get_setting_simulate_dayhour, set_setting_simulate_dayhour
from . import settings
from .. import db, app, log
from ..models import Settings, Registration
from flask_login import current_user

import unicodecsv   #import csv
import csv          #export csv
from io import StringIO

def check_admin():
    if not current_user.is_admin:
        abort(403)

def get_settings_and_show():
    return render_template('settings/settings.html',
                           schoolyear = get_global_setting_current_schoolyear(),
                           simulate_dayhour = get_setting_simulate_dayhour(),
                           title='settings')

@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def show():
    return get_settings_and_show()

@settings.route('/settings/save', methods=['GET', 'POST'])
@login_required
def save():
    if request.form['button'] == 'Bewaar':
        if 'schoolyear' in request.form:
           set_global_setting_current_schoolyear(request.form['schoolyear'])
    if 'simulate_dayhour' in request.form:
        set_setting_simulate_dayhour(request.form['simulate_dayhour'])
    return get_settings_and_show()

@settings.route('/settings/purge_database', methods=['GET', 'POST'])
@login_required
def purge_database():
    try:
        if 'delete_list' in request.form:
            pass
            # for d in document_type_list:
            #     if d in request.form['delete_doc']:
            #         if get_doc_select(d) in request.form:
            #             for i in request.form.getlist(get_doc_select(d)):
            #                 os.remove(os.path.join(get_doc_path(d), i))
    except Exception as e:
        flash('Kan niet verwijderen...')
    return redirect(url_for('admin.show'))


@settings.route('/settings/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.files['upload_students']: import_students(request.files['upload_students'])
    return redirect(url_for('settings.show'))

#NAAM           last_name
#VOORNAAM       first_name
#LEERLINGNUMMER student_code
#FOTO           photo
#KLAS           classgroup

def import_students(rfile):
    try:
        log.info('Import students from : {}'.format(rfile))
        students_file = unicodecsv.DictReader(rfile,  delimiter=';')

        nbr_students = 0
        for s in students_file:
            #skip empy records
            if s['LEERLINGNUMMER'] != '' and s['VOORNAAM'] != '' and s['NAAM'] != '' and s['KLAS'] != '':
                #add student, if not already present
                find_student=Registration.query.filter(Registration.first_name==s['VOORNAAM'], Registration.last_name==s['NAAM'],
                                                        Registration.student_code ==s['LEERLINGNUMMER'], Registration.classgroup==s['KLAS']).first()
                if not find_student:
                    student = Registration(first_name=s['VOORNAAM'], last_name=s['NAAM'], student_code=s['LEERLINGNUMMER'], classgroup=s['KLAS'])
                    db.session.add(student)
                    nbr_students += 1

        db.session.commit()
        log.info('import: added {} students'.format(nbr_students))
        flash('Leerlingen zijn geimporteerd')

    except Exception as e:
        flash('Kan bestand niet importeren, is het in UTF-8 formaat?')
        log.warning('cannot import students')
    return redirect(url_for('settings.show'))

#export a list of assets
@settings.route('/settings/export', methods=['GET', 'POST'])
@login_required
def exportcsv():
    try:
        headers = (
            u'NAAM',
            u'VOORNAAM',
            u'KLAS',
            u'LEERLINGNUMMER',
            u'COMPUTER',
            u'TIJD',
        )

        rows = []
        for r in Registration.query.all():
            rows.append((
                r.last_name,
                r.first_name,
                r.classgroup,
                r.student_code,
                r.computer_code,
                r.timestamp,
            ))

        si = StringIO()
        cw = csv.writer(si, delimiter=';')
        cw.writerow(headers)
        cw.writerows(rows)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=registraties.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    except Exception as e:
        log.error('Could not export file {}'.format(e))
        return redirect(url_for('settings.show'))

