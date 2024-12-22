from datetime import datetime
import random
from UnrulyExercise5 import UnrulySolver

trials = 20
max_steps = (10_000, 100_000, 500_000)
avg_steps_made = 0
avg_time_taken = 0.0
avg_violations = 0
avg_success_rate = 0

for steps in max_steps:
    steps_made = 0
    time_taken = 0.0
    violations = 0
    success_rate = 0

    for i in range(trials):  # get a lot measurements in order to get a mean value for all the above metrics
        random.seed(datetime.now())  # Initialize random generator with current time
        solver = UnrulySolver(input_file='inp.txt', max_steps=steps)
        solver.parse_input()
        solver.fill_random()

        start_time = datetime.now()
        best_value, steps_used = solver.simulated_annealing()
        end_time = datetime.now()
        time_elapsed = (end_time - start_time).total_seconds()

        # Update metrics
        steps_made += steps_used
        time_taken += time_elapsed
        violations += best_value
        if best_value == 0:  # A solution without violations is a success
            success_rate += 1

    # Calculate averages
    avg_steps_made = steps_made / trials
    avg_time_taken = time_taken / trials
    avg_violations = violations / trials
    avg_success_rate = (success_rate / trials) * 100

    # Print results for the current max_steps
    print(f"Max Steps: {steps}")
    print(f"Average Steps Made: {avg_steps_made:.2f}")
    print(f"Average Time Taken (s): {avg_time_taken:.2f}")
    print(f"Average Violations: {avg_violations:.2f}")
    print(f"Success Rate (%): {avg_success_rate:.2f}%")
    print("-" * 40)

