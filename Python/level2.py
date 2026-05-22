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
    password='1234',
    port=5432
)

sns.set_theme(style='whitegrid')
PURPLE = '#7F77DD'
TEAL   = '#1D9E75'
CORAL  = '#D85A30'
print('Connected!')

# ── Task 1: Rating Distribution ───────────────────────────
df = pd.read_sql('SELECT * FROM v_l2_rating_distribution', conn)
df_votes = pd.read_sql('SELECT * FROM v_l2_avg_votes', conn)

order = ['Not Rated','0-2 (Poor)','2-3 (Average)','3-3.5 (Good)',
         '3.5-4 (Very Good)','4-4.5 (Excellent)','4.5-5 (Outstanding)']
df['rating_range'] = pd.Categorical(df['rating_range'], categories=order, ordered=True)
df = df.sort_values('rating_range')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Restaurant Ratings Analysis', fontsize=16, fontweight='bold')

bar_colors = ['#888780','#E24B4A','#EF9F27','#FAC775','#1D9E75','#0F6E56','#085041']
axes[0].bar(df['rating_range'], df['restaurant_count'], color=bar_colors)
axes[0].set_title('Rating Distribution')
axes[0].tick_params(axis='x', rotation=30)

avg_v = int(df_votes['avg_votes_overall'].iloc[0])
axes[1].text(0.5, 0.6, str(avg_v), ha='center', va='center',
             fontsize=60, fontweight='bold', color=PURPLE,
             transform=axes[1].transAxes)
axes[1].text(0.5, 0.35, 'Average Votes per Restaurant',
             ha='center', fontsize=13, color='gray',
             transform=axes[1].transAxes)
axes[1].axis('off')

plt.tight_layout()
plt.savefig('solutions/L2_Task1_Ratings.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Most common rating: {df.loc[df['restaurant_count'].idxmax(), 'rating_range']}")

# ── Task 2: Cuisine Combinations ─────────────────────────
df = pd.read_sql(
    'SELECT * FROM v_l2_cuisine_combinations ORDER BY restaurant_count DESC LIMIT 15', conn)

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Cuisine Combinations', fontsize=16, fontweight='bold')

axes[0].barh(df['cuisine_combination'][::-1], df['restaurant_count'][::-1], color=PURPLE)
axes[0].set_title('Most Common Combinations')
axes[0].set_xlabel('Restaurant Count')

df_rated = df.sort_values('avg_rating', ascending=False).head(10)
axes[1].barh(df_rated['cuisine_combination'][::-1], df_rated['avg_rating'][::-1], color=TEAL)
axes[1].set_title('Top Combos by Avg Rating')
axes[1].set_xlim(0, 5)

plt.tight_layout()
plt.savefig('solutions/L2_Task2_Combos.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Task 3: Geographic Map ────────────────────────────────
df = pd.read_sql('SELECT * FROM v_l2_geographic', conn)

fig, ax = plt.subplots(figsize=(14, 8))
scatter = ax.scatter(
    df['longitude'], df['latitude'],
    c=df['aggregate_rating'],
    cmap='RdYlGn', alpha=0.5, s=10, vmin=0, vmax=5
)
plt.colorbar(scatter, ax=ax, label='Rating')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Geographic Distribution of Restaurants\n(Green = High Rating, Red = Low)',
             fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('solutions/L2_Task3_Map.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Total restaurants plotted: {len(df)}")

# ── Task 4: Restaurant Chains ─────────────────────────────
df = pd.read_sql(
    'SELECT * FROM v_l2_restaurant_chains ORDER BY outlet_count DESC LIMIT 15', conn)

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Restaurant Chains', fontsize=16, fontweight='bold')

axes[0].barh(df['restaurant_name'][::-1], df['outlet_count'][::-1], color=PURPLE)
axes[0].set_title('Top Chains by Outlet Count')

axes[1].scatter(df['outlet_count'], df['avg_rating'],
                s=df['total_votes']/50, alpha=0.7,
                color=TEAL, edgecolors='white')
for _, row in df.iterrows():
    axes[1].annotate(row['restaurant_name'],
                     (row['outlet_count'], row['avg_rating']), fontsize=7)
axes[1].set_xlabel('Outlet Count')
axes[1].set_ylabel('Avg Rating')
axes[1].set_title('Outlets vs Rating (bubble = votes)')

plt.tight_layout()
plt.savefig('solutions/L2_Task4_Chains.png', dpi=150, bbox_inches='tight')
plt.show()

conn.close()
print('Level 2 Done! Check solutions folder.')