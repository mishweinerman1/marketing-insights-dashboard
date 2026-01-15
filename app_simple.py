"""
Marketing Insights Dashboard - Simplified Version
Using native Dash tabs for reliability.
"""

import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from config.branding import ClientBranding
from components.header import create_header
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

# App layout with native Dash tabs
app.layout = html.Div([
    dcc.Store(id='data-store', storage_type='session'),

    # Header
    create_header(client_name='Dossier', theme=theme),

    # File upload
    html.Div([
        html.Div([
            html.H3("Upload Marketing Data", style={'color': '#2c3e50', 'marginBottom': '15px'}),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.I(className='fas fa-cloud-upload-alt', style={'fontSize': '36px', 'color': '#667eea', 'marginBottom': '10px'}),
                    html.Div(['Drag and Drop or ', html.A('Select Excel File', style={'color': '#667eea', 'fontWeight': 'bold'})]),
                ]),
                style={
                    'width': '100%',
                    'height': '120px',
                    'lineHeight': '120px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderRadius': '10px',
                    'borderColor': '#667eea',
                    'textAlign': 'center',
                    'background': '#f8f9fa',
                    'cursor': 'pointer'
                },
                multiple=False
            ),
            html.Div(id='upload-status', style={'marginTop': '15px'}),

            # Business goals selection
            html.Div([
                html.Label("Select Business Goals:", style={
                    'fontWeight': '600',
                    'marginTop': '25px',
                    'marginBottom': '12px',
                    'color': '#2c3e50',
                    'fontSize': '15px'
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
                    value=['acquisition', 'conversion'],  # Default selections
                    style={'marginBottom': '20px'},
                    labelStyle={'display': 'block', 'marginBottom': '8px', 'fontSize': '14px', 'color': '#34495e'}
                )
            ], id='goals-section', style={'display': 'none', 'marginTop': '10px'})
        ], style={'maxWidth': '600px', 'margin': '0 auto', 'padding': '30px'})
    ], id='upload-section', style={'padding': '20px'}),

    # Native Dash tabs
    html.Div([
        dcc.Tabs(id='tabs', value='executive', children=[
            dcc.Tab(label='📊 Executive Summary', value='executive', style={'padding': '10px'}, selected_style={'padding': '10px', 'fontWeight': 'bold'}),
            dcc.Tab(label='📈 Overall Performance', value='performance', style={'padding': '10px'}, selected_style={'padding': '10px', 'fontWeight': 'bold'}),
            dcc.Tab(label='💰 Paid Search', value='paid-search', style={'padding': '10px'}, selected_style={'padding': '10px', 'fontWeight': 'bold'}),
            dcc.Tab(label='🔍 SEO', value='seo', style={'padding': '10px'}, selected_style={'padding': '10px', 'fontWeight': 'bold'}),
            dcc.Tab(label='🎯 Tactics Matrix', value='tactics', style={'padding': '10px'}, selected_style={'padding': '10px', 'fontWeight': 'bold'}),
        ], style={'marginBottom': '20px'}),
        html.Div(id='tab-content', style={'padding': '20px'})
    ], id='dashboard-section', style={'display': 'none'}),

    # Footer
    html.Div([
        html.P('Powered by AUX Insights | Marketing Intelligence Dashboard',
               style={'textAlign': 'center', 'color': '#95a5a6', 'fontSize': '14px'})
    ], style={'padding': '20px', 'marginTop': '40px', 'background': '#2c3e50'})
], style={'fontFamily': "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto", 'background': '#f8f9fa', 'minHeight': '100vh'})

# Upload callback
@app.callback(
    [Output('data-store', 'data'),
     Output('upload-status', 'children'),
     Output('upload-section', 'style'),
     Output('dashboard-section', 'style'),
     Output('data-status-indicator', 'children'),
     Output('data-status-indicator', 'style'),
     Output('goals-section', 'style')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def upload_file(contents, filename):
    if contents is None:
        return (None, "", {'padding': '20px'}, {'display': 'none'},
                [html.I(className='fas fa-exclamation-circle', style={'marginRight': '8px'}), 'No Data'],
                {'padding': '10px 20px', 'background': 'rgba(255,255,255,0.2)', 'borderRadius': '8px', 'color': '#ffffff', 'display': 'flex', 'alignItems': 'center'},
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
            return (None, html.Div(f"❌ Error: {error_msg}", style={'color': '#e74c3c'}),
                    {'padding': '20px'}, {'display': 'none'},
                    [html.I(className='fas fa-times-circle', style={'marginRight': '8px'}), 'Error'],
                    {'padding': '10px 20px', 'background': 'rgba(231,76,60,0.2)', 'borderRadius': '8px', 'color': '#ffffff', 'display': 'flex', 'alignItems': 'center'},
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
            html.I(className='fas fa-check-circle', style={'marginRight': '10px', 'color': '#27ae60'}),
            f"✓ Successfully loaded: {filename}"
        ], style={'color': '#27ae60', 'fontWeight': 'bold'})

        return (serializable_data, success_msg, {'display': 'none'}, {'display': 'block'},
                [html.I(className='fas fa-check-circle', style={'marginRight': '8px'}), 'Data Loaded'],
                {'padding': '10px 20px', 'background': 'rgba(46,204,113,0.3)', 'borderRadius': '8px', 'color': '#ffffff', 'display': 'flex', 'alignItems': 'center'},
                {'display': 'block', 'marginTop': '10px'})

    except Exception as e:
        return (None, html.Div(f"❌ Error: {str(e)}", style={'color': '#e74c3c'}),
                {'padding': '20px'}, {'display': 'none'},
                [html.I(className='fas fa-exclamation-triangle', style={'marginRight': '8px'}), 'Error'],
                {'padding': '10px 20px', 'background': 'rgba(231,76,60,0.2)', 'borderRadius': '8px', 'color': '#ffffff', 'display': 'flex', 'alignItems': 'center'},
                {'display': 'none'})

# Tab content callback
@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value'),
     Input('data-store', 'data')]
)
def render_tab_content(active_tab, data):
    from layouts import executive_summary, overall_performance, tactics_matrix
    from callbacks.navigation import create_paid_search_page, create_seo_page

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

    if active_tab == 'executive':
        channel_data = processed_data.get('executive_summary') if processed_data else None
        return executive_summary.create_layout(channel_data)
    elif active_tab == 'performance':
        return overall_performance.create_layout(processed_data)
    elif active_tab == 'paid-search':
        return create_paid_search_page(processed_data)
    elif active_tab == 'seo':
        return create_seo_page(processed_data)
    elif active_tab == 'tactics':
        tactics_df = processed_data.get('tactics') if processed_data else None
        return tactics_matrix.create_layout(tactics_df)
    else:
        return html.Div("Select a tab to view content")

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
    ║  🚀 Marketing Insights Dashboard (Simplified)           ║
    ║                                                          ║
    ║  📊 Dashboard URL: http://localhost:8050                ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=8050)
