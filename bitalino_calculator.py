import numpy as np
import csv
from biosppy import storage
from biosppy.signals import eeg

np.set_printoptions(threshold=np.nan)

moods = ["bored", "calm","frustrated"]

def eeg_calc(valor):
    return (((valor / 2 ** 10) - (1/2)) * 3.3) / 40000

def converter(iid):
    valores_modificados = []
    locais_ficheiros = []
    q = iid
    
    for a in moods:    
        with open ("D:\\Documents\\DIIC\\user_tests\\"+ q +"\\"+ a +".txt", "r") as file:
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

        local = "D:\\Documents\\DIIC\\user_tests\\"+ q +"\\"+ a +"_eeg_values.txt"
        locais_ficheiros.append([local, q, a]) #a = mood q = id
        with open(local, "w") as file:
            for i in valores_modificados: 
                file.write(str(i) + "\n")

    return locais_ficheiros

def get_info(local_ficheiro ,idd , mood):
    signal, mdata = storage.load_txt(local_ficheiro)
    signal = signal[:, np.newaxis]
    out = eeg.eeg(signal = signal, sampling_rate = 1000., show=False, name_to_file="D:\\Documents\\DIIC\\user_tests\\"+ idd +"\\"+ mood +"_eeg_")
    return out

def create_individual_csv(info, time_in_secs,name, id_number):
    len_file = int(info[0])
    current_lines = 0
    creating_csv = {}
    fieldnames = []

    for key,values in info[1].items():
        creating_csv[key] = {}
        fieldnames.append(key)

        var = []
        std = []
        median = []
        mean = []
        fft = []

        current_lines = 0
        num_lines = (2 * float(len_file)) / float(time_in_secs)
        num_lines = int(num_lines)

        while current_lines != len_file:
            data_array = []
            if (current_lines + num_lines >= len_file):
                num_lines = len_file - current_lines
            
            for x in values[current_lines:current_lines + num_lines]:
                data_array.append(x)
            mean.append(np.mean(data_array))
            median.append(np.median(data_array))
            std.append(np.std(data_array))
            var.append(np.var(data_array))

            array_fft = []
            for v in data_array:
                numero = str(v)[1]
                numero = int(numero)
                if 2 <= numero <= 3:
                    array_fft.append(v)


            
            fft.append(np.sum(np.fft.fft(v)))

            current_lines = current_lines + num_lines


        creating_csv[key]["mean"] = mean
        creating_csv[key]["median"] = median
        creating_csv[key]["std"] = std
        creating_csv[key]["var"] = var
        creating_csv[key]["fft"] = fft



    #creating the CSV
    #print(creating_csv)

    leng = len(creating_csv[key]["mean"])
    with open(name +"_"+ id_number + '.csv', 'w') as csvfile:
        
        fieldnames = ['theta_mean',
                      'theta_median',
                      'theta_std',
                      'theta_var',
                      'theta_fft',
                      'alpha_low_mean',
                      'alpha_low_median',
                      'alpha_low_std',
                      'alpha_low_var',
                      'alpha_low_fft',
                      'alpha_high_mean',
                      'alpha_high_median',
                      'alpha_high_std',
                      'alpha_high_var',
                      'alpha_high_fft',
                      'beta_mean',
                      'beta_median',
                      'beta_std',
                      'beta_var',
                      'beta_fft',
                      'gamma_mean',
                      'gamma_median',
                      'gamma_std',
                      'gamma_var',
                      'gamma_fft',
                      'state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(leng):
            writer.writerow({'theta_mean': creating_csv["theta"]["mean"][i],
                             'theta_median': creating_csv["theta"]["median"][i],
                             'theta_std' : creating_csv["theta"]["std"][i],
                             'theta_var' : creating_csv["theta"]["var"][i],
                             'theta_fft' : creating_csv["theta"]["fft"][i],
                             'alpha_low_mean' : creating_csv["alpha_low"]["mean"][i],
                             'alpha_low_median' : creating_csv["alpha_low"]["median"][i],
                             'alpha_low_std' : creating_csv["alpha_low"]["std"][i],
                             'alpha_low_var' : creating_csv["alpha_low"]["var"][i],
                             'alpha_low_fft' : creating_csv["alpha_low"]["fft"][i],
                             'alpha_high_mean' : creating_csv["alpha_high"]["mean"][i],
                             'alpha_high_median' : creating_csv["alpha_high"]["median"][i],
                             'alpha_high_std' : creating_csv["alpha_high"]["std"][i],
                             'alpha_high_var' : creating_csv["alpha_high"]["var"][i],
                             'alpha_high_fft' : creating_csv["alpha_high"]["fft"][i],
                             'beta_mean' : creating_csv["beta"]["mean"][i],
                             'beta_median' : creating_csv["beta"]["median"][i],
                             'beta_std' : creating_csv["beta"]["std"][i],
                             'beta_var' : creating_csv["beta"]["var"][i],
                             'beta_fft' : creating_csv["beta"]["fft"][i],
                             'gamma_mean' : creating_csv["gamma"]["mean"][i],
                             'gamma_median' : creating_csv["gamma"]["median"][i],
                             'gamma_std' : creating_csv["gamma"]["std"][i],
                             'gamma_var' : creating_csv["gamma"]["var"][i],
                             'gamma_fft' : creating_csv["gamma"]["fft"][i],
                             'state' : name})
        
        #writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        #writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})



while True:
    b = input("id: ")
    if b == "exit":
        break

    data = b.split()
    #DESCOMENTAR DEPOIS
    ficheiros = converter(data[0])

    bored_calculus = get_info(ficheiros[0][0], ficheiros[0][1] ,ficheiros[0][2])
    calm_calculus = get_info(ficheiros[1][0], ficheiros[1][1] ,ficheiros[1][2])
    frustrated_calculus = get_info(ficheiros[2][0], ficheiros[2][1] ,ficheiros[2][2])

    # calm  : 120 segundos
    # bored : 240 segundos
    # frust : 240 segundos


    #teste = [2645
    # ,["D:\\Documents\\DIIC\\user_tests\\1\\bored_eeg_alpha_high.txt",
    # "D:\\Documents\\DIIC\\user_tests\\1\\bored_eeg_alpha_low.txt",
    # "D:\\Documents\\DIIC\\user_tests\\1\\bored_eeg_beta.txt",
    # "D:\\Documents\\DIIC\\user_tests\\1\\bored_eeg_gamma.txt",
    # "D:\\Documents\\DIIC\\user_tests\\1\\bored_eeg_theta.txt"]]
    #create_individual_csv(teste, data[1])
    
    create_individual_csv(bored_calculus, 120, "bored", data[0])
    create_individual_csv(calm_calculus, 240, "calm", data[0])
    create_individual_csv(frustrated_calculus, 240, "frustrated", data[0])
        

    #print(calculos1)
    #print(calculos1)
