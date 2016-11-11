import requests
import json
from requests.packages import urllib3
import csv
import Get_Zendesk_Data

urllib3.disable_warnings()
ticket = open('Tickets.txt','r').read().replace('\n', ',').replace('\r', ',').replace('\t', ',')
f = csv.writer(open("results.csv", "w"))

# DATOS NECESARIOS
user_account = "user@exceda.com"
passwd = "pass"
headers = {'Content-Type': 'application/json'}
UTC_OFFSET = 3

#Get_Zendesk_Data.renovar_datos(user_account,passwd)

organization_dict = {}
with open("organizations.txt") as fin:
    for line in fin:
        try:
            k, v, q, w = line.strip().split(',')
            organization_dict[k] = [v]
        except:
            pass

org_owner_dict = {}
with open("organizations.txt") as fin:
    for line in fin:
        try:
            k, v, q, w = line.strip().split(',')
            org_owner_dict[k] = [q]
        except:
            pass

agents_dict = {}
with open("usuarios.txt") as fin:
    for line in fin:
        k, v = line.strip().split(',')
        agents_dict[k] = [v]

groups_dict = {}
with open("groups.txt") as fin:
    for line in fin:
        k, v = line.strip().split(',')
        groups_dict[k] = [v]

# FIN DATOS NECESARIOS

f.writerow(['tk_n','status','requester_name','organization','org_owner','subject','tk_open_hour','solver_name',
            'tk_close_hour','tk_close_hour_date','prioridad','tk_1st_response','tk_1st_response_date',
            'tk_group','aka_tkt?', 'aka_tkt_open','aka_tkt_close','partner_reason','Service','platform','reason',
            'delivery_date'])

num_lines = sum(1 for line in open('Tickets.txt')) -1

for tk_n in ticket.split(','):
    print "Working on ticket:",tk_n," - ",num_lines, "to go...."

    while True:
        try:
            ticketMetrics = json.loads(requests.get('https://exceda-latam.zendesk.com/api/v2/tickets/' + tk_n + '/metrics.json',auth=(user_account, passwd))._content)
            #print json.dumps(ticketMetrics, indent=4, sort_keys=False)
            break
        except: continue

    while True:
        try:
            ticketData = json.loads(requests.get('https://exceda-latam.zendesk.com/api/v2/tickets/' + tk_n + '.json',auth=(user_account, passwd))._content)
            # print json.dumps(ticketData, indent=4, sort_keys=False)
            break
        except: continue

    aka_tkt = str(ticketData['ticket']['custom_fields'][0]['value'])

    aka_tkt_number = str(ticketData['ticket']['custom_fields'][1]['value'])
    aka_tkt_open = str(ticketData['ticket']['custom_fields'][2]['value'])
    if aka_tkt_open == 'None': aka_tkt_open = ''
    aka_tkt_close = str(ticketData['ticket']['custom_fields'][3]['value'])
    if aka_tkt_close == 'None': aka_tkt_open = ''

    partner_reason = str(ticketData['ticket']['custom_fields'][4]['value'])
    service = str(ticketData['ticket']['custom_fields'][6]['value'])
    platform = str(ticketData['ticket']['custom_fields'][7]['value'])
    reason = str(ticketData['ticket']['custom_fields'][8]['value'])
    delivery_date = str(ticketData['ticket']['custom_fields'][9]['value'])

    tk_n = str(tk_n)
    status = str(ticketData['ticket']['status'])

    try: requester_name = str(agents_dict[str(ticketData['ticket']['submitter_id'])]).replace('[','').replace(']','').replace("'","")
    except: requester_name = ''

    try: organization = str(organization_dict[str(ticketData['ticket']['organization_id'])]).replace('[','').replace(']','').replace("'","")
    except: organization = ''

    try: org_owner = str(org_owner_dict[str(ticketData['ticket']['organization_id'])]).replace('[','').replace(']','').replace("'","")
    except: org_owner = ''

    subject = str(ticketData['ticket']['raw_subject'].encode('utf-8'))
    tk_open_hour = str(Get_Zendesk_Data.corregir_gmt(ticketData['ticket']['created_at'], UTC_OFFSET))

    try: solver_name = str(agents_dict[str(ticketData['ticket']['assignee_id'])]).replace('[','').replace(']','').replace("'","")
    except: solver_name = ''

    tk_close_hour = str(ticketMetrics['ticket_metric']['full_resolution_time_in_minutes']['calendar'])
    if tk_close_hour == 'None': tk_close_hour = ''
    try: tk_close_hour_date = Get_Zendesk_Data.dameLaFechayHora(tk_open_hour,tk_close_hour)
    except: tk_close_hour_date = ''

    prioridad = str(ticketData['ticket']['custom_fields'][5]['value'])
    tk_1st_response = str(ticketMetrics['ticket_metric']['reply_time_in_minutes']['calendar'])
    if tk_1st_response == 'None': tk_1st_response = ''
    try: tk_1st_response_date = Get_Zendesk_Data.dameLaFechayHora(tk_open_hour, tk_1st_response)
    except: tk_1st_response_date = ''

    tk_group = str(groups_dict[str(ticketData['ticket']['group_id'])]).replace('[','').replace(']','').replace("'","")

    f.writerow([tk_n, status, requester_name, organization, org_owner, subject, tk_open_hour,solver_name,
                tk_close_hour, tk_close_hour_date, prioridad, tk_1st_response, tk_1st_response_date ,
                tk_group, aka_tkt,aka_tkt_open,aka_tkt_close,partner_reason,service,platform,reason,delivery_date])

    num_lines-=1

print "Done."