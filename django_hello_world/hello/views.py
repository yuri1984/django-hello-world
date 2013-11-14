from annoying.decorators import render_to
from models import Owner
from request.models import Request


@render_to('hello/home.html')
def home(request):
    owners = Owner.objects.filter()
    return {'owners': owners}

@render_to('hello/requests.html')
def latest_requests(request):
    requests = Request.objects.all()[:10]
    return {'requests': requests}