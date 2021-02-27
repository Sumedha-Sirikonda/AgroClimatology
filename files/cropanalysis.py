import pandas as pd
import datetime as dt
import bottleneck as bn
import matplotlib.pyplot as plt
import seaborn as sns


# def load_data(csv):
dataset = pd.read_csv("united_states_of_america_maize_s1.csv")
dataset.head()


# def manipulate_data(dataset):
dataset = dataset.drop("Unnamed: 0", axis=1)
dataset["datetime"] = pd.to_datetime(dataset["datetime"], format="%Y-%m-%d")
dataset["Year"] = dataset["Year"].astype(int)
dataset["Month"] = dataset["Month"].astype(int)
dataset["Day"] = dataset["Day"].astype(int)

# def impute_data(feature):
cropCalDF = dataset[dataset["crop_cal"].isin([1.0, 2.0, 3.0])]

# Imputing Missing values to check if this makes any difference.
cropCalDF['ndvi'].fillna(cropCalDF['ndvi'].mean(), inplace=True)

"""  
    The requirement is to get the  average mean values of
    any particular variable, for a given date. We calculated 
    average mean of years in the past.The function segments the
    original dataset based on state first and then day and Month,
    then get the dates in the year range. Calculate average mean 
    of the selected column and return to the user
"""
def climatology(col_name, state, date, noYear):
    state = state.lower()

    inMon = date.month
    inDay = date.day
    inyear = date.year
    
    
    try:
        byState = cropCalDF[cropCalDF.adm1_name == state]
        if (noYear>5):
            pastyear = inyear - noYear
        else:
            raise Exception("Calculate atleast for 5 years")
        byDate = byState[
            (byState.Day == inDay)
            & (byState.Month == inMon)
            & ((byState.Year <= inyear) & (byState.Year > pastyear))
        ]
        if byDate.empty:
            raise Exception("No data found for this date")
        byColumn = byDate[col_name].mean()
        return byColumn
    except Exception as e:
        print(e)


def graphics(cropCalDF, state, year, features):
    cropcal = cropCalDF.copy()
    #     Get the required years details based the state and the year
    current_time = cropcal[(cropcal.adm1_name == state) & (cropcal.Year == year)]
    #     Calculate Climatology for past 5 years for every date in the time series
    new_val = [climatology(features, state, date, 5) for date in current_time.datetime]
    #     Scale it down as per NDVI requirement --> just a test setting
    toScale = [((x - 50) / 200) for x in new_val]
    #     Scale down NDVI requirement --> test setting
    current_time[features] = [((x - 50) / 200) for x in current_time[features]]
    #     Assigning scaled climatology value to a new column in the dataframe
    current_time[features + "_Climatology"] = toScale

    #     Calculate moving mean with 5 day window and minimum count =1 for both Feature and Climatology setting
    rm_ndvi = bn.move_mean(current_time[features], window=5, min_count=1)
    rmc_ndvi = bn.move_mean(
        current_time[features + "_Climatology"], window=5, min_count=1
    )

    #     Plot graphs using Matplotlib Library.
    plt.figure(figsize=(14, 7))
    plt.plot(current_time.datetime, rm_ndvi, "b", label=features)
    plt.plot(current_time.datetime, rmc_ndvi, "g", label=features + "_Cimatology")
    plt.title("NDVI and 5 year Climatology for {}".format(state))
    plt.xlabel("Date")
    plt.ylabel("NDVI")
    plt.legend()

    plt.show()


if __name__ == "main":
    url = "united_states_of_america_maize_s1.csv"
    # data = load_data(url)
    # manipulate_data(data)
    impute_data('ndvi')
    graphics(data, "alabama", 2019, "ndvi")
