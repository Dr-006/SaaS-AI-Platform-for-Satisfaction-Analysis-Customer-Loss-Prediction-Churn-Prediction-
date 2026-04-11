import pandas as pd

def preprocess(df: pd.DataFrame, selected_features: list):

    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

    df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    return df_encoded.reindex(columns=selected_features, fill_value=0)