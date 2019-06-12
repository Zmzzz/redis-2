
class PricePolicyValid(Exception):
    def __init__(self,msg):
        self.msg=msg


class NotFindPricePolicy(Exception):
    def __init__(self,msg):
        self.msg=msg
