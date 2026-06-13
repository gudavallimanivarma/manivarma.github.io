from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def secondfun(request):
    return render(request, 'second.html') 

def calculator(request):
    if request.method == 'GET':
        return render(request, 'calculator.html')
    
    if request.method == 'POST':
        print(request.POST)

        v1 = int(request.POST.get('t1'))
        v2 = int(request.POST.get('t2'))
        if 'add' in request.POST:
            res=v1+v2
            action="addition"
        elif 'sub' in request.POST:
            res=v2-v1
            action="subtraction"
        elif 'mul' in request.POST:
            res=v1*v2
            action="multiplication"

        elif 'div' in request.POST:
            if v2!=0:
              res= v1/v2
            else:
               res="error:division by zero"
            action="division"
        return  render(request, 'calculator.html',{'result':res,'action':action})


    