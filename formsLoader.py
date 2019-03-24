import tools
import json


base_url = 'https://su-ati.crewplatform.aero/CrewServices/crewForms/v1/lightweightSearch/SU?'
start = 'startDateRange={0}-{1}-{2}'
end = '&endDateRange={0}-{1}-{2}'
form = '&formId={}'

dayinmonth = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:15}
start_month = 11
finish_month = 11
year = 2017
#  form IDs:
#   23=отчет СБ о рейсе,
#   38=Оказание медицинской помощи на борту ВС,
#   40=Нарушения пассажирами правил поведения,
#   41=Urgent Notification
forms = ['23', '38', '40', '41']


def h(i):
    return '0' + str(i) if i < 10 else str(i)


def dict_to_str(line):
    s = '{idForm};{formTitle};{idFlight};{staffId};{departureAirport};{flightNumber};{departureDate}'
    return s.format(**line)


resp = []
session = tools.authentication()

for f in forms:
    for m in range(start_month, finish_month+1):
        for d in range(1, dayinmonth[m]+1):
            start_url = start.format(year, h(m), h(d))
            end_url = end.format(year, h(m), h(d))
            form_url = form.format(f)
            url = base_url + start_url + end_url + form_url
            r = session.get(url)
            r = r.content.decode('utf-8')
            r = json.loads(r)
            resp += r['formsSearchResults']

resp = [dict_to_str(line) for line in resp]

dates = '['+ str(year) + '] ' + h(start_month) + '.01' + '-' + h(finish_month) + '.' + h(dayinmonth[finish_month])
file = open('reports ' + dates + '.csv','w')
file.write('Form ID;Form title;Flight ID;Staff ID;Departure airport;Flight number;Departure date\n')
for line in resp:
    file.write(line+'\n')
file.close()
