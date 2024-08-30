import pandas as pd

# >> Load your CSV file
mos_df = pd.read_csv('../data_release/ground_truth.csv')

# Define the function to categorize MOS
def categorize_mos(mos):
    if mos < 0.33:
        return 'Low'
    elif mos < 0.66:
        return 'Medium'
    else:
        return 'High'

# Apply the function to create a new column with categories
mos_df['AesA1_Score'] = mos_df['MOS'].apply(categorize_mos)

# Display the original and categorized MOS values
print(mos_df[['MOS', 'AesA1_Score']].head())

# Optionally, you can save the updated dataframe with the new Category column
mos_df.to_csv('../data_release/ground_truth_AesA1.csv', index=False)