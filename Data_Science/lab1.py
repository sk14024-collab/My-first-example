import csv
import math

import pandas as pd


def round_up_half(x):
    """Округление вверх до 0.5: 2.3 -> 2.5, 2.6 -> 3, 2 -> 2, 2.5 -> 2.5"""
    return math.ceil(round(x * 2, 9)) / 2


def main():
    try:
        # 1. Создаём ages.txt
        with open("ages.txt", "w") as f:
            f.write("12.7,15.3,16.2,10.5,12,14.0,13.1,16.3")

        # 2. Читаем первые n чисел в список ages
        n = int(input("Enter n: "))
        with open("ages.txt", "r") as f:
            numbers = [float(x) for x in f.read().strip().split(",")]

        if len(numbers) < n:
            print(f"The file contains only {len(numbers)} numbers, "
                  f"which is less than n = {n}.")
            return
        ages = numbers[:n]

        # 3. Округляем вниз до целого и меняем список
        ages = [math.floor(a) for a in ages]

        # 4. Создаём scores.csv
        with open("scores.csv", "w", newline="") as f:
            f.write("Name,Score\n"
                    "Andrew,88.3\n"
                    "Ben,92.6\n"
                    "Carol,89.7\n")

        # 5. Читаем scores.csv в словарь dic (ключ -> список значений)
        dic = {"Name": [], "Score": []}
        with open("scores.csv", "r", newline="") as f:
            for row in csv.DictReader(f):
                dic["Name"].append(row["Name"])
                dic["Score"].append(float(row["Score"]))

        # 6. Добавляем ages как новый столбец после Name
        if len(ages) < len(dic["Name"]):
            print("Not enough ages for all rows in scores.csv.")
            return
        dic = {
            "Name": dic["Name"],
            "Age": ages[:len(dic["Name"])],  # лишние возрасты отбрасываем
            "Score": dic["Score"],
        }

        # 7. Преобразуем в DataFrame и печатаем
        df = pd.DataFrame(dic)
        print(df)

        # 8. Максимальный возраст
        print("Maximum age:", df["Age"].max())

        # 9. Добавляем новую строку: Daniel,10,78
        new_row = pd.DataFrame([{"Name": "Daniel", "Age": 10, "Score": 78.0}])
        df = pd.concat([df, new_row], ignore_index=True)

        # 10. Вычитаем p из Score во второй строке (индекс 1)
        p = float(input("Enter deduction p: "))
        df.loc[1, "Score"] -= p

        # 11. Округляем Score вверх до 0.5
        df["Score"] = df["Score"].apply(round_up_half)

        # 12. Среднее и медиана
        print("Updated DataFrame:")
        print(df)
        print("Mean Score:", df["Score"].mean())
        print("Median Score:", df["Score"].median())

        # 13. Фильтрация: возраст от 12 до 15 включительно
        df_filtered = df[(df["Age"] >= 12) & (df["Age"] <= 15)].reset_index(drop=True)
        print("Filtered DataFrame:")
        print(df_filtered)

        # 14. Среднее и медиана для отфильтрованных данных
        print("Mean Score in Filtered DataFrame:", df_filtered["Score"].mean())
        print("Median Score:", df_filtered["Score"].median())

    except FileNotFoundError as e:
        print("File not found:", e)
    except ValueError as e:
        print("Invalid value:", e)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
