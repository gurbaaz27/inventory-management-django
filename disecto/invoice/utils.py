from disecto.settings import MEDIA_ROOT
from weasyprint import HTML, CSS
import jinja2
from datetime import datetime
from pathlib import Path


def construct_filename(customer_name, date_time):
    return f"{customer_name.strip().replace(' ','-')}-{date_time.strftime('%Y-%m-%d--%H-%M-%S')}"


def makepdf(html):
    """Generate a PDF file from a string of HTML."""
    htmldoc = HTML(string=html, base_url="")
    css = CSS(filename=MEDIA_ROOT+'/template/invoice.css')
    return htmldoc.write_pdf(stylesheets=[css])


def create_invoice_pdf(path_to_file, invoice_info, invoice_items):
    invoice  = invoice_info["id"]
    customer = invoice_info["customer"]
    items    = []
    date     = datetime.now().strftime("%d/%m/%Y")

    total = 0

    for item in invoice_items:
        price = int(item["item"]["price"] * item["quantity"])
        total += price
        
        items.append([item["item"]["description"], item["item"]["price"], item["quantity"], price])
    
    subs = jinja2.Environment( 
              loader=jinja2.FileSystemLoader(MEDIA_ROOT+'/template')      
              ).get_template('invoice.html').render(invoice=invoice, date=date, customer=customer, items=items, total=total) 

    with open(path_to_file+'.html','w') as f:
        f.write(subs)

    html = Path(path_to_file+'.html').read_text()
    pdf = makepdf(html)
    Path(path_to_file+'.pdf').write_bytes(pdf)
