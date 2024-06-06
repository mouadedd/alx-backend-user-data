#!/usr/bin/env python3
"""7. New view for Session Authentication"""
import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def sess_auth():
    """handle routes for session authentication"""
    e_mail = request.form.get('email')
    pswd = request.form.get('password')
    if e_mail is None or e_mail == '':
        return jsonify({"error": "email missing"}), 400
    if pswd is None or pswd == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": e_mail})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(pswd):
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            sess_name = os.getenv('SESSION_NAME')
            res.set_cookie(sess_name, sess_id)
            return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def sess_logout():
    """8- logout handel"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
