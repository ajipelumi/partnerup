#!/usr/bin/python3
""" Partners module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.partner import Partner
from flask import jsonify, abort, request


@app_views.route('/partners', methods=['GET'], strict_slashes=False)
def get_partners():
    """ Retrieves the list of all Partner objects. """
    partners = []
    all_partners = storage.all(Partner)
    for obj in all_partners.values():
        partners.append(obj.to_dict())
    return jsonify(partners)


@app_views.route('/partners', methods=['POST'], strict_slashes=False)
def create_partner():
    """ Creates a partner object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'username' not in json_data.keys():
        abort(400, 'Missing username')
    if 'email' not in json_data.keys():
        abort(400, 'Missing email')
    new_partner = Partner(**json_data)
    storage.new(new_partner)
    storage.save()
    return jsonify(new_partner.to_dict()), 201


@app_views.route('/partners/<partner_id>',
                 methods=['GET'], strict_slashes=False)
def get_partner_object(partner_id):
    """ Retrieves a partner object. """
    obj = storage.get(Partner, partner_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/partners/<partner_id>', methods=['DELETE'])
def delete_partner(partner_id):
    """ Deletes a partner object. """
    obj = storage.get(Partner, partner_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
