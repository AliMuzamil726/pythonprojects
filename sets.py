#This is set 

"""x={1,2,3,4,5,"Ali"}
print(x)
 used to find types of string
print(type(x))"""

# That is empty set
"""s=set()
print(type(s))"""

s={1,2,3,4,5,6,7,8,9,10}
x={1,11,2,3,12,41,15,19,20,0}
#len means length of set
print(len(s))
print(len(x))
"""for i in s:
    print(i)
for i in x:
    print(i)"""


 #intersection of two sets
print(len(s.intersection(x)))
print(x.intersection(s))
#union of two sets
print(s.union(x))
print(x.union(s))
#difference of two sets
print(s.difference(x))
print(x.difference(s))
#Add element from set
s.add(121)
x.add(122)
print(s)
print(x)
#Remove element from set
s.remove(1)
x.remove(11)
print(s)
print(x)




   


    


