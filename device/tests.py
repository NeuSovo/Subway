from django.test import TestCase
import time

# Create your tests here.
a = 1000000
b = 1
count = 0
time1 = time.time()
for i in range(a):
    if (i % 100 == 0):
        b = 1.0
        count += 1
    b = b * 1.5

print(time.time() - time1)
print(b,count)
