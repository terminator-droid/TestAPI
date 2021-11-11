import urllib
import sys
import json
import requests

client_id = "om-service"
client_secret = "fa248699-fdce-49e0-9c26-3e454ce56075"
authorization_base_url = 'https://secure-keycloak-suep-cdp-prod.app-test.nlmk.com/auth'
token_url_cdp = 'https://secure-keycloak-suep-cdp-prod.app-test.nlmk.com/auth/realms/master/protocol/openid-connect/token'
token_url_omp = 'https://secure-keycloak-suep-omp-prod.app-ep.nlmk.com/auth/realms/master/protocol/openid-connect/token'
grant_type = 'client_credentials'
property_url_cdp = 'https://portal-suep-cdp-prod.app-test.nlmk.com/zif-om-properties'
property_url_omp = 'https://portal-suep-omp-prod.app-ep.nlmk.com/zif-om-properties'
token = ''
headers = {}


def get_token(token_url):
    global token
    global headers
    response = requests.post(
        token_url,
        auth=(client_id, client_secret),
        data={'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret})
    token = 'Bearer ' + json.loads(response.content)['access_token']
    headers = {'Authorization': '{}'.format(token)}


def get_property():
    get_token(token_url=token_url_cdp)
    url = property_url_cdp + '/restapi/propertyprimitives?caseSensitive=false&onlyRoot=true&size=695'
    response = requests.get(url, headers=headers)
    properties = (json.loads(response.content))
    return properties


def post_properties():
    properties = get_property()
    get_token(token_url_omp)
    url = property_url_omp + '/restapi/propertyprimitives'
    for prop in properties['content']:
        response = requests.post(url, json=prop, headers=headers)
        if response.status_code == 400:
            print('Не добавлен шаблон {}'.format(prop['id']))
        elif response.status_code == 409:
            print(response.status_code, 'Шаблон {} уже существует'.format(prop['id']))
        elif response.status_code == 401:
            get_token(token_url_omp)
        else:
            print(response.status_code, 'Шаблон добавлен')


def get_classes():
    get_token(token_url_omp)
    url = property_url_omp + '/restapi/classes?caseSensitive=false&size=100'
    response = requests.get(url, headers=headers)
    return json.loads(response.content)


def post_classes():
    classes = get_classes()
    get_token(token_url_omp)
    url = property_url_omp + '/restapi/classes'
    for clas in classes['content']:
        response = requests.post(url, headers=headers, json=clas)
        if response.status_code == 400:
            print('Не добавлен класс {}'.format(clas['id']))
        elif response.status_code == 409:
            print(response.status_code, 'Класс {} уже существует'.format(clas['id']))
        elif response.status_code == 401:
            get_token(token_url_omp)
        else:
            print(response.status_code, 'Класс добавлен')


def post_all_primitives():
    classes = get_classes()
    for clas in classes['content']:
        class_id = clas['id']
        print('Обрабатывается класс {}'.format(class_id))
        post_class_primitives(class_id)


def post_class_primitives(class_id):
    primitives = get_class_primitives(class_id)
    get_token(token_url_omp)
    url = property_url_omp + '/restapi/classes/' + class_id + '/propertyprimitives/'
    if not primitives:
        return False
    if not primitives['content']:
        print('Класс {} не имеет свойств'.format(class_id))
    else:
        for primitive in primitives['content']:
            response = requests.post(url=url + primitive['id'], headers=headers)
            if response.status_code == 400:
                print('Не добавлен шаблон  {}'.format(primitive['id']))
            elif response.status_code == 409:
                print(response.status_code, 'Шаблон {} уже добавлен'.format(primitive['id']))
            elif response.status_code == 401:
                get_token(token_url_omp)
            else:
                print(response.status_code, 'Шаблон добавлен')
        print('Класс {} наполнен свойствами'.format(class_id))


def get_class_primitives(class_id):
    get_token(token_url_cdp)
    url = property_url_cdp + '/restapi/classes/' + class_id + '/propertyprimitives?size=100'
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print('Класс {} внутренний, наполнение не нужно'.format(class_id))
        return False
    else:
        return json.loads(response.content)


# post_properties()
post_all_primitives()
