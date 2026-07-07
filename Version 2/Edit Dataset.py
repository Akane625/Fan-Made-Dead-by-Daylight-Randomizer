import pandas as pd

df = pd.read_csv("Killer Perks Dataset.csv")

# Remove "The " only if it appears at the beginning
df["killer"] = df["killer"].str.replace(r"^The\s+", "", regex=True)

print(df["killer"].unique())

df.to_csv("Killer Perks Dataset 2.csv", index=False)
