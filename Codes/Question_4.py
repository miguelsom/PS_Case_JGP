import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy.stats import levene, shapiro, f_oneway
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.stats.diagnostic import acorr_ljungbox

# Constants for series IDs
SERIES_ID_CPI_ALL_ITEMS_SEASONALLY_ADJUSTED = "CUSR0000SA0"
SERIES_ID_CPI_GASOLINE_ALL_TYPES_SEASONALLY_ADJUSTED = "CUSR0000SEGA"








#####          Data Preparation          #####

# Load the CSV data into a DataFrame
df_pivot = pd.read_csv('cpi_data.csv')

# Filter data for the required series
df_filtered = df_pivot[['date', SERIES_ID_CPI_ALL_ITEMS_SEASONALLY_ADJUSTED, SERIES_ID_CPI_GASOLINE_ALL_TYPES_SEASONALLY_ADJUSTED]].copy()

# Convert 'date' column to datetime format
df_filtered['date'] = pd.to_datetime(df_filtered['date'])

# Log-transform the data to stabilize variance and improve normality
# Using log transformation in input values offers several advantages, such as 
# stabilizing variance, linearizing relationships, and reducing the impact of outliers
df_filtered['log_CPI_All_Items'] = np.log(df_filtered[SERIES_ID_CPI_ALL_ITEMS_SEASONALLY_ADJUSTED])
df_filtered['log_Gasoline'] = np.log(df_filtered[SERIES_ID_CPI_GASOLINE_ALL_TYPES_SEASONALLY_ADJUSTED])





#####          Data Validation          #####

# Median analysis
median_all_items = df_filtered['log_CPI_All_Items'].median()
median_gasoline = df_filtered['log_Gasoline'].median()
print(f'\nMedian Log CPI All items: {median_all_items}')
print(f'Median Log Gasoline: {median_gasoline}')

# Plot the data distributions
plt.figure(figsize=(12, 6))

# Histogram for Log CPI All items
plt.subplot(2, 1, 1)
plt.hist(df_filtered['log_CPI_All_Items'], bins=20, alpha=0.7, label='Log CPI All items')
plt.axvline(median_all_items, color='red', linestyle='dashed', linewidth=1)
plt.title('Distribution of Log CPI All items (Seasonally Adjusted)')
plt.xlabel('Log CPI Value')
plt.ylabel('Frequency')
plt.legend()

# Histogram for Log Gasoline
plt.subplot(2, 1, 2)
plt.hist(df_filtered['log_Gasoline'], bins=20, alpha=0.7, label='Log Gasoline')
plt.axvline(median_gasoline, color='red', linestyle='dashed', linewidth=1)
plt.title('Distribution of Log Gasoline (Seasonally Adjusted)')
plt.xlabel('Log CPI Value')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.show()




#####          Linear Regression          #####

# Prepare data for linear regression
X = df_filtered[['log_Gasoline']]
X = sm.add_constant(X)  # Add a constant term to the predictor
y = df_filtered['log_CPI_All_Items']

# Fit the linear regression model
model = sm.OLS(y, X).fit()
predictions = model.predict(X)

# Plot the results
plt.figure(figsize=(12, 6))

# Time series plot
plt.subplot(2, 1, 1)
plt.plot(df_filtered['date'], df_filtered['log_CPI_All_Items'], label='Log All items (SA)')
plt.plot(df_filtered['date'], df_filtered['log_Gasoline'], label='Log Gasoline (SA)', linestyle='--')
plt.title('Log CPI All items vs Log Gasoline (Seasonally Adjusted)')
plt.xlabel('Date')
plt.ylabel('Log CPI Value')
plt.legend()

# Regression plot
plt.subplot(2, 1, 2)
plt.scatter(df_filtered['log_Gasoline'], df_filtered['log_CPI_All_Items'], alpha=0.5, label='Data')
plt.plot(df_filtered['log_Gasoline'], predictions, color='red', label='Regression Line')
plt.title('Relation between Log All items and Log Gasoline')
plt.xlabel('Log Gasoline (SA)')
plt.ylabel('Log All items (SA)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Print the model summary
print(model.summary())









#####           Statistical Tests and Inference           #####

# Calculate and print the Durbin-Watson statistic
# Use the Durbin-Watson (DW) statistic to detect the presence of autocorrelation in the residuals of a regression analysis, ensuring the validity of the model's assumptions.
dw = sm.stats.stattools.durbin_watson(model.resid)
print(f'Durbin-Watson: {dw:.2f}')

# t-test for the coefficients
t_values = model.tvalues
p_values = model.pvalues
coef_summary = pd.DataFrame({
    'Coefficient': model.params,
    'Standard Error': model.bse,
    't-value': t_values,
    'p-value': p_values
})
print("\nStudent's t-test for the coefficients:\n", coef_summary)

# Statistical inference and ETS model
# Fit the ETS model to the CPI All Items data
# Statistical inference and ETS model
# Fit the ETS model to the CPI All Items data
model_ets = ExponentialSmoothing(df_filtered['log_CPI_All_Items'], trend='add', seasonal='add', seasonal_periods=12).fit()

# Make forecasts using the ETS model
steps = 12  # Number of forecast steps
last_date = df_filtered['date'].iloc[-1]
pred_dates = pd.date_range(last_date, periods=steps + 1, freq='ME')[1:]  # Future dates for forecast
pred_ets = model_ets.forecast(steps)

# Manually calculate confidence intervals
forecast_errors = model_ets.fittedvalues - df_filtered['log_CPI_All_Items']
mean_forecast_error = np.mean(forecast_errors)
var_forecast_error = np.var(forecast_errors)

# 95% confidence level
conf_int_upper = pred_ets + 1.96 * np.sqrt(var_forecast_error)
conf_int_lower = pred_ets - 1.96 * np.sqrt(var_forecast_error)

# Plot the forecasts with confidence intervals
plt.figure(figsize=(12, 6))
plt.plot(df_filtered['date'], df_filtered['log_CPI_All_Items'], label='Log CPI All items (SA)')
plt.plot(pred_dates, pred_ets, label='ETS Forecast', color='red')
plt.fill_between(pred_dates, conf_int_lower, conf_int_upper, color='pink', alpha=0.3)
plt.title('ETS Model Forecast for Log CPI All items with 95% Confidence Intervals')
plt.legend()
plt.show()


# Ljung-Box test for autocorrelation in the residuals
lb_test = acorr_ljungbox(model.resid, lags=[12], return_df=True)
print("\nLjung-Box test for autocorrelation in residuals:\n", lb_test)

# Analysis of Variance (ANOVA)
anova_results = f_oneway(df_filtered['log_CPI_All_Items'], df_filtered['log_Gasoline'])
print(f'\nANOVA F-statistic: {anova_results.statistic}, p-value: {anova_results.pvalue}')



# Levene's test for homogeneity of variances
levene_test = levene(df_filtered['log_CPI_All_Items'], df_filtered['log_Gasoline'])
print(f'\nLevene’s test for homogeneity of variances: Statistic={levene_test.statistic}, p-value={levene_test.pvalue}')

# Shapiro-Wilk test for normality
shapiro_test_all_items = shapiro(df_filtered['log_CPI_All_Items'])
shapiro_test_gasoline = shapiro(df_filtered['log_Gasoline'])
print(f'\nShapiro-Wilk test for Log CPI All items: Statistic={shapiro_test_all_items.statistic}, p-value={shapiro_test_all_items.pvalue}')
print(f'Shapiro-Wilk test for Log Gasoline: Statistic={shapiro_test_gasoline.statistic}, p-value={shapiro_test_gasoline.pvalue}')




