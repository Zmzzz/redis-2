from  rest_framework.views import APIView
from api import models
import redis
from rest_framework.response import Response
from api.auth.login_auth import LoginAuth
from api.connect_redis.redis_pool import pool
from api.utils.Response_msg import Response_msg
from django.core.exceptions import ObjectDoesNotExist
from  api.utils.exception import PricePolicyValid,NotFindPricePolicy
from  luffy_course import settings
import json
class shopping_car(APIView):
    authentication_classes = [LoginAuth]
    conn=redis.Redis(connection_pool=pool)
    def post(self,request,*args,**kwargs):
        ret = Response_msg()
        try:
            # 获取用户提交的课程id和价格策略id
            course_id = request.data.get('course_id')
            policy_id = int(request.data.get('policy_id'))
            # 获取课程对象
            course_obj=models.Course.objects.get(id=course_id)
            # 获取该课程所有的价格策略
            price_policy_list=course_obj.price_policy.all()
            price_policy_dict={}
            for item in  price_policy_list:
                price_policy_dict[item.id]={'period':item.valid_period,'period_display':item.get_valid_period_display(),'price':item.price}
            print(price_policy_dict)
            # 校验用户提交的价格策略是否合法
            if policy_id not in price_policy_dict:
                raise PricePolicyValid('价格策略不合法')
            key=settings.KEY %(request.auth.user_id,course_id)
            print(key)
            car_dict={
                'title':course_obj.name,
                'img':course_obj.course_img,
                'defalut':policy_id,
                'policy':json.dumps(price_policy_dict)
            }
            print(car_dict)
            self.conn.hmset(key,car_dict)
            ret.data='添加成功'
        except PricePolicyValid as  e:
            ret.code=1001
            ret.error=e.msg
        except ObjectDoesNotExist as e:
            ret.code = 1001
            ret.error = '课程不存在'
        except Exception as e:
            ret.code=1001
            ret.error='获取购物车失败'
        return Response(ret.dict)
    def delete(self,request,*args,**kwargs):
        ret = Response_msg()
        try:
            course_id_list=request.data.get('course_id')
            for course_id in course_id_list:
                key=settings.KEY %(request.auth.user_id,course_id)
                if not self.conn.hgetall(key):
                    raise NotFindPricePolicy('价格策略未找到')
                self.conn.delete(key)
            ret.data='删除成功'
        except NotFindPricePolicy as e:
           ret.code=1001
           ret.error=e.msg
        except Exception as  e:
            ret.code = 1001
            ret.error ='删除出错'
        return Response(ret.dict)
    def patch(self,request,*args,**kwargs):
        ret = Response_msg()
        try:
            course_id=request.data.get('course_id')
            price_policy_id=str(request.data.get('policy_id'))
            key = settings.KEY % (request.auth.user_id, course_id)
            if not self.conn.hgetall(key):
                raise NotFindPricePolicy('购物车中找不到这个课程')
            price_policy_dict=json.loads(str(self.conn.hget(key,'policy'),encoding='utf-8'))
            if price_policy_id not in price_policy_dict:
                raise  PricePolicyValid('价格策略不合法')
            self.conn.hset(key,'default',price_policy_id)
            ret.data='修改成功'
        except PricePolicyValid as e:
            ret.code=1001
            ret.error=e.msg
        except NotFindPricePolicy as e:
            ret.code=1001
            ret.error=e.msg
        except Exception as e:
            ret.code=1001
            ret.error='删除错误'
        return  Response(ret.dict)
    def get(self,request,*args,**kwargs):
        ret=Response_msg()
        try:
            key_match=settings.KEY%(request.auth.user_id,'*')
            data_dict={}
            for key in self.conn.scan_iter(key_match,count=10):
                key_str=str(key,encoding='utf-8')
                data_dict[key_str] = {
                    'title': str(self.conn.hget(key_str, 'title'), encoding='utf-8'),
                    'img': str(self.conn.hget(key_str, 'img'), encoding='utf-8'),
                    'policy': json.loads(str(self.conn.hget(key_str, 'policy'), encoding='utf-8')),
                    'default': str(self.conn.hget(key_str, 'defalut'), encoding='utf-8')
                }
            ret.data=data_dict
        except Exception as e:
            ret.code=1001
            ret.error='查看出错'
        return  Response(ret.dict)
