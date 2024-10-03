import random
import concurrent.futures

STRING_LENGTH = 1000

# Function for each thread to count digit occurrences
def count_occurrences(start_idx, end_idx, input_string, digit_to_find):
    local_count = sum(1 for i in range(start_idx, end_idx) if input_string[i] == str(digit_to_find))
    print(f"Thread working on indices {start_idx}-{end_idx} found {local_count} occurrences.")
    return local_count

# Main function
def main():
    # Generate a random string of 1000 digits (0-9)
    input_string = ''.join(random.choice('0123456789') for _ in range(STRING_LENGTH))
    print(f"Random string: {input_string}")
    print(f"Length of input string: {len(input_string)}")
    
    # Ask the user for the digit to find
    digit_to_find = int(input("Enter a digit to find (0-9): "))
    
    # Number of threads
    num_threads = 4
    part_size = STRING_LENGTH // num_threads
    print(f"Number of threads: {num_threads}")
    
    total_count = 0

    # Use ThreadPoolExecutor to mimic OpenMP parallelism
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start_idx = i * part_size
            end_idx = STRING_LENGTH if i == num_threads - 1 else (start_idx + part_size)
            futures.append(executor.submit(count_occurrences, start_idx, end_idx, input_string, digit_to_find))
        
        for future in concurrent.futures.as_completed(futures):
            total_count += future.result()
    
    # Print the total occurrences
    print(f"The total occurrences of the digit {digit_to_find} are {total_count}.")

if __name__ == "__main__":
    main()

## file name as digit_count.py 

## job.sh file 
#!/bin/bash
#SBATCH --job-name=digit_count
#SBATCH --output=digit_count.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00
#SBATCH --partition=normal

# module load python
# python3 digit_count.py

### end of job.sh file 


#  command to schule job run -  sbatch job.sh

# run this file using python on your cluster python3 digit_count.py





