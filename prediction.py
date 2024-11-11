import pandas as pd

# Load the CSV file
df = pd.read_excel('waittime.xlsx')

# Parameters
ride_duration = 10 # minutes per ride
ride_capacity = 2  # people per ride

def calculate_worst_case_wait_time(df):
    # Total number of people in the queue
    total_people = df['Num_People_in_Zone1'].sum()
    
    # Calculate the number of full batches required for everyone in the queue
    full_batches = total_people // ride_capacity
    remaining_people = total_people % ride_capacity
    
    # Total wait time calculation:
    # - Full batches contribute full ride durations.
    # - If there are remaining people, add one more ride duration.
    if remaining_people > 0:
        worst_case_wait_time = (full_batches + 1) * ride_duration
    else:
        worst_case_wait_time = full_batches * ride_duration

    return f"The worst-case wait time for the last person in line is approximately {worst_case_wait_time} minutes."

# Calculate and print the worst-case wait time
print(calculate_worst_case_wait_time(df))
