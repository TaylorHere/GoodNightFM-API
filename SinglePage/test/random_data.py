# coding:utf-8
import random
import uuid


class random_data():
    """docstring for Random_data"""

    def telephone(self):
        header = random.choice(['151', '135', '185', '137', '187', '181'])
        body = random.sample(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)
        tail = random.sample(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)
        return header + ''.join(body) + ''.join(tail)

    def people_name(self):
        return random.choice(['taylor', 'shaohen', 'leefanv', 'p0h5'])

    def sex(self):
        return random.choice(['male', 'female', 'unknown'])

    def img_url(self):
        return random.choice(['http://www.baidu.com'])

    def id(self):
        return str(uuid.uuid1())

    def strings(self):
        return ''.join(random.sample(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], 8))

    def address(self):
        return random.choice(['花草秀xxx', '四川tuopu'])

    def bool(self):
        return random.choice([False, True])

    def topic(self):
        return random.choice(['干洗', '取快递', '圣诞抢苹果', '食堂打饭'])

    def sentence(self):
        return random.choice(['一食堂炸酱面', '我简直寂寞如雪', '可乐一瓶', '来人聊会天呢', '拿个快递谢谢'])

    def time(self):
        import time
        return time.time() + random.uniform(10, 100)

    def int(self, a, b):
        return random.randint(a, b)
# todo 随机函数仅在加载时随机，要做到实例化随机
