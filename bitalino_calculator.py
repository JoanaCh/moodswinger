import numpy as np

from biosppy import storage
from biosppy.signals import eeg

moods = ["bored", "calm","frustrated"]
valores_modificados = []


def eeg_calc(valor):
    return (((valor / 2 ** 10) - (1/2)) * 3.3) / 40000

def converter():
    q = ""
    while q != "exit":
        q = input("diga o id: ")
        for a in moods:    
            with open ("C:\\Users\\ric_j\\moodswinger\\user_tests\\"+ q +"\\"+ a +".txt", "r") as file:
                valores_modificados = []
                l = False
                for i in file.readlines():
                    if l:
                        y = int(i.split()[5])
                        valores_modificados.append(eeg_calc(y))
                        #exit(1)
                        continue

                    if i.endswith("EndOfHeader\n"):
                        l = True


            with open("C:\\Users\\ric_j\\moodswinger\\user_tests\\"+ q +"\\"+ a +"_eeg_values.txt", "w") as file:
                for i in valores_modificados:
                    file.write(str(i) + "\n")


signal, mdata = storage.load_txt("C:\\Users\\ric_j\\moodswinger\\user_tests\\1\\calm_eeg_values.txt")
signal = signal[:, np.newaxis]
#signal= numpy.loadtxt("C:\\Users\\ric_j\\moodswinger\\user_tests\\1\\calm_eeg_values.txt")
print(mdata)
out = eeg.eeg(signal = signal, sampling_rate = 1000., show=False, name_to_file="calm_eeg_values")
print(out)