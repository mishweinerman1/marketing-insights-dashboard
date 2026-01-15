"""
Marketing Insights Dashboard - VortexMini Professional Style
Professional sidebar navigation with clean, hierarchical design.
"""

import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from config.branding import ClientBranding
from components.sidebar_nav import create_sidebar_nav, create_top_header
import pandas as pd

# Initialize app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v6.1.1/css/all.css'
    ],
    suppress_callback_exceptions=True,
    title="Marketing Insights Dashboard"
)

server = app.server
theme = ClientBranding.get_theme('dossier')

# App layout with VortexMini professional design
app.layout = html.Div([
    dcc.Store(id='data-store', storage_type='session'),
    dcc.Location(id='url', pathname='/', refresh=False),

    # Left Sidebar Navigation (220px fixed)
    html.Div(id='sidebar-container'),

    # Top Header (60px dark bar)
    html.Div(id='header-container'),

    # Main Content Area (offset for sidebar and header)
    html.Div([
        # File upload (shown when no data)
        html.Div([
            html.Div([
                html.H3("Upload Marketing Data", style={
                    'color': '#2c3e50',
                    'marginBottom': '15px',
                    'fontSize': '24px',
                    'fontWeight': '600'
                }),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        html.I(className='fas fa-cloud-upload-alt', style={
                            'fontSize': '48px',
                            'color': '#5c6bc0',
                            'marginBottom': '15px'
                        }),
                        html.Div('Drag and Drop or ', style={
                            'display': 'inline',
                            'fontSize': '16px',
                            'color': '#7f8c8d'
                        }),
                        html.A('Select Excel File', style={
                            'color': '#5c6bc0',
                            'fontWeight': '600',
                            'textDecoration': 'underline',
                            'fontSize': '16px'
                        }),
                    ], style={
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'height': '100%'
                    }),
                    style={
                        'width': '100%',
                        'height': '200px',
                        'borderWidth': '3px',
                        'borderStyle': 'dashed',
                        'borderRadius': '12px',
                        'borderColor': '#5c6bc0',
                        'textAlign': 'center',
                        'background': 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)',
                        'cursor': 'pointer',
                        'transition': 'all 0.3s ease'
                    },
                    multiple=False
                ),
                html.Div(id='upload-status', style={'marginTop': '20px'}),

                # Business goals selection
                html.Div([
                    html.Label("Select Business Goals:", style={
                        'fontWeight': '600',
                        'marginTop': '30px',
                        'marginBottom': '15px',
                        'color': '#2c3e50',
                        'fontSize': '16px'
                    }),
                    dcc.Checklist(
                        id='business-goals',
                        options=[
                            {'label': ' Increase Traffic (Acquisition)', 'value': 'acquisition'},
                            {'label': ' Improve Conversions', 'value': 'conversion'},
                            {'label': ' Boost Customer Lifetime Value', 'value': 'ltv'},
                            {'label': ' Enhance User Experience', 'value': 'user_experience'},
                            {'label': ' Reduce Bounce Rate', 'value': 'engagement'},
                            {'label': ' Improve SEO Rankings', 'value': 'seo'}
                        ],
                        value=['acquisition', 'conversion'],
                        style={'marginBottom': '20px'},
                        labelStyle={
                            'display': 'block',
                            'marginBottom': '12px',
                            'fontSize': '15px',
                            'color': '#34495e',
                            'fontWeight': '500'
                        }
                    )
                ], id='goals-section', style={'display': 'none', 'marginTop': '15px'})
            ], style={
                'maxWidth': '700px',
                'margin': '0 auto',
                'padding': '40px',
                'background': 'white',
                'borderRadius': '15px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.08)'
            })
        ], id='upload-section', style={
            'padding': '40px',
            'minHeight': 'calc(100vh - 60px)',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        }),

        # Dashboard content (shown after upload)
        html.Div([
            html.Div(id='page-content', style={'padding': '30px'})
        ], id='dashboard-section', style={'display': 'none', 'minHeight': 'calc(100vh - 60px)'})

    ], id='main-content', style={
        'marginLeft': '220px',
        'marginTop': '60px',
        'background': '#fafafa',
        'minHeight': 'calc(100vh - 60px)'
    }),

    # Footer
    html.Div([
        html.Div([
            html.Span('Powered by ', style={'color': '#95a5a6', 'fontSize': '13px'}),
            html.Span('AUX Insights', style={'color': '#5c6bc0', 'fontWeight': '600', 'fontSize': '13px'}),
            html.Span(' | Marketing Intelligence Dashboard', style={'color': '#95a5a6', 'fontSize': '13px'})
        ], style={'textAlign': 'center', 'padding': '20px'})
    ], style={
        'marginLeft': '220px',
        'background': '#2c3e50',
        'borderTop': '1px solid #34495e'
    })
], style={
    'fontFamily': "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    'background': '#fafafa'
})

# Sidebar and header dynamic callbacks
@app.callback(
    [Output('sidebar-container', 'children'),
     Output('header-container', 'children')],
    [Input('url', 'pathname'),
     Input('data-store', 'data')]
)
def update_navigation(pathname, data):
    """Update sidebar and header based on current page and data status."""
    is_complete = data is not None
    sidebar = create_sidebar_nav(current_page=pathname or '/')
    header = create_top_header(
        report_title='Marketing Insights',
        client_name='Dossier',
        is_complete=is_complete
    )
    return sidebar, header

# Upload callback
@app.callback(
    [Output('data-store', 'data'),
     Output('upload-status', 'children'),
     Output('upload-section', 'style'),
     Output('dashboard-section', 'style'),
     Output('goals-section', 'style')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def upload_file(contents, filename):
    if contents is None:
        return (None, "",
                {'padding': '40px', 'minHeight': 'calc(100vh - 60px)', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
                {'display': 'none'},
                {'display': 'none'})

    try:
        from data.loader import ExcelDataLoader
        from data.processor import DataProcessor
        from data.validators import DataValidator
        import io, base64

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        excel_file = io.BytesIO(decoded)

        is_valid, error_msg, warnings = DataValidator.validate_excel_structure(excel_file)
        if not is_valid:
            return (None, html.Div(f"❌ Error: {error_msg}", style={'color': '#e74c3c', 'fontWeight': '600'}),
                    {'padding': '40px', 'minHeight': 'calc(100vh - 60px)', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
                    {'display': 'none'},
                    {'display': 'none'})

        excel_file.seek(0)
        loader = ExcelDataLoader(excel_file)
        sheets = loader.load_all_sheets()
        processor = DataProcessor()
        processed_data = processor.process_all_data(sheets)

        # Convert to JSON-serializable
        serializable_data = {}
        for key, value in processed_data.items():
            if hasattr(value, 'to_dict'):
                serializable_data[key] = value.to_dict('records')
            else:
                serializable_data[key] = value

        success_msg = html.Div([
            html.I(className='fas fa-check-circle', style={'marginRight': '10px', 'color': '#27ae60', 'fontSize': '20px'}),
            f"✓ Successfully loaded: {filename}"
        ], style={'color': '#27ae60', 'fontWeight': 'bold', 'fontSize': '16px'})

        return (serializable_data, success_msg,
                {'display': 'none'},
                {'display': 'block', 'minHeight': 'calc(100vh - 60px)'},
                {'display': 'block', 'marginTop': '15px'})

    except Exception as e:
        return (None, html.Div(f"❌ Error: {str(e)}", style={'color': '#e74c3c', 'fontWeight': '600'}),
                {'padding': '40px', 'minHeight': 'calc(100vh - 60px)', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
                {'display': 'none'},
                {'display': 'none'})

# Page content callback (navigation routing)
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('data-store', 'data')]
)
def display_page(pathname, data):
    """Route to different pages based on URL pathname."""
    from layouts import executive_summary, overall_performance, tactics_matrix
    from callbacks.navigation import create_paid_search_page, create_seo_page
    from components.keyword_insights_pro import create_keywords_page_layout

    # Convert data back to DataFrames
    processed_data = None
    if data:
        processed_data = {}
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                try:
                    processed_data[key] = pd.DataFrame(value)
                except:
                    processed_data[key] = value
            else:
                processed_data[key] = value

    # Route to appropriate page
    if pathname == '/' or pathname is None:
        channel_data = processed_data.get('executive_summary') if processed_data else None
        return executive_summary.create_layout(channel_data)

    elif pathname == '/performance':
        return overall_performance.create_layout(processed_data)

    elif pathname == '/tactics':
        tactics_df = processed_data.get('tactics') if processed_data else None
        return tactics_matrix.create_layout(tactics_df)

    elif pathname == '/paid-search':
        return create_paid_search_page(processed_data)

    elif pathname == '/seo':
        return create_seo_page(processed_data)

    elif pathname == '/keywords-organic':
        keywords_df = processed_data.get('keywords_organic') if processed_data else None
        return create_keywords_page_layout(keywords_df, keyword_type='Organic', primary_company='dossier.co')

    elif pathname == '/keywords-paid':
        keywords_df = processed_data.get('keywords_paid') if processed_data else None
        return create_keywords_page_layout(keywords_df, keyword_type='Paid', primary_company='dossier.co')

    else:
        return html.Div([
            html.H2("404: Page Not Found", style={'color': '#e74c3c', 'textAlign': 'center', 'marginTop': '50px'}),
            html.P("The page you're looking for doesn't exist.", style={'textAlign': 'center', 'color': '#95a5a6'})
        ])

# Register recommendations callbacks
from callbacks.recommendations import register_recommendations_callbacks
register_recommendations_callbacks(app)

# Register competitive intelligence callbacks
from callbacks.competitive_intel import register_competitive_intel_callbacks
register_competitive_intel_callbacks(app)

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║  🚀 Marketing Insights Dashboard (VortexMini Style)     ║
    ║                                                          ║
    ║  📊 Dashboard URL: http://localhost:8050                ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=8050)
