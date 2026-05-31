import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE        = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE, '..', 'data_folder')
OUTPUT_DIR  = os.path.join(BASE, '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(DATA_FOLDER, 'clean.csv'))

# Rebuild analysis dataframes
station_stats = (
    df.groupby('station_name')
      .agg(
          avg_delay   = ('delay_mins',  'mean'),
          avg_on_time = ('on_time_pct', 'mean'),
          total_rows  = ('train_number', 'count')
      )
      .reset_index().round(1)
)
top15_worst = station_stats[station_stats['total_rows'] >= 5].sort_values('avg_delay', ascending=False).head(15)
top15_best  = station_stats[station_stats['total_rows'] >= 5].sort_values('avg_on_time', ascending=False).head(15)

type_stats = (
    df.groupby('train_type')
      .agg(avg_delay=('delay_mins','mean'), avg_on_time=('on_time_pct','mean'), count=('train_number','count'))
      .reset_index().sort_values('avg_on_time', ascending=False).round(1)
)

delay_dist = pd.DataFrame({
    'category': ['On time', 'Slight delay', 'Significant delay', 'Cancelled'],
    'avg_pct' : [df['on_time_pct'].mean(), df['slight_pct'].mean(),
                 df['heavy_pct'].mean(),   df['cancelled_pct'].mean()]
}).round(1)

sns.set_theme(style='ticks')

# ── Chart 1: Top 15 worst stations by avg delay
avg = top15_worst['avg_delay'].mean()
colors = ['#E24B4A' if d > avg else '#85B7EB' for d in top15_worst['avg_delay']]

fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(top15_worst['station_name'], top15_worst['avg_delay'], color=colors)
ax.axvline(avg, color='#888780', linestyle='--', linewidth=1,
           label=f'Group avg: {avg:.1f} min')
for i, v in enumerate(top15_worst['avg_delay']):
    ax.text(v + 1, i, f'{v:.1f}', va='center', fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('Average delay (minutes)')
ax.set_title('Top 15 worst stations by average delay')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'chart_01_worst_stations.png'), dpi=150)
plt.show()

# ── Chart 2: Top 15 best stations by on-time %
fig, ax = plt.subplots(figsize=(10, 7))
sns.barplot(data=top15_best, x='avg_on_time', y='station_name',
            hue='avg_on_time', palette='dark:b_r', legend=False, ax=ax)
for i, v in enumerate(top15_best['avg_on_time']):
    ax.text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('Average on-time %')
ax.set_title('Top 15 most punctual stations')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'chart_02_best_stations.png'), dpi=150)
plt.show()

# ── Chart 3: Train type punctuality
fig, ax = plt.subplots(figsize=(9, 5))
colors_type = ['#E24B4A' if t == 'Duronto' else '#85B7EB' for t in type_stats['train_type']]
ax.barh(type_stats['train_type'], type_stats['avg_on_time'], color=colors_type)
for i, v in enumerate(type_stats['avg_on_time']):
    ax.text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('Average on-time %')
ax.set_title('Train category punctuality — Duronto worst despite premium status')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'chart_03_train_type.png'), dpi=150)
plt.show()

# ── Chart 4: Overall delay breakdown
colors_dist = ['#3B6D11', '#EF9F27', '#E24B4A', '#888780']
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(delay_dist['category'], delay_dist['avg_pct'], color=colors_dist)
for i, v in enumerate(delay_dist['avg_pct']):
    ax.text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('Average % of trains')
ax.set_title('Only 49.8% of trains run on time across the network')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'chart_04_delay_breakdown.png'), dpi=150)
plt.show()