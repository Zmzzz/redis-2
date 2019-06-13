# redis-2
对购物车进行完善，添加了结算中心功能
1.结算功能完善

  查看{
    "data": {
        "course_list": [
            {
                "coupon": {
                    "7": {
                        "type": 0,
                        "type_name": "立减券",
                        "money_equivalent_value": 10
                    },
                    "8": {
                        "type": 1,
                        "type_name": "满减券",
                        "minimum_consume": 1000,
                        "money_equivalent_value": 100
                    },
                    "9": {
                        "type": 2,
                        "type_name": "折扣券",
                        "off_percent": 79
                    }
                },
                "policy_id": "3",
                "period": "14",
                "period_display": "2周",
                "img": "sasa.png",
                "default_coupon": "7",
                "title": "linux基础",
                "course_id": "1",
                "price": "3999.0"
            },
            {
                "course_id": "2",
                "title": "python基础",
                "img": "aaa.png",
                "coupon": {},
                "policy_id": "2",
                "default_coupon": "0",
                "period": "30",
                "period_display": "1个月",
                "price": "500.0"
            }
        ],
        "global_coupon_dict": {
            "coupon": {
                "4": {
                    "type": 0,
                    "type_name": "立减券",
                    "money_equivalent_value": 10
                },
                "5": {
                    "type": 1,
                    "type_name": "满减券",
                    "minimum_consume": 1000,
                    "money_equivalent_value": 100
                },
                "6": {
                    "type": 2,
                    "type_name": "折扣券",
                    "off_percent": 79
                }
            },
            "default_coupon": "5"
        }
    },
    "code": 1000,
    "error": null
}
