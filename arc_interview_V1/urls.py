
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('', include('app.urls')),
]

handler401 = 'app.views.error_401'
handler403 = 'app.views.error_403'
handler404 = 'app.views.error_404'
handler405 = 'app.views.error_405'
handler500 = 'app.views.error_500'
handler502 = 'app.views.error_502'
handler503 = 'app.views.error_503'
