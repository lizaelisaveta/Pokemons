from django.shortcuts import render

def list_names(request):
    return render(request, 'aplication/list_names.html', {})