from test import IRIS


instance = IRIS()

print(str(instance.memory))

instance.set("test/yeah", "thing")
#print(instance.get("test/yeah*"))

instance.set("array0/0", "thing1")
instance.set("array0/1", "thing2")

print(instance.get("test/yeah"))
print(instance.get("test/yeah*"))
print(instance.get("array0/0*"))

print(str(instance.memory))
