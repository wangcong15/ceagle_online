from django.http import HttpResponse
import json
from models import asser_rec, asser_count
from django.shortcuts import render_to_response
from django.template import RequestContext

def rec_index(request):

	data_array = []
	asserRecs = asser_rec.objects.order_by('?')[:10]
	for asserRecs_i in asserRecs:
		data_array.append({'id':asserRecs_i.id, 'code':asserRecs_i.arcode, 'asserFlag':asserRecs_i.arasserflag, 'asserVar':asserRecs_i.arasservar, 'asserExpr':asserRecs_i.arasserexpr})

	httpRep = HttpResponse(json.dumps({'data':data_array}), content_type="application/json")

	httpRep['Access-Control-Allow-Origin'] = '*'
	return httpRep

def rec_count(request):
	new_count_ip = get_client_ip(request)
	new_count = asser_count(acnumber=new_count_ip)
	new_count.save()
	number = asser_count.objects.count()
	httpRep = HttpResponse(json.dumps({'data':number}), content_type="application/json")
	httpRep['Access-Control-Allow-Origin'] = '*'
	return httpRep

def rec_commit(request):
	# unfinished
	print request.GET['param1']
	print request.GET['param10']
	httpRep = HttpResponse(json.dumps({'flag':1}), content_type="application/json")
	httpRep['Access-Control-Allow-Origin'] = '*'
	return httpRep

def rec_addData(request):
	return render_to_response('rec_index.html', {}, context_instance=RequestContext(request))

def rec_addData_api(request):
	code = request.GET['code']
	asserFlag = request.GET['asser_flag']
	variable = request.GET['variable']
	expression = request.GET['expression']
	if asserFlag == "false":
		asserFlag = False
	else:
		asserFlag = True
	new_asser_rec = asser_rec(arcode=code,arasserflag=asserFlag,arasservar=variable,arasserexpr=expression)
	new_asser_rec.save()
	return HttpResponse(json.dumps({'data':1}), content_type="application/json") 

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip