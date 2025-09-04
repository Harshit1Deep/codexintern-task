import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv("diversity_school.csv")

# Quick look at the data
print("First few rows:")
print(data.head())

print("\nDataset Info:")
data.info()

print("\nSummary (numerical columns):")
print(data.describe())

# Average enrollment across all categories
avg_enroll = data["enrollment"].mean()
print(f"\nAverage enrollment: {avg_enroll:.2f}")

# ---- Plots ----

# Category distribution
plt.figure(figsize=(10, 6))
data["category"].value_counts().plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Demographic Category Distribution")
plt.xlabel("Category")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.show()

# Scatter: total enrollment vs category enrollment
plt.figure(figsize=(8, 5))
plt.scatter(data["total_enrollment"], data["enrollment"], alpha=0.6, color="crimson")
plt.title("Total Enrollment vs Category Enrollment")
plt.xlabel("Total Enrollment")
plt.ylabel("Category Enrollment")
plt.tight_layout()
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 6))
corr = data.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()

# Notes
print("\nNotes:")
print("- Categories represent demographic groups.")
print("- Bar chart shows most common demographics.")
print("- Scatter plot shows relationship between overall size and group size.")
print("- Heatmap shows correlations between numeric fields.")
