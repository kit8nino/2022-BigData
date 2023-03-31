import matplotlib.pyplot as plt 
import numpy as np 

def to_UART(data: str):

    ARR = [list(format(x, "08b")) for x in bytearray(data, "utf-8")]
    _ARR = [[1,0] + [(int(x) for x in ELEMENT)] + [1,1,1,1] for ELEMENT in ARR]

    result = []

    for ELEMENT in ARR:
        result.extend(ELEMENT)
    return result

data = input()
x = to_UART(data)
print(x)
print(bytearray(data, "utf-8"))

plt.ylim([-0.5, 1.5])
plt.step(range(len(x)), x)

plt.show()