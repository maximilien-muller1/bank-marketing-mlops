
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

from mlops_projet.data.load import load_bank_data
from mlops_projet.features.build import build_features, build_target


def main():
    df = load_bank_data()

    X = build_features(df)
    y = build_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    categories = X.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()

    preprocessing = ColumnTransformer(
        [
            ("categories", OneHotEncoder(handle_unknown="ignore"), categories)
        ],
        remainder="passthrough"
    )

    model = Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        ))
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilites = model.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, predictions))
    print("ROC AUC :", roc_auc_score(y_test, probabilites))


if __name__ == "__main__":
    main()
