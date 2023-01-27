from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from members_info.models import members
from django.urls import reverse
from . import blockchain
from django.contrib import messages

marks_list=[]

def showform(request):
    try:
        memberlist=members.objects.all().order_by("-marks").values()
        mlist=members.objects.all().order_by("-marks")
        for i in mlist:
            if(len(i.marks)>0):
                marks_list.append(int(i.marks))
        context={'memberlist':memberlist}
    except Exception as e:
        print(e)
    return HttpResponse(loader.get_template("details.html").render(context,request))



def adddata(request):
  #  global marks
    roll=request.GET['roll']
    name=request.GET['name']
    marks=request.GET['marks']
    marks_list.append(int(marks))
    mem=members(roll=roll,name=name,marks=marks)
    mem.save()
    return HttpResponseRedirect(reverse('members_info'))

def deletedata(request,roll):
    mem=members.objects.get(roll=roll)
    mem.delete()
    return HttpResponseRedirect(reverse('members_info'))

def updatedata(request,roll):
    try:
        mem=members.objects.get(roll=roll)
        mem.marks=str(int(mem.marks)+1)
        marks_list.append(1)
        mem.save()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(reverse('members_info'))

blockchain=blockchain.Blockchain(str(sum(marks_list)/(len(marks_list)+1)))

def mine_block(request):
   # global blockchain
    try:
        previous_block=blockchain.get_previous_block()
        previous_proof=previous_block['proof']
        proof=blockchain.proof_of_work(previous_proof)
        previous_hash=blockchain.hash(previous_block)
        block=blockchain.create_block(proof,previous_hash)
        response={'message':'Congo you mined a block!!!!','index':block['index'],'timestamp':block['timestamp'],'proof':block['proof'],'previous_hash':block['previous_hash']}
        messages.success(request,'Congo!!! Got your entry.')
        return HttpResponseRedirect(reverse('members_info'))
    except Exception as e:
        print(e)
    


def is_valid(request):
   # global blockchain
    response={"validity":blockchain.is_chain_valid(blockchain.chain)}
    if(response['validity']==True):
        messages.success(request,'Successfully Got the Marks Entry.')
    else:
        messages.error(request,'OOPS!!! Something issue. Try back again after sometimes.')
    return HttpResponseRedirect(reverse('members_info'))