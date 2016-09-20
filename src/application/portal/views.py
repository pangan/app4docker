

# -*- coding: utf-8 -*-
"""
    :py:mod:`credentials.portal`
    ============================

    Package providing a :py:class:`~flask.Blueprint` for the ``/portal`` API endpoint.



    .. moduleauthor:: Amir Mofakhar <amofakhar@smithmicro.com>

    .. versionadded:: 3.0
"""

from portal import portal
from flask import request, render_template, redirect, url_for
from ua_parser import user_agent_parser
from wtforms import validators, StringField
from language import _CAPTIONS
from devices import check_if_device_supported
from flask_wtf import Form

__all__ = ['portal_page_blueprint', 'portal_page']



@portal.route('/')
def index():
    return 'This is index!'


@portal.route('/portal', methods=['GET', 'POST'])
def portal_page():
    """.. http:get:: /portal

       renders the portal page.

    .. http:post:: /portal

       receives IMSI and redirects to the correct end point based on the device model.

       :form uid: IMSI of the device




    """

    _user_agent = request.headers['User-Agent']
    _device = user_agent_parser.ParseDevice(_user_agent)
    _os = user_agent_parser.ParseOS(_user_agent)
    _os_ver = '{0}.{1}'.format(str(_os['major'] or ''), str(_os['minor'] or ''))
    _form = _UserIdForm(request.form)

    if request.method == 'POST' and _form.validate_on_submit():
        return redirect(
            '{0}?imsi={1}&vendor={2}&model={3}&,version={4}&origin=CL'.format(
                _find_passpoint_url(_device),
                request.form["uid"],
                _device['brand'],
                _device['model'],
                _os_ver
                )
        )

    return render_template('portal.html',
                           device=_device['model'],
                           os_ver=_os_ver,
                           os_family=_os['family'],
                           form=_form,
                           supported=check_if_device_supported(_device['model'], _os_ver),
                           captions=_CAPTIONS)


def _find_passpoint_url(device):
    if 'brand' in device and device['brand'] == 'Apple':
        #return 'ios_passpoint_blueprint.ios_passpoint'
        return 'http://passport-qa.smithmicro.io/android/passpoint'

    else:
        #return 'android_passpoint_blueprint.android_passpoint'
        return 'http://passport-qa.smithmicro.io/android/passpoint'


class _UserIdForm(Form):
    uid = StringField(
        _CAPTIONS['landing']['user_id'],
        [validators.InputRequired(_CAPTIONS['landing']['error']['1']),
         validators.Regexp('[0-9]{15}$', message=_CAPTIONS['landing']['error']['2'])]
        )
