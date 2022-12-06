import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from linearmodels import IV2SLS

with open('Fulton_fish_market_data.txt') as infile:
    # Read space-delimited file and replace all empty spaces by commas
    data = infile.read().replace(' ', ',')
    # Write the CSV data in the output file
    print(data, file=open('my_file.csv', 'w'))




df = pd.read_csv("my_file.csv", sep="\t")

x= df["price"]
y= df["qty"]

plt.scatter(x,y)
plt.xlabel("Log of Price")
plt.ylabel("Log of Quantity")
plt.title("Quantity and price")
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.show()





# OLS estimation
X= np.asarray(x).reshape(-1, 1)
Y= np.asarray(y).reshape(-1, 1)
model = LinearRegression()
reg = model.fit(X, Y)
print(reg.score(X, Y))
print(reg.coef_)
print(reg.intercept_)



# IV Estimation
iv_reg = IV2SLS.from_formula("qty ~ 1 + [price ~ stormy]", df).fit()
print(iv_reg.summary)