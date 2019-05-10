import io
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from invoice.models import Client, Doctor, Invoice, Appointment
from datetime import datetime
from .render import render_to_pdf
from .pdf import draw_pdf


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
    doctor = Doctor.objects.get(pk=request.POST['doctor'])
    available_dates = _get_available_dates(doctor=request.POST['doctor'], client_id=client_id, insurance=insurance)
    context = {
        'client': client,
        'insurance': insurance,
        'payment': payment,
        'doctor': doctor,
        'dates': available_dates,
        'client_id': client_id,
        'doctor_id': request.POST['doctor'],
    }
    return HttpResponse(render(request, 'invoice/generateinvoice.html', context))

def makepdf(request):
    # invoice model info
    client_id = request.POST['client_id']
    doctor_id = request.POST['doctor_id']
    print(client_id)
    date_id = request.POST['appointment']
    # invoice pdf info
    invoice_name = request.POST['invoice_name']
    client_name = request.POST['client']
    insurance = request.POST['insurance']
    payment = request.POST['payment']
    doctor = request.POST['doctor']

    print(invoice_name, client_name, insurance, payment, doctor)

    print(invoice_name, date_id, client_id, doctor_id)
    # save invoice in db
    Invoice.objects.create(
        invoice_name = invoice_name,
        pub_date_id = date_id,
        client_id = client_id,
        doctor_id = doctor_id
    )

    # generating pdf
    params = {
        'invoice_name': invoice_name,
        'client_name': client_name,
        'insurance': insurance,
        'payment': payment,
        'doctor': doctor,
        'service_date': str(Appointment.objects.get(pk=date_id)),
        'current_date': str(datetime.now().strftime('%a, %b %d, %Y')),
    }
    pdf = render_to_pdf('pdf.html', params)
    return HttpResponse(pdf, content_type='application/pdf')

def _get_available_dates(doctor, client_id, insurance):
    # get clients with the same insurance as the current client    
    clients_in_insurance = Client.objects.filter(insurance=insurance)
    # get all the appointments with the same doctor and same insurance
    unavailable_dates = Invoice.objects.filter(doctor=doctor, client_id__in=clients_in_insurance).values('pub_date')
    #exclude unavailable dates    
    available_dates = Appointment.objects.exclude(id__in=unavailable_dates)
    return available_dates
