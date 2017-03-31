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
            dirty_formamide = form.cleaned_data['formamide']
            decimal_formamide = re.compile(r'[^\d.]+')
            clean_formamide = float(decimal_formamide.sub('', dirty_formamide))
            print (clean_formamide)

            dirty_ssc = form.cleaned_data['ssc']
            decimal_ssc = re.compile(r'[^\d.]+')
            clean_ssc = float(decimal_ssc.sub('', dirty_ssc))


            dirty_sequence = form.cleaned_data['sequence']
            clean_sequence = re.sub('[^ACTG]', '', dirty_sequence)  # Removes all characters and whitespace except ACTG
            melting_temperature = calculate_temperature(clean_formamide, clean_ssc, clean_sequence)

            message = ''

            if melting_temperature == 0:
                message = 'The sequence entered was likely not valid. Under the hood, the tool only looks at A, G, C and T characters (uppercase) and ignores everything else. Check the notes section below!'
            if 0 < melting_temperature <80:
                message = 'The melting temperature value is lower than usual. Maybe you are using formamide concentration higher than 50% or SSC lower than 5X, in which case it might be valid. Either way, make sure your input is correct (check the notes section below) and submit again just to be safe!'
            if melting_temperature < 0:
                message = 'The melting temperature is subzero, which does not make sense. Probably something wrong with the input. Please check the notes section below and make sure your submission is valid.'
            if melting_temperature >100:
                message = 'The melting temperature value is higher than usual. Maybe you are using formamide concentration lower than 50% or SSC higher than 5X, in which case it might be valid. Either way, make sure your input is correct (check the notes section below) and submit again just to be safe!'

            context['melting_temperature'] = melting_temperature
            context['ideal_temperature'] = round(melting_temperature - 25, 1)
            context['success'] = True
            context['message'] = message

    return render(request, 'temperature/index.html', context)


def calculate_temperature(formamide, ssc, sequence):
    gc_content = _calculate_gc(sequence)
    try:
        melting_temperature = round(
            79.8 + 18.5 * math.log(0.33 / 2 * ssc) + 0.58 * gc_content + 0.0012 * math.pow(gc_content, 2) - 820 / len(
                sequence) - 0.35 * formamide, 1)
    except ZeroDivisionError:
        melting_temperature = 0


    return melting_temperature


def _calculate_gc(sequence):
    try:
        gc_content = (sequence.count('C') + sequence.count('G')) / float(len(sequence)) * 100
    except ZeroDivisionError:
        gc_content = 0
    return gc_content
