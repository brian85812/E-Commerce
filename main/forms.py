from django import forms

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=True)
    bank_account = forms.CharField(required=True)
    receiver_name = forms.CharField(required=True)