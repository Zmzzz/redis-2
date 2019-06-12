from django.shortcuts import render
from  rest_framework import  serializers
from rest_framework.response import Response
from  rest_framework.views import APIView
from  rest_framework.viewsets import ViewSetMixin
from api.models import *
from  api import  models
# Create your views here.
class CourseModelSerializes(serializers.ModelSerializer):
    course_type=serializers.CharField(source='get_course_type_display')
    level=serializers.CharField(source='get_level_display')
    status=serializers.CharField(source='get_status_display')
    sub_category=serializers.CharField(source='sub_category.name')
    class Meta:
        model=Course
        fields='__all__'
class CourseDetailModelSerializes(serializers.ModelSerializer):
    course=serializers.CharField(source='course.name')
    price_policy=serializers.SerializerMethodField()
    class Meta:
        model=CourseDetail
        fields='__all__'
    def get_price_policy(self,obj):
        temp=[]
        for item in obj.course.price_policy.all():
            temp.append({'price':item.price,'valid_period':item.get_valid_period_display()})
        return temp
class course(ViewSetMixin,APIView):
    def list(self,*args,**kwargs):
        course_obj=models.Course.objects.all()
        ret=CourseModelSerializes(course_obj,many=True)
        return Response(ret.data)
    def retrieve(self,*args,**kwargs):
        course_id=kwargs.get('pk')
        courseDetail_obj=models.CourseDetail.objects.filter(course_id=course_id).first()
        ret=CourseDetailModelSerializes(courseDetail_obj)
        return Response(ret.data)