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

launch_sites = [{ 'label' : x , 'value' : x} for x in spacex_df['Launch Site'].unique()]
launch_sites.insert(0,{'label': 'All Sites', 'value': 'ALL'})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options = launch_sites,
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),



                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 2500: '2500', 5000:'5000', 7500:'7500'},
                                    value=[min(spacex_df['Payload Mass (kg)']), max(spacex_df['Payload Mass (kg)'])]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
                names='Launch Site', 
                title='Total Success Launched by Sites'
        )
        return fig
    else :
        #print(spacex_df.loc[spacex_df['Launch Site']== entered_site])
        filtered_df = spacex_df.loc[spacex_df['Launch Site']== entered_site]
        fig = px.pie(filtered_df, 
                values=filtered_df['class'].value_counts().values, 
                names=filtered_df['class'].value_counts().index, 
                title='Total Success Launched by '+entered_site
        )
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', "figure"),
    [Input('site-dropdown', 'value'), Input("payload-slider", "value")]
)
def get_scatter_chart(site, payload_range):
    filter_df = spacex_df.loc[
        (spacex_df['Payload Mass (kg)']>=payload_range[0]) 
        & 
        (spacex_df['Payload Mass (kg)']<=payload_range[1])
    ]
    print(site, payload_range)
    if site == 'ALL':
        
        fig = px.scatter(filter_df, x="Payload Mass (kg)", y="class",
            color="Booster Version Category",
            title = 'Correlation between Payload and Success for all Sites'
        )
        return fig
    else:
        fig = px.scatter(filter_df.loc[filter_df['Launch Site']==site], 
            x="Payload Mass (kg)", y="class", color="Booster Version Category",
            title = 'Correlation between Payload and Success for '+site +' Site'
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
