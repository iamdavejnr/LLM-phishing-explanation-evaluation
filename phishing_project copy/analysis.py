import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('evaluation/scores.csv')

metrics = ['fidelity', 'readability', 'accuracy', 'clarity', 'completeness']
styles = ['technical', 'simple', 'narrative']

# Print mean scores per style
print("\n--- Mean Scores Per Style ---")
for metric in metrics:
    print(f"\n{metric.upper()}")
    for style in styles:
        col = f'{style}_{metric}'
        print(f"  {style}: {df[col].mean():.3f}")

# Statistical testing
print("\n--- Statistical Tests (Kruskal-Wallis) ---")
for metric in metrics:
    groups = [df[f'{style}_{metric}'] for style in styles]
    stat, p = stats.kruskal(*groups)
    print(f"{metric}: H={stat:.3f}, p={p:.4f} {'*** Significant' if p < 0.05 else 'Not significant'}")

# Visualisation — Bar Charts
for metric in metrics:
    means = [df[f'{style}_{metric}'].mean() for style in styles]
    plt.figure(figsize=(8, 5))
    plt.bar(styles, means, color=['steelblue', 'seagreen', 'tomato'])
    plt.title(f'Mean {metric.capitalize()} Score by Explanation Style')
    plt.ylabel('Mean Score')
    plt.xlabel('Explanation Style')
    plt.tight_layout()
    plt.savefig(f'results/{metric}_bar_chart.png')
    plt.close()

# Heatmap
heatmap_data = pd.DataFrame({
    style: [df[f'{style}_{metric}'].mean() for metric in metrics]
    for style in styles
}, index=metrics)

plt.figure(figsize=(8, 5))
sns.heatmap(heatmap_data, annot=True, fmt='.3f', cmap='YlGnBu')
plt.title('Evaluation Scores Heatmap')
plt.tight_layout()
plt.savefig('results/heatmap.png')
plt.close()

print("\nAll charts saved to results/ folder.")