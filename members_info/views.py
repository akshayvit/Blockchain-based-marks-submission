from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from members_info.models import members
from django.urls import reverse
from . import blockchain
from django.contrib import messages
from django.shortcuts import render
import faust

marks_list=[]

def showform(request):
    try:
        memberlist=members.objects.all().order_by("-marks").values()
        mlist=members.objects.all().order_by("-marks")
        for i in mlist:
            if(len(i.marks)>0 and len(i.roll)>0):
                marks_list.append([int(i.roll),int(i.marks)])
        context={'memberlist':memberlist}
    except Exception as e:
        print(e)
    return HttpResponse(loader.get_template("details.html").render(context,request))



def adddata(request):
  #  global marks
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
    try:
        mem=members.objects.get(roll=roll)
        mem.marks=str(int(mem.marks)+1)
        mem.save()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(reverse('members_info'))

blockchain=blockchain.Blockchain(str(sum(marks_list)/(len(marks_list)+1)))


def publish(request):
    global marks_list
    try:
        app = faust.App('member-marks',broker='kafka://localhost:9092', store='rocksdb://')
        channel = app.channel(value_type=list)
        marks_list=marks_list.sort(reverse=True)
        @app.agent(channel)
        async def greet(marks):
            rank=1
            async for mark in marks:
                with open('marks.txt','w+') as f:
                    f.write(str(rank)+" "+str(mark[0])+" "+str(mark[1]))
                f.close()
                rank+=1
        @app.timer(1.0)
        async def populate():
            await channel.publish_message(marks_list)
        print(channel.subscriber_count)
        return render(request,'submitted.html',{'status':'Published','next_status':'close it now.'})
    except Exception as e:
        print(e)
        return render(request,'submitted.html',{'status':'Not published','next_status':'try again.'})


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