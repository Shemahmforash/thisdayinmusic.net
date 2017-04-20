from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>This Day in Music</title><html>')
