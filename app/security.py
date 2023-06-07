import streamlit as st
import msal
import requests

# Replace with your own values
CLIENT_ID = '6009117b-d0ce-4267-baec-a7b18a9f59be'
CLIENT_SECRET = '3ii8Q~Atz-MXcfDiQ~EgixN.m8ljSdgtopc2Adn2' 
TENANT_ID = '46c98d88-e344-4ed4-8496-4ed7712e255d'

AUTHORITY = 'https://login.microsoftonline.com/46c98d88-e344-4ed4-8496-4ed7712e255d'
SCOPE = ["User.ReadBasic.All"]
REDIRECT_URI = 'http://localhost:8502'

app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)


def get_auth_url():
    auth_url = app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return auth_url


def get_token_from_code(auth_code):
    app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    result = app.acquire_token_by_authorization_code(auth_code, scopes=SCOPE, redirect_uri=REDIRECT_URI)
    
    roles = []

    if 'roles' in result['id_token_claims']:
        roles =  result['id_token_claims']['roles']
        
    st.session_state['roles'] = roles

    return result['access_token']


def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()


def handle_redirect():
    if not st.session_state.get('access_token'):
        code = st.experimental_get_query_params().get('code')
        if code:
            access_token = get_token_from_code(code)
            st.session_state['access_token'] = access_token
            st.experimental_set_query_params()
