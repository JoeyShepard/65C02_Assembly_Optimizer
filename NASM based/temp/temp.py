
class foo():
    somelist=[]

x=[]

for i in range(3):
    x.append(foo())

for i,bar in enumerate(x):
    x[i].somelist=[i+1]

print([a.somelist for a in x])
#output: [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
#why not [[1], [2], [3]]?

x[0].somelist+=[4]
print([a.somelist for a in x])
#output: [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
#why does it affect every instance, not just the first?

def func(num):
    temp=foo()
    temp.somelist+=[num+1]
    return temp

y=[]

for i in range(3):
    y.append(func(i))

print([a.somelist for a in y])
