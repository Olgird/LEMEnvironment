import pandas as pd

file = 'data\citylearn_challenge_2022_phase_all\Building_7.csv'

df = pd.read_csv(file)
df = df.values.tolist()

print(type(df[25][1]))
print(df[25][1])




