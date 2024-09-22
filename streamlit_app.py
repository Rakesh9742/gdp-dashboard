import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
data = pd.read_csv('NIRF20.3 - nirf1234.csv')

# Convert Institute column to string and remove NaN or non-string values
data['Institute'] = data['Institute'].astype(str)
data = data[data['Institute'].notna() & data['Institute'] != 'nan']

# Sort institutes alphabetically
sorted_institutes = sorted(data['Institute'].unique())

# Streamlit app
st.title('Institute Performance Dashboard')

# Dropdown for selecting institute
selected_institute = st.selectbox('Select Institute:', sorted_institutes)

# Dropdown for selecting view option
view_option = st.selectbox(
    'Select View:',
    ['Institute Info', 'Year-wise Graphs', 'Rank Impact Analysis'],
    index=1  # Default to 'Year-wise Graphs'
)

# Function to display institute data
def display_institute_data(institute, view_option):
    if institute:
        # Filter data for the selected institute
        institute_data = data[data['Institute'] == institute]

        if view_option == 'Institute Info':
            # Display the Institute Rank and Year
            rank_year_data = institute_data[['Year', 'Rank']]
            st.subheader(f"Rank and Year for {institute}")
            st.dataframe(rank_year_data)

        elif view_option == 'Year-wise Graphs':
            # Plot year-wise trends for each parameter
            parameters = ['SS', 'FSR', 'FQE', 'FRU', 'PU', 'QP', 'IPR', 'FPPP', 'GPH', 'GUE', 'MS', 'GPHD', 'RD', 'WD', 'ESCS', 'PCS', 'PR']

            for param in parameters:
                plt.figure(figsize=(8, 5))
                sns.lineplot(x='Year', y=param, data=institute_data, marker='o')
                plt.title(f'Year-wise trend of {param} for {institute}')
                st.pyplot(plt)
                plt.clf()

        elif view_option == 'Rank Impact Analysis':
            # Perform correlation analysis between rank and other parameters
            parameters = ['SS', 'FSR', 'FQE', 'FRU', 'PU', 'QP', 'IPR', 'FPPP', 'GPH', 'GUE', 'MS', 'GPHD', 'RD', 'WD', 'ESCS', 'PCS', 'PR']

            # Check if Rank and Parameters have numeric data
            institute_data_numeric = institute_data[['Rank'] + parameters].dropna()
            if not institute_data_numeric.empty:
                correlation = institute_data_numeric.corr()['Rank'].drop('Rank')

                # Select only high impact correlations (absolute value > 0.5)
                high_impact = correlation[abs(correlation) > 0.5].sort_values(ascending=False)

                if not high_impact.empty:
                    # Display correlation values in a simple bar chart
                    plt.figure(figsize=(8, 5))
                    sns.barplot(x=high_impact.index, y=high_impact.values, palette="coolwarm")
                    plt.xticks(rotation=45, ha='right')
                    plt.title(f'Parameters Impacting Rank for {institute}')
                    plt.ylabel('Correlation with Rank')
                    st.pyplot(plt)

                    # Interpretation for user
                    st.subheader(f"Parameters with strong impact on rank for {institute}")
                    for param, value in high_impact.items():
                        impact_type = "positive" if value > 0 else "negative"
                        st.write(f" - {param}: {impact_type} impact (correlation: {value:.2f})")
                else:
                    st.write(f"No significant parameters impacting the rank for {institute} (correlation threshold: 0.5).")
            else:
                st.write(f"No numerical data available for correlation analysis for {institute}.")

# Call the function to display data
display_institute_data(selected_institute, view_option)
