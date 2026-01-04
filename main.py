from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
import os

# Global Styles and Constants
COLORS = {
    'background_main': '#181818',  # Soft Black
    'background_sidebar': '#2b2b2b',  # Dark Gray
    'background_card': '#242424',  # Cards background
    'text_header': '#e0e0e0',  # Soft White
    'text_body': '#b0b0b0',  # Light Gray
    'accent_text': '#90caf9',  # Soft Blue
    'divider': '#424242'  # Divider lines
}

SUB_HEADER_STYLE = {
    'fontFamily': "'Montserrat', sans-serif",
    'color': COLORS['text_header'],
    'marginTop': '35px',
    'marginBottom': '20px',
    'fontSize': '1.6rem',
    'fontWeight': '600'
}

TEXT_STYLE = {
    'fontFamily': "'Rubik', sans-serif",
    'lineHeight': '1.8',
    'color': COLORS['text_body'],
    'fontSize': '1.05rem',
    'fontWeight': '300',
    'marginBottom': '20px'
}

TEXT_STYLE_2 = {
    'fontFamily': "'Rubik', sans-serif",
    'lineHeight': '1.5',
    'color': COLORS['text_body'],
    'fontSize': '1.05rem',
    'fontWeight': '300',
    'marginBottom': '10px'
}

# Typography Styles
HEADER_STYLE = {
    'fontFamily': "'Montserrat', sans-serif",
    'marginBottom': '20px',
    'marginTop': '0px',
    'fontWeight': '700',
    'fontSize': '2.6rem',
    'color': COLORS['text_header'],
    'letterSpacing': '1px',
    'lineHeight': '1.2'
}

# Sidebar Style
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "4rem 1rem 2rem 1rem",
    "backgroundColor": COLORS['background_sidebar'],
    "color": "#ecf0f1",
    "zIndex": 100,
    "boxShadow": "2px 0 10px rgba(0,0,0,0.3)"
}

# Base Style for Sidebar Links
NAV_LINK_STYLE = {
    "color": "#ecf0f1",
    "textDecoration": "none",
    "display": "block",
    "margin": "20px 0",
    "fontSize": "1.1rem",
    "transition": "color 0.3s ease"
}

# Active Link Style
NAV_LINK_ACTIVE_STYLE = {
    "color": COLORS['accent_text'],
    "textDecoration": "none",
    "display": "block",
    "margin": "20px 0",
    "fontSize": "1.1rem",
    "fontWeight": "bold",
    "borderRight": f"3px solid {COLORS['accent_text']}"  # Optional: visual marker
}

# Content Style (Main Area)
CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "4rem",
    "padding-top": "4rem",
    "padding-bottom": "2rem",
    "backgroundColor": COLORS['background_main'],
    "minHeight": "100vh",
    "color": "white"
}

CARD_STYLE = {
    "backgroundColor": COLORS['background_card'],
    "padding": "15px",
    "borderRadius": "12px",
    "boxShadow": "0 4px 6px rgba(0,0,0,0.3)",
    "textAlign": "center",
    "width": "180px",
    "minWidth": "180px",
    "margin": "0 15px",
    "display": "flex",
    "flexDirection": "column",
    "justifyContent": "center"
}

# Style for the horizontal filter bar
FILTER_BAR_STYLE = {
    'backgroundColor': COLORS['background_card'],
    'padding': '15px 25px',
    'borderRadius': '12px',
    'boxShadow': '0 4px 10px rgba(0,0,0,0.3)',
    'marginBottom': '15px',
    'display': 'flex',
    'flexDirection': 'row',
    'alignItems': 'center',
    'justifyContent': 'space-between',
    'width': '90%',
    'boxSizing': 'border-box',
    'height': 'auto',
    'gap': '15px',
    'flexWrap': 'wrap'
}

FILTER_BAR_STYLE_MAP = {
    'backgroundColor': COLORS['background_card'],
    'padding': '15px 20px',
    'borderRadius': '10px',
    'boxShadow': '0 4px 10px rgba(0,0,0,0.3)',
    'marginBottom': '20px',
    'display': 'flex',
    'flexDirection': 'row',
    'alignItems': 'center',
    'justifyContent': 'space-between',
    'width': '100%',
    'boxSizing': 'border-box',
}

VERTICAL_DIVIDER_STYLE = {
    'borderLeft': '1px solid #555',
    'height': '40px',
    'margin': '0 20px'
}


# ------------ Data Loading and Preprocessing ------------

def load_data():
    file_path = 'combined_clean_data.csv'
    cords_path = 'cities_coords.csv'

    if os.path.exists(file_path) and os.path.exists(cords_path):
        combined_df = pd.read_csv(file_path)
        coords = pd.read_csv(cords_path)

        main_df = combined_df.merge(coords, left_on='OriginCityName', right_on='CityName', how='left')
        main_df.rename(columns={'Lat': 'OriginLat', 'Lon': 'OriginLon'}, inplace=True)
        main_df.drop(columns=['CityName'], inplace=True)

        main_df = main_df.merge(coords, left_on='DestinationCityName', right_on='CityName', how='left')
        main_df.rename(columns={'Lat': 'DestLat', 'Lon': 'DestLon'}, inplace=True)
        main_df.drop(columns=['CityName'], inplace=True)

        main_df = main_df.dropna(subset=['OriginLat', 'OriginLon', 'DestLat', 'DestLon'])
        return main_df

    raise FileNotFoundError("Files not found.")

# Initialize Data
df = load_data().copy()

# ------------ Visualization Functions ------------

def create_grouped_bar_chart(df_in):
    df_new = helper_plot(df_in, 10)

    fig = px.bar(
        df_new, x='ClusterName', y='Avg Passengers', color='Time Window',
        barmode='group', template='plotly_dark',
        color_discrete_sequence=px.colors.sequential.Teal
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Rubik', color='white'), title_text='',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="Service Cluster", yaxis_title="Avg Weekly Passengers"
    )
    return fig


def create_line_plot(df_in):
    df_new = helper_plot(df_in, 30)

    fig = px.line(
        df_new, x='Time Window', y='Avg Passengers', color='ClusterName',
        markers=True, template='plotly_dark'
    )

    # Updated Layout with Hover Label fix
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Rubik', color='white'), title_text='',
        xaxis_title="Time Window", yaxis_title="Avg Weekly Passengers",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=COLORS['background_card'],  # Dark background matching cards
            font=dict(color='white'),  # White text
            bordercolor=COLORS['divider']  # Subtle border
        )
    )
    return fig


def helper_plot(df_in, size):
    top_clusters = df_in.groupby('ClusterName')['WeeklyPassengers'].sum().nlargest(size).index.tolist()
    df_top = df_in[df_in['ClusterName'].isin(top_clusters)]
    time_windows = ['WorkDay - 06:00-08:59', 'WorkDay - 09:00-11:59', 'WorkDay - 12:00-14:59', 'WorkDay - 15:00-18:59']
    df_agg = df_top.groupby('ClusterName')[time_windows].mean().reset_index()
    df_melted = df_agg.melt(id_vars='ClusterName', value_vars=time_windows, var_name='Time Window',
                            value_name='Avg Passengers')
    df_melted['Time Window'] = df_melted['Time Window'].str.replace('WorkDay - ', '')
    return df_melted


# ------------ App and Layouts ------------
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                background-color: {COLORS['background_main']};
                font-family: 'Rubik', sans-serif;
            }}
            .nav-link:hover {{
                color: {COLORS['accent_text']} !important;
                font-weight: bold;
                transition: 0.3s;
            }}
            ::-webkit-scrollbar {{ width: 10px; }}
            ::-webkit-scrollbar-track {{ background: {COLORS['background_main']}; }}
            ::-webkit-scrollbar-thumb {{ background: #555; border-radius: 5px; }}
            ::-webkit-scrollbar-thumb:hover {{ background: #888; }}
            .Select-control {{ background-color: #2b2b2b !important; border: 1px solid #555 !important; color: white !important; }}
            .Select-value-label {{ color: white !important; }}
            .Select-menu-outer {{ background-color: #2b2b2b !important; border: 1px solid #555 !important; color: white !important; }}
            .Select-option {{ background-color: #2b2b2b !important; color: white !important; }}
            .Select-option:hover {{ background-color: #444 !important; }}
            .Select-placeholder {{ color: #aaa !important; }}
            .Select-arrow-zone {{ color: white !important; }}
            .Select-arrow {{ border-top-color: white !important; }}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

# Overview Page
layout_overview = html.Div([
    html.H1("Public Transportation Analysis Dashboard", style=HEADER_STYLE),
    html.Hr(style={'borderColor': COLORS['divider'], 'marginBottom': '40px'}),

    html.H3("Project Overview", style=SUB_HEADER_STYLE),
    html.P(
        "This project analyzes usage patterns of public transportation in Israel, "
        "applying principles of information visualization theory and design. "
        "The goal is to identify and compare spatial and temporal trends in transit usage."
        , style=TEXT_STYLE),

    html.H3("Research Objectives", style=SUB_HEADER_STYLE),
    html.Ul([
        html.Li("Distribution Analysis: Examining load distribution across different times of day.",
                style=TEXT_STYLE_2),
        html.Li("Trend Analysis: Analyzing how usage volume changes over time.", style=TEXT_STYLE_2),
        html.Li("Correlation Analysis: Investigating relationship between route characteristics and popularity.",
                style=TEXT_STYLE_2),
    ], style={'lineHeight': '3', 'marginBottom': '30px'}),

    html.H3("Data Sources", style=SUB_HEADER_STYLE),
    html.P("Data sourced from government databases (Data Gov), merging records from 2023 and 2024.", style=TEXT_STYLE),

    html.A("Click here to visit Data.gov.il",
           href="https://data.gov.il/he/datasets/ministry_of_transport/ridership",
           target="_blank",
           style={'color': COLORS['accent_text'], 'textDecoration': 'underline', 'fontSize': '1rem'}),

    # Cards Row
    html.Div([
        html.Div([
            html.H4("Records", style={'color': '#b0b0b0', 'fontSize': '0.85rem', 'marginBottom': '5px'}),
            html.H2("26,888", style={'color': COLORS['accent_text'], 'fontWeight': 'bold', 'fontSize': '1.4rem',
                                     'fontFamily': 'Montserrat'})
        ], style=CARD_STYLE),

        html.Div([
            html.H4("Years", style={'color': '#b0b0b0', 'fontSize': '0.85rem', 'marginBottom': '5px'}),
            html.H2("2023-24", style={'color': COLORS['accent_text'], 'fontWeight': 'bold', 'fontSize': '1.4rem',
                                      'fontFamily': 'Montserrat'})
        ], style=CARD_STYLE),

        html.Div([
            html.H4("Source", style={'color': '#b0b0b0', 'fontSize': '0.85rem', 'marginBottom': '5px'}),
            html.H2("Gov.il", style={'color': COLORS['accent_text'], 'fontWeight': 'bold', 'fontSize': '1.4rem',
                                     'fontFamily': 'Montserrat'})
        ], style=CARD_STYLE),
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'marginTop': '80px',
        'justifyContent': 'center',
        'alignItems': 'center',
        'width': '100%'
    }),
], style={'paddingRight': '20%', 'boxSizing': 'border-box'})

# Page 1 (Task 1: Map)
layout_page_1 = html.Div([
    html.H1("Load Analysis across Areas and Times", style=HEADER_STYLE),
    html.Hr(style={'borderColor': COLORS['divider']}),

    html.Div([
        # Left Column: Text
        html.Div([
            html.H3("Purpose", style=SUB_HEADER_STYLE),
            html.P(
                "This interactive interface is designed to analyze public transportation load distributions"
                " across Israel's diverse regions and time windows. By visualizing complex transit data, the map enables"
                " the discovery of spatial and temporal trends, helping planners identify high-demand corridors and"
                " operational anomalies. This tool serves as a 'visual memory' to support transit optimization and"
                " data-driven decision-making, significantly reducing the cognitive effort required to evaluate national"
                " passenger flow."
                , style=TEXT_STYLE
            ),
            html.H3("How To Use", style=SUB_HEADER_STYLE),
            html.Ul([
                html.Li("Select 'Day Type' and 'Time Window' to filter data by time.", style=TEXT_STYLE_2),
                html.Li("White points on the map represent Cities.", style=TEXT_STYLE_2),
                html.Li("Use the 'Min Passengers' slider to filter routes by load (0-450).", style=TEXT_STYLE_2),
                html.Li("Lines represent routes; Color/Thickness = Load intensity.", style=TEXT_STYLE_2),
                html.Li("Zoom and Pan to explore specific regions.", style=TEXT_STYLE_2)
            ], style={'paddingLeft': '20px', 'lineHeight': '1.6'}),
        ], style={'width': '38%', 'marginRight': '2%'}),

        # Right Column: Filter Bar + Map
        html.Div([
            # Filter Bar
            html.Div([
                # Day Type
                html.Div([
                    html.Label("Day Type:",
                               style={'fontWeight': 'bold', 'color': COLORS['text_header'], 'marginBottom': '5px',
                                      'fontSize': '0.9rem'}),
                    dcc.RadioItems(
                        id='map-day-type',
                        options=[
                            {'label': ' Weekday', 'value': 'WorkDay'},
                            {'label': ' Friday', 'value': 'Friday'}
                        ],
                        value='WorkDay',
                        labelStyle={'display': 'block', 'color': COLORS['text_body'], 'fontSize': '0.85rem',
                                    'marginBottom': '2px'},
                        style={'display': 'block'}
                    ),
                ]),

                html.Div(style=VERTICAL_DIVIDER_STYLE),

                # Time Window
                html.Div([
                    html.Label("Time Window:",
                               style={'fontWeight': 'bold', 'color': COLORS['text_header'], 'marginBottom': '5px',
                                      'fontSize': '0.9rem'}),
                    dcc.Dropdown(
                        id='map-time-window',
                        options=[
                            {'label': '06:00 - 09:00 (Morning)', 'value': '06:00-08:59'},
                            {'label': '09:00 - 12:00 (Late Morning)', 'value': '09:00-11:59'},
                            {'label': '12:00 - 15:00 (Noon)', 'value': '12:00-14:59'},
                            {'label': '15:00 - 19:00 (Afternoon)', 'value': '15:00-18:59'},
                            {'label': '19:00 - 00:00 (Night)', 'value': '19:00-23:59'}
                        ],
                        value='06:00-08:59',
                        clearable=False,
                        style={'width': '150px'}
                    ),
                ]),

                html.Div(style=VERTICAL_DIVIDER_STYLE),

                # Slider
                html.Div([
                    html.Label("Min Passengers:",
                               style={'fontWeight': 'bold', 'color': COLORS['text_header'], 'marginBottom': '5px',
                                      'fontSize': '0.9rem'}),
                    html.Div([
                        dcc.Slider(
                            id='map-threshold',
                            min=0, max=450, step=40, value=0,
                            marks={0: {'label': '0', 'style': {'color': 'white', 'fontSize': '0.7rem'}},
                                   150: {'label': '150', 'style': {'color': 'white', 'fontSize': '0.7rem'}},
                                   300: {'label': '300', 'style': {'color': 'white', 'fontSize': '0.7rem'}},
                                   450: {'label': '450', 'style': {'color': 'white', 'fontSize': '0.7rem'}}
                                   },
                        ),
                    ], style={'width': '160px'})
                ]),

                html.Div(style=VERTICAL_DIVIDER_STYLE),

                # Stats
                html.Div(id='map-stats',
                         style={'minWidth': '100px', 'color': 'white', 'textAlign': 'right', 'fontSize': '0.9rem'})

            ], style=FILTER_BAR_STYLE_MAP),

            # Map
            html.Div([
                dcc.Graph(id='traffic-map', style={'height': '75vh', 'width': '100%'})
            ], style={'width': '100%', 'borderRadius': '12px', 'overflow': 'hidden'})

        ], style={'width': '60%'})

    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'})
])

# Page 2 (Task 2)
layout_page_2 = html.Div([
    html.H1("Temporal Trends Analysis", style=HEADER_STYLE),
    html.Hr(style={'borderColor': COLORS['divider']}),

    html.Div([
        html.Div([
            html.H3("Purpose", style=SUB_HEADER_STYLE),
            html.P(
                "This visualization examines how public transportation usage volumes change over time throughout the day."
                , style=TEXT_STYLE
            ),

            html.H3("How To Use", style=SUB_HEADER_STYLE),
            html.Ul([
                html.Li("The graph shows average passengers per cluster over time.", style=TEXT_STYLE_2),
                html.Li("Click on cluster names in the legend to toggle them.", style=TEXT_STYLE_2),
                html.Li("Double-click a name to isolate that cluster.", style=TEXT_STYLE_2)
            ], style={'paddingLeft': '20px', 'lineHeight': '1.6', 'marginBottom': '20px'}),

        ], style={'width': '30%', 'paddingRight': '40px'}),

        html.Div([
            dcc.Graph(id="graph-task-2", figure=create_line_plot(df), style={'height': '600px'})
        ], style={'width': '70%'})

    ], style={'display': 'flex', 'flexDirection': 'row'})
])

# Page 3 (Task 3)
numeric_options = [
    {'label': 'Route Length', 'value': 'RouteLength'},
    {'label': 'Avg Speed', 'value': 'AverageSpeed'},
    {'label': 'Trip Duration', 'value': 'AverageTripDuration'},
    {'label': 'Cost Per Passenger', 'value': 'OperatingCostPerPassenger'},
    {'label': 'Weekly Total Passengers', 'value': 'WeeklyPassengers'}
]

layout_page_3 = html.Div([
    html.H1("Correlation Analysis", style=HEADER_STYLE),
    html.Hr(style={'borderColor': COLORS['divider']}),

    html.Div([
        # Left Column: Text (Purpose & How to Use)
        html.Div([
            html.H3("Purpose", style=SUB_HEADER_STYLE),
            html.P(
                "This section investigates the statistical relationship between different physical and operational characteristics of routes."
                , style=TEXT_STYLE
            ),

            html.H3("How To Use", style=SUB_HEADER_STYLE),
            html.Ul([
                html.Li("Use the top filters to select the Year and Quarter.", style=TEXT_STYLE_2),
                html.Li("Select variables for X and Y axes to explore correlations.", style=TEXT_STYLE_2),
                html.Li("Each point represents a route.", style=TEXT_STYLE_2),
                html.Li("Hover over points to see route details.", style=TEXT_STYLE_2)
            ], style={'paddingLeft': '20px', 'lineHeight': '1.6', 'marginBottom': '20px'}),

        ], style={'width': '38%', 'marginRight': '2%'}),

        # Right Column: Filter Bar (Top) + Graph (Bottom)
        html.Div([
            # 1. Filter Bar (Horizontal)
            html.Div([
                # Year & Quarter Group
                html.Div([
                    html.Label("Time Period:",
                               style={'fontWeight': 'bold', 'color': COLORS['text_header'], 'fontSize': '0.9rem',
                                      'marginRight': '10px'}),
                    dcc.Dropdown(
                        id='task3-year',
                        options=[{'label': '2023', 'value': 2023}, {'label': '2024', 'value': 2024}],
                        value=2024, clearable=False,
                        style={'width': '70px', 'display': 'inline-block', 'marginRight': '5px'}
                    ),
                    dcc.Dropdown(
                        id='task3-quarter',
                        options=[{'label': f'Q{i}', 'value': i} for i in range(1, 5) if i != 3],
                        value=1, clearable=False, style={'width': '40px', 'display': 'inline-block'}
                    ),
                ], style={'display': 'flex', 'alignItems': 'center'}),

                html.Div(style=VERTICAL_DIVIDER_STYLE),

                # X Axis
                html.Div([
                    html.Label("X Axis:",
                               style={'fontWeight': 'bold', 'color': COLORS['text_header'], 'fontSize': '0.9rem',
                                      'marginRight': '10px'}),
                    dcc.Dropdown(
                        id='task3-xaxis',
                        options=numeric_options,
                        value='RouteLength',
                        clearable=False,
                        style={'width': '160px'}
                    ),
                ], style={'display': 'flex', 'alignItems': 'center'}),

                html.Div(style=VERTICAL_DIVIDER_STYLE),

                # Y Axis
                html.Div([
                    html.Label("Y Axis:",
                               style={'fontWeight': 'bold', 'color': COLORS['text_header'], 'fontSize': '0.9rem',
                                      'marginRight': '10px'}),
                    dcc.Dropdown(
                        id='task3-yaxis',
                        options=numeric_options,
                        value='WeeklyPassengers',
                        clearable=False,
                        style={'width': '160px'}
                    ),
                ], style={'display': 'flex', 'alignItems': 'center'}),

            ], style=FILTER_BAR_STYLE),

            # 2. Graph
            html.Div([
                dcc.Graph(id="graph-task-3", style={'height': '600px'})
            ], style={'width': '100%', 'borderRadius': '12px', 'overflow': 'hidden'})

        ], style={'width': '60%'})

    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'})
])

# Sidebar - RESTORED ORIGINAL NAMES
sidebar_content = html.Div([
    html.H2("Menu", style={
        "textAlign": "center",
        "marginTop": "10px",
        "marginBottom": "20px",
        "color": "white",
        "letterSpacing": "2px",
        "fontWeight": "300",
        "fontFamily": "Montserrat",
        "fontSize": "2rem",
        "height": "auto",
        "lineHeight": "1.2"
    }),
    html.Hr(style={'borderColor': '#555'}),
    html.Div([
        dcc.Link("Overview", href="/", id="link-overview", className="nav-link", style=NAV_LINK_STYLE),
        dcc.Link("Load Analysis", href="/page-1", id="link-page-1", className="nav-link", style=NAV_LINK_STYLE),
        dcc.Link("Load Trends by Times", href="/page-2", id="link-page-2", className="nav-link", style=NAV_LINK_STYLE),
        dcc.Link("Load Correlation", href="/page-3", id="link-page-3", className="nav-link", style=NAV_LINK_STYLE),
    ])
], style=SIDEBAR_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar_content,
    html.Div(id="page-content", style=CONTENT_STYLE)
])


# ------------ Callbacks ------------

# Callback 1: Update Traffic Map
@app.callback(
    [Output('traffic-map', 'figure'),
     Output('map-stats', 'children')],
    [Input('map-day-type', 'value'),
     Input('map-time-window', 'value'),
     Input('map-threshold', 'value')]
)
def update_traffic_map(day_type, time_window, threshold):
    col_name = f"{day_type} - {time_window}"
    if col_name not in df.columns:
        return go.Figure(), "No Data"

    # Set effective threshold to 1 if slider is at 0 to avoid empty data issues
    effective_threshold = threshold if threshold > 0 else 1

    grouped = df.groupby(['OriginCityName', 'DestinationCityName', 'OriginLat', 'OriginLon', 'DestLat', 'DestLon'])[
        col_name].sum().reset_index()

    filtered = grouped[grouped[col_name] >= effective_threshold]
    fig = go.Figure()

    # Determine line visibility based on threshold
    line_visibility = True if threshold > 0 else 'legendonly'

    bins = [
        {'min': 0, 'max': 50, 'color': '#3498db', 'width': 1, 'name': 'Low Volume (<50)'},
        {'min': 50, 'max': 200, 'color': '#f1c40f', 'width': 3, 'name': 'Medium Volume (50-200)'},
        {'min': 200, 'max': 999999, 'color': '#e74c3c', 'width': 5, 'name': 'High Volume (>200)'}
    ]

    bin_coords = {i: {'lat': [], 'lon': []} for i in range(len(bins))}
    # Assign routes to bins
    for _, row in filtered.iterrows():
        val = row[col_name]
        bin_idx = 0
        for i, b in enumerate(bins):
            if b['min'] <= val < b['max']:
                bin_idx = i
                break

        bin_coords[bin_idx]['lat'].extend([row['OriginLat'], row['DestLat'], None])
        bin_coords[bin_idx]['lon'].extend([row['OriginLon'], row['DestLon'], None])

    # Add traces for each bin
    for i, b in enumerate(bins):
        if bin_coords[i]['lat']:
            fig.add_trace(go.Scattermap(
                mode="lines",
                lon=bin_coords[i]['lon'],
                lat=bin_coords[i]['lat'],
                line=dict(width=b['width'], color=b['color']),
                opacity=0.7,
                hoverinfo='skip',
                name=b['name'],
                visible=line_visibility
            ))

    # Add city markers
    all_origins = df[['OriginCityName', 'OriginLat', 'OriginLon']].rename(
        columns={'OriginCityName': 'City', 'OriginLat': 'Lat', 'OriginLon': 'Lon'})
    all_dests = df[['DestinationCityName', 'DestLat', 'DestLon']].rename(
        columns={'DestinationCityName': 'City', 'DestLat': 'Lat', 'DestLon': 'Lon'})

    cities_df = pd.concat([all_origins, all_dests]).drop_duplicates().reset_index(drop=True)
    # Add city markers
    fig.add_trace(go.Scattermap(
        mode="markers",
        lon=cities_df['Lon'],
        lat=cities_df['Lat'],
        marker=dict(size=6, color='#ecf0f1', opacity=0.9),
        text=cities_df['City'],
        hoverinfo='text',
        name="Cities",
        visible=True
    ))
    # Update layout
    fig.update_layout(
        map=dict(
            style="carto-darkmatter",
            center=dict(lat=31.4, lon=35.0),
            zoom=6.5
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=True,
        legend=dict(
            x=0, y=1,
            bgcolor='rgba(255,255,255,0.8)',
            font=dict(color='black'),
            itemclick="toggle",
            itemdoubleclick="toggleothers"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Rubik')
    )

    # Stats Calculation
    display_count = len(filtered) if threshold > 0 else 0
    display_passengers = int(filtered[col_name].sum()) if threshold > 0 else 0

    stats_text = html.Div([
        html.Div(f"Total Routes: {display_count}", style={'marginBottom': '5px', 'fontSize': '1.1rem'}),
        html.Div(f"Passengers: {display_passengers:,}", style={'fontSize': '1.1rem'})
    ], style={'textAlign': 'center', 'width': '100%'})

    return fig, stats_text


# Callback 2: Render Page Content
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return layout_overview
    elif pathname == "/page-1":
        return layout_page_1
    elif pathname == "/page-2":
        return layout_page_2
    elif pathname == "/page-3":
        return layout_page_3
    return html.Div([html.H1("404 - Page not found", style={'color': 'white'})])


# Callback 3: Update Active Link Style
@app.callback(
    [Output("link-overview", "style"),
     Output("link-page-1", "style"),
     Output("link-page-2", "style"),
     Output("link-page-3", "style")],
    [Input("url", "pathname")]
)
def update_active_links(pathname):
    # Default styling for all links
    default_style = NAV_LINK_STYLE
    active_style = NAV_LINK_ACTIVE_STYLE

    # Logic to return styles
    if pathname == "/" or pathname is None:
        return active_style, default_style, default_style, default_style
    elif pathname == "/page-1":
        return default_style, active_style, default_style, default_style
    elif pathname == "/page-2":
        return default_style, default_style, active_style, default_style
    elif pathname == "/page-3":
        return default_style, default_style, default_style, active_style
    else:
        return default_style, default_style, default_style, default_style


# Callback 4: Update Correlation Graph (Task 3)
@app.callback(
    Output("graph-task-3", "figure"),
    [Input("task3-year", "value"),
     Input("task3-quarter", "value"),
     Input("task3-xaxis", "value"),
     Input("task3-yaxis", "value")]
)
def update_correlation_graph(year, quarter, x_axis, y_axis):
    # Filter Data
    filtered_df = df[(df['year'] == year) & (df['Q'] == quarter)].copy()

    # Clean data for selected columns
    filtered_df = filtered_df.dropna(subset=[x_axis, y_axis])
    filtered_df = filtered_df[filtered_df[y_axis] > 0]

    if filtered_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available for this selection",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        return fig

    # Create Standard Scatter Plot
    fig = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        color='ClusterName',
        hover_data=['RouteName', 'OriginCityName', 'DestinationCityName'],
        template='plotly_dark',
        opacity=0.7
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Rubik', color='white'),
        title_text='',
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        showlegend=False
    )
    return fig

# ------------ Run Server ------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
