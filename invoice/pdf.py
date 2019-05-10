from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from invoice.models import Client, Doctor, Invoice, Appointment
import xhtml2pdf.pisa as pisa

constants = {
    'name': 'RICHMONDHILL CLINIC',
    'address': '9080 Yonge Street, Unit 8',
    'city_province': 'Richmondhill, ON',
    'postal_code': 'L4J 0YZ',
    'phone': 'Tel: 647-292-4772',
}

def draw_pdf(invoice_name, client_name, insurance, payment, doctor, date_id):
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    pdf = canvas.Canvas(response)

    # Clinic address
    x = 20
    pdf.setFont('Helvetica', 14)
    pdf.drawString(x, 800, constants['name'])
    pdf.setFontSize(11)
    pdf.drawString(x, 780, constants['address'])
    pdf.drawString(x, 765, constants['city_province'])
    pdf.drawString(x, 750, constants['postal_code'])
    pdf.drawString(x, 735, constants['phone'])

    # date and time
    date_x = 490
    print(str(Appointment.objects.get(pk=date_id)))
    pdf.drawString(date_x, 800, 'Date:')
    pdf.drawString(date_x, 780, str(datetime.now().strftime('%a, %b %d, %Y')))

    # line
    line_x1 = 20
    line_x2 = 200
    line_y = 700
    pdf.line(line_x1, line_y, line_x2, line_y)

    # client info
    client_y = 600
    pdf.drawString(x, client_y, 'To: ')
    pdf.drawString(x, client_y-20, 'Name: '+client_name)
    pdf.drawString(x, client_y-35, 'Doctor: '+doctor)
    pdf.drawString(x, client_y-50, 'Insurance Provider: '+insurance)

    # service info
    service_y = 300
    cm = 2.54
    elements = []
    doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)
    data = [['date of service', 'service provided', 'patient fee'],
            [str(Appointment.objects.get(pk=date_id)), 'Treatment', payment]]
    table = Table(data, colWidths=30, rowHeights=30)
    elements.append(pdf)
    elements.append(table)
    doc.build(elements)
    # pdf.drawString(date_x, 800, str(Appointment.objects.get(pk=date_id)))



    # pdf.showPage()
    # pdf.save()
    
    return response