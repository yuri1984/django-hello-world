from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from models import Owner
from forms import EditOwner
from request.models import Request


@render_to('hello/home_base.html')
def home(request):
    owners = Owner.objects.filter()
    return {'owners': owners}

@render_to('hello/requests.html')
def latest_requests(request):
    requests = Request.objects.all()[:10]
    return {'requests': requests}

@login_required
@render_to('hello/home_base.html')
def edit_home(request):
    owners = Owner.objects.filter()
    if owners.count():
        form = EditOwner(request.POST or None, instance=owners[0])
    else:
        form = EditOwner(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()

    return {'form': form}