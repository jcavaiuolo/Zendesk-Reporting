import requests
import json
from requests.packages import urllib3
import datetime

urllib3.disable_warnings()

def dameLaFechayHora(string_fecha,offset):
    asd = datetime.datetime.strptime(string_fecha,"%Y-%m-%d %H:%M:%S")
    return (asd + datetime.timedelta(minutes=int(offset)))

def corregir_gmt(fyh,UTC_OFFSET):
    fyh = fyh.replace("Z","").replace("T"," ")
    local_datetime = datetime.datetime.strptime(fyh, "%Y-%m-%d %H:%M:%S")
    return str(local_datetime - datetime.timedelta(hours=UTC_OFFSET))

def filtra_vacios(stringobjetojson):
    if stringobjetojson != 'None':
        return stringobjetojson
    else:
        return 'Campo Vacio'

def renovar_datos(user_account,passwd):

    url = 'https://exceda-latam.zendesk.com/api/v2/users.json?page=1' # Primer request

    f = open('usuarios.txt', 'w')

    print "Recolectando los datos de usuarios...."

    while (url != None):
        headers = {'Content-Type': 'application/json'}
        obj = json.loads(requests.get(url, auth=(user_account, passwd))._content)
        for x in range(0, len(obj['users'])):
            #print obj['users'][x]
            id = str (obj['users'][x]['id'])
            name = str(obj['users'][x]['name'].replace(',','').encode("utf-8"))
            # if '@exceda.com' in str(obj['users'][x]['email']):
            #     #print id + ',' + email
            #     f.write((id + "," + email+"\n"))
            f.write(id + "," + name + "\n")
        url = obj['next_page']

    f.close()

    print "Listo...."

    url = 'https://exceda-latam.zendesk.com/api/v2/groups.json?page=1' # Primer request
    f = open("groups.txt", "w")
    # FIN DATOS NECESARIOS

    print "Recolectando los datos de Grupos...."

    while (url != None):
        obj = json.loads(requests.get(url, auth=(user_account, passwd))._content)

        for x in obj['groups']:
            #print x['id'],x['name']
            f.write(str(x['id']) + ',' + x['name'] + '\n')
        url = obj['next_page']

    f.close()

    print "Listo...."

    url = 'https://exceda-latam.zendesk.com/api/v2/organizations.json?page=1' # Primer request
    f = open("organizations.txt", "w")

    print "Recolectando los datos de Organizaciones...."

    while (url != None):
        obj = json.loads(requests.get(url, auth=(user_account, passwd))._content)
        for x in obj['organizations']:
            #print 'Name = ' + x['name']
            f.write(str(x['id']) + ',' + x['name'].encode('utf-8') + ',')
            try:
                #print 'Owner = ' + x['organization_fields']['account_owner'] +', '+ x['organization_fields']['account_owner_email']
                f.write(x['organization_fields']['account_owner'] +','+ x['organization_fields']['account_owner_email'])
            except:
                #print 'Owner = Emtpy'
                f.write('Emtpy,Empty')
            f.write('\n')
        url = obj['next_page']

    f.close()

    print "Listo...."