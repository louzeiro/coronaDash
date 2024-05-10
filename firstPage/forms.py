from django import forms


class MyForm(forms.Form):
    campus = forms.CharField(label='Campus', required=False)
    unidades = forms.CharField(label='Unidades', required=False)
