str = "aaa"

def init():
 print("call init")
 global str
 str = "bbb"

print(str)
init()
print(str)

