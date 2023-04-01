import pandas as pd
import numpy as np

# Generate random predicted data for temp_data
temp_index = pd.date_range(start='2023-04-01', periods=6, freq='4H', tz='Africa/Lagos')
temp_data = pd.Series(np.random.randn(6), index=temp_index)

# Generate random predicted data for hum_data
hum_index = pd.date_range(start='2023-04-01', periods=6, freq='4H', tz='Africa/Lagos')
hum_data = pd.Series(np.random.randn(6), index=hum_index)

# Merge the predicted data into a single DataFrame
preds = pd.concat([temp_data, hum_data], axis=1)

# Save the predicted data to a CSV file
preds.to_csv('predicted/predictions.csv')

print(preds)