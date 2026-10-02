import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

def load_data(train_path, test_path):
    # Load datasets
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    # Clean data
    train_df = clean_data(train_df)
    test_df = clean_data(test_df)

    # Split features and labels
    X_train = train_df.drop("prognosis", axis=1)
    y_train = train_df["prognosis"]

    X_test = test_df.drop("prognosis", axis=1)
    y_test = test_df["prognosis"]

    # Encode labels
    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train)
    y_test = encoder.transform(y_test)

    return X_train, X_test, y_train, y_test, encoder