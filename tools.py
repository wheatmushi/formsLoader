import requests
import json
import re
import getpass


email_RE = '[^@]+@[^@]+\.[^@]+'


def authentication():  # provide authentication routine and return requests.session obj
    login = input('\nenter your login as "firstname.lastname" (with or without domain)\n')
    password = getpass.getpass('\nenter your password\n')
    print('\nopening session...')

    if not re.match(email_RE, login):
        login = login + '@sita.aero'

    url_login = 'https://su-ati.crewplatform.aero/j_spring_security_check'
    url_admin = 'https://su-ati.crewplatform.aero/CrewServices/adminConsole/adminData'

    ssl = 'certs.pem'

    headers = {'j_username': login, 'j_password': password}

    session = requests.Session()
    p = session.post(url_login, headers, verify=ssl)

    if 'login_error=1' in p.url:
        print('\nincorrect login or password, try again!')
        return authentication()

    session.cookies.update({'username': login})

    admin = session.get(url_admin)
    admin = json.loads(admin.content)
    key = admin['airlines'][0]['key']

    session.headers.update({'X-apiKey': key})
    print('\nsession loaded successfully')
    return session
