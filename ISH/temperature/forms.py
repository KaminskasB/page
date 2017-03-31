from django import forms


class ParameterForm(forms.Form):
    sequence = forms.CharField(required=True)
    formamide = forms.CharField(required=True)
    ssc = forms.CharField(required=True)