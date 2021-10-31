import time
import subprocess
import fileinput

kill_process = r"taskkill /im XVIIx64.exe /t /f"

files = ['compx_func_4_size_2_sim']

step = 0.1
preferred_ratio = 1

pre_process_sleep = 1
process_sleep = 2

for c in range(len(files)):
    start_process = r".\XVIIx64.exe -run .\{}.spi".format(files[c])

    n_original_width_line_0 = "Mnmos@0 f w net@0 gnd N L=0.2U W=1.6U"
    n_original_width_line_1 = "Mnmos@1 net@0 z gnd gnd N L=0.2U W=1.6U"
    n_original_width_line_2 = "Mnmos@2 f x net@38 gnd N L=0.2U W=1.6U"
    n_original_width_line_3 = "Mnmos@3 net@38 y gnd gnd N L=0.2U W=1.6U"


    p_original_width_line_0 = "Mpmos@0 vdd w net@2 vdd P L=0.2U W=4U"
    p_original_width_line_1 = "Mpmos@1 vdd z net@2 vdd P L=0.2U W=4U"
    p_original_width_line_2 = "Mpmos@2 net@2 x f vdd P L=0.2U W=4U"
    p_original_width_line_3 = "Mpmos@3 net@2 y f vdd P L=0.2U W=4U"

    nmos_width = n_original_width_line_0.split("W=",1)[1] 
    nmos_width = nmos_width.split("U",1)[0] 
    nmos_width = float(nmos_width)

    pmos_width = p_original_width_line_0.split("W=",1)[1] 
    pmos_width = pmos_width.split("U",1)[0] 
    pmos_width = float(pmos_width)

    print ('pmos_width = ', pmos_width)
    print ('nmos_width = ', nmos_width)

    n_original_width_line_0_partitions = n_original_width_line_0.partition("W=")
    n_original_width_line_1_partitions = n_original_width_line_1.partition("W=")
    n_original_width_line_2_partitions = n_original_width_line_2.partition("W=")
    n_original_width_line_3_partitions = n_original_width_line_3.partition("W=")

    p_original_width_line_0_partitions = p_original_width_line_0.partition("W=")
    p_original_width_line_1_partitions = p_original_width_line_1.partition("W=")
    p_original_width_line_2_partitions = p_original_width_line_2.partition("W=")
    p_original_width_line_3_partitions = p_original_width_line_3.partition("W=")

    
    
            
    
    #p_original_width_line = "Mpmos@0 vdd A F vdd P L=0.2U W=2U"
    #n_original_width_line = "Mnmos@0 F A gnd gnd N L=0.2U W=0.8U"
    log_file = open(files[c] + '.log')
    lines = log_file.readlines()

    
    result_file = open(files[c] + '_sizing_results' + '.txt', 'w')
    result_file.truncate(0)
    result_file.write("Trying out PMOS size = " + "{:g}".format(pmos_width) + " and NMOS size = " + "{:g}".format(nmos_width) + '\n')

    for line in lines:
        if 'tpdr=' in line:
            tpdr = line.split("=",1)[1] 
            tpdr = tpdr.split(' ')[0]
            tpdr = float(tpdr)
            print('tpdr = ',tpdr)

        elif 'tpdf=' in line:
            tpdf = line.split("=",1)[1] 
            tpdf = tpdf.split(' ')[0]
            tpdf = float(tpdf)
            print('tpdf = ',tpdf)
    print('(tpdr / tpdf) = ', (tpdr / tpdf))
    print()
    

    log_file.close()

    result_file.write("Obtained: \n")
    result_file.write("tpdr = " + "{:g}".format(tpdr) + '\n')
    result_file.write("tpdf = " + "{:g}".format(tpdf) + '\n')
    result_file.write("tpdr/tpdf = " + "{:g}".format(tpdr/tpdf) + '\n')
    result_file.write("----------------------------------------------------------------------\n")


    if (tpdr / tpdf) > preferred_ratio:
        while (tpdr / tpdf) > preferred_ratio:
            
            pmos_width += step

            p_replacing_line_0 = p_original_width_line_0_partitions[0] + p_original_width_line_0_partitions[1] + "{:g}".format(pmos_width) + "U\n"
            p_replacing_line_1 = p_original_width_line_1_partitions[0] + p_original_width_line_1_partitions[1] + "{:g}".format(pmos_width) + "U\n"
            p_replacing_line_2 = p_original_width_line_2_partitions[0] + p_original_width_line_2_partitions[1] + "{:g}".format(pmos_width) + "U\n"
            p_replacing_line_3 = p_original_width_line_3_partitions[0] + p_original_width_line_3_partitions[1] + "{:g}".format(pmos_width) + "U\n"
            
            #if (nmos_width - step) > 0.4:
            #    nmos_width -= step

            n_replacing_line_0 = n_original_width_line_0_partitions[0] + n_original_width_line_0_partitions[1] + "{:g}".format(nmos_width) + "U\n"
            n_replacing_line_1 = n_original_width_line_1_partitions[0] + n_original_width_line_1_partitions[1]  + "{:g}".format(nmos_width) + "U\n"
            n_replacing_line_2 = n_original_width_line_2_partitions[0] + n_original_width_line_2_partitions[1]  + "{:g}".format(nmos_width) + "U\n"
            n_replacing_line_3 = n_original_width_line_3_partitions[0] + n_original_width_line_3_partitions[1]  + "{:g}".format(nmos_width) + "U\n"
                
            print ('nmos_width = ', nmos_width)
            print ('pmos_width = ', pmos_width)
            

            for line in fileinput.FileInput(files[c] + ".spi", inplace=1):
                line = line.replace(n_original_width_line_0, n_replacing_line_0)
                line = line.replace(n_original_width_line_1, n_replacing_line_1)
                line = line.replace(n_original_width_line_2, n_replacing_line_2)
                line = line.replace(n_original_width_line_3, n_replacing_line_3)

                line = line.replace(p_original_width_line_0, p_replacing_line_0)
                line = line.replace(p_original_width_line_1, p_replacing_line_1)
                line = line.replace(p_original_width_line_2, p_replacing_line_2)
                line = line.replace(p_original_width_line_3, p_replacing_line_3)
                
                print(line, end='')
            p_original_width_line_0 = p_replacing_line_0
            p_original_width_line_1 = p_replacing_line_1
            p_original_width_line_2 = p_replacing_line_2
            p_original_width_line_3 = p_replacing_line_3
            
            n_original_width_line_0 = n_replacing_line_0
            n_original_width_line_1 = n_replacing_line_1
            n_original_width_line_2 = n_replacing_line_2
            n_original_width_line_3 = n_replacing_line_3

            time.sleep(pre_process_sleep)
            open_process = subprocess.Popen(start_process, stdout=subprocess.PIPE,shell=True)  # run spice process
            time.sleep(process_sleep)
            kill_process_flag = subprocess.Popen(kill_process, stdout=subprocess.PIPE,shell=True)  # kill the process created

            log_file = open(files[c] + '.log')
            lines = log_file.readlines()

            for line in lines:
                if 'tpdr=' in line:
                    tpdr = line.split("=",1)[1] 
                    tpdr = tpdr.split(' ')[0]
                    tpdr = float(tpdr)
                    print('tpdr = ',tpdr)

                elif 'tpdf=' in line:
                    tpdf = line.split("=",1)[1] 
                    tpdf = tpdf.split(' ')[0]
                    tpdf = float(tpdf)
                    print('tpdf = ',tpdf)

            print('(tpdr / tpdf) = ', (tpdr / tpdf))
            print()

            log_file.close()

            result_file.write("Trying out PMOS size = " + "{:g}".format(pmos_width) + " and NMOS size = " + "{:g}".format(nmos_width) + '\n')
            result_file.write("Obtained: \n")
            result_file.write("tpdr = " + "{:g}".format(tpdr) + '\n')
            result_file.write("tpdf = " + "{:g}".format(tpdf) + '\n')
            result_file.write("tpdr/tpdf = " + "{:g}".format(tpdr/tpdf) + '\n')
            result_file.write("----------------------------------------------------------------------\n")
        
    else:
        while (tpdr / tpdf) < preferred_ratio:
            print('(tpdr / tpdf) = ', (tpdr / tpdf))
            nmos_width += step
            n_replacing_line_0 = n_original_width_line_0_partitions[0] + n_original_width_line_0_partitions[1] + "{:g}".format(nmos_width) + "U\n"
            n_replacing_line_1 = n_original_width_line_1_partitions[0] + n_original_width_line_1_partitions[1]  + "{:g}".format(nmos_width) + "U\n"
            n_replacing_line_2 = n_original_width_line_2_partitions[0] + n_original_width_line_2_partitions[1]  + "{:g}".format(nmos_width) + "U\n"
            n_replacing_line_3 = n_original_width_line_3_partitions[0] + n_original_width_line_3_partitions[1]  + "{:g}".format(nmos_width) + "U\n"
            
            #if (pmos_width - step) > 1:
            #    pmos_width -= step

            p_replacing_line_0 = p_original_width_line_0_partitions[0] + p_original_width_line_0_partitions[1] + "{:g}".format(pmos_width) + "U\n"
            p_replacing_line_1 = p_original_width_line_1_partitions[0] + p_original_width_line_1_partitions[1] + "{:g}".format(pmos_width) + "U\n"
            p_replacing_line_2 = p_original_width_line_2_partitions[0] + p_original_width_line_2_partitions[1] + "{:g}".format(pmos_width) + "U\n"
            p_replacing_line_3 = p_original_width_line_3_partitions[0] + p_original_width_line_3_partitions[1] + "{:g}".format(pmos_width) + "U\n"
                
            print ('nmos_width = ', nmos_width)
            print ('pmos_width = ', pmos_width)

            for line in fileinput.FileInput(files[c] + ".spi", inplace=1):
                line = line.replace(n_original_width_line_0, n_replacing_line_0)
                line = line.replace(n_original_width_line_1, n_replacing_line_1)
                line = line.replace(n_original_width_line_2, n_replacing_line_2)
                line = line.replace(n_original_width_line_3, n_replacing_line_3)

                line = line.replace(p_original_width_line_0, p_replacing_line_0)
                line = line.replace(p_original_width_line_1, p_replacing_line_1)
                line = line.replace(p_original_width_line_2, p_replacing_line_2)
                line = line.replace(p_original_width_line_3, p_replacing_line_3)
                print(line, end='')

            p_original_width_line_0 = p_replacing_line_0
            p_original_width_line_1 = p_replacing_line_1
            p_original_width_line_2 = p_replacing_line_2
            p_original_width_line_3 = p_replacing_line_3
            
            n_original_width_line_0 = n_replacing_line_0
            n_original_width_line_1 = n_replacing_line_1
            n_original_width_line_2 = n_replacing_line_2
            n_original_width_line_3 = n_replacing_line_3

            time.sleep(pre_process_sleep)
            open_process = subprocess.Popen(start_process, stdout=subprocess.PIPE,shell=True)  # run spice process
            time.sleep(process_sleep)
            kill_process_flag = subprocess.Popen(kill_process, stdout=subprocess.PIPE,shell=True)  # kill the process created

            log_file = open(files[c] + '.log')
            lines = log_file.readlines()

            for line in lines:
                if 'tpdr=' in line:
                    tpdr = line.split("=",1)[1] 
                    tpdr = tpdr.split(' ')[0]
                    tpdr = float(tpdr)
                    print('tpdr = ',tpdr)

                elif 'tpdf=' in line:
                    tpdf = line.split("=",1)[1] 
                    tpdf = tpdf.split(' ')[0]
                    tpdf = float(tpdf)
                    print('tpdf = ',tpdf)

            print('(tpdr / tpdf) = ', (tpdr / tpdf))
            print()

            log_file.close()
            result_file.write("Trying out PMOS size = " + "{:g}".format(pmos_width) + " and NMOS size = " + "{:g}".format(nmos_width) + '\n')
            result_file.write("Obtained: \n")
            result_file.write("tpdr = " + "{:g}".format(tpdr) + '\n')
            result_file.write("tpdf = " + "{:g}".format(tpdf) + '\n')
            result_file.write("tpdr/tpdf = " + "{:g}".format(tpdr/tpdf) + '\n')
            result_file.write("----------------------------------------------------------------------\n")
    
    result_file.close()