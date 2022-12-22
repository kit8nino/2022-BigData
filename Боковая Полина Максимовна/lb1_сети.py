import matplotlib.pyplot as plt
text = input("enter a string to convert into ascii values:")
ascii_values = []
for character in text:
    ascii_values.append(ord(character))
print(ascii_values)
b=[]
p=""
for i in ascii_values:
    p="1110"
    while i>0:
        p=p+str(i%2)
        i=i//2
    b.append(p)
    #b.append(bin(ascii_values[i]))
print(b)
n=""
for i in b:
    n=n+(i+"111")
print(n)
ba=[int(num) for num in n]
print(ba)
plt.plot(ba,drawstyle="steps-post")
plt.show()
