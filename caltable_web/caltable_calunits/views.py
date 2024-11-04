from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required()
def calunits_home(request):
    return HttpResponse(f'User Email: {request.user.id}')