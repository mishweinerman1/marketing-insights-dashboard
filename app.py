"""
Marketing Insights Dashboard - Main Application
Interactive Dash dashboard for marketing analysis and tactics prioritization.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.branding import ClientBranding
from components.header import create_header, create_navigation_tabs

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v6.1.1/css/all.css'  # Font Awesome icons
    ],
    suppress_callback_exceptions=True,
    title="Marketing Insights Dashboard | AUX Insights"
)

# For gunicorn deployment
server = app.server

# Get default theme
theme = ClientBranding.get_theme('dossier')

# App layout
app.layout = html.Div([
    # URL routing
    dcc.Location(id='url', refresh=False),

    # Data storage (client-side)
    dcc.Store(id='data-store', storage_type='session'),

    # Header
    create_header(client_name='Dossier', theme=theme, subtitle='Outside-In Analysis'),

    # Navigation tabs
    create_navigation_tabs(active_tab='executive'),

    # File upload section (shown when no data is loaded)
    html.Div([
        html.Div([
            html.H2("Welcome to Marketing Insights Dashboard", style={
                'color': '#2c3e50',
                'marginBottom': '15px',
                'textAlign': 'center'
            }),
            html.P(
                "Upload your marketing analysis Excel file to begin",
                style={
                    'color': '#7f8c8d',
                    'fontSize': '16px',
                    'textAlign': 'center',
                    'marginBottom': '30px'
                }
            ),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.I(className='fas fa-cloud-upload-alt', style={
                        'fontSize': '48px',
                        'color': '#667eea',
                        'marginBottom': '15px'
                    }),
                    html.Div([
                        'Drag and Drop or ',
                        html.A('Select Excel File', style={'color': '#667eea', 'fontWeight': 'bold'})
                    ], style={'fontSize': '16px', 'color': '#7f8c8d'})
                ]),
                style={
                    'width': '100%',
                    'height': '200px',
                    'lineHeight': '200px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderRadius': '15px',
                    'borderColor': '#667eea',
                    'textAlign': 'center',
                    'background': '#f8f9fa',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease'
                },
                style_active={
                    'borderColor': '#2ecc71',
                    'background': '#e8f8f5'
                },
                multiple=False
            ),
            html.Div(id='upload-status', style={'marginTop': '20px'}),
            html.Div([
                html.H4("Expected File Structure:", style={
                    'color': '#2c3e50',
                    'marginTop': '30px',
                    'marginBottom': '15px'
                }),
                html.Ul([
                    html.Li("Similarweb Lead Enrichment (traffic data)"),
                    html.Li("Similarweb PPC Spend (paid advertising)"),
                    html.Li("Low Hanging Fruit (marketing tactics)"),
                    html.Li("IE Matrix (effort vs. impact scores)"),
                    html.Li("Core Web Vitals (performance metrics)"),
                    html.Li("Keyword reports (paid and organic)")
                ], style={'color': '#7f8c8d', 'fontSize': '14px', 'lineHeight': 1.8})
            ], style={
                'marginTop': '30px',
                'padding': '20px',
                'background': '#f8f9fa',
                'borderRadius': '10px'
            })
        ], style={
            'maxWidth': '800px',
            'margin': '0 auto',
            'padding': '40px',
            'background': '#ffffff',
            'borderRadius': '15px',
            'boxShadow': '0 4px 20px rgba(0,0,0,0.08)'
        })
    ], style={'padding': '40px'}, id='upload-section'),

    # Main content area (pages will be rendered here)
    html.Div(id='page-content', style={'minHeight': '600px'}),

    # Footer
    html.Div([
        html.Div([
            html.Div([
                html.Span('Powered by ', style={'color': '#95a5a6'}),
                html.Strong('AUX Insights', style={'color': '#667eea'}),
                html.Span(' | Marketing Intelligence Dashboard', style={'color': '#95a5a6'})
            ], style={'textAlign': 'center', 'fontSize': '14px'}),
            html.Div([
                html.Span('Built with ', style={'color': '#95a5a6', 'marginRight': '5px'}),
                html.I(className='fas fa-heart', style={'color': '#e74c3c', 'marginRight': '5px'}),
                html.Span('using Dash & Plotly', style={'color': '#95a5a6'})
            ], style={'textAlign': 'center', 'fontSize': '12px', 'marginTop': '10px'})
        ])
    ], style={
        'padding': '30px',
        'background': '#2c3e50',
        'marginTop': '60px',
        'color': '#ffffff'
    })
], style={
    'fontFamily': "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    'background': '#f8f9fa',
    'minHeight': '100vh'
})

# Register callbacks
from callbacks import data_upload, navigation

data_upload.register_callbacks(app)
navigation.register_callbacks(app)

# Run app
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║  🚀 Marketing Insights Dashboard Starting...            ║
    ║                                                          ║
    ║  📊 Dashboard URL: http://localhost:8050                ║
    ║                                                          ║
    ║  📁 Upload your Excel file to begin analysis            ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=8050)
