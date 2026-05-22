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

# ── Task 1: Votes Analysis ────────────────────────────────
df_all = pd.read_sql('SELECT * FROM v_l3_votes_analysis', conn)
df_top = pd.read_sql('SELECT * FROM v_l3_top10_votes LIMIT 10', conn)
df_bot = pd.read_sql('SELECT * FROM v_l3_bottom10_votes LIMIT 10', conn)

fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle('Votes Analysis', fontsize=16, fontweight='bold')

axes[0].scatter(df_all['votes'], df_all['aggregate_rating'],
                alpha=0.3, color=PURPLE, s=10)
axes[0].set_xlabel('Votes')
axes[0].set_ylabel('Rating')
axes[0].set_title('Votes vs Rating (Correlation)')

axes[1].barh(df_top['restaurant_name'][::-1], df_top['votes'][::-1], color=TEAL)
axes[1].set_title('Top 10 Most Voted')
axes[1].set_xlabel('Votes')

axes[2].barh(df_bot['restaurant_name'], df_bot['votes'], color=CORAL)
axes[2].set_title('Bottom 10 Least Voted')
axes[2].set_xlabel('Votes')

plt.tight_layout()
plt.savefig('solutions/L3_Task1_Votes.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Task 2: Price Range vs Services ──────────────────────
df = pd.read_sql('SELECT * FROM v_l3_price_vs_services', conn)

fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(df))
width = 0.35

bars1 = ax.bar([i - width/2 for i in x], df['delivery_pct'],
               width, label='Online Delivery %', color=PURPLE)
bars2 = ax.bar([i + width/2 for i in x], df['booking_pct'],
               width, label='Table Booking %', color=TEAL)

ax.set_xticks(list(x))
ax.set_xticklabels(df['price_label'])
ax.set_ylabel('Percentage (%)')
ax.set_title('Price Range vs Online Delivery & Table Booking',
             fontsize=14, fontweight='bold')
ax.legend()

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{bar.get_height():.1f}%', ha='center', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{bar.get_height():.1f}%', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('solutions/L3_Task2_PriceServices.png', dpi=150, bbox_inches='tight')
plt.show()

conn.close()
print('Level 3 Done! Check solutions folder.')