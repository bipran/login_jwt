from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse

from .models import Student
from .serializers import StudentSerializer
# Create your views here.

def studentDetail(request,pk):
    stu         = Student.objects.get(id = pk)
    serializer  = StudentSerializer(stu)
    jsonData    = JSONRenderer().render(serializer.data)

    return HttpResponse(jsonData,content_type='application/json')


def allStudent(request):
    stu         = Student.objects.all()
    serializer  = StudentSerializer(stu,many=True)
    jsonData    = JSONRenderer().render(serializer.data)

    return HttpResponse(jsonData,content_type='application/json')