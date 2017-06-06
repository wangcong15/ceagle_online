# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect 
from forms import DocumentForm
import json
import commands
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import xml.etree.ElementTree as ET
from models import users, user_coefficient, fileassertion
import md5
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from training import propertyRecommendation

#check the username and the password
#the password has been encrypted by md5 algorithm
def check_login(user_name, password):
    select_user = users.objects.filter(uname=user_name).filter(upass=password)
    if len(select_user) == 0:
        return False
    else:
        return True

#check the cookie
def check_cookie(request):
    d = request.COOKIES.keys()
    if "user_name" in d and "user_pass" in d:
        username = request.COOKIES['user_name']
        password = request.COOKIES['user_pass']
        select_user = users.objects.filter(uname=username).filter(upass=password)
        if len(select_user) == 0:
            return False
        else:
            return True
    else:
        return False

#the index page of the website
def index(request):
    if not check_cookie(request):
        return HttpResponseRedirect('/login/')
    username = request.COOKIES['user_name']
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file_upload = request.FILES['docfile']
            file_name = file_upload.name
            if file_name.endswith('.c'):
                file_content = file_upload.read()
                path = os.path.join(settings.MEDIA_ROOT, username, file_upload.name)
                default_storage.save(path, ContentFile(file_content))
                return HttpResponseRedirect('/index')
            elif file_name.endswith('.zip'):
                file_content = file_upload.read()
                path = os.path.join(settings.MEDIA_ROOT, username, file_upload.name)
                default_storage.save(path, ContentFile(file_content))
                os.system("unzip " + path + " -d " + path[0:len(path)-4])
                os.system("rm " + path)
                return HttpResponseRedirect('/index')
            else:
                response_data = {}
                response_data['result'] = 'failure'
                return HttpResponseRedirect('/index')
    else:
        form = DocumentForm()
        zNodes = get_zNodes(os.path.join(settings.MEDIA_ROOT, username))
        response_data = {}
        response_data['form'] = form
        response_data['zNodes'] = json.dumps(zNodes)
    return render_to_response('index.html', response_data, context_instance=RequestContext(request))

def get_zNodes(path):
    result = []
    root_node = {'name':"Projects", 'open':'true'}
    sub_array = []
    sub_files = os.listdir(path)
    for file in sub_files:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            sub_array.append({'name': file, 'isParent': 1, 'children': get_sub_zNodes(file_path)})
    for file in sub_files:
        file_path = os.path.join(path, file)
        #if os.path.isfile(file_path) and file_path.endswith('.c'):
        if os.path.isfile(file_path):
            sub_array.append({'name': file})
    root_node['children'] = sub_array
    result.append(root_node)
    return result

def get_sub_zNodes(path):
    result = []
    sub_files = os.listdir(path)
    for file in sub_files:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            result.append({'name': file, 'isParent': 1, 'children': get_sub_zNodes(file_path)})
    for file in sub_files:
        file_path = os.path.join(path, file)
        #if os.path.isfile(file_path) and file_path.endswith('.c'):
        if os.path.isfile(file_path):
            result.append({'name': file})
    return result

#get the content of the file
def filecontent(request):
    if not check_cookie(request):
        return HttpResponse(json.dumps({}), content_type="application/json")
    username = request.COOKIES['user_name']
    if request.method == 'GET':
        file_name = request.GET['filename']
        fo = open(os.path.join(settings.MEDIA_ROOT, username, file_name), "r")
        file_content = fo.read()
        fo.close()
        response_data = {}
        response_data['data'] = file_content
        return HttpResponse(json.dumps(response_data), content_type="application/json") 

def assertionrecommend(request):
    if not check_cookie(request):
        return HttpResponse(json.dumps({}), content_type="application/json")
    username = request.COOKIES['user_name']
    if request.method == 'GET':
        file_name = request.GET['filename']
        fp = os.path.join(settings.MEDIA_ROOT, username, file_name)
        fa = fileassertion.objects.filter(fapath=fp)
        response_data = {}
        if len(fa) == 1:
            if fa[0].faneed:
                response_data['need'] = "Need"
            else:
                response_data['need'] = "No Need"
            response_data['expr'] = fa[0].faexpr
            if fa[0].faaccept==0:
                response_data['accept'] = "NOT DECIDED"
            elif fa[0].faaccept==1:
                response_data['accept'] = "ACCEPT"
            else:
                response_data['accept'] = "REJECT"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def update_file(request):
    if request.method == 'POST':
        if not check_cookie(request):
            return HttpResponse(json.dumps({}), content_type="application/json") 
        username = request.COOKIES['user_name']
        response_data = {}
        file_name = request.POST['filename']
        file_content = request.POST['filecontent']
        fo = open(os.path.join(settings.MEDIA_ROOT, username, file_name), "w")
        fo.write(file_content)
        fo.close()
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def rename_file(request):
    if request.method == 'POST':
        if not check_cookie(request):
            return HttpResponse(json.dumps({}), content_type="application/json") 
        username = request.COOKIES['user_name']
        response_data = {'status':1}
        file_name = request.POST['filename']
        new_name = request.POST['new_name']
        path = os.path.join(settings.MEDIA_ROOT, username, file_name)
        path_arr = os.path.split(file_name)
        new_path = os.path.join(settings.MEDIA_ROOT, username, path_arr[0], new_name)
        line = "mv " + path + " " + new_path
        os.system(line)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        if not check_cookie(request):
            return HttpResponse(json.dumps({}), content_type="application/json") 
        username = request.COOKIES['user_name']
        response_data = {'status':1}
        file_name = request.POST['filename']
        path = os.path.join(settings.MEDIA_ROOT, username, file_name)
        line = "rm -r " + path
        os.system(line)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def create_folder(request):
    if request.method == 'POST':
        if not check_cookie(request):
            return HttpResponse(json.dumps({}), content_type="application/json") 
        username = request.COOKIES['user_name']
        response_data = {'status':1}
        file_name = request.POST['filename']
        new_name = request.POST['new_name']
        path = os.path.join(settings.MEDIA_ROOT, username, file_name, new_name)
        line = "mkdir " + path
        os.system(line)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def create_file(request):
    if request.method == 'POST':
        if not check_cookie(request):
            return HttpResponse(json.dumps({}), content_type="application/json") 
        username = request.COOKIES['user_name']
        response_data = {'status':1}
        file_name = request.POST['filename']
        new_name = request.POST['new_name']
        path = os.path.join(settings.MEDIA_ROOT, username, file_name, new_name)
        line = "touch " + path
        os.system(line)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

#verify the program
def shell(request):
    if not check_cookie(request):
        return HttpResponse(json.dumps({}), content_type="application/json") 
    username = request.COOKIES['user_name']
    if request.method == 'GET':
        response_data = {}
        elems = []
        file_name = request.GET['filename']
        line1 = "media/ceagle/ceagle_1.0/dc.sh media/" + username + "/" + file_name
        term_out = os.popen(line1).read()
        term_out = term_out.replace("\n", "</p><p>")
        response_data['term_out'] = term_out
        line2 = "media/" + username + "/" + file_name + ".graphml"
        if os.path.exists(line2):
            response_data['flag'] = 0
            tree = ET.parse(line2)
            root = tree.getroot()
            children  = root.getchildren()
            for child in children:
                if child.tag.find("graph") >= 0:
                    children2 = child.getchildren()
                    for child2 in children2:
                        if child2.tag.find("edge") >= 0:
                            children3 = child2.getchildren()
                            for child3 in children3:
                                if child3.attrib['key'] == 'originline':                          
					elems.append(child3.text)
            response_data['data'] = elems
        else:
            response_data['flag'] = 1
        line3 = "rm media/" + username + "/" + file_name + ".*"
        os.system(line3)
        return HttpResponse(json.dumps(response_data), content_type="application/json") 

#login page of the website
def login(request):
    if check_cookie(request):
        return HttpResponseRedirect('/index/')
    if request.method == 'GET':
        return render_to_response('login.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        username = request.POST['form-username']
        password = request.POST['form-password']
        m1 = md5.new()
        m1.update(password)
        password =  m1.hexdigest()
        if(check_login(username, password)):
            response = HttpResponseRedirect('/index/')
            response.set_cookie('user_name', username, 3600)
            response.set_cookie('user_pass', password, 3600)
            return response
        else:
            return render_to_response('login.html', {'errro_message':"Wrong Username Or Password"}, context_instance=RequestContext(request))
def to_login(request):
    return HttpResponseRedirect('/login/')

def register(request):
    if request.method == 'GET':
        return render_to_response('register.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST':
        request_ip = get_client_ip(request)
        username = request.POST['form-username']
        if len(username) > 20:
            return render_to_response('register.html', {'errro_message':"Username Should Be Shorter Than 20"}, context_instance=RequestContext(request))
        password = request.POST['form-password']
        if len(password) > 50:
            return render_to_response('register.html', {'errro_message':"Password Should Be Shorter"}, context_instance=RequestContext(request))
        m1 = md5.new()
        m1.update(password)
        password =  m1.hexdigest()
        if(check_register(username, password, request_ip)):
            response = HttpResponseRedirect('/index/')
            response.set_cookie('user_name', username, 3600)
            response.set_cookie('user_pass', password, 3600)
            return response
        else:
            return render_to_response('register.html', {'errro_message':"Existed Username Or Duplicated IP Address"}, context_instance=RequestContext(request))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#check the username and the ip address
#if the 
def check_register(user_name, password, req_ip):
    select_user = users.objects.filter(uname=user_name)
    if len(select_user) > 0:
        return False
    select_user2 = users.objects.filter(ureqip=req_ip)
    if len(select_user) > 4:
        return False
    else:
        new_user = users(uname=user_name,upass=password,ureqip=req_ip)
        new_user.save()
        line1 = "mkdir media/" + user_name
        os.system(line1)
        line2 = "cp media/example/* media/" + user_name + "/"
        os.system(line2)
        return True


def download(request):
    def file_iterator(file_name, t_f_name="", f_name=""):
        with open(file_name) as f:
            while True:
                c = f.read(512)
                if c:
                    yield c
                else:
                    if t_f_name != "":
                        line2 = "cd " + t_f_name + ";rm " + f_name + ".zip"
                        os.system(line2)
                    break
    file_name = request.GET['filename']
    username = request.COOKIES['user_name']
    the_file_name = os.path.join(settings.MEDIA_ROOT, username, file_name)
    file_name_arr = file_name.split("/")
    file_name = file_name_arr[len(file_name_arr) - 1]
    file_style = request.GET['type']
    if file_style == "1":
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    else:
        line = "cd " + the_file_name + ";zip -r " + file_name + ".zip *"
        os.system(line)
        zip_file_name = the_file_name + "/" + file_name + ".zip"
        response = StreamingHttpResponse(file_iterator(zip_file_name,the_file_name,file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name + ".zip")
    return response

def assertion_recommendation(request):
    if not check_cookie(request):
        return HttpResponse(json.dumps({}), content_type="application/json")
    username = request.COOKIES['user_name']
    if request.method == 'GET':
        file_name = request.GET['filename']
        fo = os.path.join(settings.MEDIA_ROOT, username, file_name)
        response_data = propertyRecommendation(fo, username)
        fa = fileassertion.objects.filter(fapath=fo)
        if len(fa) == 1:
            if response_data[0]['needAssertion'] == 'Need':
                fileassertion.objects.filter(fapath=fo).update(faneed=True, faexpr=response_data[0]['expr'])
            else:
                fileassertion.objects.filter(fapath=fo).update(faneed=False, faexpr=response_data[0]['expr'])
        else:
            if response_data[0]['needAssertion']=='Need':
                fa1 = fileassertion.objects.create(fapath=fo, faneed=True, faexpr=response_data[0]['expr'], faaccept=0)
                fa1.save()
            else:
                fa1 = fileassertion.objects.create(fapath=fo, faneed=False, faexpr=response_data[0]['expr'], faaccept=0)
                fa1.save()
        return HttpResponse(json.dumps(response_data), content_type="application/json") 

def accept_common(request):
    if not check_cookie(request):
        return HttpResponse(json.dumps({}), content_type="application/json")
    username = request.COOKIES['user_name']
    if request.method == 'GET':
        cia = request.GET['cia']
        cia = cia.split(',')
        file_name = request.GET['filename']
        fo = os.path.join(settings.MEDIA_ROOT, username, file_name)
        fileassertion.objects.filter(fapath=fo).update(faaccept=1)
        for i in range(len(cia)):
            cia[i] = int(cia[i])
        ucdata = user_coefficient.objects.filter(ucuser=username)[0]
        current_efficient = ucdata.ucefficient
        current_efficient = current_efficient.replace("[","")
        current_efficient = current_efficient.replace("]","")
        current_efficient = current_efficient.split(", ")
        for i in range(len(current_efficient)):
            current_efficient[i] = float(current_efficient[i])
        for cia_i in cia:
            current_efficient[cia_i] += 0.05
        ucdata.ucefficient = str(current_efficient)
        ucdata.save()
        response_data={'flag': 1}
        return HttpResponse(json.dumps(response_data), content_type="application/json") 

def reject_common(request):
    if not check_cookie(request):
        return HttpResponse(json.dumps({}), content_type="application/json")
    username = request.COOKIES['user_name']
    if request.method == 'GET':
        cia = request.GET['cia']
        cia = cia.split(',')
        file_name = request.GET['filename']
        fo = os.path.join(settings.MEDIA_ROOT, username, file_name)
        fileassertion.objects.filter(fapath=fo).update(faaccept=2)
        for i in range(len(cia)):
            cia[i] = int(cia[i])
        ucdata = user_coefficient.objects.filter(ucuser=username)[0]
        current_efficient = ucdata.ucefficient
        current_efficient = current_efficient.replace("[","")
        current_efficient = current_efficient.replace("]","")
        current_efficient = current_efficient.split(", ")
        for i in range(len(current_efficient)):
            current_efficient[i] = float(current_efficient[i])
        for cia_i in cia:
            if current_efficient[cia_i] > 0.05:
                current_efficient[cia_i] -= 0.05
        ucdata.ucefficient = str(current_efficient)
        ucdata.save()
        response_data={'flag': 1}
        return HttpResponse(json.dumps(response_data), content_type="application/json") 