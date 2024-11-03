from math import *
p = 1009
q = 3643
fy = (p - 1) * (q - 1)
n = p * q

elist = [e for e in range(2, fy) if gcd(e, fy) == 1]
num=[]
for i in range(len(elist)):
    num.append((1+gcd(elist[i]-1,p-1))*(1+gcd(elist[i]-1,q-1)))
minx=min(num)
print(minx)
count=0
for i in range(len(elist)):
    if num[i]==minx:
        count+=elist[i]

print(count)
