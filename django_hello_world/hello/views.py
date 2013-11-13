from annoying.decorators import render_to
from models import Owner


@render_to('hello/home.html')
def home(request):
    owners = Owner.objects.filter()
    return {'owners': owners}
