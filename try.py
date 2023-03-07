import pandas as pd

file = 'data\citylearn_challenge_2022_phase_all\Building_1.csv'

df = pd.read_csv(file)
df = df.values.tolist()

print(type(df[0][7]))
print(df[0][7])
