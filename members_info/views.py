from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from members_info.models import members
from django.urls import reverse
from . import blockchain
from django.contrib import messages
from django.shortcuts import render

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
'''
import faust

app = faust.App('members_info', broker='kafka://localhost')


@app.agent(value_type=members)
async def getmatks(marks):
    async for mark in marks:
        print(f'Submission for {mark.roll}: {mark.marks}')

kafka_topic = app.topic('marks', key_type=str, value_type=int)
marklist = app.Table('marks', default=int)


@app.agent(kafka_topic)
async def marklistsub(markstlist):
    async for roll, marks in markstlist.items():
        marklist[roll] += marks
'''

def mine_block(request):
   # global blockchain
    try:
        previous_block=blockchain.get_previous_block()
        previous_proof=previous_block['proof']
        proof=blockchain.proof_of_work(previous_proof)
        previous_hash=blockchain.hash(previous_block)
        block=blockchain.create_block(proof,previous_hash)
        response={'message':'Congo you mined a block!!!!','index':block['index'],'timestamp':block['timestamp'],'proof':block['proof'],'previous_hash':block['previous_hash']}
        messages.add_message(request, messages.SUCCESS,'Congo!!! Your entry is entered.', extra_tags='ex-tag')
        return render(request,'submitted.html',{'status':'submitted','next_status':'Confirm and Send'})
    except Exception as e:
        print(e)
    


def is_valid(request):
   # global blockchain
    response={"validity":blockchain.is_chain_valid(blockchain.chain)}
    if(response['validity']==True):
        return render(request,'submitted.html',{'status':'confirmed and sent','next_status':'can Add more entries'})
    return render(request,'submitted.html',{'status':'not succesfully sent','next_status':'try again'})