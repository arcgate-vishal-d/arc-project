import os
import time
from django.shortcuts import redirect, render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa


def typing_test(sentence, user_input, end_time, start_time):
    start_time = float(start_time)
    end_time = float(end_time)

    # Calculate typing speed
    time_elapsed = end_time - start_time
    words = len(sentence.split())
    typing_speed = words / (time_elapsed / 60)

    # Calculate accuracy
    accuracy = 0
    if len(user_input) > len(sentence):
        char_count = len(sentence)
    else:
        char_count = len(user_input)

    for i in range(char_count):
        if (sentence[i] == user_input[i]):
            accuracy += 1
    accuracy = accuracy / len(sentence) * 100
    return (accuracy, typing_speed)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/html')
    return None

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path


def time_refresh(request):
    try:
        if request.session['endgame']:
            start_time = request.session['endgame']
            request.session['endgame'] = time.time()
            end_time = time.time()
            diff = round((end_time - start_time))
            del request.session['endgame'] 
            return diff
    except:
        end_time  = time.time()
        request.session['endgame'] = end_time
        return 0
