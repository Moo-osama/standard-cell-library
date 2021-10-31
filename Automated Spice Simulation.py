import time
import subprocess
import fileinput

kill_process = r"taskkill /im XVIIx64.exe /t /f"

files = ['compx_func_4_size_4_sim']


for c in range(len(files)):
    start_process = r".\XVIIx64.exe -run .\{}.spi".format(files[c])

    pulse_original_command = "vin a 0 DC pulse 0 1.8 0.1n 0.00001f 0.00001f 5n 10n\n"
    cload_original_command= "cload f 0 9fF\n"

    
    cinv=[133.0440, 266.088, 532.176, 1064.352]   #assumed the cinv to be 100fF
    time_values = [0,125,500,1000]
    

    file_name = files[c] + '_timing_results.txt'
    resultfilehandle = open(file_name, "w")  #this is for the result file

    print("\n" + files[c] + " values:")

    n_time_values = len(time_values)
    n_cinv = len(cinv)
    for i in range(n_time_values):

        pulse_replacing_command = "vin a 0 DC pulse 0 1.8 0.1n " + str(time_values[i]) + "p " + str(time_values[i]) + "p 5n 10n\n"
        print(pulse_replacing_command)
        for line in fileinput.FileInput(files[c] + ".spi", inplace=1):
            line = line.replace(pulse_original_command, pulse_replacing_command)
            print(line, end='')
        pulse_original_command = pulse_replacing_command
        for j in range(n_cinv):
            replacment_string_cload = "cload f 0 " + str(cinv[j]) + "fF\n"
            for line in fileinput.FileInput(files[c] + ".spi", inplace=1):
                line = line.replace(cload_original_command,replacment_string_cload)  # replace the initial value with the new one
                print(line, end='')
            cload_original_command = replacment_string_cload
            if (i < n_time_values and j < n_cinv):
                time.sleep(1)
                open_process = subprocess.Popen(start_process, stdout=subprocess.PIPE,shell=True)  # run spice process
                time.sleep(2)
                kill_process_flag = subprocess.Popen(kill_process, stdout=subprocess.PIPE,shell=True)  # kill the process created
                logfile = open(files[c] + ".log", "r")  # Getting tpdr, tpdf from the created log file

                resultfilehandle.write("\nValues for capacitance: " + str(cinv[j]) + "fF, time: " + str(time_values[i]) + "ps.\n")

                contents = logfile.readlines()

                for line in contents:
                    if "tpdr" in line:
                        string = line.partition("FROM")[0] + "\n"
                        resultfilehandle.write(string)
                        print(line.partition("FROM")[0])       
                    if "tpdf" in line:
                        string = line.partition("FROM")[0] + "\n ______________________________________________ \n"
                        resultfilehandle.write(string)
                        print(line.partition("FROM")[0]) 

                logfile.close()

    resultfilehandle.close()