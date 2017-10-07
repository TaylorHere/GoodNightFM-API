# coding:utf-8
import requests
import time
url = "http://127.0.0.1:5050/users/?includes=addresses,escortores"
headers = {'XXX-base':'$6$rounds=656000$RXsXDTLjHsnk3myE$Bkde.yujrHZYH.pIKoTI./ePV29Ch0UldpIobk850WxyrvjMfSeUI9uhTqUNGPMJNkQ79BM.frDlFUK2weQQq.'}
times = []


def main():
    start = time.time()
    requests.get(url=url, headers=headers)
    end = time.time()
    times.append(end - start)
    print '耗时： %s' % times[-1]
if __name__ == '__main__':
    for i in xrange(100):
        main()
    sum = 0
    for t in times:
        sum = sum + t
    print '平均耗时：%s' % (sum / len(times))
