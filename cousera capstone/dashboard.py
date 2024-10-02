# Import necessary libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load SpaceX data into a pandas dataframe
spacex_df = pd.read_csv(r"C:\Users\HP\Desktop\IBM Cert\dataset_part_2.csv")

# Create a Dash app
app = dash.Dash(__name__)

# List of launch sites for dropdown
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}]
launch_sites += [{'label': site, 'value': site} for site in spacex_df['LaunchSite'].unique()]

# Set max and min payload for the range slider
min_payload = spacex_df['PayloadMass'].min()
max_payload = spacex_df['PayloadMass'].max()

# App layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),

    # Dropdown for Launch Site
    dcc.Dropdown(id='site-dropdown',
                 options=launch_sites,
                 value='ALL',
                 placeholder='Select a Launch Site',
                 searchable=True),
    
    # Pie chart for success rates
    html.Div(dcc.Graph(id='success-pie-chart')),

    # Payload Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload, max=max_payload, step=1000,
                    marks={int(i): str(i) for i in range(int(min_payload), int(max_payload)+1, 1000)},
                    value=[min_payload, max_payload]),

    # Scatter plot for success vs payload mass
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Pie chart for all sites
        fig = px.pie(spacex_df, names='LaunchSite', values='Class',
                     title='Total Successful Launches by Site')
    else:
        # Pie chart for the selected site
        filtered_df = spacex_df[spacex_df['LaunchSite'] == selected_site]
        fig = px.pie(filtered_df, names='Class', title=f'Total Success Launches for site {selected_site}')
    return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, selected_payload):
    filtered_df = spacex_df[
        (spacex_df['PayloadMass'] >= selected_payload[0]) &
        (spacex_df['PayloadMass'] <= selected_payload[1])
    ]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['LaunchSite'] == selected_site]

    fig = px.scatter(filtered_df, x='PayloadMass', y='Class',
                     color='BoosterVersion',
                     title=f'Payload vs. Outcome for {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

