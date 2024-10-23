import time

epoch_time = int(input())
datetime_object = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

print(datetime_object) #Just for verification
