from django.shortcuts import render
from temperature.forms import ParameterForm
import re
import math


def temperature_index(request):
    return render(request, 'temperature/index.html')


def get_parameters(request):
    context = {
        'submitted': True,
    }
    if request.method == 'POST':
        form = ParameterForm(request.POST)
        print ('method is post')
        if form.is_valid():
            print ('form is valid')
            formamide = form.cleaned_data['formamide']
            ssc = form.cleaned_data['ssc']
            dirty_sequence = form.cleaned_data['sequence']
            clean_sequence = re.sub('[^ACTG]', '', dirty_sequence)  # Removes all characters and whitespace except ACTG
            melting_temperature = calculate_temperature(formamide, ssc, clean_sequence)

            context['melting_temperature'] = melting_temperature
            context['ideal_temperature'] = round(melting_temperature - 25, 1)
            context['success'] = True

    return render(request, 'temperature/index.html', context)


def calculate_temperature(formamide, ssc, sequence):
    gc_content = _calculate_gc(sequence)
    melting_temperature = round(
        79.8 + 18.5 * math.log(0.33 / 2 * ssc) + 0.58 * gc_content + 0.0012 * math.pow(gc_content, 2) - 820 / len(
            sequence) - 0.35 * formamide, 1)

    return melting_temperature


def _calculate_gc(sequence):
    gc_content = (sequence.count('C') + sequence.count('G')) / float(len(sequence)) * 100
    return gc_content
