from app import app
from app.forms import *
from flask import render_template, flash, redirect, url_for, make_response, session
from flask import request as frequest
from Aruba_Central import *
from class_meraki import my_meraki
import time
from app.meraki_functions import *


@app.route('/')
@app.route('/index',endpoint='index')
def index():
    user = {'username': "John Pi Root yahaoooo"}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
    else:
        session['visits'] = 1  # setting session data


    print("Total visits: {}".format(session.get('visits')))

    template = render_template('index.html', title='Home Cacahuete', user=user, posts=posts)
    #template.set_cookie('')
    return make_response(template)


@app.route('/devices')
def devices():
    if 'sw_list' in locals():
        print(sw_list['switches'])
    else:
        print("sw_list doesn't exist")
    token = get_token()
    sw_list = get_switches(token)
    ap_list = get_aps(token)
    #print(sw_list['switches'])

    return render_template('devices.html', title='Devices list', switches=sw_list['switches'], aps=ap_list['aps'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(" Login requested for user" + form.username.data + " remember_me: " + str(
            form.remember_me.data) + "cahuete: " + form.cahuete.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/meraki', methods=['GET', 'POST'])
def get_meraki():
    if 'meraki_token' in session:
        toktok = session.get('meraki_token')
        print("token: " + toktok)
        org_list = meraki_request("ORG_LIST",toktok)
        print(org_list)
        return render_template('meraki.html', org_list=org_list)
    else:
        # get Meraki token to access dashboard
        form = TokenForm()
        if form.validate_on_submit():
            session['meraki_token'] = form.token.data

            return redirect(url_for('list_org_meraki'))
            #return render_template('meraki.html',org_id=meraki.token)
        else:
            return render_template('token_meraki.html',form=form)
        return render_template('meraki.html', org_id=meraki.token)


@app.route('/list_org_meraki', methods=['GET', 'POST'])
def list_org_meraki():
    org_list = meraki.get_orga_list()
    print(org_list)
    return render_template('meraki.html',org_list=org_list)

@app.route('/meraki/<org_id>')
@app.route('/meraki/<org_id>/')
def cahuete(org_id):

    if not 'meraki_token' in session:
        return redirect(url_for('get_meraki'))
    else:
        token = session.get('meraki_token')
    # assign organization ID depending the name
    session['meraki_org_id'] = org_id
    #org_id = meraki_request("ORG_ID",token,org_name=org_name)
    # get network list from organization
    #net_list = meraki.get_network_list()
    net_list = meraki_request('NET_LIST',token,org_id=org_id)
    return render_template('meraki.html',net_list=net_list)

@app.route('/meraki/<org_name>/<net_id>/devices')
def devices_list(org_name,net_id):
    if not 'meraki_token' in session:
        return redirect(url_for('get_meraki'))
    else:
        token = session.get('meraki_token')

    dev_list = meraki_request("DEVICES_LIST", token, network_id=net_id)

    return render_template('meraki.html', devices_list=dev_list)

@app.route('/meraki/<org_name>/<net_id>/vlans')
def vlans_list(org_name,net_id):
    if not 'meraki_token' in session:
        return redirect(url_for('get_meraki'))
    else:
        token = session.get('meraki_token')

    vlan_list = meraki_request("VLAN_LIST", token, network_id=net_id)

    return render_template('meraki.html', vlan_list=vlan_list)


@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    #return make_response(
    return render_template("404.html"), 404
