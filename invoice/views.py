from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from invoice.models import Client, Doctor


@login_required(login_url='/admin/login/')
def index(request):
    # pylint: disable=no-member
    clients_list = Client.objects.order_by('name')
    print(clients_list[1].insurance)
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
    }
    return HttpResponse(render(request, 'invoice/getinfo.html', context))

def generateinvoice(request):
    print(request.POST)
    client = request.POST['client']
    insurance = request.POST['insurance']
    payment = request.POST['payment']
    doctor = Doctor.objects.get(pk=request.POST['doctor'])
    context = {
        'client': client,
        'insurance': insurance,
        'payment': payment,
        'doctor': doctor,
    }
    return HttpResponse(render(request, 'invoice/generateinvoice.html', context))
