# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

sideDropdown_list = [
    {'label': 'All Sites', 'value': 'ALL'},
]

for launch_list in spacex_df['Launch Site'].unique():
    sideDropdown_list.append({'label': launch_list, 'value': launch_list})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=sideDropdown_list,
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True),
                                html.Br(),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=spacex_df['Payload Mass (kg)'].min(
                                                ),
                                                max=10000,
                                                marks={
                                                    0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[0, 10000]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        data_value_all = spacex_df.groupby(['Launch Site'])[
            'class'].count().reset_index()
        fig = px.pie(data_value_all, values='class',
                     names='Launch Site',
                     title='All Launch Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] ==
                                entered_site]['class'].value_counts().reset_index()
        filtered_df['status'] = filtered_df['class'].apply(
            lambda x: 'success' if x == 1 else 'failed')

        fig = px.pie(filtered_df, values='count',
                     names='status',
                     title=entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(payload):
    gap_value = [p for p in payload]
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(
        gap_value[0], gap_value[1])]

    fig = px.scatter(x=filtered_df['Payload Mass (kg)'],
                     y=filtered_df['class'], color=filtered_df['Launch Site'], labels={'x': 'Payload Mass (kg)', 'y': 'class'})
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
