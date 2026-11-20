import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import (train_test_split, ParameterGrid, GridSearchCV,
                                     StratifiedKFold, cross_val_score)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, classification_report,
                             confusion_matrix, roc_curve, roc_auc_score,
                             precision_score, recall_score)

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

le = LabelEncoder()
y = le.fit_transform(df["Position"])

# ============ ЧАСТЬ I ============

# ---- 1. Разбиение на train / validation / test (60% / 20% / 20%) ----
# Датасет небольшой (~600 строк), поэтому 60/20/20 - нормальное соотношение
def safe_split(X, y, test_size):
    # stratify не работает, если в каком-то классе меньше 2 объектов
    try:
        return train_test_split(X, y, test_size=test_size,
                                random_state=42, stratify=y)
    except ValueError:
        return train_test_split(X, y, test_size=test_size, random_state=42)

X_temp, X_test, y_temp, y_test = safe_split(X, y, 0.2)        # сначала отрезаем test (20%)
X_train, X_val, y_train, y_val = safe_split(X_temp, y_temp, 0.25)  # 0.25 от 80% = 20% всего

print("Размеры выборок:")
print("train:", X_train.shape[0], " val:", X_val.shape[0], " test:", X_test.shape[0])

# ---- 5. Баланс классов ----
print("\n=== Баланс классов (Position) ===")
counts = df["Position"].value_counts()
print(counts)
print("\nДоли классов, %:")
print((counts / counts.sum() * 100).round(1))

plt.figure(figsize=(9, 4))
counts.plot(kind="bar", color="steelblue")
plt.title("Class balance: Position")
plt.xlabel("Position")
plt.ylabel("Number of players")
plt.tight_layout()
plt.show()

# ---- 2-3. Дерево решений с параметрами по умолчанию ----
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)
print("\nДерево по умолчанию: F1 (weighted) на validation =",
      round(f1_score(y_val, tree.predict(X_val), average="weighted", zero_division=0), 3))

# ---- 4. Подбор гиперпараметров ----
# Подход 1: перебор по сетке (Grid Search), оценка на validation-выборке
param_grid = {
    "criterion": ["gini", "entropy"],
    "max_depth": [None, 3, 5, 7, 10],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 5],
}

results = []
for params in ParameterGrid(param_grid):
    model = DecisionTreeClassifier(random_state=42, **params)
    model.fit(X_train, y_train)
    f1_tr = f1_score(y_train, model.predict(X_train), average="weighted", zero_division=0)
    f1_va = f1_score(y_val, model.predict(X_val), average="weighted", zero_division=0)
    results.append({**params, "train_f1": f1_tr, "val_f1": f1_va})

res_df = pd.DataFrame(results).sort_values("val_f1", ascending=False)
print("\n=== Топ-10 комбинаций гиперпараметров (по F1 на validation) ===")
print(res_df.head(10).round(3).to_string(index=False))

best_params = res_df.iloc[0][["criterion", "max_depth", "min_samples_split",
                              "min_samples_leaf"]].to_dict()
# max_depth после DataFrame мог стать float/NaN -> приводим обратно
md = best_params["max_depth"]
best_params["max_depth"] = None if pd.isna(md) else int(md)
best_params["min_samples_split"] = int(best_params["min_samples_split"])
best_params["min_samples_leaf"] = int(best_params["min_samples_leaf"])
print("\nЛучшие параметры:", best_params)

# Влияние max_depth на качество (переобучение / недообучение)
depths = list(range(1, 21))
tr_scores, va_scores = [], []
for d in depths:
    m = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)
    tr_scores.append(f1_score(y_train, m.predict(X_train), average="weighted", zero_division=0))
    va_scores.append(f1_score(y_val, m.predict(X_val), average="weighted", zero_division=0))

plt.figure(figsize=(7, 4))
plt.plot(depths, tr_scores, label="train")
plt.plot(depths, va_scores, label="validation")
plt.xlabel("max_depth")
plt.ylabel("F1 (weighted)")
plt.title("Impact of max_depth")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Подход 2: GridSearchCV (перебор + кросс-валидация на train+val)
X_trval = pd.concat([X_train, X_val])
y_trval = np.concatenate([y_train, y_val])
gs = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid,
                  scoring="f1_weighted", cv=StratifiedKFold(5, shuffle=True, random_state=42))
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")   # предупреждение о редких классах
    gs.fit(X_trval, y_trval)
print("\nGridSearchCV (5-fold) лучшие параметры:", gs.best_params_)
print("GridSearchCV лучший CV F1:", round(gs.best_score_, 3))
# Другие подходы: RandomizedSearchCV (случайный перебор), Bayesian optimization (Optuna)

# ---- 6. Оценка лучшей модели на test ----
best_tree = DecisionTreeClassifier(random_state=42, **best_params)
best_tree.fit(X_train, y_train)
y_pred = best_tree.predict(X_test)

print("\n=== Лучшая модель (дерево решений) на TEST ===")
print("Best Model:", best_tree)
print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("F1 (weighted):", round(f1_score(y_test, y_pred, average="weighted", zero_division=0), 3))
print("F1 (macro):", round(f1_score(y_test, y_pred, average="macro", zero_division=0), 3))
print("\nClassification Report:")
labels = np.unique(np.concatenate([y_test, y_pred]))
print(classification_report(y_test, y_pred, labels=labels,
                            target_names=le.classes_[labels], zero_division=0))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred, labels=labels))

# ---- 7. Сравнение kNN и дерева решений ----
# Подбираем k для kNN на validation
best_k, best_k_f1 = 1, -1
for k in range(1, 26):
    knn_pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    knn_pipe.fit(X_train, y_train)
    f = f1_score(y_val, knn_pipe.predict(X_val), average="weighted", zero_division=0)
    if f > best_k_f1:
        best_k, best_k_f1 = k, f
print("\nЛучшее k для kNN:", best_k)

knn_best = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=best_k))
knn_best.fit(X_train, y_train)
knn_pred = knn_best.predict(X_test)

print("\n=== Сравнение на test-выборке ===")
print("kNN  : accuracy =", round(accuracy_score(y_test, knn_pred), 3),
      " F1 weighted =", round(f1_score(y_test, knn_pred, average="weighted", zero_division=0), 3),
      " F1 macro =", round(f1_score(y_test, knn_pred, average="macro", zero_division=0), 3))
print("Tree : accuracy =", round(accuracy_score(y_test, y_pred), 3),
      " F1 weighted =", round(f1_score(y_test, y_pred, average="weighted", zero_division=0), 3),
      " F1 macro =", round(f1_score(y_test, y_pred, average="macro", zero_division=0), 3))

# Кросс-валидация: даёт более надёжное сравнение, чем один train/test split
# (особенно на маленьком датасете с редкими классами). Масштабирование внутри pipeline,
# чтобы не было утечки данных.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
X_all_tv, y_all_tv = X_trval, y_trval
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    knn_cv = cross_val_score(knn_best, X_all_tv, y_all_tv, cv=cv, scoring="f1_weighted")
    tree_cv = cross_val_score(DecisionTreeClassifier(random_state=42, **best_params),
                              X_all_tv, y_all_tv, cv=cv, scoring="f1_weighted")
print("\n=== Кросс-валидация (5-fold, F1 weighted) ===")
print("kNN :", knn_cv.round(3), " mean =", round(knn_cv.mean(), 3), " std =", round(knn_cv.std(), 3))
print("Tree:", tree_cv.round(3), " mean =", round(tree_cv.mean(), 3), " std =", round(tree_cv.std(), 3))
print("Лучший по CV:", "kNN" if knn_cv.mean() > tree_cv.mean() else "Decision Tree")

# ============ ЧАСТЬ II: FW vs MF ============
print("\n\n=============== ЧАСТЬ II: FW vs MF ===============")

# ---- 1. Берём только FW и MF, анализ баланса ----
df2 = df[df["Position"].isin(["FW", "MF"])].copy()
X2 = df2[features].apply(pd.to_numeric, errors="coerce").fillna(0)
y2 = (df2["Position"] == "FW").astype(int)    # FW = 1 (положительный класс), MF = 0

print("Баланс классов:")
print(df2["Position"].value_counts())
print((df2["Position"].value_counts(normalize=True) * 100).round(1))

# ---- 2. Классификация (логистическая регрессия, нужны вероятности) ----
X2_train, X2_test, y2_train, y2_test = train_test_split(
    X2, y2, test_size=0.3, random_state=42, stratify=y2)

clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
clf.fit(X2_train, y2_train)

y2_pred = clf.predict(X2_test)          # порог по умолчанию 0.5
y2_proba = clf.predict_proba(X2_test)[:, 1]   # вероятность класса FW

print("\nClassification Report (порог 0.5):")
print(classification_report(y2_test, y2_pred, target_names=["MF", "FW"], zero_division=0))
print("Confusion matrix:")
print(confusion_matrix(y2_test, y2_pred))

# ---- 3. ROC-кривая ----
fpr, tpr, thresholds = roc_curve(y2_test, y2_proba)
auc_val = roc_auc_score(y2_test, y2_proba)
print("AUC =", round(auc_val, 3))

plt.figure(figsize=(6, 6))
plt.plot(fpr, tpr, color="blue", label=f"ROC Curve (AUC = {auc_val:.2f})")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve for FW vs MF Classification")
plt.legend(loc="lower right")
plt.tight_layout()
plt.show()
# Интерпретация: чем ближе кривая к левому верхнему углу и чем больше AUC (макс. 1),
# тем лучше модель разделяет классы. Диагональ (AUC = 0.5) - случайное угадывание.

# ---- 4. Оценка при разных порогах ----
print("\n=== Метрики при разных порогах ===")
rows = []
for t in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    pred_t = (y2_proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y2_test, pred_t, labels=[0, 1]).ravel()
    rows.append({
        "threshold": t,
        "accuracy": accuracy_score(y2_test, pred_t),
        "precision": precision_score(y2_test, pred_t, zero_division=0),
        "recall(TPR)": recall_score(y2_test, pred_t, zero_division=0),
        "FPR": fp / (fp + tn) if (fp + tn) > 0 else 0,
        "F1": f1_score(y2_test, pred_t, zero_division=0),
    })
print(pd.DataFrame(rows).round(3).to_string(index=False))

# Оптимальный порог по индексу Юдена (J = TPR - FPR)
best_idx = np.argmax(tpr - fpr)
print("\nОптимальный порог (Youden J):", round(thresholds[best_idx], 3),
      " TPR =", round(tpr[best_idx], 3), " FPR =", round(fpr[best_idx], 3))
# Чем ниже порог -> выше recall, но больше ложных срабатываний (FPR);
# чем выше порог -> выше precision, но recall падает.