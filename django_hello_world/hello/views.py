from annoying.decorators import render_to
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from models import Owner
from forms import EditOwner
from request.models import Request
from django.conf import settings


@render_to('hello/home_base.html')
def home(request):
    owners = Owner.objects.filter()
    return {'owners': owners}

@render_to('hello/requests.html')
def latest_requests(request):
    requests = Request.objects.all()[:10]
    return {'requests': requests}


@login_required
def edit_home(request, ajax=False):
    context = {}
    context.update(csrf(request))
    owners = Owner.objects.filter()
    if owners.exists():
        owner = owners[0]
        form = EditOwner(instance=owner)
    else:
        form = EditOwner()
    if request.POST:
        if owners.exists():
            # Editing of owner existing data
            form = EditOwner(request.POST, request.FILES, instance=owners[0])
        else:
            # No data exists
            form = EditOwner(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if ajax:
                return HttpResponse('ok')
        else:
            if ajax:
                return HttpResponseBadRequest('Wrong')

    context.update({
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL
    })
    return render_to_response('hello/home_base.html', context)