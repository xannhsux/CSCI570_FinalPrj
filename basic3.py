import os
import time
import psutil


#Create output file
def create_output(output, dp_cost, align_X, align_Y, time_taken, memory_consumed):
    dir = os.path.dirname(output)
    if os.path.exists(dir) == False:
        os.makedirs(dir)
    with open(output, 'w') as f:
        f.write(f"{dp_cost}\n")
        f.write(f"{align_X}\n")
        f.write(f"{align_Y}\n")
        f.write(f"{time_taken:.3f}\n")
        f.write(f"{memory_consumed:.1f}\n")

def basic_algorithm(input_file, output_file):
    #find X Y alignment string
    align_X = None
    align_Y = None

    #memory and time at start time
    process = psutil.Process()
    memory_info = process.memory_info()
    start_time = time.time()

    #dp function
    dp_cost = None

    #memory and time at end time
    memory_consumed = int(memory_info.rss / 1024)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000

    #Create outputfile
    create_output(output_file, dp_cost, align_X, align_Y, time_taken, memory_consumed)