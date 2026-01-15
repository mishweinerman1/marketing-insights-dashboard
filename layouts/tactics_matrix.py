"""
Tactics Prioritization Matrix layout.
IE Matrix scatter plot showing effort vs. impact for marketing tactics.
"""

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from components.charts import create_tactics_matrix_scatter
import pandas as pd


def create_layout(tactics_data=None):
    """
    Creates tactics prioritization matrix page.

    Args:
        tactics_data: pandas.DataFrame - Tactics with effort, lift, and cost

    Returns:
        html.Div - Tactics matrix layout
    """
    return html.Div([
        # Page title - VortexMini style
        html.Div([
            html.H1("Marketing Tactics: Prioritization Matrix", style={
                'color': '#2c3e50',
                'fontSize': '32px',
                'fontWeight': '600',
                'marginBottom': '8px',
                'letterSpacing': '-0.5px'
            }),
            html.P(
                "Effort vs. Impact analysis to identify quick wins and strategic initiatives",
                style={
                    'color': '#7f8c8d',
                    'fontSize': '15px',
                    'marginBottom': '30px',
                    'lineHeight': '1.5'
                }
            )
        ], style={'padding': '0 30px', 'marginBottom': '15px'}),

        # IE Matrix scatter plot - VortexMini style
        html.Div([
            html.H2("Effort vs. Impact Matrix", style={
                'color': '#2c3e50',
                'fontSize': '20px',
                'fontWeight': '600',
                'marginBottom': '12px',
                'letterSpacing': '-0.3px'
            }),
            html.P(
                "Bubble size represents projected cost. Color indicates funnel stage.",
                style={'color': '#7f8c8d', 'fontSize': '13px', 'marginBottom': '15px'}
            ),
            html.Div([
                create_tactics_matrix_scatter(tactics_data)
            ], style={
                'background': '#ffffff',
                'borderRadius': '8px',
                'padding': '25px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.08)',
                'border': '1px solid #e0e0e0'
            })
        ], style={'padding': '0 30px', 'marginBottom': '35px'}),

        # Quadrant explanations - VortexMini style
        html.Div([
            html.Div([
                html.Div([
                    html.H4("🎯 Quick Wins", style={'color': '#27ae60', 'marginBottom': '8px', 'fontSize': '16px', 'fontWeight': '600'}),
                    html.P("Low effort, high impact - Prioritize these tactics first",
                          style={'color': '#34495e', 'fontSize': '13px', 'lineHeight': '1.5'})
                ], style={
                    'background': '#ffffff',
                    'padding': '18px 20px',
                    'borderRadius': '8px',
                    'flex': 1,
                    'border': '2px solid #27ae60',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.06)'
                }),
                html.Div([
                    html.H4("🚀 Major Projects", style={'color': '#e67e22', 'marginBottom': '8px', 'fontSize': '16px', 'fontWeight': '600'}),
                    html.P("High effort, high impact - Strategic initiatives requiring resources",
                          style={'color': '#34495e', 'fontSize': '13px', 'lineHeight': '1.5'})
                ], style={
                    'background': '#ffffff',
                    'padding': '18px 20px',
                    'borderRadius': '8px',
                    'flex': 1,
                    'border': '2px solid #e67e22',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.06)'
                }),
                html.Div([
                    html.H4("⏳ Strategic", style={'color': '#5c6bc0', 'marginBottom': '8px', 'fontSize': '16px', 'fontWeight': '600'}),
                    html.P("Low effort, low impact - Tactical improvements for optimization",
                          style={'color': '#34495e', 'fontSize': '13px', 'lineHeight': '1.5'})
                ], style={
                    'background': '#ffffff',
                    'padding': '18px 20px',
                    'borderRadius': '8px',
                    'flex': 1,
                    'border': '2px solid #5c6bc0',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.06)'
                }),
                html.Div([
                    html.H4("❌ Low Priority", style={'color': '#c0392b', 'marginBottom': '8px', 'fontSize': '16px', 'fontWeight': '600'}),
                    html.P("High effort, low impact - Deprioritize or avoid",
                          style={'color': '#34495e', 'fontSize': '13px', 'lineHeight': '1.5'})
                ], style={
                    'background': '#ffffff',
                    'padding': '18px 20px',
                    'borderRadius': '8px',
                    'flex': 1,
                    'border': '2px solid #c0392b',
                    'boxShadow': '0 1px 3px rgba(0,0,0,0.06)'
                })
            ], style={'display': 'flex', 'gap': '15px', 'flexWrap': 'wrap'})
        ], style={'padding': '0 30px', 'marginBottom': '35px'}),

        # AI Recommendations Panel
        html.Div(id='recommendations-panel', style={'padding': '0 30px', 'marginBottom': '35px'}),

        # Competitive Intelligence Panel
        html.Div(id='competitive-intel-panel', style={'padding': '0 30px', 'marginBottom': '35px'}),

        # Tactics table - VortexMini style
        html.Div([
            html.H2("All Marketing Tactics", style={
                'color': '#2c3e50',
                'fontSize': '20px',
                'fontWeight': '600',
                'marginBottom': '18px',
                'letterSpacing': '-0.3px'
            }),
            html.Div([
                create_tactics_table(tactics_data) if tactics_data is not None else html.Div(
                    "Upload data to view tactics table",
                    style={'padding': '40px', 'textAlign': 'center', 'color': '#95a5a6', 'fontSize': '14px'}
                )
            ], style={
                'background': '#ffffff',
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 1px 3px rgba(0,0,0,0.08)',
                'border': '1px solid #e0e0e0'
            })
        ], style={'padding': '0 30px', 'marginBottom': '30px'})

    ], style={'padding': '20px 0', 'background': '#fafafa'})


def create_tactics_table(df):
    """
    Creates sortable tactics table.

    Args:
        df: pandas.DataFrame - Tactics data

    Returns:
        dash_table.DataTable
    """
    if df is None or df.empty:
        return html.Div("No tactics data available")

    # Select relevant columns
    display_columns = []
    column_names = {}

    if 'Marketing Tactic' in df.columns:
        display_columns.append('Marketing Tactic')
        column_names['Marketing Tactic'] = 'Tactic'
    elif 'Tactics' in df.columns:
        display_columns.append('Tactics')
        column_names['Tactics'] = 'Tactic'

    if 'Focus (Funnel Stage)' in df.columns:
        display_columns.append('Focus (Funnel Stage)')
        column_names['Focus (Funnel Stage)'] = 'Stage'

    for col in ['Total Effort', 'Projected Cost', 'Expected Lift %', 'Priority Score']:
        if col in df.columns:
            display_columns.append(col)
            column_names[col] = col

    if not display_columns:
        return html.Div("No compatible data structure")

    df_display = df[display_columns].copy()

    # Format numeric columns
    if 'Expected Lift %' in df_display.columns:
        df_display['Expected Lift %'] = (df_display['Expected Lift %'] * 100).round(2)

    if 'Priority Score' in df_display.columns:
        df_display['Priority Score'] = df_display['Priority Score'].round(2)

    columns = [
        {'name': column_names.get(col, col), 'id': col, 'type': 'numeric' if col != display_columns[0] else 'text'}
        for col in display_columns
    ]

    return dash_table.DataTable(
        data=df_display.to_dict('records'),
        columns=columns,
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Priority Score} > 2.0',
                    'column_id': 'Priority Score'
                },
                'backgroundColor': '#e8f5e9',
                'color': '#2e7d32',
                'fontWeight': '600'
            },
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            }
        ],
        sort_action='native',
        filter_action='native',
        page_size=20,
        style_cell={
            'textAlign': 'left',
            'padding': '12px 15px',
            'fontSize': '13px',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'border': 'none',
            'borderBottom': '1px solid #e0e0e0'
        },
        style_header={
            'backgroundColor': '#5c6bc0',
            'color': 'white',
            'fontWeight': '600',
            'fontSize': '13px',
            'padding': '12px 15px',
            'borderBottom': '2px solid #3f51b5'
        },
        style_data={
            'backgroundColor': 'white',
            'color': '#2c3e50'
        },
        style_table={
            'overflowX': 'auto'
        }
    )
