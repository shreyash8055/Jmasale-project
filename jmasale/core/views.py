from django.http import HttpResponse

# for debugging purpose only
def index(request):
    # return HttpResponse("Welcome to Jhaagirdaar Masale!")
    # param=request.GET.get('param', 'default')
    return HttpResponse(f"Welcome to Jhaagirdaar Masale! mate")

