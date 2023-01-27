from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from members_info.models import members
from django.urls import reverse


def showform(request):
    memberlist=members.objects.all().order_by("-marks").values()
    context={
        'memberlist':memberlist
    }
    return HttpResponse(loader.get_template("details.html").render(context,request))

def adddata(request):
    roll=request.GET['roll']
    name=request.GET['name']
    marks=request.GET['marks']
    mem=members(roll=roll,name=name,marks=marks)
    mem.save()
    return HttpResponseRedirect(reverse('members_info'))

def deletedata(request,roll):
    mem=members.objects.get(roll=roll)
    mem.delete()
    return HttpResponseRedirect(reverse('members_info'))

def updatedata(request,roll):
    mem=members.objects.get(roll=roll).values()
    mem.marks=str(int(mem.marks)+1)
    return HttpResponseRedirect(reverse('members_info'))