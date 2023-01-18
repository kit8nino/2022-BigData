import matplotlib.pyplot as plt
word=input("Введите слово: ")
xx=list(word.encode('ascii'))
print(xx)
for i in range(len(xx)):
    xx[i]=bin(xx[i])
print(xx)
str="11110"
for i in range(len(xx)):
    str=str+xx[i][3: ]
str=str+'1110'
print(str)
bin_arr=[int(num) for num in str]
plt.plot(bin_arr,drawstyle='steps-post')
plt.show()