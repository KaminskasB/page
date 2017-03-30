from django import forms


class ParameterForm(forms.Form):
    sequence = forms.CharField(required=True)
    formamide = forms.FloatField(required=True)
    ssc = forms.FloatField(required=True)