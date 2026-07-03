import plotly.express as px


def age_chart(df):
    return px.bar(
        df,
        x="Name",
        y="Age",
        color="Age",
        title="Age Distribution"
    )


def salary_chart(df):
    return px.pie(
        df,
        names="Name",
        values="Salary",
        title="Salary Distribution"
    )


def salary_line_chart(df):
    return px.line(
        df,
        x="Name",
        y="Salary",
        markers=True,
        title="Salary Trend"
    )


def city_chart(df):
    return px.histogram(
        df,
        x="City",
        color="City",
        title="Employees by City"
    )