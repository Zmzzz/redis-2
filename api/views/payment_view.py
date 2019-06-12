import json
import redis
import datetime
from  api import models
from api.utils.exception import NotFindCourse
from api.connect_redis.redis_pool import pool
from luffy_course.settings import KEY,Payment_Key
from api.utils.Response_msg import Response_msg
from  rest_framework.views import APIView
from  rest_framework.response import Response
from  api.auth.login_auth import LoginAuth
class payment(APIView):
    authentication_classes = [LoginAuth]
    conn=redis.Redis(connection_pool=pool)
    def post(self,request,*args,**kwargs):
        """
        将购物车的东西添加到结算中
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        ret=Response_msg()
        try:
            # 获取用户传来的课程id列表
            course_id_list=request.data.get('course_id')
            data_dict = {}
            global_coupon={
                'coupon':{},
                'default_coupon':0
            }
            current_time=datetime.date.today()
            # 获取用户购物车里面的信息
            for course_id in course_id_list:
                shopping_key=KEY%(request.auth.user_id,course_id)
                # 判断用户发过来的课程是否在购物车中
                b_shopping_key=bytes(shopping_key,encoding='utf-8')
                if b_shopping_key not in self.conn.keys():
                    raise NotFindCourse('购物车中没有这个课程')
                # 获取到默认价格策略的信息
                default_policy_id=str(self.conn.hget(shopping_key,'defalut'), encoding='utf-8')
                policy=json.loads(str(self.conn.hget(shopping_key,'policy'), encoding='utf-8'))
                policy_info=policy[default_policy_id]
                # 获取到这个课程的部分信息
                payment_key=Payment_Key%(request.auth.user_id,course_id)
                data_dict[payment_key] = {
                    'title': str(self.conn.hget(shopping_key, 'title'), encoding='utf-8'),
                    'img': str(self.conn.hget(shopping_key, 'img'), encoding='utf-8'),
                    'coupon':{},
                    "policy_id": default_policy_id,
                    'default_coupon':0
                }
                data_dict[payment_key].update(policy_info)
            # 获取用户所有未使用，没有过期的优惠券
            coupon_obj_list=models.CouponRecord.objects.filter(
                user=request.auth.user,
                status=0,
                coupon__valid_begin_date__lte=current_time,
                coupon__valid_end_date__gte=current_time)
            # 将优惠券进行分类
            coupon_course_dict={}
            for coupon_obj in coupon_obj_list:
                # 如果是通用券，执行global_dict,
                if not coupon_obj.coupon.object_id:
                    # 通用立减券
                    if coupon_obj.coupon.coupon_type == 0:
                        global_coupon['coupon'][coupon_obj.id] = {'type': 0,'type_name': coupon_obj.coupon.get_coupon_type_display(), 'money_equivalent_value': coupon_obj.coupon.money_equivalent_value}
                    # 通用满减券
                    if coupon_obj.coupon.coupon_type == 1:
                        global_coupon['coupon'][coupon_obj.id] = {'type': 1,'type_name': coupon_obj.coupon.get_coupon_type_display(),'minimum_consume': coupon_obj.coupon.minimum_consume,'money_equivalent_value': coupon_obj.coupon.money_equivalent_value
                                                        }
                    # 通用折扣券
                    if coupon_obj.coupon.coupon_type == 2:
                        global_coupon['coupon'][coupon_obj.id] = {
                            'type': 2,
                            'type_name': coupon_obj.coupon.get_coupon_type_display(),
                            'off_percent': coupon_obj.coupon.off_percent
                        }
                    continue
                # 立减券
                if coupon_obj.coupon.coupon_type == 0:
                    coupon_course_dict[coupon_obj.id] = {'type': 0,'type_name': coupon_obj.coupon.get_coupon_type_display(),'money_equivalent_value': coupon_obj.coupon.money_equivalent_value}
                # 满减券
                if coupon_obj.coupon.coupon_type==1:
                    coupon_course_dict[coupon_obj.id]={'type':1,'type_name':coupon_obj.coupon.get_coupon_type_display(),'minimum_consume':coupon_obj.coupon.minimum_consume,'money_equivalent_value':coupon_obj.coupon.money_equivalent_value}
                # 折扣券
                if coupon_obj.coupon.coupon_type==2:
                    coupon_course_dict[coupon_obj.id]={'type':2,'type_name':coupon_obj.coupon.get_coupon_type_display(),'off_percent':coupon_obj.coupon.off_percent}
                # 获取课程id
                course_id=str(coupon_obj.coupon.object_id)
                # 获取到优惠券，判断是否购买了这个课程
                if course_id in course_id_list:
                    payment_key = Payment_Key % (request.auth.user_id, course_id)
                    data_dict[payment_key]['coupon'][coupon_obj.id]=coupon_course_dict[coupon_obj.id]
            data_dict['global_coupon']=global_coupon
            print(data_dict)
        except NotFindCourse as e:
            ret.code = 1001
            ret.error = e.msg
        # except Exception as e:
        #     ret.code=1001
        #     ret.error='添加结算错误'
        return Response(ret.dict)
