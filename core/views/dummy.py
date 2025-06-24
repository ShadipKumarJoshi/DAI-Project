from django.shortcuts import render


def dummy(request):
    return render(request, 'core/dummy.html',)