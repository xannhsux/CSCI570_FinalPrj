import os
import sys
import time
import tracemalloc

#Create output file
def create_output(output, dp_cost, X, Y, time_taken, memory_consumed):
    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(output, 'w') as f:
        f.write(f"{'Total cost:':<15}{dp_cost}\n")
        f.write(f"{'X aligned:':<15}{X}\n")
        f.write(f"{'Y aligned:':<15}{Y}\n")
        f.write(f"{'Time (ms):':<15}{time_taken:.3f}\n")
        f.write(f"{'Memory (KB):':<15}{memory_consumed:.1f}\n")

#generate X, Y strings
def generate_str(original_str, indices):
    final_str = original_str
    
    for index in indices:
        final_str = final_str[:index+1] + final_str + final_str[index+1:]
    return final_str

def parse_input(input_file):
        # read lines from input filed
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    base_X = lines[0]
    indices_X = []
    j = 1
    while lines[j].isdigit():
        indices_X.append(int(lines[j]))
        j += 1
    base_Y = lines[j]
    indices_Y = [int(x) for x in lines[j+1:]]

    return base_X, indices_X, base_Y, indices_Y

def dp_basic(X,Y,gap_penalty,mismatch_penalty):
    m=len(X)
    n=len(Y)
    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]
    
    for i in range(m+1):
        dp[i][0] = i * gap_penalty
    for j in range(n+1):
        dp[0][j] = j * gap_penalty

    
    for i in range(1, m+1):
        for j in range(1, n+1):
            match_cost = dp[i-1][j-1] + mismatch_penalty[X[i-1]][Y[j-1]]
            gap_x_cost = dp[i-1][j] + gap_penalty
            gap_y_cost = dp[i][j-1] + gap_penalty
            dp[i][j] = min(match_cost, gap_x_cost, gap_y_cost)
    p = m
    q = n
    direction = [-1] * (m + n + 1)

    p, q = m, n
    while p > 0 or q > 0:
        idx = p + q
        if p>0 and q>0 and dp[p][q] == dp[p-1][q-1] + mismatch_penalty[X[p-1]][Y[q-1]]:
            direction[idx-2] = 1
            p, q = p-1, q-1
            idx -= 2
        elif p>0 and dp[p][q] == dp[p-1][q] + gap_penalty:
            direction[idx-1] = 0
            p -= 1
            idx -=1
        else:
            direction[idx-1] = 2
            q -= 1
            idx-=1

    X_alignment = []
    Y_alignment = []
    i = 0
    xi, yi = 0, 0
    while i < m + n - 0:
        d = direction[i]
        if d == 1:
            X_alignment.append(X[xi])
            Y_alignment.append(Y[yi])
            xi += 1; yi += 1
        elif d == 0:
            X_alignment.append(X[xi])
            Y_alignment.append('_')
            xi += 1
        elif d == 2:
            X_alignment.append('_')
            Y_alignment.append(Y[yi])
            yi += 1
        i += 1
    return (dp[m][n],''.join(X_alignment),''.join(Y_alignment))


def basic_algo(input_file, output_file):

    base_X, indices_X, base_Y, indices_Y = parse_input(input_file)
    X = generate_str(base_X, indices_X)
    Y = generate_str(base_Y, indices_Y)

    #mismatch penalty and gap penalty
    delta = 30
    alpha = {
    'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
    'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
    'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
    'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}
    }

    tracemalloc.start()
    start_time = time.perf_counter()
    dp_cost, aligned_x, aligned_y = dp_basic(X, Y, delta, alpha)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.perf_counter()
    time_taken = (end_time - start_time) * 1000 #ms
    memory_consumed = peak/1024  # KB!

    create_output(output_file, dp_cost, aligned_x, aligned_y, time_taken, memory_consumed)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("usage: python basic3.py <input_file> <output_file_1>")
        sys.exit(1)

    input_file  = sys.argv[1]
    output_file = sys.argv[2]


    basic_algo(input_file, output_file)
