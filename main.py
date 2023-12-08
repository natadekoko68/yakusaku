import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import random
from scipy.optimize import curve_fit,leastsq
import sys
from decimal import Decimal, getcontext
import warnings
warnings.simplefilter("ignore")
getcontext().prec = 3

Shrinkages = {"ACh1":[0.2, 0.4, 0.7, 0.9, 2.15, 4.4, 8.75, 11.2, 11.4, 11.4],
             "ACh2":[0, 0, 0, 0.8, 4.3, 8.9, 11.6, 12.2, 12.8, 12.8],
             "Atr_low":[0, 0, 0, 0, 0, 0.1, 0.75, 4.45, 10.1, 12.45, 13.3, 13.4],
             "Atr_high":[0, 0, 0, 0, 0, 0, 0, 0, 0, 1.4, 10.2, 12.6],
             "Pap":[4.1, 1.15, 0.9, 0.8, 0.8, 0.8, 0.9, 1.15, 1.8, 1.95, 2.1, 2]
              }
Ctr_max = max(Shrinkages["ACh2"])

Conc_Bath_ACh = []
for i in range(9, 4, -1):
    Conc_Bath_ACh.append(1 * 10 ** (-i))
    Conc_Bath_ACh.append(3 * 10 ** (-i))

Conc_Bath = []
for i in range(9, 3, -1):
    Conc_Bath.append(1 * 10 ** (-i))
    Conc_Bath.append(3 * 10 ** (-i))

Concs = {"ACh1":Conc_Bath_ACh,
         "ACh2":Conc_Bath_ACh,
         "Atr_low":Conc_Bath,
         "Atr_high":Conc_Bath,
         "Pap":Conc_Bath
         }

for key in Shrinkages:
    Shrinkages[key] = np.array(Shrinkages[key],dtype=np.longdouble)/Ctr_max*100

#データの数の確認
sample_num = {"ACh1":10,
              "ACh2":10,
              "Atr_low":12,
              "Atr_high":12,
              "Pap":12
              }
for key in Shrinkages:
    assert(len(Shrinkages[key]) == sample_num[key])

labels = {"ACh1":"ACh 1回目",
          "ACh2":"ACh 2回目",
          "Atr_low":"Atropine(low)+Ach",
          "Atr_high":"Atropine(high)+Ach",
          "Pap":"Papaverine+Ach"
          }

samples = ["ACh1","ACh2","Atr_low","Atr_high","Pap"]

def graph_processing(img_name,output_path,title):
    plt.title("アセチルコリンの濃度と収縮率の関係"+title)
    plt.xlabel("濃度(M)")
    plt.xscale("log")
    plt.ylabel("収縮率($\%$)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path+img_name+".jpg", dpi=300)
    plt.show()
    plt.close()

def graph(lst,img_name,output_path="/Users/kotaro/Desktop/",title=""):
    for key in lst:
        plt.plot(Concs[key], Shrinkages[key], label=labels[key])
    graph_processing(img_name, output_path,title)

def graph_with_curve(key,img_name,output_path="/Users/kotaro/Desktop/",title=""):
    try:
        popt_temp, _ = curve_fit(lambda x, a, b, c, EC50: a + (b - a) / (1 + (EC50 / x) ** c), Concs[key], Shrinkages[key])
        x = np.linspace(min(Concs[key]), max(Concs[key]), 100000)
        a, b, c, EC50 = popt_temp
        temp_params = {"a":a,
                       "b":b,
                       "c":c,
                       "EC50":EC50}
    except RuntimeError:
        x = np.linspace(min(Concs[key]), max(Concs[key]), 100000)
        popt_temp, _ = curve_fit(lambda x, c, EC50: min(Shrinkages[key]) + (max(Shrinkages[key]) - min(Shrinkages[key])) / (1 + (EC50 / x) ** c), Concs[key], Shrinkages[key])
        c, EC50 = popt_temp
        temp_params = {"a":min(Shrinkages[key]),
                       "b":max(Shrinkages[key]),
                       "c":c,
                       "EC50":EC50}
    finally:
        plt.plot(x, temp_params["a"] + (temp_params["b"] - temp_params["a"]) / (1 + (temp_params["EC50"] / x) ** temp_params["c"]), label="近似曲線")
        for param in temp_params:
            temp_params[param] = Decimal(temp_params[param])
        if temp_params["a"] > 0:
            latex_formula = r'$y = {a} + \frac{{({b} - {a})}}{{1 + \left(\frac{{{EC50}}}{{x}} \right)^{{{c}}}}}$'.format(
                a=+temp_params["a"], b=+temp_params["b"], c=+temp_params["c"], EC50=+temp_params["EC50"])
        else:
            latex_formula = r'$y = - {a} + \frac{{({b} + {a})}}{{1 + \left(\frac{{{EC50}}}{{x}} \right)^{{{c}}}}}$'.format(
                a = Decimal(0)-temp_params["a"], b=+temp_params["b"], c=+temp_params["c"], EC50=+temp_params["EC50"])
        plt.text(10**-9,max(Shrinkages[key])*0.6, latex_formula)
        plt.plot(Concs[key], Shrinkages[key], label=labels[key])
        graph_processing(img_name, output_path,title=" ("+labels[key]+")")
        print(labels[key]+"の最適化パラメータ: ")
        for param in temp_params:
            print("\t{} = {}".format(param,+temp_params[param]))
        return None

graph(samples,"yakusaku",output_path="/Users/kotaro/Desktop/")
for key in samples:
    graph_with_curve(key, "yakusaku " + key)




