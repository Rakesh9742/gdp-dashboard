import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Load dataset
data = pd.read_csv('NIRF20.3 - nirf1234.csv')

# Convert Institute column to string and remove NaN or non-string values
data['Institute'] = data['Institute'].astype(str)
data = data[data['Institute'].notna() & data['Institute'] != 'nan']

# Sort institutes alphabetically
sorted_institutes = sorted(data['Institute'].unique())

# Dropdown for selecting institute
institute_dropdown = widgets.Dropdown(
    options=sorted_institutes,
    description='Institute:',
    value=None,
)

# Dropdown for selecting view option (either show institution info, year-wise graphs, or rank impact analysis)
view_dropdown = widgets.Dropdown(
    options=['Institute Info', 'Year-wise Graphs', 'Rank Impact Analysis'],
    description='View:',
    value='Year-wise Graphs',  # Default view is 'Year-wise Graphs'
)

# List of parameters
parameters = ['SS', 'FSR', 'FQE', 'FRU', 'PU', 'QP', 'IPR', 'FPPP', 'GPH', 'GUE', 'MS', 'GPHD', 'RD', 'WD', 'ESCS', 'PCS', 'PR']

# Dropdown for selecting parameter
parameter_dropdown = widgets.Dropdown(
    options=parameters,
    description='Parameter:',
    value='SS',  # Default parameter is 'SS'
)

# Function to display either institute info (Rank and Year) or perform rank impact analysis
def display_institute_data(institute, view_option, selected_param):
    if institute:
        # Filter data for the selected institute
        institute_data = data[data['Institute'] == institute]

        if view_option == 'Institute Info':
            # Display the Institute Rank and Year
            rank_year_data = institute_data[['Year', 'Rank']]
            print(f"Rank and Year for {institute}:")
            print(rank_year_data.to_string(index=False))

        elif view_option == 'Year-wise Graphs':
            # Plot year-wise trend for the selected parameter
            plt.figure(figsize=(8, 5))
            sns.lineplot(x='Year', y=selected_param, data=institute_data, marker='o')
            plt.title(f'Year-wise trend of {selected_param} for {institute}')
            plt.tight_layout()
            plt.show()

        elif view_option == 'Rank Impact Analysis':
            # Perform correlation analysis between rank and the selected parameter
            institute_data_numeric = institute_data[['Rank', selected_param]].dropna()
            if not institute_data_numeric.empty:
                correlation = institute_data_numeric.corr().loc['Rank', selected_param]

                # Interpretation for user
                impact_type = "positive" if correlation > 0 else "negative"
                print(f"{selected_param} has a {impact_type} impact on the rank for {institute}.")
                print(f"Correlation value: {correlation:.2f}")
                
                # Provide reasons based on correlation value
                if correlation > 0:
                    print(f"A positive correlation means that as {selected_param} increases, the rank also tends to increase.")
                elif correlation < 0:
                    print(f"A negative correlation means that as {selected_param} increases, the rank tends to decrease.")
                else:
                    print(f"No significant correlation between {selected_param} and rank for {institute}.")
            else:
                print(f"No numerical data available for correlation analysis for {institute}.")

# Widget to handle dropdown selections
output = widgets.Output()

def on_dropdown_change(change):
    output.clear_output()
    with output:
        selected_institute = institute_dropdown.value
        view_option = view_dropdown.value
        selected_param = parameter_dropdown.value
        display_institute_data(selected_institute, view_option, selected_param)

# Observe changes in both dropdowns
institute_dropdown.observe(on_dropdown_change, names='value')
view_dropdown.observe(on_dropdown_change, names='value')
parameter_dropdown.observe(on_dropdown_change, names='value')

# Reposition dropdowns: institute_dropdown on left, view_dropdown on right, parameter_dropdown below
dropdown_layout = widgets.HBox([institute_dropdown, view_dropdown], layout=widgets.Layout(justify_content='space-between'))
parameter_layout = widgets.VBox([parameter_dropdown])

# Display the dropdowns and output
display(dropdown_layout, parameter_layout, output)
