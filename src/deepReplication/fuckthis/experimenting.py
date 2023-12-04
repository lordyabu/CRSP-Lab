import pandas as pd

# Create or load your DataFrame
# Example data:

df = pd.read_csv('replicationresults.csv')
# Get unique identifiers
identifiers = df['Identifier'].unique()

model_order = ['Naive', 'Naive Bayes', 'Log Reg', 'KNN', 'RFC', 'NN']
split_order = ['10_10_80', '10_80_10', '80_10_10', '34_33_33']

column_rename_mapping = {
    '10_10_80': 'split1',
    '10_80_10': 'split2',
    '80_10_10': 'split3',
    '34_33_33': 'split4'
}
# Replace values and convert to percentages for specific columns
columns_to_convert = ['Accuracy Test', 'Precision Test', 'Specificity Test', 'Recall Test']
for column in columns_to_convert:
    df[column] = df[column].apply(lambda x: f'{x:.2%}' if isinstance(x, (float, int)) else x)

# Create separate DataFrames for each identifier
dfs = {}
for identifier in identifiers:
    identifier_df = df[df['Identifier'] == identifier]
    accuracy_df = identifier_df.pivot(index='Model', columns='Split', values='Accuracy Test')
    precision_df = identifier_df.pivot(index='Model', columns='Split', values='Precision Test')
    specificity_df = identifier_df.pivot(index='Model', columns='Split', values='Specificity Test')
    recall_df = identifier_df.pivot(index='Model', columns='Split', values='Recall Test')
    dfs[identifier] = {
        'Accuracy': accuracy_df,
        'Precision': precision_df,
        'Specificity': specificity_df,
        'Recall': recall_df,
    }

# Save each DataFrame to separate Excel files
for identifier, tables in dfs.items():
    for metric, table_df in tables.items():
        # Fix the ordering for table_df
        dfs[identifier][metric] = table_df.applymap(lambda x: f'{x:.2%}' if isinstance(x, (float, int)) else x)

        table_df = table_df.loc[model_order]
        table_df = table_df[split_order]
        table_df.columns = ['Split 1', 'Split 2', 'Split 3', 'Split 4']

        # Save the corrected table to an Excel file
        file_name = f"{identifier}_{metric}_table.xlsx"
        table_df.to_excel(file_name)
