from django.shortcuts import render
from django.contrib import messages
from Paruluserapp.models import pusermodel, hdpmodel, kdpmodel, bdpmodel, dpmodel, ldpmodel

def index(request):
    return render(request, "index.html")

def home(request):
    return index(request)

def padmin(request):
    return render(request, "admin/padminlogin.html")

def padminloginaction(request):
    if request.method == "POST":
        uname = request.POST.get("email")
        pswd = request.POST.get("pswd")
        print(uname, pswd)
        if uname == "admin" and pswd == "admin":
            data = pusermodel.objects.all()
            return render(request, "admin/adminhome.html", {'data': data})
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "admin/padminlogin.html")

def adminhome(request):
    data = pusermodel.objects.all()
    return render(request, "admin/adminhome.html", {'data': data})

def padminlogout(request):
    return render(request, "admin/padminlogin.html")

def adminpredictions(request):
    return render(request, "admin/adminpredictions.html")

def adminshdpResults(request):
    data = hdpmodel.objects.all()
    return render(request, "admin/hdpresults.html", {'data': data})

def adminskdpResults(request):
    data = kdpmodel.objects.all()
    return render(request, "admin/kdpresults.html", {'data': data})

def adminsbdpResults(request):
    data = bdpmodel.objects.all()
    return render(request, "admin/bdpresults.html", {'data': data})

def adminsdpResults(request):
    data = dpmodel.objects.all()
    return render(request, "admin/dpresults.html", {'data': data})

def adminsldpResults(request):
    data = ldpmodel.objects.all()
    return render(request, "admin/ldpresults.html", {'data': data})
def admindeleteuser(request):
    id = request.GET.get("uid")
    print(id)
    pusermodel.objects.filter(id=id).delete()
    data = pusermodel.objects.all()
    return render(request, "admin/adminhome.html", {'data': data})