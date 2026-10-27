"""Lab Assignment #2: Data Visualization (Oscar winners)."""
import sys
import zipfile

import matplotlib
matplotlib.use("Agg")  # рисуем в файл, без окна; убери эту строку, если нужен plt.show()
import matplotlib.pyplot as plt
import pandas as pd

FILE_NAME = "oscars.xlsx"
REQUIRED_COLUMNS = ["gender", "category"]  # сравнение без учёта регистра


# ---------- 1-2. Загрузка данных ----------
def load_data(path):
    try:
        df = pd.read_excel(path)
    except FileNotFoundError:
        sys.exit(f"Ошибка: файл '{path}' не найден. Положи его в рабочую папку.")
    except PermissionError:
        sys.exit(f"Ошибка: нет доступа к файлу '{path}' (возможно, он открыт в Excel).")
    except (zipfile.BadZipFile, ValueError) as e:
        sys.exit(f"Ошибка формата файла '{path}': {e}")
    except ImportError:
        sys.exit("Не установлен openpyxl: pip install openpyxl")
    except Exception as e:
        sys.exit(f"Не удалось прочитать файл: {e}")

    if df.empty:
        sys.exit("Ошибка: файл не содержит данных.")

    # приводим названия колонок к нижнему регистру, убираем пробелы
    df.columns = [str(c).strip().lower() for c in df.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        sys.exit(f"Ошибка: в файле нет нужных колонок: {missing}. "
                 f"Найдены: {list(df.columns)}")
    return df


# ---------- 3-4. Круговая диаграмма по полу ----------
def pie_gender(df, raw=False):
    gender = df["gender"].dropna().astype(str).str.strip()
    if not raw:
        # модификация: 'female' и 'Female' -> одна категория
        gender = gender.str.capitalize()
    counts = gender.value_counts()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90,
           colors=plt.cm.Set2.colors, wedgeprops={"edgecolor": "white"})
    ax.set_title("Gender Distribution of Oscar Winners")
    return fig


# ---------- 5. Столбчатая диаграмма по всем категориям ----------
def bar_all_categories(df):
    counts = df["category"].dropna().value_counts()
    fig, ax = plt.subplots(figsize=(12, 6))
    counts.plot(kind="bar", ax=ax, color=plt.cm.Set2.colors[0])
    ax.set_title("Number of Oscar Winners by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Winners")
    plt.xticks(rotation=90, fontsize=5)
    fig.tight_layout()
    return fig


# ---------- 7, 9. Топ-n категорий (с настройкой внешнего вида) ----------
def bar_top_n(df, n):
    counts = df["category"].dropna().value_counts().head(n)
    counts = counts.sort_values()  # самый большой столбец сверху

    fig, ax = plt.subplots(figsize=(10, 0.5 * n + 2))        # размер
    bars = ax.barh(counts.index, counts.values,              # горизонтальные столбцы
                   height=0.6,                               # толщина столбцов
                   color=plt.cm.viridis_r(range(0, 256, max(1, 256 // n)))[:n])  # палитра
    ax.bar_label(bars, padding=3)                            # подписи значений у столбцов
    ax.set_title(f"Top {n} Categories with Most Oscar Winners", fontsize=14)
    ax.set_xlabel("Number of Winners")                       # подписи осей
    ax.set_ylabel("Category")
    ax.set_xlim(0, counts.max() * 1.1)
    fig.tight_layout()
    return fig


def ask_n(max_n):
    while True:
        try:
            n = int(input("Enter n: "))
        except ValueError:
            print("Введи целое число.")
            continue
        except EOFError:
            sys.exit("Ввод прерван.")
        if 1 <= n <= max_n:
            return n
        print(f"n должно быть от 1 до {max_n}.")


def main():
    df = load_data(FILE_NAME)
    print(df)

    fig = pie_gender(df, raw=True)           # шаг 3: «как есть» (видны 'female' и 'Female')
    fig.savefig("gender_distribution_raw.png", dpi=150)
    fig = pie_gender(df)                     # шаг 4: после исправления
    fig.savefig("gender_distribution.png", dpi=150)

    fig = bar_all_categories(df)
    fig.savefig("winners_by_category.png", dpi=150)

    n = ask_n(df["category"].nunique())
    fig = bar_top_n(df, n)
    fig.savefig("top_n_winners_by_category.png", dpi=150)
    print("Графики сохранены.")


if __name__ == "__main__":
    main()