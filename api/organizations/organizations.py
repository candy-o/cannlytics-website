"""
Organizations API Views | Cannlytics API
Copyright (c) Cannlytics

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 4/25/2021
Updated: 12/6/2021
License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>

Description: API to interface with organizations.
"""
# Standard imports.
from json import loads

# External imports.
import google.auth
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Internal imports.
from cannlytics.firebase import (
    access_secret_version,
    add_secret_version,
    create_secret,
    create_log,
    get_custom_claims,
    get_collection,
    get_document,
    update_custom_claims,
    update_document,
)
from api.auth.auth import authenticate_request #pylint: disable=import-error
from api.traceability.traceability import initialize_traceability


@api_view(['GET'])
def labs(request):
    """Get laboratory information (public API endpoint)."""

    # Get organization(s).
    if request.method == 'GET':
        filters = []
        order_by = 'name'

        # Get a specific organization.
        organization_id = request.query_params.get('organization_id')
        print('Organization ID:', organization_id)
        if organization_id and organization_id != 'undefined':
            filters.append({'key': 'slug', 'operation': '==', 'value': organization_id})

        # Get all organizations in a state
        state = request.query_params.get('state')
        print('State:', state)
        if state:
            filters.append({'key': 'state', 'operation': '==', 'value': state})

        # Query and return the docs.
        docs = get_collection('labs', filters=filters, order_by=order_by, desc=True)
        return Response({'data': docs}, status=200)


@api_view(['GET'])
def organization_team(request, organization_id=None, user_id=None):
    """Get team member data for an organization, given an authenticated
    request from a member of the organization.
    """
    claims = authenticate_request(request)
    print('Claims:', claims)
    try:
        if organization_id in claims['team']:
            organization_data = get_document(f'organizations/{organization_id}')
            team = organization_data['team']
            team_members = []
            if user_id:
                team = [user_id]
            for uid in team:
                team_member = get_document(f'users/{uid}')
                team_members.append(team_member)
            return Response({'data': team_members}, content_type='application/json')
        else:
            message = 'You are not a member of the requested organization.'
            return Response({'error': True, 'message': message}, status=403)
    except KeyError:
        message = 'You are not a member of any teams. Try authenticating.'
        return Response({'error': True, 'message': message}, status=401)


@api_view(['GET', 'POST'])
def organizations(request, organization_id=None, type='lab'):
    """Get, create, or update organizations.
    E.g.
        ```
        organization = {
                'owner': [],
                'name': '',
                'license': '',
                'type': '',
                'team': [],
                'support': '',
            }
        ```
    """

    # Get endpoint variables.
    model_type = 'organizations'
    _, project_id = google.auth.default()
    claims = authenticate_request(request)
    uid = claims['uid']
    print('User request to organizations:', uid)

    # Get organization(s).
    if request.method == 'GET':

        # Get organization_id parameter
        if organization_id:
            print('Query organizations by ID:', organization_id)
            data = get_document(f'{model_type}/{organization_id}')
            print('Found data:', data)
            if not data:
                message = 'No organization exists with the given ID.'
                return Response({'error': True, 'message': message}, status=404)
            elif data['public']:
                return Response({'data': data}, status=200)
            elif uid not in data['team']:
                message = """This is a private organization and you are not
                authenticated as a team member. You will need to request to
                join the organization or fix authentication before continuing."""
                return Response({'error': True, 'message': message}, status=400)
            else:
                return Response({'data': data}, status=200)

        # TODO: Get query parameters.
        keyword = request.query_params.get('name')
        if keyword:
            print('Query by name:', keyword)
            query = {
                'key': 'name',
                'operation': '==',
                'value': keyword
            }
            docs = get_collection(model_type, filters=[query])
            return Response({'data': docs}, status=200)

        # Get all of a user's organizations
        else:
            query = {
                'key': 'team',
                'operation': 'array_contains',
                'value': uid
            }
            docs = get_collection(model_type, filters=[query])
            return Response({'data': docs}, status=200)

        # Optional: Get list of other organizations.
        # Check if user is in organization's team, otherwise,
        # only return publically available information.

        # Optional: Try to get facility data from Metrc.
        # facilities = track.get_facilities()

    # Create or update an organization.
    elif request.method == 'POST':

        # Update an organization with the posted data if there is an ID.
        data = loads(request.body.decode('utf-8'))
        if organization_id:

            # Return an error if the organization does not exist.
            doc = get_document(f'{model_type}/{organization_id}')
            if not doc:
                message = 'No data exists for the given ID.'
                return Response({'error': True, 'message': message}, status=400)

            # Return an error if the user is not part of the organization's team.
            team_list = claims.get('team', [])
            owner_list = claims.get('owner', [])
            if uid not in team_list and organization_id not in owner_list:
                message = """You do not currently belong to this organization.
                You will need to request to join the organization or fix your
                authentication before continuing."""
                return Response({'error': True, 'message': message}, status=400)

            # If an organization already exists, then only the owner
            # can edit the organization's team.
            if uid != doc['owner']:
                data['team'] = doc['team']

            # Store posted API keys as secrets.
            # FIXME: Update licenses if they are being edited.
            new_licenses = data.get('licenses')
            if new_licenses:
                licenses = doc.get('licenses', [])
                for license_data in new_licenses:
                    license_number = license_data['license_number']
                    secret_id = f'{license_number}_secret'
                    try:
                        create_secret(
                            project_id,
                            secret_id,
                            license_data['user_api_key']
                        )
                    except:
                        pass
                    secret = add_secret_version(
                        project_id,
                        secret_id,
                        license_data['user_api_key']
                    )
                    version_id = secret.split('/')[-1]
                    license_data['user_api_key_secret'] = {
                        'project_id': project_id,
                        'secret_id': secret_id,
                        'version_id': version_id,
                    }
                    del license_data['user_api_key']
                    licenses.append(license_data)
                doc['licenses'] = licenses

        # Create organization if it doesn't exist
        # All organizations have a unique `organization_id`.
        else:
            doc = {}
            organization_id = slugify(data['name'])
            doc['organization_id'] = organization_id
            doc['team'] = [uid]
            doc['owner'] = uid

            # Identify created organization type.
            doc['type'] = type

            # All organizations start with the standard data models.
            # FIXME: Remove data models that have permissions
            # if the user does not have sufficient claims.
            data_models = get_collection('public/state/data_models')
            for data_model in data_models:
                key = data_model['key']
                update_document(f'{model_type}/{organization_id}/data_models/{key}', data_model)

        # Create or update the organization in Firestore.
        entry = {**doc, **data}
        print('Entry:', entry)
        update_document(f'{model_type}/{organization_id}', entry)

        # FIXME:
        # On organization creation, the creating user get custom claims.
        update_custom_claims(uid, claims={
            'owner': organization_id,
            'team': organization_id
        })

        # TODO:  Owners can add other users to the team and
        # the receiving user then gets the claims.
        # team: [organization_id, ...]

        # Create activity log.
        changes = [data]
        create_log(
            f'{model_type}/{uid}/logs',
            claims=claims,
            action='Updated organization data.',
            log_type=model_type,
            key=f'{model_type}_data',
            changes=changes
        )

        return Response({'data': entry, 'success': True}, content_type='application/json')

    elif request.method == 'DELETE':

        # TODO: Only user's with organization_id in owner claim can delete the organization.

        return Response({'error': 'not_implemented'}, content_type='application/json')

#-----------------------------------------------------------------------
# Organization team and employees
#-----------------------------------------------------------------------

@api_view(['GET', 'POST'])
def team(request):
    """Get, create, or update information about an organization's team."""
    return NotImplementedError


# FIXME: Is this a duplicate of /traceability/employees?
@api_view(['GET'])
def employees(request):
    """Get a licenses employees from Metrc.
    Args:
        request (HTTPRequest): A `djangorestframework` request.
    """

    # Authenticate the user.
    claims = authenticate_request(request)
    if not claims:
        message = 'Authentication failed. Please use the console or provide a valid API key.'
        return Response({'error': True, 'message': message}, status=403)
    _, project_id = google.auth.default()
    license_number = request.query_params.get('name')
    
    # Create a Metrc client.
    # FIXME: Also pass state and primary license? | Pass state as version ID?
    # Optional: Figure out how to pre-initialize a Metrc client.
    track = initialize_traceability(project_id, license_number, '1')

    # Make a request to the Metrc API.
    data = track.get_employees(license_number=license_number)

    # Return the requested data.
    return Response({'data': data}, content_type='application/json')


#-----------------------------------------------------------------------
# Organization actions
#-----------------------------------------------------------------------

# TODO: Implement organization actions:

def change_primary_organization():
    """Change the primary organization."""
    # Get the custom claims

    # Re-create claims with select organization at the front.


def confirm_join_organization():
    """Confirm a user's request to join an organization."""
    # new_team_member_uid # TODO: Get the ID of the user requesting
    # to join the organization.
    # update_custom_claims(new_team_member_uid, claims={'owner': [organization_id]})
    return NotImplementedError


def decline_join_organization():
    """Decline a user's request to join an organization."""
    return NotImplementedError


def leave_organization():
    """Let a user remove themselves from an organization's team.
    An owner cannot leave their own organization, instead they must
    either promote a new owner or delete the organization"""
    return NotImplementedError


def promote_organization_owner():
    """Promote a new owner to an organization."""
    return NotImplementedError


def join_organization(request):
    """Send the owner of an organization a request for a user to join."""

    # Identify the user.
    claims = authenticate_request(request)
    uid = claims['uid']
    user_email = claims['email']
    post_data = loads(request.body.decode('utf-8'))
    organization = post_data.get('organization')

    # Return an error if the organization doesn't exist.
    query = {'key': 'organization', 'operation': '==', 'value': organization}
    organizations = get_collection('organizations', filters=[query])
    if not organizations:
        message = 'Organization does not exist. Please check the organization name and try again.'
        return Response({'success': False, 'message': message}, status=400)

    # Send the owner an email requesting to add the user to the organization's team.
    org_email = organizations[0]['email']
    text = f"A user with the email address {user_email} would like to join your organization, \
        {organization}. Do you want to add this user to your organization's team? Please \
        reply YES or NO to confirm."
    paragraphs = []
    # TODO: Generate confirm, decline, and unsubscribe links with HMACs from user's uid and owner's uid.
    user_hmac = ''
    owner_hmac = ''
    # Optional: Find new home's for endpoints in api and cannlytics_website
    confirm_link = f'https://console.cannlytics.com/api/organizations/confirm?hash={owner_hmac}&member={user_hmac}'
    decline_link = f'https://console.cannlytics.com/api/organizations/decline?hash={owner_hmac}&member={user_hmac}'
    unsubscribe_link = f'https://console.cannlytics.com/api/unsubscribe?hash={owner_hmac}'
    # html_message = render_to_string('templates/console/emails/action_email_template.html', {
    #     'recipient': org_email,
    #     'paragraphs': paragraphs,
    #     'primary_action': 'Confirm',
    #     'primary_link': confirm_link,
    #     'secondary_action': 'Decline',
    #     'secondary_link': decline_link,
    #     'unsubscribe_link': unsubscribe_link,
    # })

    # TODO: Skip sending email if owner is unsubscribed.
    # send_mail(
    #     subject="Request to join your organization's team.",
    #     message=text,
    #     from_email=DEFAULT_FROM_EMAIL,
    #     recipient_list=LIST_OF_EMAIL_RECIPIENTS,
    #     fail_silently=False,
    #     html_message=html_message
    # )

    # Create activity logs.
    # create_log(f'users/{uid}/logs', claims, 'Requested to join an organization.', 'users', 'user_data', [post_data])
    # create_log(f'organization/{uid}/logs', claims, 'Request from a user to join the organization.', 'organizations', 'organization_data', [post_data])

    message = f'Request to join {organization} sent to the owner.'
    return Response({'success': True, 'message': message}, content_type='application/json')

# def join_organization(request):
#     """Send the owner of an organization a request for a user to join."""

#     # Identify the user.
#     claims = auth.authenticate(request)
#     uid = claims['uid']
#     user_email = claims['email']
#     post_data = loads(request.body.decode('utf-8'))
#     organization = post_data.get('organization')

#     # Return an error if the organization doesn't exist.
#     query = {'key': 'organization', 'operation': '==', 'value': organization}
#     organizations = get_collection('organizations', filters=[query])
#     if not organizations:
#         message = 'Organization does not exist. Please check the organization name and try again.'
#         return Response({'success': False, 'message': message}, status=400)

#     # Send the owner an email requesting to add the user to the organization's team.
#     org_email = organizations[0]['email']
#     text = f"A user with the email address {user_email} would like to join your organization, \
#         {organization}. Do you want to add this user to your organization's team? Please \
#         reply YES or NO to confirm."
#     paragraphs = []
#     # TODO: Generate confirm, decline, and unsubscribe links with HMACs from user's uid and owner's uid.
#     user_hmac = ''
#     owner_hmac = ''
#     # Optional: Find new home's for endpoints in api and cannlytics_website
#     confirm_link = f'https://console.cannlytics.com/api/organizations/confirm?hash={owner_hmac}&member={user_hmac}'
#     decline_link = f'https://console.cannlytics.com/api/organizations/decline?hash={owner_hmac}&member={user_hmac}'
#     unsubscribe_link = f'https://console.cannlytics.com/api/unsubscribe?hash={owner_hmac}'
#     html_message = render_to_string('templates/console/emails/action_email_template.html', {
#         'recipient': org_email,
#         'paragraphs': paragraphs,
#         'primary_action': 'Confirm',
#         'primary_link': confirm_link,
#         'secondary_action': 'Decline',
#         'secondary_link': decline_link,
#         'unsubscribe_link': unsubscribe_link,
#     })

#     # TODO: Skip sending email if owner is unsubscribed.
#     send_mail(
#         subject="Request to join your organization's team.",
#         message=text,
#         from_email=DEFAULT_FROM_EMAIL,
#         recipient_list=LIST_OF_EMAIL_RECIPIENTS,
#         fail_silently=False,
#         html_message=html_message
#     )

#     # Create activity logs.
#     create_log(f'users/{uid}/logs', claims, 'Requested to join an organization.', 'users', 'user_data', [post_data])
#     create_log(f'organization/{uid}/logs', claims, 'Request from a user to join the organization.', 'organizations', 'organization_data', [post_data])

#     message = f'Request to join {organization} sent to the owner.'
#     return Response({'success': True, 'message': message}, content_type='application/json')
