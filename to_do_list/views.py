from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def health_check(request):
    return HttpResponse('Web Server is online!')


def register(request):
    if request.method == 'GET':
        return render(request, 'to_do_list/cadastro/register.html')
    