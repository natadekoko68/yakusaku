# libraries
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy.optimize import curve_fit
from decimal import Decimal, getcontext
import warnings

warnings.simplefilter("ignore")
getcontext().prec = 3

""" output
ACh 1回目の最適化パラメータ: 
	a = 3.79
	b = 91.0
	c = 1.32
	EC50 = 4.47E-7
ACh 2回目の最適化パラメータ: 
	a = 0
	b = 100
	c = 1.39
	EC50 = 1.69E-7
Atropine(low)+Achの最適化パラメータ: 
	a = -0.356
	b = 104
	c = 1.56
	EC50 = 0.00000479
Atropine(high)+Achの最適化パラメータ: 
	a = -0.0538
	b = 99.4
	c = 2.90
	EC50 = 0.0000617
Papaverine+Achの最適化パラメータ: 
	a = 10.4
	b = 15.8
	c = 13.9
	EC50 = 0.00000945
"""

#input
Shrinkages = {"ACh1": [0.2, 0.4, 0.7, 0.9, 2.15, 4.4, 8.75, 11.2, 11.4, 11.4],
              "ACh2": [0, 0, 0, 0.8, 4.3, 8.9, 11.6, 12.2, 12.8, 12.8],
              "Atr_low": [0, 0, 0, 0, 0, 0.1, 0.75, 4.45, 10.1, 12.45, 13.3, 13.4],
              "Atr_high": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1.4, 10.2, 12.6],
              "Pap": [4.1, 1.15, 0.9, 0.8, 0.8, 0.8, 0.9, 1.15, 1.8, 1.95, 2.1, 2]
              }

#internal processing
Ctr_max = max(Shrinkages["ACh2"])

Conc_Bath_ACh = [j * 10 ** (-i) for i in range(9, 4, -1) for j in [1, 3]]
Conc_Bath = [j * 10 ** (-i) for i in range(9, 3, -1) for j in [1, 3]]

Concs = {"ACh1": Conc_Bath_ACh,
         "ACh2": Conc_Bath_ACh,
         "Atr_low": Conc_Bath,
         "Atr_high": Conc_Bath,
         "Pap": Conc_Bath
         }

for key in Shrinkages:
    Shrinkages[key] = np.array(Shrinkages[key], dtype=np.longdouble) / Ctr_max * 100

labels = {"ACh1": "ACh 1回目",
          "ACh2": "ACh 2回目",
          "Atr_low": "Atropine(low)+Ach",
          "Atr_high": "Atropine(high)+Ach",
          "Pap": "Papaverine+Ach"
          }

samples = ["ACh1", "ACh2", "Atr_low", "Atr_high", "Pap"]

# confirm input
sample_num = {"ACh1": 10, "ACh2": 10, "Atr_low": 12, "Atr_high": 12, "Pap": 12}
for key in Shrinkages:
    assert (len(Shrinkages[key]) == sample_num[key])

# graph
def graph_processing(img_name, output_path, title):
    plt.title("用量作用曲線" + title)
    plt.xlabel("Bath内ACh最終濃度(M)")
    plt.xscale("log")
    plt.ylabel("収縮率($\%$)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path + img_name + ".jpg", dpi=300)
    plt.show()
    plt.close()


def graph_by_list(lst, img_name, output_path="/Users/kotaro/Desktop/", title=""):
    for key in lst:
        plt.plot(Concs[key], Shrinkages[key], label=labels[key])
    graph_processing(img_name, output_path, title)


def graph_with_curve(key, img_name, output_path="/Users/kotaro/Desktop/", title=""):
    try:
        popt_temp, _ = curve_fit(lambda x, a, b, c, EC50: a + (b - a) / (1 + (EC50 / x) ** c), Concs[key],
                                 Shrinkages[key])
        x = np.logspace(np.log10(min(Concs[key])), np.log10(max(Concs[key])), 100)
        a, b, c, EC50 = popt_temp
        temp_params = {"a": a,
                       "b": b,
                       "c": c,
                       "EC50": EC50}
    except RuntimeError:
        x = np.logspace(np.log10(min(Concs[key])), np.log10(max(Concs[key])), 100)
        popt_temp, _ = curve_fit(
            lambda x, c, EC50: min(Shrinkages[key]) + (max(Shrinkages[key]) - min(Shrinkages[key])) / (
                        1 + (EC50 / x) ** c), Concs[key], Shrinkages[key])
        c, EC50 = popt_temp
        temp_params = {"a": min(Shrinkages[key]),
                       "b": max(Shrinkages[key]),
                       "c": c,
                       "EC50": EC50}
    finally:
        plt.plot(x, temp_params["a"] + (temp_params["b"] - temp_params["a"]) / (
                    1 + (temp_params["EC50"] / x) ** temp_params["c"]), label="近似曲線")
        for param in temp_params:
            temp_params[param] = Decimal(temp_params[param])
        if min(Shrinkages[key]) > 0:
            latex_formula = r'$y = {a} + \frac{{({b} - {a})}}{{1 + \left(\frac{{{EC50}}}{{x}} \right)^{{{c}}}}}$'.format(
                a=+temp_params["a"], b=+temp_params["b"], c=+temp_params["c"], EC50=+temp_params["EC50"])
        else:
            latex_formula = r'$y = {a} + \frac{{({b} - ({a}))}}{{1 + \left(\frac{{{EC50}}}{{x}} \right)^{{{c}}}}}$'.format(
                a=+temp_params["a"], b=+temp_params["b"], c=+temp_params["c"], EC50=+temp_params["EC50"])
        if max(Shrinkages[key]) > 80:
            plt.text(EC50*0.3, 50, latex_formula, horizontalalignment="right")
        else:
            plt.text(10**-9, max(Shrinkages[key])*0.7, latex_formula, horizontalalignment="left")
        plt.plot(Concs[key], Shrinkages[key], label=labels[key])
        graph_processing(img_name, output_path, title=" (" + labels[key] + ")")
        print(labels[key] + "の最適化パラメータ: ")
        for param in temp_params:
            print("\t{} = {}".format(param, +temp_params[param]))
        return None

def main():
    graph_by_list(samples, "yakusaku", output_path="")
    for key in samples:
        graph_with_curve(key, "yakusaku " + key, output_path="")


if __name__ == '__main__':
    main()

