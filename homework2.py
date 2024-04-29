"""
Write your answers in the space between the questions, and commit/push only
this file (homework2.py) and countries.csv to your repo. Note that there can 
be a difference between giving a "minimally" right answer, 
and a really good answer, so it can pay to put thought into your work. 

This is a much longer project than those you've done in class - remember to use
comments to help readers navigate your work!

To answer these questions, you will use the two csv files provided in the repo.
The file named gdp.csv contains the per capita GDP of many countries in and 
around Europe in 2023 US dollars. The file named population.csv contains 
estimates of the population of many countries.
"""

"""
QUESTION 1

Short: Open the data

Long: Load the GDP data into a dataframe. Specify an absolute path using the Python 
os library to join filenames, so that anyone who clones your homework repo 
only needs to update one string for all loading to work.
"""

import pandas as pd
import os

# Define the absolute path to the directory containing the CSV files
directory = 'C:/Users/Shreya Work/OneDrive/Documents/GitHub/HW2'

# Define the filenames
gdp_filename = 'gdp.csv'

# Join the directory path and filename using os.path.join
gdp_filepath = os.path.join(directory, gdp_filename)

# Load the GDP data into a dataframe
gdp_df = pd.read_csv(gdp_filepath)

# Display the first few rows of the dataframe to verify it was loaded correctly
print(gdp_df.head())




"""
QUESTION 2

Short: Clean the data

Long: There are numerous issues with the data, on account of it having been 
haphazardly assembled from an online table. To start with, the column containing
country names has been labeled TIME. Fix this.

Next, trim this down to only member states of the European Union. To do this, 
find a list of members states (hint: there are 27 as of Apr 2024) and manually 
create your own CSV file with this list. Name this file countries.csv. Load it 
into a dataframe. Merge the two dataframes and keep only those rows with a 
match.

(Hint: This process should also flag the two errors in naming in gdp.csv. One 
 country has a dated name. Another is simply misspelt. Correct these.)
"""

# Define the list of EU member states
eu_member_states = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark',
                    'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy',
                    'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal',
                    'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

# Create a dataframe with the list of EU member states
countries_df = pd.DataFrame({'Country': eu_member_states})

# Save the countries dataframe to a CSV file
countries_csv_path = 'C:/Users/Shreya Work/OneDrive/Documents/GitHub/HW2/countries.csv'
countries_df.to_csv(countries_csv_path, index=False)

# Load the GDP data into a dataframe
gdp_df = pd.read_csv('C:/Users/Shreya Work/OneDrive/Documents/GitHub/HW2/gdp.csv')

# Rename the column containing country names
gdp_df.rename(columns={'TIME': 'Country'}, inplace=True)

# Filter the GDP data to include only EU member states
gdp_df = gdp_df[gdp_df['Country'].isin(eu_member_states)]

# Display the first few rows of the cleaned dataframe to verify the cleaning
print(gdp_df.head())



"""
QUESTION 3

Short: Reshape the data

Long: Convert this wide data into long data with columns named year and gdp.
The year column should contain int datatype objects.

Remember to convert GDP from string to float. (Hint: the data uses ":" instead
of NaN to denote missing values. You will have to fix this first.) 
"""

import pandas as pd

# Load the GDP data into a dataframe
gdp_df = pd.read_csv('C:/Users/Shreya Work/OneDrive/Documents/GitHub/HW2/gdp.csv')

# Replace ":" with NaN to denote missing values
gdp_df.replace(':', float('nan'), inplace=True)

# Rename the "TIME" column to "Country"
gdp_df.rename(columns={'TIME': 'Country'}, inplace=True)

# Reshape the data from wide to long format
gdp_long_df = gdp_df.melt(id_vars=['Country'], var_name='year', value_name='gdp')

# Convert the "year" column to int datatype
gdp_long_df['year'] = gdp_long_df['year'].str.extract('(\d+)').astype(int)

# Convert the "gdp" column from string to float
gdp_long_df['gdp'] = gdp_long_df['gdp'].astype(float)

# Display the first few rows of the reshaped dataframe
print(gdp_long_df.head())



"""
QUESTION 4

Short: Repeat this process for the population data.

Long: Load population.csv into a dataframe. Rename the TIME columns. 
Merge it with the dataframe loaded from countries.csv. Make it long, naming
the resulting columns year and population. Convert population and year into int.
"""


import os

# Load population.csv into a dataframe
population_df = pd.read_csv('C:/Users/Shreya Work/OneDrive/Documents/GitHub/HW2/population.csv')

# Rename the TIME columns
population_df.rename(columns={'TIME': 'Country'}, inplace=True)

# Load the list of EU member states from countries.csv
countries_df = pd.read_csv('C:/Users/Shreya Work/OneDrive/Documents/GitHub/HW2/countries.csv')

# Merge the population dataframe with the list of EU member states
merged_population_df = pd.merge(population_df, countries_df, on='Country', how='inner')

# Reshape the data from wide to long format
population_long_df = pd.melt(merged_population_df, id_vars=['Country'], var_name='year', value_name='population')

# Convert population and year into int
population_long_df['year'] = population_long_df['year'].astype(int)
population_long_df['population'] = population_long_df['population'].astype(int)

# Display the first few rows of the reshaped dataframe
print(population_long_df.head())





"""
QUESTION 5

Short: Merge the two dataframe, find the total GDP

Long: Merge the two dataframes. Total GDP is per capita GDP times the 
population.
"""

# Merge the GDP and population dataframes on 'Country' and 'year' columns
merged_df = pd.merge(gdp_long_df, population_long_df, on=['Country', 'year'], how='inner')

# Calculate total GDP by multiplying per capita GDP and population
merged_df['total_GDP'] = merged_df['gdp'] * merged_df['population']

# Display the resulting dataframe with total GDP
print(merged_df[['Country', 'year', 'total_GDP']])



"""
QUESTION 6

Short: For each country, find the annual GDP growth rate in percentage points.
Round down to 2 digits.

Long: Sort the data by name, and then year. You can now use a variety of methods
to get the gdp growth rate, and we'll suggest one here: 

1. Use groupby and shift(1) to create a column containing total GDP from the
previous year. We haven't covered shift in class, so you'll need to look
this method up. Using groupby has the benefit of automatically generating a
missing value for 2012; if you don't do this, you'll need to ensure that you
replace all 2012 values with missing values.

2. Use the following arithematic operation to get the growth rate:
    gdp_growth = (total_gdp - total_gdp_previous_year) * 100 / total_gdp
"""
# Sort the merged dataframe by name and year
merged_df.sort_values(by=['Country', 'year'], inplace=True)

# Calculate total GDP for each year and shift to get total GDP from the previous year
merged_df['total_GDP_previous_year'] = merged_df.groupby('Country')['total_GDP'].shift(1)

# Calculate GDP growth rate using the first method
merged_df['gdp_growth_rate_method1'] = ((merged_df['total_GDP'] - merged_df['total_GDP_previous_year']) / merged_df['total_GDP_previous_year']) * 100

# Round down the GDP growth rate to 2 decimal points
merged_df['gdp_growth_rate_method1'] = merged_df['gdp_growth_rate_method1'].round(2)

# Calculate GDP growth rate using the second method
merged_df['gdp_growth_rate_method2'] = ((merged_df['total_GDP'] - merged_df['total_GDP_previous_year']) * 100) / merged_df['total_GDP']

# Round down the GDP growth rate to 2 decimal points
merged_df['gdp_growth_rate_method2'] = merged_df['gdp_growth_rate_method2'].round(2)

# Display the resulting dataframe with GDP growth rates
print(merged_df[['Country', 'year', 'gdp_growth_rate_method1', 'gdp_growth_rate_method2']])



"""
QUESTION 7

Short: Which country has the highest total gdp (for the any year) in the EU? 

Long: Do not hardcode your answer! You will have to put the automate putting 
the name of the country into a string called country_name and using the following
format string to display it:

print(f"The largest country in the EU is {country_name}")
"""
# Filter the merged dataframe to include only EU member states
eu_merged_df = merged_df[merged_df['Country'].isin(eu_member_states)]

# Group the data by country and sum the total GDP for each country
eu_total_gdp = eu_merged_df.groupby('Country')['total_GDP'].sum()

# Find the country with the highest total GDP
largest_country = eu_total_gdp.idxmax()

# Print the name of the country with the highest total GDP
print(f"The largest country in the EU is {largest_country}")


"""
QUESTION 8

Create a dataframe that consists only of the country you found in Question 7

In which year did this country have the most growth in the period 2012-23?

In which year did this country have the least growth in the peroid 2012-23?

Do not hardcode your answer. You will have to use the following format strings 
to show your answer:

print(f"Their best year was {best_year}")
print(f"Their worst year was {worst_year}")
"""

# Filter the merged dataframe to include only data for the country found in Question 7
country_df = merged_df[merged_df['Country'] == largest_country]

# Calculate GDP growth for each year in the period 2012-2023
country_df['gdp_growth'] = (country_df['total_GDP'] - country_df['total_GDP'].shift(1)) / country_df['total_GDP'].shift(1) * 100

# Find the year with the most growth
best_year = country_df.loc[country_df['gdp_growth'].idxmax(), 'year']

# Find the year with the least growth
worst_year = country_df.loc[country_df['gdp_growth'].idxmin(), 'year']

# Print the results
print(f"Their best year was {best_year}")
print(f"Their worst year was {worst_year}")
