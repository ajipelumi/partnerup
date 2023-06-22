#!/usr/bin/python3
""" Users module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request, redirect, session


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User object. """
    # Get JSON data from request
    json_data = request.get_json()

    # Get all User objects
    all_users = storage.all(User)

    # Check if JSON data exists
    if not json_data:
        abort(400, 'Not a JSON')

    # Check if JSON data contains 'username' key
    if 'username' not in json_data.keys():
        abort(400, 'Missing username')

    # Check if JSON data contains 'password' key
    if 'password' not in json_data.keys():
        abort(400, 'Missing password')

    # Check if JSON data contains 'email' key
    if 'email' not in json_data.keys():

        # If no email, user is logging in
        for obj in all_users.values():

            # Check if username and password exist
            if obj.to_dict().get('username') == json_data['username']:
                if obj.to_dict().get('password') == json_data['password']:

                    # Save user to session if username and password exist
                    session['user'] = obj.to_dict()

                    # Return user object
                    return jsonify(obj.to_dict()), 201
                else:
                    # Return error message if password is incorrect
                    error_message = 'Incorrect password'
                    return jsonify(message=error_message), 400

        # Return error message if username does not exist
        error_message = 'Username does not exist'
        return jsonify(message=error_message), 400

    # If email exists, user is signing up
    if 'email' in json_data.keys():

        # Iterate through all User objects
        for obj in all_users.values():

            # Check if username exists
            if obj.to_dict().get('username') == json_data['username']:
                # Return error message if username exists
                error_message = 'Username already exists'
                return jsonify(message=error_message), 400

        # Create new User object
        new_user = User(**json_data)
        # Save new User object
        storage.new(new_user)
        # Save database changes
        storage.save()
        # Save user to session
        session['user'] = new_user.to_dict()
        # Return new User object
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_object(user_id):
    """ Retrieves a User object. """
    # Get User object
    obj = storage.get(User, user_id)

    # Check if User object exists
    if not obj:
        abort(404)

    # Return User object
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a user object. """
    # Get User object
    obj = storage.get(User, user_id)

    # Check if User object exists
    if not obj:
        abort(404)

    # Delete User object
    storage.delete(obj)

    # Save database changes
    storage.save()

    # Return empty JSON response
    return jsonify({}), 200
