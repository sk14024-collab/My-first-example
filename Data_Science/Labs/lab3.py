import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path
df = pd.read_csv(Path(__file__).parent / "PL_Players.csv", encoding="latin-1")
df = df.dropna()

rename_map = {
    "Pos": "Position",
    "90s": "Total minutes played divided by 90",
    "Tkl": "Tackles",
    "TklW": "Tackles Won",
    "Def 3rd": "Tackles won in defensive 3rd",
    "Mid 3rd": "Tackles won in midfield",
    "Att 3rd": "Tackles won in attacking 3rd",
    "Press": "number of times opponent put under pressure",
    "Succ": "Successful press",
    "%": "% of successful press",
    "Def 3rd.1": "Press in defense",
    "Mid 3rd.1": "Press in midfield",
    "Att 3rd.1": "Press in attack",
    "Blocks": "Blocked the ball",
    "Pass": "Passes blocked",
    "Int": "Interceptions",
    "Tkl+Int": "Tackles+Interceptions",
    "Clr": "Clearances",
    "Err": "Errors leading to goal",
}
df = df.rename(columns=rename_map)

le = LabelEncoder()                         # Целевая переменная: позиция игрока -> числа
y = le.fit_transform(df["Position"])

features = [
    "Tackles", "Tackles Won",
    "Tackles won in defensive 3rd", "Tackles won in midfield",
    "Tackles won in attacking 3rd",
    "number of times opponent put under pressure", "Successful press",
    "% of successful press",
    "Press in defense", "Press in midfield", "Press in attack",
    "Blocked the ball", "Passes blocked", "Interceptions",
    "Tackles+Interceptions", "Clearances", "Errors leading to goal",
]
features = [f for f in features if f in df.columns]
X = df[features].apply(pd.to_numeric, errors="coerce").fillna(0)


def split(X, y, test_size=0.2):
    # 5. Разбиение; stratify может не сработать при очень редких классах
    try:
        return train_test_split(X, y, test_size=test_size,
                                random_state=42, stratify=y)   # stratify=y -> пропорции классов в train/test будут одинаковыми
    except ValueError:
        return train_test_split(X, y, test_size=test_size, random_state=42)


def run_knn(X, y, n, test_size=0.2, verbose=True):
    X_train, X_test, y_train, y_test = split(X, y, test_size)     # разбиение на train/test

    # kNN чувствителен к масштабу признаков -> стандартизация
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 7. kNN
    knn = KNeighborsClassifier(n_neighbors=n)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)

    # 8. Метрики
    acc = accuracy_score(y_test, y_pred)
    if verbose:
        print(f"Accuracy: {acc:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))
    return acc

n = int(input("Enter n: "))
run_knn(X, y, n)