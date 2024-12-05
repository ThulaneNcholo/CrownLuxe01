from django.shortcuts import render
from django.conf import settings
import hashlib
import urllib.parse

# models import 
from cart.models import *

# Create your views here.
def generateSignature(dataArray, passPhrase=''):
    payload = ""
    for key in dataArray:
        # Prepare the parameter string and URL encode
        payload += key + "=" + urllib.parse.quote_plus(dataArray[key].replace("+", " ")) + "&"
    
    # Remove the last '&' and append passphrase if exists
    payload = payload[:-1]
    if passPhrase != '':
        payload += f"&passphrase={passPhrase}"
    
    # Generate MD5 hash of the payload
    return hashlib.md5(payload.encode()).hexdigest()


def PaymentsView(request, id):
    customer_order = CustomerOrderModel.objects.get(id=id)
    
    # Prepare the data for signature generation
    pfData = {
        "merchant_id": settings.MERCHANT_ID,
        "merchant_key": settings.MERCHANT_KEY,
        "return_url": "http://localhost:8000/cart/payment-successful",  # Replace with your actual URL
        "notify_url": "http://localhost:8000/payments/notify",  # Replace with your actual URL
        "m_payment_id": str(customer_order.id),  # Use your unique order ID or reference
        "amount": f"{customer_order.total:.2f}",  # Format the amount with 2 decimals
        "item_name": customer_order.reference,
    }

    # Use the generateSignature function to calculate the signature
    passPhrase = settings.PASSPHRASE  # Fetch from settings if you have it
    signature = generateSignature(pfData, passPhrase)

    # Pass data to the template
    context = {
        "customer_order" : customer_order,
        "merchant_id": settings.MERCHANT_ID,
        "merchant_key": settings.MERCHANT_KEY,
        "signature": signature,
        "pfData": pfData,
        "merchant_url": settings.PAY_URL,  # PayFast URL
    }

    return render(request, 'payments/paymentsView.html', context)


def CancelPaymentView(request):
    return render(request,'payments/cancel_payment.html')

def NotifyView(request):
    return render(request,'payments/notify.html')
