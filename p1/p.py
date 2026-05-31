import zipfile
import pandas as pd
import os

zip_file_path = 'p1/archive (1).zip'
extract_to = 'data_folder'

csv_file_path = os.path.join(extract_to, 'etrain_delays.csv')

# Build path relative to THIS script file — works no matter where you run from
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE, '..', 'data_folder')

df = pd.read_csv(os.path.join(DATA_FOLDER, 'etrain_delays.csv'))

# See ALL columns without truncation
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df['scraped_at'] = pd.to_datetime(df['scraped_at'] , utc= True)
df['date'] = df['scraped_at'].dt.date
df['month'] = df['scraped_at'].dt.month
df['month_name'] = df['scraped_at'].dt.strftime('%b')

df = df.rename(columns={
    'average_delay_minutes' : 'delay_mins',
    'pct_right_time' : 'on_time_pct',
    'pct_slight_delay' : 'slight_pct',
    'pct_significant_delay' : 'heavy_pct',
    'pct_cancelled_unknown' : 'cancelled_pct'
})

df = df.dropna(subset=['delay_mins'])
df = df[df['delay_mins'] >= 0]

zone_map = {
    '1': 'Central (CR)',
    '2': 'North/West (NR/WR)',
    '3': 'East/South (ER/SR)',
    '4': 'South/SC (SR/SCR)',
    '5': 'NE/NF (NER/NFR)',
    '6': 'SE/EC (SER/ECR)',
    '7': 'South Central (SCR)',
    '8': 'SW/WC (SWR/WCR)',
    '9': 'West/NW (WR/NWR)',
    '0': 'Misc/Metro'
}
df['zone'] = (df['train_number']
              .astype('str')
              .str[0]
              .map(zone_map)
              .fillna('Unknown'))

def get_train_type(name): 
    name = str(name).upper()
    if 'RAJDHANI'  in name: return 'Rajdhani'
    if 'SHATABDI'  in name: return 'Shatabdi'
    if 'VANDE'     in name: return 'Vande Bharat'
    if 'DURONTO'   in name: return 'Duronto'
    if 'SUPERFAST' in name: return 'Superfast'
    if 'EXPRESS'   in name: return 'Express'
    if 'MAIL'      in name: return 'Mail'
    if 'PASSENGER' in name: return 'Passenger'
    return 'Other'
df['train_type'] = df['train_name'].apply(get_train_type)


df['delay_cat'] = pd.cut(
    df['delay_mins'],
    bins=[-1, 5, 15, 30, 60, 9999],
    labels=['On time', 'Slight (5–15)',
            'Moderate (15–30)', 'Heavy (30–60)', 'Severe (60+)']
)

df.to_csv(os.path.join(DATA_FOLDER, 'clean.csv'), index=False)

print(f"Clean rows  : {len(df):,}")
print(f"Zones       : {df['zone'].value_counts().to_dict()}")
print(f"Train types : {df['train_type'].value_counts().to_dict()}")