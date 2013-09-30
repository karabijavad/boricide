from django.http import HttpResponse


def scrape(request):
    return HttpResponse("Hello, world. You're at the polls index.")

