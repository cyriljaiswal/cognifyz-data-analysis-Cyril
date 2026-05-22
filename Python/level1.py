import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('solutions', exist_ok=True)

conn = psycopg2.connect(
    host='localhost',
    database='restaurant_db',
    user='postgres',
    password='1234',   # your pgAdmin password here
    port=5432
)

sns.set_theme(style='whitegrid')
PURPLE = '#7F77DD'
TEAL   = '#1D9E75'
CORAL  = '#D85A30'
print('Connected!')

# ── Task 1: Top Cuisines ──────────────────────────────────
df = pd.read_sql('SELECT * FROM v_l1_top_cuisines LIMIT 15', conn)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Top 15 Most Common Cuisines', fontsize=16, fontweight='bold')

axes[0].barh(df['cuisine'][::-1], df['restaurant_count'][::-1], color=PURPLE)
axes[0].set_xlabel('Number of Restaurants')
axes[0].set_title('Restaurant Count by Cuisine')

axes[1].barh(df['cuisine'][::-1], df['percentage'][::-1], color=TEAL)
axes[1].set_xlabel('Percentage (%)')
axes[1].set_title('Percentage of Restaurants per Cuisine')

plt.tight_layout()
plt.savefig('solutions/L1_Task1_Cuisines.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Top 3 cuisines: {list(df['cuisine'][:3])}")

# ── Task 2: City Analysis ─────────────────────────────────
df = pd.read_sql('SELECT * FROM v_l1_city_analysis LIMIT 15', conn)

fig, axes = plt.subplots(1, 2, figsize=(18, 6))
fig.suptitle('City Analysis', fontsize=16, fontweight='bold')

axes[0].bar(df['city'], df['restaurant_count'], color=PURPLE)
axes[0].set_title('Restaurants per City')
axes[0].tick_params(axis='x', rotation=45)

df_sorted = df.sort_values('avg_rating', ascending=False)
axes[1].bar(df_sorted['city'], df_sorted['avg_rating'], color=TEAL)
axes[1].set_title('Average Rating per City')
axes[1].set_ylim(0, 5)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('solutions/L1_Task2_City.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Most restaurants: {df.iloc[0]['city']}")
print(f"Highest avg rating: {df_sorted.iloc[0]['city']}")

# ── Task 3: Price Range ───────────────────────────────────
df = pd.read_sql('SELECT * FROM v_l1_price_range', conn)
colors = ['#1D9E75', '#7F77DD', '#D85A30', '#D4537E']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Price Range Distribution', fontsize=16, fontweight='bold')

axes[0].bar(df['price_label'], df['restaurant_count'], color=colors)
axes[0].set_title('Restaurants per Price Range')
axes[0].set_ylabel('Count')

axes[1].pie(df['percentage'], labels=df['price_label'],
            autopct='%1.1f%%', colors=colors,
            wedgeprops=dict(width=0.5), startangle=90)
axes[1].set_title('Percentage Distribution')

plt.tight_layout()
plt.savefig('solutions/L1_Task3_Price.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Task 4: Online Delivery ───────────────────────────────
df = pd.read_sql('SELECT * FROM v_l1_online_delivery', conn)
colors = [TEAL, CORAL]

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.suptitle('Online Delivery Analysis', fontsize=16, fontweight='bold')

axes[0].pie(df['percentage'], labels=df['delivery_status'],
            autopct='%1.1f%%', colors=colors,
            explode=[0.05, 0], startangle=90)
axes[0].set_title('% Restaurants with Online Delivery')

axes[1].bar(df['delivery_status'], df['avg_rating'], color=colors, width=0.4)
axes[1].set_title('Avg Rating: With vs Without Delivery')
axes[1].set_ylim(0, 5)
for i, val in enumerate(df['avg_rating']):
    axes[1].text(i, val + 0.05, str(val), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('solutions/L1_Task4_Delivery.png', dpi=150, bbox_inches='tight')
plt.show()

conn.close()
print('Level 1 Done! Check solutions folder.')