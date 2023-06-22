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

    # Get all Partner objects
    all_partners = storage.all(Partner)

    # Convert to list of dictionaries
    for obj in all_partners.values():

        # Append to list
        partners.append(obj.to_dict())

    # Return JSON response
    return jsonify(partners)


@app_views.route('/partners', methods=['POST'], strict_slashes=False)
def create_partner():
    """ Creates a partner object. """
    # Get JSON data from request
    json_data = request.get_json()

    # Check if JSON data exists
    if not json_data:
        abort(400, 'Not a JSON')

    # Check if JSON data contains 'username' key
    if 'username' not in json_data.keys():
        abort(400, 'Missing username')

    # Check if JSON data contains 'email' key
    if 'email' not in json_data.keys():
        abort(400, 'Missing email')

    # Instantiate new Partner object
    new_partner = Partner(**json_data)

    # Save new Partner object to database
    storage.new(new_partner)

    # Save database changes
    storage.save()

    # Return new Partner object as JSON response
    return jsonify(new_partner.to_dict()), 201


@app_views.route('/partners/<partner_id>',
                 methods=['GET'], strict_slashes=False)
def get_partner_object(partner_id):
    """ Retrieves a partner object. """
    # Get Partner object
    obj = storage.get(Partner, partner_id)

    # Check if Partner object exists
    if not obj:
        abort(404)

    # Return Partner object as JSON response
    return jsonify(obj.to_dict())


@app_views.route('/partners/<partner_id>', methods=['DELETE'])
def delete_partner(partner_id):
    """ Deletes a partner object. """
    # Get Partner object
    obj = storage.get(Partner, partner_id)

    # Check if Partner object exists
    if not obj:
        abort(404)

    # Delete Partner object
    storage.delete(obj)

    # Save database changes
    storage.save()

    # Return empty JSON response with 200 status code
    return jsonify({}), 200
