import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def lineplot(x, y, xlabel, ylabel, title, labels):
    """ Funtion to Create Lineplot. Arguments:
        list of values for xaxis
        list of values for yaxis
        xlabel, ylabel and titel value
        color name
        label value
    """
    plt.style.use('tableau-colorblind10')
    plt.figure(figsize=(7, 5))
    for index in range(len(y)):
        plt.plot(x, y[index], label=labels[index], linestyle='--')
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))
    plt.xticks(rotation=90)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig('Line_plot.jpg', dpi=500)
    plt.show()
    return


def barplot(dataframe, xlabel, ylabel, title):
    dataframe.plot(kind='bar', figsize=(10, 6))
    # Set plot labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig('barplot.jpg', dpi=500)
    plt.show()
    return


def draw_scatter_plot(
        x,
        y,
        title='Scatter Plot',
        xlabel='X-Axis',
        ylabel='Y-Axis',
        color='blue',
        marker='o',
        label=None):
    """
    Draw a scatter plot using Matplotlib.

    Parameters:
        x (list): X-axis data points.
        y (list): Y-axis data points.
        title (str): Title of the scatter plot.
        xlabel (str): Label for the X-axis.
        ylabel (str): Label for the Y-axis.
        color (str): Color of the markers.
        marker (str): Marker style.
        label (str): Label for the legend.
    """
    plt.scatter(x, y, color=color, marker=marker, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if label is not None:
        plt.legend()
    plt.show()


def get_heat_map(df, title, cmap='viridis'):
    correlation_matrix = df.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    heatmap = ax.pcolormesh(correlation_matrix, cmap=cmap)
    cbar = plt.colorbar(heatmap)
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            ax.text(j + 0.5, i + 0.5, f'{correlation_matrix.iloc[i, j]:.2f}',
                    ha='center', va='center', color='white')
    ax.set_xticks(range(len(correlation_matrix.columns)))
    ax.set_yticks(range(len(correlation_matrix.columns)))
    ax.set_xticklabels(correlation_matrix.columns, rotation=90)
    ax.set_yticklabels(correlation_matrix.columns)
    plt.title(title)
    plt.savefig('Heatmap_plot.jpg', dpi=500)
    plt.show()


def func_for_data_cleaning(df, countries, s_year, up_to_year):
    df = df.T
    df = df.drop(['Country Code', 'Indicator Name', 'Indicator Code'])
    df.columns = df.iloc[0]
    df = df.drop(['Country Name'])
    df = df.reset_index()
    df['Years'] = df['index']
    df = df.drop('index', axis=1)
    df = df[(df['Years'] >= s_year) & (df['Years'] <= up_to_year)]
    selected_data = df[countries]
    selected_data = selected_data.fillna(selected_data.iloc[:, :-1].mean())
    return selected_data


def get_country_data(
        data_frame_list,
        country_to_search,
        names,
        s_year,
        end_year):
    country_data = []
    for i, data in enumerate(data_frame_list):
        data = func_for_data_cleaning(data, country_to_search, s_year, end_year)
        data = data.rename(columns={country_to_search[0]: names[i]})
        country_data.append(data)
    country_data = pd.concat(country_data, axis=1)
    country_data = country_data.T.drop_duplicates().T
    country_data = country_data.drop('Years', axis=1)
    return country_data


def get_lists(df, cols):
    column_lists = [df[col].tolist() for col in cols[:-1]]
    return column_lists


def data_to_make_bar(df, years):
    df = df[df['Years'].isin(years)]
    df = df.set_index('Years')
    return df


Manufacturing_value_added_USD = pd.read_csv(
    'Manufacturing_value_added_USD.csv', skiprows=4)
CO2_emissions = pd.read_csv('CO2_emissions.csv', skiprows=4)
total_population = pd.read_csv('total_population.csv', skiprows=4)
Urban_population = pd.read_csv('Urban_population.csv', skiprows=4)
CO2_emissions = pd.read_csv('CO2_emissions.csv', skiprows=4)
Renewable_energy_consumption = pd.read_csv(
    'Renewable_energy_consumption.csv', skiprows=4)
Electric_power_consumption = pd.read_csv(
    'Electric_power_consumption.csv', skiprows=4)
Agricultural_land = pd.read_csv('Agricultural_land.csv', skiprows=4)
cols = [
    'United States',
    'China',
    'Germany',
    'Japan',
    'India',
    'United Kingdom',
    'France',
    'Years']
s_year = '2000'
end_year = '2021'
lineplot(list(func_for_data_cleaning(Manufacturing_value_added_USD,
                              cols,
                              s_year,
                              end_year)['Years']),
         get_lists(func_for_data_cleaning(Manufacturing_value_added_USD,
                                   cols,
                                   s_year,
                                   end_year),
                   cols),
         'Years',
         'USD',
         'Manufacturing value added GDP USD',
         cols[:-1])
lineplot(list(func_for_data_cleaning(CO2_emissions,
                              cols,
                              s_year,
                              end_year)['Years']),
         get_lists(func_for_data_cleaning(CO2_emissions,
                                   cols,
                                   s_year,
                                   end_year),
                   cols),
         'Years',
         "CO2 emissions(kt)",
         'CO2 Emissions',
         cols[:-1])
years = ['1995', '2000', '2005', '2010', '2015', '2020']
barplot(
    data_to_make_bar(
        func_for_data_cleaning(
            Urban_population,
            cols,
            s_year,
            end_year),
        years),
    'Years',
    'Population',
    'Urban Population')
barplot(
    data_to_make_bar(
        func_for_data_cleaning(
            Electric_power_consumption,
            cols,
            s_year,
            end_year),
        years),
    'Years',
    "Power in (kwh per capita)",
    "Electric Power Consumption")

names = [
    'Agricultural_land',
    'Urban_population',
    'Manufacturing_GDP',
    'CO2_emissions',
    'total_population',
    'Electric_power_consumption',
    'Renewable_energy_consumption']
data_frames = [
    Agricultural_land,
    Urban_population,
    Manufacturing_value_added_USD,
    CO2_emissions,
    total_population,
    Electric_power_consumption,
    Renewable_energy_consumption]
country_to_search = ['China', 'Years']
get_heat_map(
    get_country_data(
        data_frames,
        country_to_search,
        names,
        '1990',
        '2020'),
    'China',
    'cool')
country_to_search = ['Japan', 'Years']
get_heat_map(
    get_country_data(
        data_frames,
        country_to_search,
        names,
        '1990',
        '2020'),
    'Janpan',
    'tab20b')
country_to_search = ['United Kingdom', 'Years']
get_heat_map(
    get_country_data(
        data_frames,
        country_to_search,
        names,
        '1990',
        '2020'),
    'United Kingdom',
    'brg')
country = ['China', 'Years']
China_data = get_country_data(
    data_frames, country, names, '1990', '2020')
draw_scatter_plot(
    China_data['CO2_emissions'],
    China_data['Urban_population'],
    'CO2 Emissions vs Manufacturing GDP in China',
    'CO2 Emissions',
    'Manufacturing GDP USD',
    color='green',
    marker='o',
    label='Scatter Points')
