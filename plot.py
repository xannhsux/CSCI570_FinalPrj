import os
import sys
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_problem_size(input_file):
    """Extract problem size from an input file by parsing and calculating total string lengths."""
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    base_X = lines[0]
    j = 1
    indices_X = []
    while j < len(lines) and lines[j].isdigit():
        indices_X.append(int(lines[j]))
        j += 1
    
    base_Y = lines[j]
    j += 1
    indices_Y = []
    while j < len(lines) and lines[j].isdigit():
        indices_Y.append(int(lines[j]))
        j += 1
    
    # Calculate string lengths
    len_X = len(base_X) * (2 ** len(indices_X))
    len_Y = len(base_Y) * (2 ** len(indices_Y))
    
    return len_X + len_Y

def extract_metrics(output_file):
    """Extract time and memory metrics from an output file."""
    with open(output_file, 'r') as f:
        lines = f.readlines()
    
    time_match = re.search(r'Time \(ms\):\s+(\d+\.\d+)', lines[3])
    memory_match = re.search(r'Memory \(KB\):\s+(\d+\.\d+)', lines[4])
    
    time_ms = float(time_match.group(1)) if time_match else 0
    memory_kb = float(memory_match.group(1)) if memory_match else 0
    
    return time_ms, memory_kb

def run_algorithm(algorithm_script, input_file, output_file):
    """Run the algorithm script on the input file and save results to output file."""
    try:
        cmd = ['python', algorithm_script, input_file, output_file]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Error running {algorithm_script} on {input_file}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_tests.py datapoints_directory")
        sys.exit(1)
    
    datapoints_dir = sys.argv[1]
    results_dir = "results"
    
    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)
    
    # Find all input files in datapoints directory
    input_files = sorted([os.path.join(datapoints_dir, f) for f in os.listdir(datapoints_dir)
                   if f.endswith('.txt')])
    
    # Data structures to store results
    problem_sizes = []
    basic_times = []
    basic_memories = []
    efficient_times = []
    efficient_memories = []
    
    # Run tests for each input file
    for input_file in input_files:
        file_name = os.path.basename(input_file)
        print(f"Processing {file_name}...")
        
        # Calculate problem size
        problem_size = extract_problem_size(input_file)
        problem_sizes.append(problem_size)
        
        # Basic algorithm
        basic_output = os.path.join(results_dir, f"basic_{file_name}")
        if run_algorithm("basic3.py", input_file, basic_output):
            basic_time, basic_memory = extract_metrics(basic_output)
            basic_times.append(basic_time)
            basic_memories.append(basic_memory)
        else:
            basic_times.append(0)
            basic_memories.append(0)
        
        # Efficient algorithm
        efficient_output = os.path.join(results_dir, f"efficient_{file_name}")
        if run_algorithm("efficient3.py", input_file, efficient_output):
            efficient_time, efficient_memory = extract_metrics(efficient_output)
            efficient_times.append(efficient_time)
            efficient_memories.append(efficient_memory)
        else:
            efficient_times.append(0)
            efficient_memories.append(0)
    
    # Sort all data by problem size
    sorted_indices = np.argsort(problem_sizes)
    problem_sizes = [problem_sizes[i] for i in sorted_indices]
    basic_times = [basic_times[i] for i in sorted_indices]
    basic_memories = [basic_memories[i] for i in sorted_indices]
    efficient_times = [efficient_times[i] for i in sorted_indices]
    efficient_memories = [efficient_memories[i] for i in sorted_indices]
    
    # Print table for the report
    print("\nResults for Summary Report:")
    print("Problem Size (m+n) | Basic Time (ms) | Basic Memory (KB) | Efficient Time (ms) | Efficient Memory (KB)")
    print("-" * 90)
    for i in range(len(problem_sizes)):
        print(f"{problem_sizes[i]:16d} | {basic_times[i]:14.2f} | {basic_memories[i]:16.2f} | {efficient_times[i]:18.2f} | {efficient_memories[i]:20.2f}")
    
    # Create a CSV file with results
    with open(os.path.join(results_dir, "results.csv"), "w") as f:
        f.write("Problem Size (m+n),Basic Time (ms),Basic Memory (KB),Efficient Time (ms),Efficient Memory (KB)\n")
        for i in range(len(problem_sizes)):
            f.write(f"{problem_sizes[i]},{basic_times[i]:.2f},{basic_memories[i]:.2f},{efficient_times[i]:.2f},{efficient_memories[i]:.2f}\n")
    
    # Plot Time vs Problem Size
    plt.figure(figsize=(10, 6))
    plt.plot(problem_sizes, basic_times, 'bo-', label='Basic Algorithm')
    plt.plot(problem_sizes, efficient_times, 'ro-', label='Memory-Efficient Algorithm')
    plt.xlabel('Problem Size (m+n)')
    plt.ylabel('Time (milliseconds)')
    plt.title('CPU Time vs Problem Size')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, 'time_plot.png'), dpi=300)
    
    # Plot Memory vs Problem Size
    plt.figure(figsize=(10, 6))
    plt.plot(problem_sizes, basic_memories, 'bo-', label='Basic Algorithm')
    plt.plot(problem_sizes, efficient_memories, 'ro-', label='Memory-Efficient Algorithm')
    plt.xlabel('Problem Size (m+n)')
    plt.ylabel('Memory (KB)')
    plt.title('Memory Usage vs Problem Size')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(results_dir, 'memory_plot.png'), dpi=300)
    
    print(f"\nPlots and results saved to the {results_dir} directory")

if __name__ == "__main__":
    main()
