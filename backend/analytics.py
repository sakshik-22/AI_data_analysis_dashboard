def total_rows(df):
    return df.shape[0]


def total_columns(df):
    return df.shape[1]


def missing_values(df):
    return df.isnull().sum().sum()


def average_age(df):
    if "Age" in df.columns:
        return round(df["Age"].mean(), 2)
    return 0


def average_salary(df):
    if "Salary" in df.columns:
        return round(df["Salary"].mean(), 2)
    return 0