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
        # Page title
        html.Div([
            html.H1("Marketing Tactics: Prioritization Matrix", style={
                'color': '#2c3e50',
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px'
            }),
            html.P(
                "Effort vs. Impact analysis to identify quick wins and strategic initiatives",
                style={
                    'color': '#7f8c8d',
                    'fontSize': '16px',
                    'marginBottom': '30px'
                }
            )
        ], style={'padding': '0 40px'}),

        # IE Matrix scatter plot
        html.Div([
            html.H2("Effort vs. Impact Matrix", style={
                'color': '#2c3e50',
                'fontSize': '24px',
                'fontWeight': '700',
                'marginBottom': '15px'
            }),
            html.P(
                "Bubble size represents projected cost. Color indicates funnel stage.",
                style={'color': '#7f8c8d', 'fontSize': '14px', 'marginBottom': '15px'}
            ),
            html.Div([
                create_tactics_matrix_scatter(tactics_data)
            ], style={
                'background': '#ffffff',
                'borderRadius': '15px',
                'padding': '20px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                'marginBottom': '30px'
            })
        ], style={'padding': '0 40px', 'marginBottom': '40px'}),

        # Quadrant explanations
        html.Div([
            html.Div([
                html.Div([
                    html.H4("🎯 Quick Wins", style={'color': '#27ae60', 'marginBottom': '10px'}),
                    html.P("Low effort, high impact - Prioritize these tactics first",
                          style={'color': '#7f8c8d', 'fontSize': '14px'})
                ], style={
                    'background': '#d4edda',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'flex': 1,
                    'margin': '0 10px'
                }),
                html.Div([
                    html.H4("🚀 Major Projects", style={'color': '#e67e22', 'marginBottom': '10px'}),
                    html.P("High effort, high impact - Strategic initiatives requiring resources",
                          style={'color': '#7f8c8d', 'fontSize': '14px'})
                ], style={
                    'background': '#fff3cd',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'flex': 1,
                    'margin': '0 10px'
                }),
                html.Div([
                    html.H4("⏳ Strategic", style={'color': '#3498db', 'marginBottom': '10px'}),
                    html.P("Low effort, low impact - Tactical improvements for optimization",
                          style={'color': '#7f8c8d', 'fontSize': '14px'})
                ], style={
                    'background': '#d1ecf1',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'flex': 1,
                    'margin': '0 10px'
                }),
                html.Div([
                    html.H4("❌ Low Priority", style={'color': '#c0392b', 'marginBottom': '10px'}),
                    html.P("High effort, low impact - Deprioritize or avoid",
                          style={'color': '#7f8c8d', 'fontSize': '14px'})
                ], style={
                    'background': '#f8d7da',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'flex': 1,
                    'margin': '0 10px'
                })
            ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'})
        ], style={'padding': '0 40px', 'marginBottom': '40px'}),

        # AI Recommendations Panel
        html.Div(id='recommendations-panel', style={'padding': '0 40px'}),

        # Tactics table
        html.Div([
            html.H2("All Marketing Tactics", style={
                'color': '#2c3e50',
                'fontSize': '24px',
                'fontWeight': '700',
                'marginBottom': '15px'
            }),
            html.Div([
                create_tactics_table(tactics_data) if tactics_data is not None else html.Div(
                    "Upload data to view tactics table",
                    style={'padding': '40px', 'textAlign': 'center', 'color': '#95a5a6'}
                )
            ], style={
                'background': '#ffffff',
                'borderRadius': '15px',
                'padding': '20px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'
            })
        ], style={'padding': '0 40px', 'marginBottom': '40px'})

    ], style={'padding': '30px 0'})


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
                'backgroundColor': '#d4edda',
                'color': '#155724',
                'fontWeight': 'bold'
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
            'padding': '12px',
            'fontSize': '13px',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto'
        },
        style_header={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'fontWeight': 'bold',
            'fontSize': '14px',
            'padding': '15px'
        },
        style_table={
            'overflowX': 'auto'
        }
    )
