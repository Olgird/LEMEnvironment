# import pandas as pd

# file = 'data\citylearn_challenge_2022_phase_all\Building_7.csv'

# df = pd.read_csv(file)
# df = df.values.tolist()

# print(type(df[25][1]))
# print(df[25][1])

import random

L = list(range(1,365))
random.shuffle(L)
validation_set = L[:50]
training_set = training = L[50:]

print(random.choices(training_set)[0])


# L = [1,2,3]
# a,b,c = L

# print(a,b,c)


