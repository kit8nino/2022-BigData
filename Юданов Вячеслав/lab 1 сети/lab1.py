import matplotlib.pyplot as plt

def to_ascii(msg):
    return list(msg.encode('ascii'))

def to_binary(msg):
    binary = []
    for i in msg:
        binary.append(bin(i))
    return binary

msg = 'привет мир!'
binary = to_binary(to_ascii(msg))

bin_str = "1110"
for i in binary:
    tmp = str(i[2:])
    while len(tmp) < 8:
        tmp = "0" + tmp
    bin_str += tmp
bin_str += "1111"

bin_arr = [int(num) for num in bin_str]

plt.plot(bin_arr, drawstyle='steps-post')
plt.show()