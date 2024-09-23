import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
data = pd.read_csv('NIRF20.3 - nirf1234.csv')
# Convert Institute column to string and remove NaN or non-string values including "nan"
data['Institute'] = data['Institute'].astype(str)
data = data[data['Institute'].notna() & data['Institute'] != 'nan']

# Sort institutes alphabetically and remove "nan" from the dropdown
sorted_institutes = sorted(data['Institute'].unique())

# Streamlit app layout
st.title("Institute Data Analysis")

# Create separate menu for Institute Info
menu = ['Institute Info', 'Data Analysis']
selected_menu = st.selectbox("Select Menu", menu)

# Dropdown for selecting institute
institute = st.selectbox('Select Institute', sorted_institutes)

# List of parameters
parameters = ['SS', 'FSR', 'FQE', 'FRU', 'PU', 'QP', 'IPR', 'FPPP', 'GPH', 'GUE', 'MS', 'GPHD', 'RD', 'WD', 'ESCS', 'PCS', 'PR']

# Dropdown for selecting parameter
if selected_menu == 'Data Analysis':
    view_option = st.selectbox(
        'Select View Option',
        ['Year-wise Graphs', 'Rank Impact Analysis'],
        index=0  # Default view is 'Year-wise Graphs'
    )
    selected_param = st.selectbox('Select Parameter', parameters, index=0)

# Function to display year-wise graph or rank impact analysis
def display_institute_data(institute, view_option, selected_param):
    if institute:
        # Filter data for the selected institute
        institute_data = data[data['Institute'] == institute]

        if view_option == 'Year-wise Graphs':
            # Sort by Year but keep the original parameter values
            institute_data = institute_data.sort_values('Year')

            # Convert the selected parameter column to numeric, forcing errors to NaN
            institute_data[selected_param] = pd.to_numeric(institute_data[selected_param], errors='coerce')

            # Drop rows with NaN values in the selected parameter column
            institute_data = institute_data.dropna(subset=[selected_param])

            # Ensure we have valid data to plot
            if not institute_data.empty:
                plt.figure(figsize=(8, 5))
                sns.lineplot(x='Year', y=selected_param, data=institute_data, marker='o')

                # Ensure x-axis is sorted by Year, y-axis shows actual values
                plt.xticks(sorted(institute_data['Year'].unique()))  # Ensure x-axis is in increasing order
                plt.title(f'Year-wise trend of {selected_param} for {institute}')
                
                # Correct the y-axis scaling and ensure no misrepresentation
                plt.ylim(institute_data[selected_param].min() - 0.5, institute_data[selected_param].max() + 0.5)
                plt.yticks(sorted(institute_data[selected_param].unique()))  # Ensure y-axis shows correct values

                plt.tight_layout()
                st.pyplot(plt)
            else:
                st.write(f"No valid data to display for {selected_param} in {institute}.")

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

# Function to display institute rank and year info
def display_institute_info(institute):
    if institute:
        # Filter data for the selected institute
        institute_data = data[data['Institute'] == institute]
        
        # Select only 'Year' and 'Rank' columns and sort by 'Year'
        rank_year_data = institute_data[['Year', 'Rank']].sort_values('Year')
        
        # Reset index to remove index column
        rank_year_data = rank_year_data.reset_index(drop=True)
        
        # Display the filtered data as a table with only 'Year' and 'Rank'
        st.write(f"Rank and Year for {institute}:")
        st.dataframe(rank_year_data, use_container_width=True)  # Use Streamlit dataframe for a clean display

# Display based on selected menu
if selected_menu == 'Data Analysis':
    display_institute_data(institute, view_option, selected_param)
elif selected_menu == 'Institute Info':
    display_institute_info(institute)

