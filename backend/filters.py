def filter_city(df, city):

    if city == "All":
        return df

    return df[df["City"] == city]