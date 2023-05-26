#!/usr/bin/python3
""" Users module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request, redirect, session


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects. """
    users = []
    all_users = storage.all(User)
    for obj in all_users.values():
        users.append(obj.to_dict())
    return jsonify(users)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User object. """
    json_data = request.get_json()
    all_users = storage.all(User)
    if not json_data:
        abort(400, 'Not a JSON')
    if 'username' not in json_data.keys():
        abort(400, 'Missing username')
    if 'password' not in json_data.keys():
        abort(400, 'Missing password')
    if 'email' not in json_data.keys():
        for obj in all_users.values():
            if obj.to_dict().get('username') == json_data['username']:
                if obj.to_dict().get('password') == json_data['password']:
                    session['user'] = obj.to_dict()
                    return jsonify(obj.to_dict()), 201
                else:
                    error_message = 'Incorrect password'
                    return jsonify(message=error_message), 400
        error_message = 'Username does not exist'
        return jsonify(message=error_message), 400
    if 'email' in json_data.keys():
        for obj in all_users.values():
            if obj.to_dict().get('username') == json_data['username']:
                error_message = 'Username already exists'
                return jsonify(message=error_message), 400
        new_user = User(**json_data)
        storage.new(new_user)
        storage.save()
        session['user'] = new_user.to_dict()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_object(user_id):
    """ Retrieves a User object. """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a user object. """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
