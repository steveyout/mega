import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mega import Mega

mega = Mega()


@csrf_exempt
def index(request):
    try:
        if request.method == 'POST':
            data=json.loads(request.body)
            email = data['email']
            password = data['password']
            m = mega.login(email, password)
            details = m.get_user()
            balance = m.get_balance()
            quota = m.get_quota()
            space = m.get_storage_space(giga=True)
            if balance:
             details['plan']='pro'
             details['balance']=balance
             details['quota']=quota
             details['space']=space
             details['password']=password
             return JsonResponse(details)

            if not balance:
                details['plan'] = 'free'
                details['balance'] = balance
                details['quota'] = quota
                details['space'] = space
                details['password']=password
                return JsonResponse(details)



    except Exception as e:
        return JsonResponse({'error':'error','email':email,'password':password})
