import io
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from invoice.models import Client, Doctor, Invoice, Appointment
from datetime import datetime, date
from dateutil import parser
from dateutil.rrule import rrule, HOURLY
from .render import render_to_pdf
import holidays


@login_required(login_url='/admin/login/')
def index(request):
    # pylint: disable=no-member
    clients_list = Client.objects.order_by('name')
    # print(clients_list[1].insurance)
    context = {
        'client_list': clients_list,
    }
    return HttpResponse(render(request, 'invoice/index.html', context))

def getinfo(request):
    client_id = request.POST['client']
    client = Client.objects.get(pk=client_id)
    doctor_list = Doctor.objects.all()
    context = {
        'client': client,
        'doctor_list': doctor_list,
        'client_id': client_id,
    }
    return HttpResponse(render(request, 'invoice/getinfo.html', context))

def generateinvoice(request):
    # print(request.POST)
    client = request.POST['client']
    client_id = request.POST['client_id']
    # print('client id is: ', client_id)
    insurance = request.POST['insurance']
    payment = request.POST['payment']
    doctor = Doctor.objects.get(name=request.POST['doctor'])
    print(doctor.id)
    available_dates = _get_available_dates(doctor_id=doctor.id, client_id=client_id, insurance=insurance)
    context = {
        'client': client,
        'insurance': insurance,
        'payment': payment,
        'doctor': request.POST['doctor'],
        'dates': available_dates,
        'client_id': client_id,
        'doctor_id': doctor.id,
    }
    return HttpResponse(render(request, 'invoice/generateinvoice.html', context))

def makepdf(request):
    # invoice model info
    client_id = request.POST['client_id']
    doctor_id = request.POST['doctor_id']
    appointment_time = str(request.POST['appointment'])
    # parses can not parse 'noon' so replacing it with 12 p.m.
    if('noon' in appointment_time):
        appointment_time = appointment_time.replace('noon', '12 p.m.')

    date = Appointment.objects.get(date=parser.parse(appointment_time))
    # invoice pdf info
    invoice_name = request.POST['invoice_name']
    client_name = request.POST['client']
    insurance = request.POST['insurance']
    payment = request.POST['payment']
    doctor = request.POST['doctor']

    print(invoice_name, client_name, insurance, payment, doctor)

    print(invoice_name, date.id, client_id, doctor_id)
    # save invoice in db
    Invoice.objects.create(
        invoice_name = invoice_name,
        pub_date_id = date.id,
        client_id = client_id,
        doctor_id = doctor_id,
    )

    # generating pdf
    params = {
        'invoice_name': invoice_name,
        'client_name': client_name,
        'insurance': insurance,
        'payment': payment,
        'doctor': doctor,
        'service_date': appointment_time,
        'current_date': str(datetime.now().strftime('%a, %b %d, %Y')),
    }
    pdf = render_to_pdf('pdf.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

def resetdates(request):
    ca_holidays = holidays.CountryHoliday('CA', prov='ON')

    start = date(2019, 1, 1)
    end = date(2019, 12, 30)

    start_hour = 10
    end_hour = 18

    Appointment.objects.all().delete()
    for dt in rrule(HOURLY, dtstart=start, until=end):
        if(dt not in ca_holidays and dt.hour <= 18 and dt.hour >= 10 and dt.weekday() < 6):
            Appointment.objects.create(date=dt)

    context = {
        'start_date': start,
        'end_date': end,
        'start_hour': start_hour,
        'end_hour': end_hour,
    }
    return HttpResponse(render(request, 'invoice/resetdates.html', context))

# utility functions
def _get_available_dates(doctor_id, client_id, insurance):
    # get clients with the same insurance as the current client    
    clients_in_insurance = Client.objects.filter(insurance=insurance)
    # get all the appointments with the same doctor and same insurance
    unavailable_dates = Invoice.objects.filter(doctor=doctor_id, client_id__in=clients_in_insurance).values('pub_date')
    #exclude unavailable dates    
    available_dates = Appointment.objects.exclude(id__in=unavailable_dates)
    return available_dates
