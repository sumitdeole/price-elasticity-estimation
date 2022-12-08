import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from linearmodels import IV2SLS

with open('Fulton_fish_market_dataset.txt') as infile:
    # Read space-delimited file and replace all empty spaces by commas
    data = infile.read().replace(' ', ',')
    # Write the CSV data in the output file
    print(data, file=open('my_file.csv', 'w'))

# Open the dataframe
df = pd.read_csv("my_file.csv", sep="\t")


# Indicate the variables of interest
x= df["price"]
y= df["qty"]

# Let's try to understand the price-quantity relationship
plt.scatter(df["price"], df["qty"])
plt.xlabel("Log of Price")
plt.ylabel("Log of Quantity")
plt.title("Quantity and price")
plt.plot(np.unique(df["price"]), np.poly1d(np.polyfit(df["price"], df["qty"], 1))(np.unique(df["price"])))
plt.show()

# A simple scatterplot suggests a weak negative relationship.
# However, it is not as informative given no consideration to the time dimension of the data
# Let's plot a time series evolution of quantity-price observations
df.groupby('date').agg({'qty': 'sum', 'price': 'sum'}).plot(title='number of items sold and revenue over time', secondary_y='price',figsize=(16, 5))
# The relationship is not so straightforward as many observations in the middle

# Let's skip earlier data points to get a rather smooth time series
df1=df.loc[df["date"]>911231] #we lose 21 observations
df1.groupby('date').agg({'qty': 'sum', 'price': 'sum'}).plot(title='number of items sold and revenue over time', secondary_y='price',figsize=(16, 5))
# In contrast to the earlier observation, this graph suggests a strong negative relationship between price and quantity




# Now let's study the relationship more formally
# Linear Regression Model
# add an intercept to our model (beta_0)
df['const'] = 1

# Fit ols and print summary
results_ols = sm.OLS(df['qty'],
                    df[['const', 'price']]).fit()
print(results_ols.summary())



plt.scatter(df["stormy"], df["price"])
plt.xlabel("Log of Price")
plt.ylabel("Log of Quantity")
plt.title("Quantity and price")
plt.plot(np.unique(df["stormy"]), np.poly1d(np.polyfit(df["stormy"], df["stormy"], 1))(np.unique(df["stormy"])))
plt.show()

# Fit the first stage regression and print summary
results_fs = sm.OLS(df['price'],
                    df[['const', 'stormy']],
                    missing='drop').fit()
print(results_fs.summary())


# Add a constant variable
results_iv = IV2SLS(dependent=df['qty'],
            exog=df['const'],
            endog=df['price'],
            instruments=df['stormy']).fit(cov_type='unadjusted')
print(results_iv.summary)



