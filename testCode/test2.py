str = "aaa"

def aaa():
 print("call aaa str>>bbb")
 global str
 str = "bbb"

print(str)
aaa()
print(str)
