import os
import time
import psutil


#Create output file
def create_output(output, dp_cost, X, Y, time_taken, memory_consumed):
    dir = os.path.dirname(output)
    if os.path.exists(dir) == False:
        os.makedirs(dir)
    with open(output, 'w') as f:
        f.write(f"{dp_cost}\n")
        f.write(f"{X}\n")
        f.write(f"{Y}\n")
        f.write(f"{time_taken:.3f}\n")
        f.write(f"{memory_consumed:.1f}\n")


#generate X, Y strings
def generate_str(original_str, indices):
    final_str = original_str
    for index in indices:
        final_str = final_str[:index+1] + final_str + final_str[index+1:]
    return final_str

def parse_input(input_file):
    # read lines from input filed
    with open(input_file, 'r') as f:
        for line in f.readlines():
            if line.strip() != None:
                lines = line.strip()

    base_X = lines[0]
    indices_X = []
    j = 0
    while line[j+1].isdigit():
        indices_X.append(int(lines[i]))
        j += 1
    base_Y = lines[j+1]
    indices_Y = lines[j+2:]

    return base_X, indices_X, base_Y, indices_Y

def dp_baisc():


def basic_algo(input_file, output_file):
    #generate X Y string from input_file
    base_X, indices_X, base_Y, indices_Y = parse_input(input_file)
    X = generate_str(base_X, indices_X)
    Y = generate_str(base_Y, indices_Y)

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
    create_output(output_file, dp_cost, X, Y, time_taken, memory_consumed)