import pandas as pd
# Replace 'handoff_events_bonus.csv' with the path to your CSV file if it's in a different directory
csv_filename = 'handoff_events.csv'
df = pd.read_csv(csv_filename)
row_count = df['Device ID'].count()
print(f"Total number of rows: {row_count}")
