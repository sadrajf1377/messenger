from django.shortcuts import render


def custom_handler_404(request,exception):
    return render(request, '404_handler.html')
