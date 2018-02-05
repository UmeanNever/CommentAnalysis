# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json
import socket
from django.shortcuts import render


def dashboard(request):
    data = {'title': 'Comment Analysis'}
    return render(request, 'dashboard.html', data)


def analysis_result(request):
    rtn = {"status": "failed"}
    try:
        if request.method == "POST":
            query = request.POST['q']
        else:
            query = request.GET['q']
    except:
        rtn["err_msg"] = "parameter q is not passed."
        return HttpResponse(json.dumps(rtn))
    try:
        result = json.loads(request_analysis(query))
        rtn["data"] = result
    except:
        rtn["err_msg"] = "Analysis Server Error"
        return HttpResponse(json.dumps(rtn))
    rtn["status"] = "sucess"
    return HttpResponse(json.dumps(rtn))


def request_analysis(text):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('127.0.0.1', 8888))
    conn.send(text)
    result = str(conn.recv(102400))
    conn.close()
    return result
