# 没有这个价格策略
class PricePolicyValid(Exception):
    def __init__(self,msg):
        self.msg=msg

# 价格策略不在购物车中
class NotFindPricePolicy(Exception):
    def __init__(self,msg):
        self.msg=msg
# 在购物车中没有找到这个课程
class NotFindCourse(Exception):
    def __init__(self,msg):
        self.msg=msg
