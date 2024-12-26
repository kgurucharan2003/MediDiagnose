"""Paruladminapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Paruladminapp import views as paruladmins
from Paruluserapp import views as parulusers

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', paruladmins.index, name="index"),
    path('home/', paruladmins.home, name="home"),

    path('padmin/', paruladmins.padmin, name="padmin"),
    path('padminloginaction/', paruladmins.padminloginaction, name="padminloginaction"),
    path('adminhome/', paruladmins.adminhome, name="adminhome"),
    path('padminlogout/', paruladmins.padminlogout, name="padminlogout"),
    path("adminpredictions/", paruladmins.adminpredictions, name="adminpredictions"),
    path('admindeleteuser/', paruladmins.admindeleteuser, name="admindeleteuser"),
    path('adminshdpResults/', paruladmins.adminshdpResults, name="adminshdpResults"),
    path('adminskdpResults/', paruladmins.adminskdpResults, name="adminskdpResults"),
    path('adminsbdpResults/', paruladmins.adminsbdpResults, name="adminsbdpResults"),
    path('adminsdpResults/', paruladmins.adminsdpResults, name="adminsdpResults"),
    path('adminsldpResults/', paruladmins.adminsldpResults, name="adminsldpResults"),
  

    path('puser/', parulusers.puser, name="puser"),
    path('puserlogin/', parulusers.puser, name="puserlogin"),
    path('puserregister/', parulusers.puserregister, name="puserregister"),
    path('puserloginaction/', parulusers.puserloginaction, name="puserloginaction"),
    path('puserhome/', parulusers.puserhome, name="puserhome"),
    path('userprofile/', parulusers.userprofile, name="userprofile"),
    path('userprofileupdate/', parulusers.userprofileupdate, name="userprofileupdate"),
    path('puserlogout/', parulusers.puserlogout, name="puserlogout"),
    path('contact/', parulusers.contact_form, name='contact'),

    path('hdp/', parulusers.hdp, name="hdp"),
    path('kdp/', parulusers.kdp, name="kdp"),
    path('bdp/', parulusers.bdp, name="bdp"),
    path('dp/', parulusers.dp, name="dp"),
    path('ldp/', parulusers.ldp, name="ldp"),

    path('hdpaction/', parulusers.hdpaction, name="hdpaction"),
    path('kdpaction/', parulusers.kdpaction, name="kdpaction"),
    path('bdpaction/', parulusers.bdpaction, name="bdpaction"),
    path('dpaction/', parulusers.dpaction, name="dpaction"),
    path('ldpaction/', parulusers.ldpaction, name="ldpaction"),

    path('puserredictions/', parulusers.puserredictions, name="puserredictions"),
    path('hdpResults/', parulusers.hdpResults, name="hdpResults"),
    path('kdpResults/', parulusers.kdpResults, name="kdpResults"),
    path('bdpResults/', parulusers.bdpResults, name="bdpResults"),
    path('dpResults/', parulusers.dpResults, name="dpResults"),
    path('ldpResults/', parulusers.ldpResults, name="ldpResults"),
]
