# %%
import math
import pandas as pd


f = open("ages.txt", "w")
f.write("12.4,15.8,16.1")
f.close()


n = int(input("Enter n: "))
f = open("ages.txt", "r")
text = f.read()
f.close()

numbers = []
for x in text.split(","):
    numbers.append(float(x))

if len(numbers) < n:
    print("The file contains less than", n, "numbers")
    ages = numbers
else:
    ages = numbers[:n]

for i in range(len(ages)):
    ages[i] = math.floor(ages[i])

f = open("scores.csv", "w")
f.write("Name,Score\n")
f.write("Andrew,88.3\n")
f.write("Ben,92.6\n")
f.write("Carol,89.7\n")
f.close()

f = open("scores.csv", "r")
lines = f.read().split("\n")
f.close()

dic = {"Name": [], "Score": []}
for line in lines[1:]:
    if line != "":
        name, score = line.split(",")
        dic["Name"].append(name)
        dic["Score"].append(float(score))

if len(ages) < len(dic["Name"]):
    print("Not enough ages for all names")
    exit()
ages = ages[:len(dic["Name"])]
dic = {"Name": dic["Name"], "Age": ages, "Score": dic["Score"]}

df = pd.DataFrame(dic)
print(df)

print("Maximum age:", df["Age"].max())

new_row = pd.DataFrame([{"Name": "Daniel", "Age": 10, "Score": 78.0}])
df = pd.concat([df, new_row], ignore_index=True)

p = float(input("Enter deduction p: "))
df.loc[1, "Score"] = df.loc[1, "Score"] - p

for i in range(len(df)):
    df.loc[i, "Score"] = math.ceil(df.loc[i, "Score"] * 2) / 2

print("Updated DataFrame:")
print(df)
print("Mean Score:", df["Score"].mean())
print("Median Score:", df["Score"].median())

df_filtered = df[(df["Age"] >= 12) & (df["Age"] <= 15)]
print("Filtered DataFrame:")
print(df_filtered)

print("Mean Score in Filtered DataFrame:", df_filtered["Score"].mean())
print("Median Score:", df_filtered["Score"].median())

print("Hello world", "this is my code")
# %%
