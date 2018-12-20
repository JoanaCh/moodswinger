from os import listdir
from os.path import isfile, join
import random 
local = "D:\\Documents\\DIIC\\csv"

ficheiros = [f for f in listdir(local) if isfile(join(local, f))]
ficheiros.pop(-1)

append_list = []

for i in ficheiros:
    with open(i, "r") as file:
        x = file.readlines()
    x.pop(0)
    for v in (x):
        append_list.append(v)



print(append_list[1].strip())
exit(1)

with open("final.csv", "w") as final:
    final.write("theta_mean,theta_median,theta_std,theta_var,theta_fft,alpha_low_mean,alpha_low_median,alpha_low_std,alpha_low_var,alpha_low_fft,alpha_high_mean,alpha_high_median,alpha_high_std,alpha_high_var,alpha_high_fft,beta_mean,beta_median,beta_std,beta_var,beta_fft,gamma_mean,gamma_median,gamma_std,gamma_var,gamma_fft,state\n")
    for _ in range(len(append_list)):
        final.write(append_list.pop())
        random.shuffle(append_list)
        
            


