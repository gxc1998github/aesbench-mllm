import pandas as pd

# Load the CSV file from the specified location
mos_df = pd.read_csv('../data_release/mos_ground_truth.csv')

# Define the function to categorize MOS
def categorize_mos(mos):
    if mos < 0.33:
        return 'Low'
    elif mos <= 0.66:
        return 'Medium'
    else:
        return 'High'

# Apply the transformations
mos_df['AesA3_Score'] = (1 + 9 * mos_df['MOS']).round(4)  # Scale 1-10 with 4 decimal places
mos_df['AesA2_Score'] = (1 + 4 * mos_df['MOS']).round(4)  # Scale 1-5 with 4 decimal places
mos_df['AesA1_Score'] = mos_df['MOS'].apply(categorize_mos)  # Categorisation

# Save the updated dataframe to the specified location
mos_df.to_csv('../data_release/ground_truth.csv', index=False)