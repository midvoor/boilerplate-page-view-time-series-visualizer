import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=["date"])
df=df.set_index('date')

# Clean data
df = df[df["value"].between(
    df["value"].quantile(0.025),
    df["value"].quantile(0.975)
)]


def draw_line_plot():
    # Draw line plot
    df_copy = df.copy()
    fig,ax=plt.subplots()
    ax.plot(df_copy.index, df_copy["value"])
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    df_grouped = df_bar.groupby(["year", "month"], as_index=False)["value"].mean()
    df_grouped.rename(columns={"value": "monthly_avg"}, inplace=True)
    df_pivot = df_grouped.pivot(index="year", columns="month", values="monthly_avg")
    month_map = {1: "January", 2: "February", 3: "March", 4: "April",
             5: "May", 6: "June", 7: "July", 8: "August",
             9: "September", 10: "October", 11: "November", 12: "December"}
    df_pivot.columns = df_pivot.columns.map(month_map)

    # Draw bar plot
    fig, ax = plt.subplots()
    df_pivot.plot(kind="bar", ax=ax)
    ax.set_title("Monthly Average Page Views by Year")
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    ax.legend(title="Months")


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]

    fig, axes = plt.subplots(1, 2, figsize=(15,6))

    # -------------------------
    # Year-wise box plot
    # -------------------------
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # -------------------------
    # Month-wise box plot
    # -------------------------
    sns.boxplot(x="month", y="value", data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
