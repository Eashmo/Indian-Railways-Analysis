import pandas as pd
import os

# Same path setup as p.py
BASE        = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE, '..', 'data_folder')

# Load the CLEAN file saved by p.py — not the raw one
df = pd.read_csv(os.path.join(DATA_FOLDER, 'clean.csv'))

print(df.shape)
print(df.columns.tolist())


# Q1 — Top 15 stations by average delay (more interesting than 2 zones)
station_stats = (
    df.groupby('station_name')
      .agg(
          avg_delay   = ('delay_mins',  'mean'),
          avg_on_time = ('on_time_pct', 'mean'),
          total_rows  = ('train_number', 'count')
      )
      .reset_index()
      .sort_values('avg_delay', ascending=False)
      .round(1)
)

# Top 15 worst stations (min 5 records for reliability)
top15_worst = station_stats[station_stats['total_rows'] >= 5].head(15)
print("Q1 — Top 15 worst stations:\n", top15_worst)

# Q2 (revised) — Top 15 most punctual stations
top15_best = (
    station_stats[station_stats['total_rows'] >= 5]
    .sort_values('avg_on_time', ascending=False)
    .head(15)
)
print("Q2 — Top 15 most punctual stations:\n", top15_best)

type_stats = (df.groupby('train_type').agg(
    avg_delay = ('delay_mins', 'mean'),
    avg_on_time = ('on_time_pct', 'mean'),
    count = ('train_number', 'count')
).reset_index()
.sort_values('avg_on_time', ascending = False)
.round(1)

              )
print("\nQ3 — Train type punctuality:\n", type_stats)

delay_dist = pd.DataFrame({
    'category'  : ['On time', 'Slight delay',
                    'Significant delay', 'Cancelled/unknown'],
    'avg_pct'   : [
        df['on_time_pct']    .mean(),
        df['slight_pct']     .mean(),
        df['heavy_pct']      .mean(),
        df['cancelled_pct']  .mean()
    ]
}).round(1)
print("\nQ4 — Delay distribution:\n", delay_dist)