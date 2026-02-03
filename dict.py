#dictionary in python
d={"name":"john","age":30,"city":"new york"}
print(d["name"])
print(d["age"])
print(d["city"])
d["age"]=31
print(d["age"])
d["job"]="developer"
print(d)
del d["city"]
print(d)
print(len(d))
for key in d:
    print(key,d[key])
for key,value in d.items():
    print(key,value)
print(d.keys())
print(d.values())
print(d.items())
d2=d.copy()
print(d2)
d2.clear()
print(d2)
