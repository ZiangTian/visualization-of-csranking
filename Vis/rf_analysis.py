import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import glob
from utils import get_region_and_field

all_files = glob.glob('../WithLocation/location_*.csv')
df_list = []
for file in all_files:
    df = pd.read_csv(file)
    df_list.append(df)


all_list = []

for index in range(len(df_list)):

    uni_list =  df_list[index]['University'].to_list()
    field_list = df_list[index]['field'].to_list()
    lat_list = df_list[index]['lat'].to_list()
    lat_list = [0 if np.isnan(x) else x for x in lat_list]
    lon_list = df_list[index]['lon'].to_list()
    lon_list = [0 if np.isnan(x) else x for x in lon_list]
    fac_list = df_list[index]['Faculty Count'].to_list()
    fac_list = [0 if np.isnan(x) else x for x in fac_list]
    pub_list = df_list[index]['Publication Count'].to_list()
    pub_list = [0 if np.isnan(x) else x for x in pub_list]

    # Sample data with latitude, longitude, faculty count, and publication count
    data = {
        'University': uni_list,
        'Latitude': lat_list,
        'Longitude': lon_list,
        'FacultyCount': fac_list,
        'PublicationCount': pub_list,
        'Field': field_list
    }

    df = pd.DataFrame(data)
    all_list.append(df)


# Dash app initialization
app = dash.Dash(__name__)

# Dash app layout
app.layout = html.Div([
    html.H1("World Map with Heat Maps for Faculty Count and Publication Count"),

    dcc.Dropdown(
        id = 'field-dropdown',
        options = [
            {'label': 'All', 'value': 3},
            {'label': 'Artificial Intelligence', 'value': 9},
            {'label': 'Networks', 'value': 11},
            {'label': 'Architecure', 'value': 2},
            {'label': 'Database', 'value': 1},
            {'label': 'HPC', 'value': 5},
            {'label': 'Metrics', 'value': 0},
            {'label': 'Operating System', 'value': 6},
            {'label': 'Other', 'value': 7},
            {'label': 'Programming Language', 'value': 4},
            {'label': 'System', 'value': 8},
            {'label': 'Theory', 'value': 10},
        ],
        value = 3,
        style = {'width': '85%'}
    ),
    dcc.Graph(id='world-map'),
])

# Dash app callback to update the map based on the selected field
@app.callback(
    Output('world-map', 'figure'),
    [Input('field-dropdown', 'value')]
)
def update_map(selected_field):

    selected_df = all_list[selected_field]
    field = selected_df['Field'][0]
    selected_df.to_csv("tmp.csv")
    fig = px.scatter_geo(selected_df, 
                         lat='Latitude', 
                         lon='Longitude', 
                         text='University', 
                         size='FacultyCount', 
                         color='PublicationCount',
                         title = 'World Map in {}'.format(field),
                         labels={'FacultyCount': 'Faculty Count', 'PublicationCount': 'Publication Count'},
                         hover_data=['FacultyCount', 'PublicationCount'],
                         color_continuous_scale='Viridis',  # Adjust the color scale as needed
                        #  projection="natural earth",
                         custom_data=['University', 'FacultyCount', 'PublicationCount']  # Specify the data to include in custom_data
    )
    
    # Update the hovertemplate to exclude lat and lon
    fig.update_traces(
        hovertemplate='<br>'.join([
            'University: %{customdata[0]}',
            'Faculty Count: %{customdata[1]}',
            'Publication Count: %{customdata[2]}'
        ])
    )
    
    fig.write_html("../images/region_analysis/world_map_{}.html".format(field))


    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)