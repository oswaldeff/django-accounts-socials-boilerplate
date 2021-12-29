from django.views import View
from collections import defaultdict
import requests
import os
import json

# Create your views here.

class SocialLoginProfile(View):
    
    
    def naver(request, access_code):
        
        try:
            client_id = os.environ.get('NAVER_CLIENT_ID')
            client_secret = os.environ.get('NAVER_CLIENT_SECRET')
            
            code = access_code
            state = os.environ.get('NAVER_STATE')
            
            api_url = f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}'
            
            headers = {
                'X-Naver-Client-Id': client_id,
                'X-Naver-Client-Secret': client_secret
            }
            
            token_response = requests.get(api_url, headers=headers)
            token_response_code = int(token_response.status_code)
            if token_response_code != 200:
                return token_response
            token_json = token_response.json()
            access_token = token_json['access_token']
        except:
            pass
        
        try:
            header = 'Bearer ' + access_token
            profile_url = 'https://openapi.naver.com/v1/nid/me'
            headers = {'Authorization' : f'Bearer {access_token}'}
            profile_response = requests.get(profile_url, headers=headers)
            profile_response_code = int(profile_response.status_code)
            if profile_response_code != 200:
                return profile_response
            profile_json = profile_response.json()
        except:
            pass
        
        try:
            data = defaultdict(str)
            data['id'] = str(profile_json['response']['id'])
            data['email'] = ''
            data['phone'] = ''
            data['name'] = ''
            data['birthday'] = ''
            data['birthyear'] = ''
        except:
            pass
        
        if 'email' in list(profile_json['response'].keys()):
            data['email'] = str(profile_json['response']['email'])
        if 'mobile' in list(profile_json['response'].keys()):
            data['phone'] = str(profile_json['response']['mobile']).replace('-', '', 2)
        if 'name' in list(profile_json['response'].keys()):
            data['name'] = str(profile_json['response']['name'])
        if 'birthday' in list(profile_json['response'].keys()):
            data['birthday'] = str(profile_json['response']['birthday']).replace('-', '')
        if 'birthyear' in list(profile_json['response'].keys()):
            data['birthyear'] = str(profile_json['response']['birthyear'])
        return data
    
    
    def kakao(request, access_code):
        
        try:
            client_id = os.environ.get('KAKAO_CLIENT_ID')
            
            redirect_uri = 'http://localhost:3700/oauth/kakao'
            code = access_code
            
            api_url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}'
            
            token_response = requests.get(api_url)
            token_response_code = int(token_response.status_code)
            if token_response_code != 200:
                return token_response
            token_json = token_response.json()
            access_token = token_json['access_token']
        except:
            pass
        
        try:
            profile_url = 'https://kapi.kakao.com/v2/user/me'
            headers = {'Authorization' : f'Bearer {access_token}'}
            profile_response = requests.get(profile_url, headers=headers)
            profile_response_code = int(profile_response.status_code)
            if profile_response_code != 200:
                return profile_response
            profile_json = profile_response.json()
        except:
            pass
        
        try:
            data = defaultdict(str)
            data['id'] = str(profile_json['id'])
            data['email'] = ''
            data['phone'] = ''
            data['name'] = str(profile_json['properties']['nickname'])
            data['birthday'] = ''
            data['birthyear'] = ''
        except:
            pass
        
        if 'email' in list(profile_json['kakao_account'].keys()):
            data['email'] = str(profile_json['kakao_account']['email'])
        if 'phone' in list(profile_json['kakao_account'].keys()):
            data['phone'] = str(profile_json['kakao_account']['phone'])
        if 'birthday' in list(profile_json['kakao_account'].keys()):
            data['birthday'] = str(profile_json['kakao_account']['birthday'])
        if 'birthyear' in list(profile_json['kakao_account'].keys()):
            data['birthyear'] = str(profile_json['kakao_account']['birthyear'])
        
        return data