import time
import subprocess
import fileinput

kill_process = r"taskkill /im XVIIx64.exe /t /f"

files = ['inverter_size_8_sim']

step = 0.1
preferred_ratio = 1

for c in range(len(files)):
    start_process = r".\XVIIx64.exe -run .\{}.spi".format(files[c])

    spi_file = open(files[c] + '.spi')
    lines = spi_file.readlines()
    
    n_original_width_line = "Mnmos@0 F A gnd gnd N L=0.2U W=3.2U"
    p_original_width_line = "Mpmos@0 vdd A F vdd P L=0.2U W=7.8U"
    

    for line in lines:
        if 'Mpmos@0' in line:
            line = line.replace(line, p_original_width_line + '\n')
            pmos_width = p_original_width_line.split("W=",1)[1] 
            pmos_width = pmos_width.split("U",1)[0] 
            pmos_width = float(pmos_width)
            print ('pmos_width = ', pmos_width)

        elif 'Mnmos@0' in line:
            line = line.replace(line, n_original_width_line + '\n')
            nmos_width = n_original_width_line.split("W=",1)[1] 
            nmos_width = nmos_width.split("U",1)[0] 
            nmos_width = float(nmos_width)
            print ('nmos_width = ', nmos_width)

    spi_file.close()
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
        n_replacing_line = n_original_width_line
        while (tpdr / tpdf) > preferred_ratio:
            
            pmos_width += step
            p_replacing_line = "Mpmos@0 vdd A F vdd P L=0.2U W=" + "{:g}".format(pmos_width) + "U\n"
            

            
            if (nmos_width - step) > 0.4:
                nmos_width -= step
                n_replacing_line = "Mnmos@0 F A gnd gnd N L=0.2U W=" + "{:g}".format(nmos_width) + "U\n"
                
            

            for line in fileinput.FileInput(files[c] + ".spi", inplace=1):
                line = line.replace(p_original_width_line, p_replacing_line)
                line = line.replace(n_original_width_line, n_replacing_line)
                print(line, end='')
            p_original_width_line = p_replacing_line
            n_original_width_line = n_replacing_line

            time.sleep(1)
            open_process = subprocess.Popen(start_process, stdout=subprocess.PIPE,shell=True)  # run spice process
            time.sleep(2)
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
        p_replacing_line = p_original_width_line
        while (tpdr / tpdf) < preferred_ratio:
            print('(tpdr / tpdf) = ', (tpdr / tpdf))
            nmos_width += step
            n_replacing_line = "Mnmos@0 F A gnd gnd N L=0.2U W=" + "{:g}".format(nmos_width) + "U\n"
            print(n_replacing_line)

            
            if (pmos_width - step) > 1:
                pmos_width -= step
                p_replacing_line = "Mpmos@0 vdd A F vdd P L=0.2U W=" + "{:g}".format(pmos_width) + "U\n"
                print(p_replacing_line)
                
            

            for line in fileinput.FileInput(files[c] + ".spi", inplace=1):
                line = line.replace(p_original_width_line, p_replacing_line)
                line = line.replace(n_original_width_line, n_replacing_line)
                print(line, end='')
            p_original_width_line = p_replacing_line
            n_original_width_line = n_replacing_line

            #time.sleep(1)
            open_process = subprocess.Popen(start_process, stdout=subprocess.PIPE,shell=True)  # run spice process
            time.sleep(1)
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