import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import random
from scipy.optimize import curve_fit
import sys
import decimal

Conc_Bath_ACh = []
for i in range(9, 4, -1):
    Conc_Bath_ACh.append(1 * 10 ** (-i))
    Conc_Bath_ACh.append(3 * 10 ** (-i))

Conc_Bath = []
for i in range(9, 3, -1):
    Conc_Bath.append(1 * 10 ** (-i))
    Conc_Bath.append(3 * 10 ** (-i))

ACh1 = [0.2, 0.4, 0.7, 0.9, 2.15, 4.4, 8.75, 11.2, 11.4, 11.4]
ACh2 = [0, 0, 0, 0.8, 4.3, 8.9, 11.6, 12.2, 12.8, 12.8]
Atr_low = [0, 0, 0, 0, 0, 0.1, 0.75, 4.45, 10.1, 12.45, 13.3, 13.4]
Atr_high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1.4, 10.2, 12.6]
Pap = [4.1, 1.15, 0.9, 0.8, 0.8, 0.8, 0.9, 1.15, 1.8, 1.95, 2.1, 2]

# """ for test """
# # for i in range(10):
# #     ACh1.append(i*random.random())
# #     ACh2.append(i * random.random())
# for i in range(12):
# #     Atr_low.append(i*random.random())
# #     Atr_high.append(i*random.random())
#     Pap.append(i*random.random())

ACh1 = np.array(ACh1)
ACh2 = np.array(ACh2)
Atr_low = np.array(Atr_low)
Atr_high = np.array(Atr_high)
Pap = np.array(Pap)

ACh2_max = max(ACh2)

ACh1 /= ACh2_max
ACh2 /= ACh2_max
Atr_low /= ACh2_max
Atr_high /= ACh2_max
Pap /= ACh2_max

ACh1 *= 100
ACh2 *= 100
Atr_low *= 100
Atr_high *= 100
Pap *= 100

assert (len(Conc_Bath_ACh) == 10)
assert (len(Conc_Bath) == 12)
assert (len(ACh1) == 10)
assert (len(ACh2) == 10)
assert (len(Atr_low) == 12)
assert (len(Atr_high) == 12)
assert (len(Pap) == 12)

plt.plot(Conc_Bath_ACh, ACh1, label="アセチルコリン1回目")
plt.plot(Conc_Bath_ACh, ACh2, label="アセチルコリン2回目")
plt.plot(Conc_Bath, Atr_low, label="低容量アトロピン")
plt.plot(Conc_Bath, Atr_high, label="高容量アトロピン")
plt.plot(Conc_Bath, Pap, label="パパベリン")
plt.title("アセチルコリンの濃度と収縮率の関係")
plt.xlabel("濃度(M)")
plt.xscale("log")
plt.ylabel("収縮率($\%$)")
plt.legend()
plt.savefig("/Users/kotaro/Desktop/yakusaku.jpg", dpi=300)
plt.show()
plt.close()

def f(x, a, b, c, EC50):
    return a + (b - a) / (1 + (EC50 / x) ** c)

def g(x,c,EC50):
    return  + (max() - min()) / (1 + (EC50 / x) ** c)

def f_ACh2(x, c, EC50):
    return min(ACh2) + (min(ACh2) - max(ACh2)) / (1 + (EC50 / x) ** c)

def f_Pap(x, c, EC50):
    return min(Pap) + (max(Pap) - min(Pap)) / (1 + (EC50 / x) ** c)


popt_ACh1, _ = curve_fit(f, Conc_Bath_ACh, ACh1)
popt_ACh1_g, _ = curve_fit(g, Conc_Bath_ACh, ACh1)
# popt_ACh2, _ = curve_fit(f_ACh2, Conc_Bath_ACh, ACh2)
popt_Atr_low, _ = curve_fit(f, Conc_Bath, Atr_low)
popt_Atr_high, _ = curve_fit(f, Conc_Bath, Atr_high)
# popt_Pap, _ = curve_fit(f_Pap, Conc_Bath, Pap)


x = np.linspace(10 ** -9, 10 ** -3, 1000)

a, b, c, EC50 = popt_ACh1

# 有効数字4桁指定
decimal.getcontext().prec = 2

a, b, c, EC50 = popt_ACh1
e,f = popt_ACh1_g
plt.plot(Conc_Bath_ACh, ACh1, label="アセチルコリン1回目")
plt.plot(x, f(x, a, b, c, EC50), label="近似曲線")
plt.title("アセチルコリンの濃度と収縮率の関係")
plt.xlabel("濃度(M)")
plt.xscale("log")
plt.ylabel("収縮率($\%$)")
a = decimal.Decimal(a)
b = decimal.Decimal(b)
c = decimal.Decimal(c)
EC50 = decimal.Decimal(EC50)
plt.text(1.0*10**-9,60, r'$y = {a} + \frac{{{b} - {a}}}{{1 + \left(\frac{{{EC50}}}{{x}}\right)^{{{c}}}}}$'.format(a=+a,b=+b,c=+c,EC50=+EC50))
plt.legend()
plt.tight_layout()
plt.savefig("/Users/kotaro/Desktop/yakusaku_ACh1.jpg", dpi=300)
plt.show()
plt.close()

# c, EC50 = popt_ACh2
# plt.plot(Conc_Bath_ACh, ACh2, label="アセチルコリン2回目")
# plt.plot(x, f_ACh2(x, c, EC50), label="近似曲線")
# plt.title("アセチルコリンの濃度と収縮率の関係")
# plt.xlabel("濃度(M)")
# plt.xscale("log")
# plt.ylabel("収縮率($\%$)")
# a = decimal.Decimal(a)
# b = decimal.Decimal(b)
# c = decimal.Decimal(c)
# EC50 = decimal.Decimal(EC50)
# plt.text(1.0*10**-9,60, r'$y = {a} + \frac{{{b} - {a}}}{{1 + \left(\frac{{{EC50}}}{{x}}\right)^{{{c}}}}}$'.format(a=+a,b=+b,c=+c,EC50=+EC50))
# plt.legend()
# plt.savefig("/Users/kotaro/Desktop/yakusaku_ACh2.jpg", dpi=300)
# plt.show()
# plt.close()

a, b, c, EC50 = popt_Atr_low
plt.plot(Conc_Bath, Atr_low, label="低容量アトロピン")
plt.plot(x, f(x, a, b, c, EC50), label="近似曲線")
plt.title("アセチルコリンの濃度と収縮率の関係")
plt.xlabel("濃度(M)")
plt.xscale("log")
plt.ylabel("収縮率($\%$)")
a = decimal.Decimal(a)
b = decimal.Decimal(b)
c = decimal.Decimal(c)
EC50 = decimal.Decimal(EC50)
plt.text(1.0*10**-9,60, r'$y = {a} + \frac{{{b} - {a}}}{{1 + \left(\frac{{{EC50}}}{{x}}\right)^{{{c}}}}}$'.format(a=+a,b=+b,c=+c,EC50=+EC50))
plt.legend()
plt.savefig("/Users/kotaro/Desktop/yakusaku_Atr_low.jpg", dpi=300)
plt.show()
plt.close()

a, b, c, EC50 = popt_Atr_high
plt.plot(Conc_Bath, Atr_high, label="高容量アトロピン")
plt.plot(x, f(x, a, b, c, EC50), label="近似曲線")
plt.title("アセチルコリンの濃度と収縮率の関係")
plt.xlabel("濃度(M)")
plt.xscale("log")
plt.ylabel("収縮率($\%$)")
a = decimal.Decimal(a)
b = decimal.Decimal(b)
c = decimal.Decimal(c)
EC50 = decimal.Decimal(EC50)
plt.text(1.0*10**-9,60, r'$y = {a} + \frac{{{b} - {a}}}{{1 + \left(\frac{{{EC50}}}{{x}}\right)^{{{c}}}}}$'.format(a=+a,b=+b,c=+c,EC50=+EC50))
plt.legend()
plt.savefig("/Users/kotaro/Desktop/yakusaku_popt_Atr_high.jpg", dpi=300)
plt.show()
plt.close()


# c, EC50 = popt_Pap
# plt.plot(Conc_Bath, Pap, label="パパベリン")
# plt.plot(x, f(x, a, b, c, EC50), label="近似曲線")
# plt.title("アセチルコリンの濃度と収縮率の関係")
# plt.xlabel("濃度(M)")
# plt.xscale("log")
# plt.ylabel("収縮率($\%$)")
# a = decimal.Decimal(a)
# b = decimal.Decimal(b)
# c = decimal.Decimal(c)
# EC50 = decimal.Decimal(EC50)
# plt.text(1.0*10**-9,60, r'$y = {a} + \frac{{{b} - {a}}}{{1 + \left(\frac{{{EC50}}}{{x}}\right)^{{{c}}}}}$'.format(a=+a,b=+b,c=+c,EC50=+EC50))
# plt.legend()
# plt.savefig("/Users/kotaro/Desktop/yakusaku_popt_Pap.jpg", dpi=300)
# plt.show()
# plt.close()
#
#
