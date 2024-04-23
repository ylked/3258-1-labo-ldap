import ldap3
import os
from flask import Flask, request, Response
from ldap3 import Server, Connection
from ldap3.core.exceptions import LDAPBindError

app = Flask(__name__)

try:
    HOSTNAME = os.environ['FLASKLDAP_HOSTNAME']
    BASE = os.environ['FLASKLDAP_BASE']

    print(f"LDAP config : ")
    print(f"Hostname : {HOSTNAME}")
    print(f"Base     : {BASE}")

except KeyError:
    print("FATAL ERROR : The two environment variables 'FLASKLDAP_HOSTNAME' and "
          "'FLASKLDAP_BASE' MUST be defined and accessible by the app to run successfully!\n"
          "For example : \n"
          "FLASKLDAP_BASE='dc=ylked,dc=ch'\n"
          "FLASKLDAP_HOSTNAME='ldap-service'")
    exit(-1)


def authenticate(cn: str, password: str):
    dn = f'cn={cn},{BASE}'
    conn = Connection(Server(HOSTNAME), dn, password)

    try:
        if conn.bind():
            base = f'cn={cn},{BASE}'
            conn.search(base, search_filter='(&(objectClass=inetOrgPerson))', search_scope='BASE',
                        attributes=ldap3.ALL_ATTRIBUTES)

            if not conn.entries:
                return 404, '[ ERROR ] : could not find user object.'

            entry = conn.entries[0]
            fullname = f'{entry.givenName} {entry.sn}'

            return 200, fullname

        else:
            return 401, '[ ERROR ] : invalid username and/or password.'

    except LDAPBindError:
        return 500, '[ ERROR ] : could not connect to LDAP server!'


@app.route('/fullname')
def auth():
    a = request.authorization
    if a and a.username and a.password:
        status, msg = authenticate(a.username, a.password)
        return Response(msg, status=status)
    else:
        return Response('[ ERROR ] : could not authenticate. Please use HTTP basic authentication.', 400)


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
