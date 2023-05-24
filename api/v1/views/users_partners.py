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
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    partners = [partner.to_dict() for partner in user.partners]
    return jsonify(partners)


@app_views.route('/users/<user_id>/partners/<partner_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user_partners(user_id, partner_id):
    """ Deletes a specific User partner. """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    partner = storage.get(Partner, partner_id)
    if not partner:
        abort(404)
    if partner not in user.partners:
        abort(404)
    user.partners.remove(partner)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>/partners/<partner_id>',
                 methods=['POST'], strict_slashes=False)
def create_user_partners(user_id, partner_id):
    """ Link a partner to a user. """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    partner = storage.get(Partner, partner_id)
    if not partner:
        abort(404)
    if partner in user.partners:
        return make_response(jsonify(partner.to_dict()), 200)
    else:
        user.partners.append(partner)
    storage.save()
    return make_response(jsonify(partner.to_dict()), 201)
