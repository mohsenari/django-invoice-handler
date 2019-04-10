from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from invoice.models import Client


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
    context = {
        'client': client,
    }
    return HttpResponse(render(request, 'invoice/getinfo.html', context))

@login_required(login_url='/admin/login/')
def number(request, invoice_number):
    # pylint: disable=no-member
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'invoice_number': invoice_number,
    }
    return HttpResponse(render(request, 'invoice/number.html', context))
