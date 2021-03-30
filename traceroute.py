import argparse
import subprocess
import time
import sys
import os
import json
import statistics

def parse_args():
    parser = argparse.ArgumentParser(description=' Run traceroute multiple times towards a given target host')
    parser.add_argument('-n', help= 'Number of times traceroute will run', dest = 'NUM_RUNS' , type=int,default=2)
    parser.add_argument('-d', help= 'Number of seconds to wait between two consecutive runs', dest = 'RUN_DELAY', type= int, default = 2)
    parser.add_argument('-m', help= 'Max number of hops that traceroute will probe', dest = 'MAX_HOPS', type=str, default = '30')
    parser.add_argument('-o', help= 'Path and name (without extension) of the .json output file', dest = 'OUTPUT', type= str, default='traceroute_output')
    parser.add_argument('-t', help= 'A target domain name or IP address', dest= 'TARGET', type = str, default= 'www.google.com')
    parser.add_argument('--test', help= 'Directory containing num_runs text files, each of which contains the output of a traceroute run. If present, this will override all other options and traceroute will not be invoked. Statistics will be computed over the traceroute output stored in the text files only.', dest= 'TEST_DIR', type= str, default ='test_dir')
    args = parser.parse_args()
    return args

def create_directory():
    args = parse_args()
    test_folder = sys.path[0] +'/'+ args.TEST_DIR
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    os.chdir(test_folder)
    return test_folder

def save_result_in_txt():
    args = parse_args()
    total = 0
    names = []

    for i in range(args.NUM_RUNS):
        total += i+1   #calculate the sum
        filename = f'{i+1}.txt'
        names.append(filename)
        with open(filename, 'w') as f:  #simplified grammer by using "with", it automatic includes 3 steps:
            print('executing traceroute...')
            subprocess.Popen(['traceroute', '-m', args.MAX_HOPS, args.TARGET],stdout = f, stderr=subprocess.STDOUT).wait()
        time.sleep(args.RUN_DELAY) 
        print('number of runs completed thus far: {} of {}'.format(i+1,args.NUM_RUNS))
        print('time between delays: {} sec'.format(args.RUN_DELAY))
    return names

def parsing_text():
    path = create_directory()
    args = parse_args()
    json_output_file = args.OUTPUT + '.json'
    fileList = os.listdir(path)
    d = {}
    
    print('json file path output:', path, args.OUTPUT)

    filenames = []
    for i in fileList:
        filenames.append(i)

    files = [open(i, 'r') for i in filenames]
    entirity = []
    for line in zip(*files):
        all = [' '.join(line)]
        for i in all:
            entirity.append(i.split())

    entirity.pop(0)
    
    for line in entirity:
        host =[]
        time = []
        #print(line)
        if '*' not in line:
            for i in range(len(line)):
                d['hop'] = line[0]    
                if line[i].find('(') != -1 :
                    host.append(line[i-1])
                    host.append(line[i])
                if line[i].find('ms') != -1:
                    val = float(line[i-1])
                    time.append(val)  

            max_val = max(time)
            min_val = min(time)
            med_org = statistics.median(time)
            med_val = '{:.3f}'.format(med_org)
            avg_org = statistics.mean(time)
            avg = '{:.3f}'.format(avg_org)

            #print(json.dumps({'avg': avg, 'hop': d['hop'], 'hosts': host, 'max': max_val, 'med': med_val, 'min': min_val}, indent=2))
            with open(json_output_file, 'a') as outfile:
                json.dump({'avg': avg, 'hop': d['hop'], 'hosts': host, 'max': max_val, 'med': med_val, 'min': min_val}, outfile, indent=2)


if __name__ == '__main__':
    parse_args()
    args = parse_args()
    folder_with_txt = sys.path[0] +'/'+ args.TEST_DIR
    if os.path.exists(folder_with_txt):
        print('not running traceroute. files exist. now parsing')
        parsing_text()
    else:
        create_directory()
        save_result_in_txt()
        parsing_text()
