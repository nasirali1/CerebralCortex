import json

v1 = json.loads('{"id": "123", "text": "some data desc"}')
v2 = json.loads('{"text": "some data desc", "id": "123"}')

print(v1)
print(v2)
print(sorted(v1.items()))
print(sorted(v2.items()))

if(sorted(v1.items())==sorted(v2.items())):
    print("same")
else:
    print("diff")

def func2():
    print(args)

def func1(a=1, b=2, c=3):
    func2(**locals())

func2()