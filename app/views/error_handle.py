from django.shortcuts import render


def error_401(request,exception):
    return render(request, 'elements/403.html')


def error_403(request,exception):
    return render(request, 'elements/403.html')


def error_404(request,exception):
    return render(request, 'elements/error_page.html')


def error_405(request,exception):
    return render(request, 'elements/error_page.html')


def error_500(request):
    return render(request, 'elements/error_page.html')
