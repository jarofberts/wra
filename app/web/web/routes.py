# all the imports
import os
import re
import typing
from datetime import date
from enum import Enum

from flask import Flask, request, session, g, redirect, url_for, render_template, flash
import sqlite3

from wra.app.data_model import unpack_typing
from wra.app.database import db_path, save
from wra.app.data_model.client import Client, get_enum_member_by_value

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , routes.py


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=db_path(),
    SECRET_KEY='development key'
))
app.config.from_envvar('WRA-APP_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    try:
        path2db = app.config['DATABASE']
    except Exception as e:
        path2db = db_path()
    assert os.path.isfile(path2db)
    return sqlite3.connect(path2db)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def main():
    return redirect(url_for(register_client.__name__))


def find(key, dictionary: dict, generator: bool=True):
    """
    Adapted from https://gist.github.com/douglasmiranda/5127251
    """
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v, generator):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d, generator):
                    yield result


def prepare_value(field_type_info, value):
    if not value and field_type_info['type'] not in (bool, typing.List):
        return None
    if field_type_info['type'] == str:
        return value
    elif field_type_info['type'] == date:
        parsed = value.split('-')
        return date(int(parsed[0]), int(parsed[1]), int(parsed[2]))
    elif type(field_type_info['type']) == type(Enum):
        return get_enum_member_by_value(enum_type=field_type_info['type'], value=int(value))
    elif field_type_info['type'] == int:
        return int(value)
    elif field_type_info['type'] == bool:
        return bool(value)
    elif field_type_info['type'] == typing.List:
        # if dealing with typing.List, return a list, and extend the other list outside of here.
        # will want to make it recursive and call with a modified field_type_info
        value = prepare_value({'type': field_type_info['of'], 'of': None}, value)
        return [value] if value else []
    return value


@app.route('/client', methods=['GET', 'POST'])
def register_client():
    # variables = {key: value for key, value in Client()}
    if request.method == 'GET':
        return render_template('register_client.html', groups=Client.field_groups())
    elif request.method == 'POST':
        # create Client object
        c = Client()
        # write Client object
        for field, value in request.form.items():
            if field[0] == '_':
                # disregard constituent fields that are supposed to be combined together into another field,
                # this pattern is followed in register_client.html
                continue
            matches = re.match('(.*)([[]\d*[]])', field)
            field = matches.groups()[0] if matches else field
            field_type = unpack_typing(Client.__annotations__[field])
            value = prepare_value(field_type, value)
            if matches:
                if field_type['type'] == typing.List:
                    values = c.__getattribute__(field)
                    values = [] if not values else values
                    values.extend(value)
                    c.__setattr__(field, values)
                else:
                    c.__setattr__(field, [value])
            else:
                c.__setattr__(field, value)
        save(c, db=get_db())
        msg = 'Registration submitted'
        flash(msg)
        return redirect(url_for(main.__name__, msg=msg))


# @app.route('/apply', methods=['GET', 'POST'])
# def volunteer_apply():
#     msg = None
#     if request.method == 'GET':
#         return render_template('apply.html')
#     elif request.method == 'POST':
#         values = []
#         values.extend(parse_names(request.form['name']))
#         values.append(request.form['street'])
#         values.append(request.form['city'])
#         values.append(request.form['state'])
#         values.append(request.form['zipcode'])
#         values.append(request.form['phone'])
#         values.append(request.form['voicemail'])
#         values.append(request.form['email'])
#         values.append(request.form['contact_preference'])
#         values.extend(fixed_length_list(request.form['birthday'].split('/'), 2))
#         values.append(request.form['emergency_name'])
#         values.append(request.form['emergency_phone'])
#         values.append(request.form['emergency_relation'])
#         values.append(request.form['ed_level'])
#         db = get_db()
#         db_fields_people = ['first_name', 'middle_name', 'last_name',
#                             'street_address', 'city', 'state', 'zip_code',
#                             'phone', 'voicemail_ok', 'email', 'contact_preference',
#                             'birthday_month', 'birthday_day_of_month',
#                             'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
#                             'highest_education']
#         cur = db.execute('insert into people ({}) values ({})'.format(','.join(db_fields_people), ','.join(['?'] * 17)), values)
#         person_id = cur.lastrowid
#         language_ids = [cur.lastrowid for cur in list(db.execute('insert into languages (name) values (?)', [language])
#                                                       for language in reluctant_split(request.form['language'], ','))]
#         for lang_id in language_ids:
#             db.execute('insert into languages_known (person_id, language_id) values (?, ?)', [person_id, lang_id])
#
#         cur = db.execute('insert into volunteers (id, currently_employed, has_resume,'
#                          'medical_insurance_provider, health_factors,inventory,research,'
#                          'outreach,marketing,reception_scheduling,speakers,maintenance,'
#                          'other_details,advocate,computer,resumes_mock_interview,image_consultant,'
#                          'dbase,felon,felon_incident_date,felon_file_date,felon_nature,felon_incident_loc,'
#                          'felon_file_lo,felon_dispos,emp_term,emp_term_incident_date,emp_term_file_date,'
#                          'emp_term_nature,emp_term_incident_loc,emp_term_file_loc,emp_term_dispos,'
#                          'emp_term_employer,emp_term_city,emp_term_state,name_appl_decl_auth_release,'
#                          'date_appl_decl_auth_release,name_confidentiality_agree,date_confidentiality_agree,'
#                          'name_informed_consent,date_informed_consent)')
#         db.commit()
#         msg = 'Application submitted successfully'
#         flash(msg)
#     return redirect(url_for(main.__name__, msg=msg))


def user_exists(user_name: str, password: str = None) -> (bool, int):
    """
    If the user exists, and password was provided return the user id (int), 

    :rtype: (bool, int)
    :type user_name: str
    :type password: str
    """
    if password:
        query = 'select id from users where user_name=? and password=?'
        values = [user_name, password]
    else:
        query = 'select count(id) from users where lower(user_name)=?'
        values = [user_name.lower()]
    cur = get_db().execute(query, values)
    response = cur.fetchone()
    return response[0] if password else response[0] > 0


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if session.get('user_id'):
        return redirect(url_for(logout.__name__))
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        if user_exists(request.form['username']) > 0:
            return render_template('register.html', error='Invalid credentials provided')
        db = get_db()
        db.execute('insert into users (user_name, password) values (?, ?)', [request.form['username'], request.form['password']])
        db.commit()
        return redirect(url_for(login.__name__, msg='Registration submitted'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    msg = None
    if request.method == 'POST':
        user_id = user_exists(request.form['username'], request.form['password'])
        if user_id:
            session['user_id'] = user_id
            msg = 'You were logged in'
            return redirect(url_for(main.__name__, msg=msg))
    try:
        error = request.args.get('error')
    except KeyError:
        pass
    try:
        msg = request.args.get('msg')
    except KeyError:
        pass
    return render_template('login.html', error=error, msg=msg)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)
