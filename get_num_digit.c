#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#define STRING_LENGTH 1000

int main() {
    char input_string[STRING_LENGTH + 1];
    int digit_to_find;
    int count = 0;
    
    // Initialize the random number generator
    srand(time(0));
    
    // Generate a random string of 1000 digits (0-9)
    for (int i = 0; i < STRING_LENGTH; i++) {
        input_string[i] = '0' + (rand() % 10);  // random digit from '0' to '9'
    }
    input_string[STRING_LENGTH] = '\0';  // Null terminate the string
    
    // Print the random string (optional)
    printf("Random string: %s\n", input_string);
    
    // Ask the user for the digit to find
    printf("Enter a digit to find (0-9): ");
    scanf("%d", &digit_to_find);
    
    // Set the number of threads
    int num_threads = 4;
    int part_size = STRING_LENGTH / num_threads;
    
    // Parallel region to count occurrences
    #pragma omp parallel num_threads(num_threads)
    {
        int thread_id = omp_get_thread_num();
        int local_count = 0;
        
        int start_idx = thread_id * part_size;
        int end_idx = (thread_id == num_threads - 1) ? STRING_LENGTH : (start_idx + part_size);
        
        for (int i = start_idx; i < end_idx; i++) {
            if (input_string[i] == (digit_to_find + '0')) {
                local_count++;
            }
        }
        
        // Update global count safely
        #pragma omp atomic
        count += local_count;
    }
    
    // Output the result
    printf("The digit %d appears %d times in the random string.\n", digit_to_find, count);

    return 0;
}
