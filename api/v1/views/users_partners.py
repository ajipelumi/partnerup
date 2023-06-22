#!/usr/bin/python3
""" Partners module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.user import User
from models.partner import Partner
from flask import jsonify, abort, make_response


@app_views.route('/users/<user_id>/partners',
                 methods=['GET'], strict_slashes=False)
def get_user_partners(user_id):
    """ Retrieves a User's partners. """
    # Get User object
    user = storage.get(User, user_id)

    # Check if User object exists
    if not user:
        abort(404)

    # Get User partners
    partners = [partner.to_dict() for partner in user.partners]

    # Return partners as JSON response
    return jsonify(partners)


@app_views.route('/users/<user_id>/partners/<partner_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user_partners(user_id, partner_id):
    """ Deletes a specific User partner. """
    # Get User object
    user = storage.get(User, user_id)

    # Check if User object exists
    if not user:
        abort(404)

    # Get Partner object
    partner = storage.get(Partner, partner_id)

    # Check if Partner object exists
    if not partner:
        abort(404)

    # Check if Partner is linked to User
    if partner not in user.partners:
        abort(404)

    # Remove Partner from User if linked
    user.partners.remove(partner)

    # Save database changes
    storage.save()

    # Return empty JSON response
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>/partners/<partner_id>',
                 methods=['POST'], strict_slashes=False)
def create_user_partners(user_id, partner_id):
    """ Link a partner to a user. """
    # Get User object
    user = storage.get(User, user_id)

    # Check if User object exists
    if not user:
        abort(404)

    # Get Partner object
    partner = storage.get(Partner, partner_id)

    # Check if Partner object exists
    if not partner:
        abort(404)

    # Check if Partner is already linked to User
    if partner in user.partners:
        # Return Partner as JSON response
        return make_response(jsonify(partner.to_dict()), 200)
    else:
        # Link Partner to User
        user.partners.append(partner)

    # Save database changes
    storage.save()

    # Return Partner as JSON response
    return make_response(jsonify(partner.to_dict()), 201)
