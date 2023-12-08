import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import random

Conc_Bath_ACh = []
for i in range(9, 4, -1):
    Conc_Bath_ACh.append(1 * 10 ** (-i))
    Conc_Bath_ACh.append(3 * 10 ** (-i))

Conc_Bath = []
for i in range(9, 3, -1):
    Conc_Bath.append(1 * 10 ** (-i))
    Conc_Bath.append(3 * 10 ** (-i))

ACh = []
Atr_low = []
Atr_high = []
Pap = []

""" for test
# for i in range(10):
#     ACh.append(i*random.random())
# for i in range(12):
#     Atr_low.append(i*random.random())
#     Atr_high.append(i*random.random())
#     Pap.append(i*random.random())
"""

assert (len(Conc_Bath_ACh) == 10)
assert (len(Conc_Bath) == 12)
assert (len(ACh) == 10)
assert (len(Atr_low) == 12)
assert (len(Atr_high) == 12)
assert (len(Pap) == 12)

plt.plot(Conc_Bath_ACh, ACh, label="Ach")
plt.plot(Conc_Bath, Atr_low, label="Atr_low")
plt.plot(Conc_Bath, Atr_high, label="Atr_high")
plt.plot(Conc_Bath, Pap, label="Pap")
plt.xscale("log")
plt.legend()
plt.savefig("/Users/kotaro/Desktop/yakusaku.jpg", dpi=300)
plt.show()
