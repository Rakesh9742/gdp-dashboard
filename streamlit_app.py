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

# Streamlit app layout
st.title("Institute Data Analysis")

# Dropdown for selecting institute
institute = st.selectbox('Select Institute', sorted_institutes)

# Dropdown for selecting view option (either show institution info, year-wise graphs, or rank impact analysis)
view_option = st.selectbox(
    'Select View Option', 
    ['Institute Info', 'Year-wise Graphs', 'Rank Impact Analysis'],
    index=1  # Default view is 'Year-wise Graphs'
)

# List of parameters
parameters = ['SS', 'FSR', 'FQE', 'FRU', 'PU', 'QP', 'IPR', 'FPPP', 'GPH', 'GUE', 'MS', 'GPHD', 'RD', 'WD', 'ESCS', 'PCS', 'PR']

# Dropdown for selecting parameter
selected_param = st.selectbox('Select Parameter', parameters, index=0)

# Function to display either institute info (Rank and Year) or perform rank impact analysis
def display_institute_data(institute, view_option, selected_param):
    if institute:
        # Filter data for the selected institute
        institute_data = data[data['Institute'] == institute]

        if view_option == 'Institute Info':
            # Display the Institute Rank and Year
            rank_year_data = institute_data[['Year', 'Rank']]
            st.write(f"Rank and Year for {institute}:")
            st.dataframe(rank_year_data)

        elif view_option == 'Year-wise Graphs':
            # Plot year-wise trend for the selected parameter
            plt.figure(figsize=(8, 5))
            sns.lineplot(x='Year', y=selected_param, data=institute_data, marker='o')
            plt.title(f'Year-wise trend of {selected_param} for {institute}')
            plt.tight_layout()
            st.pyplot(plt)

        elif view_option == 'Rank Impact Analysis':
            # Perform correlation analysis between rank and the selected parameter
            institute_data_numeric = institute_data[['Rank', selected_param]].dropna()
            if not institute_data_numeric.empty:
                correlation = institute_data_numeric.corr().loc['Rank', selected_param]

                # Interpretation for user
                impact_type = "positive" if correlation > 0 else "negative"
                st.write(f"{selected_param} has a {impact_type} impact on the rank for {institute}.")
                st.write(f"Correlation value: {correlation:.2f}")

                # Provide reasons based on correlation value
                if correlation > 0:
                    st.write(f"A positive correlation means that as {selected_param} increases, the rank also tends to increase.")
                elif correlation < 0:
                    st.write(f"A negative correlation means that as {selected_param} increases, the rank tends to decrease.")
                else:
                    st.write(f"No significant correlation between {selected_param} and rank for {institute}.")
            else:
                st.write(f"No numerical data available for correlation analysis for {institute}.")

# Display the results based on selected options
display_institute_data(institute, view_option, selected_param)

