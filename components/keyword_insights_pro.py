"""
Professional Keyword Insights Components
Matches VortexMini-style data tables and visualizations.
"""

from dash import html, dcc, dash_table
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict


def create_keywords_summary_table(keywords_df: pd.DataFrame, primary_company: str = None) -> html.Div:
    """
    Creates professional keyword summary table with competitor breakdown.

    Args:
        keywords_df: DataFrame with keyword data including competitor columns
        primary_company: Primary company domain (e.g., 'dossier.co')

    Returns:
        html.Div - Professional data table
    """
    if keywords_df is None or keywords_df.empty:
        return html.Div("No keyword data available", style={
            'padding': '40px',
            'textAlign': 'center',
            'color': '#95a5a6'
        })

    # Identify competitor columns (domains)
    competitor_cols = [col for col in keywords_df.columns
                      if '.' in col and 'Unnamed' not in col]

    # Prepare display columns
    display_cols = ['Keyword']
    if 'Clicks' in keywords_df.columns:
        display_cols.append('Clicks')
    if 'Search Volume' in keywords_df.columns:
        display_cols.append('Search Volume')

    # Add competitor columns
    display_cols.extend(competitor_cols)

    # Filter to display columns that exist
    available_cols = [col for col in display_cols if col in keywords_df.columns]
    table_data = keywords_df[available_cols].head(20)

    # Format data for display
    formatted_data = table_data.to_dict('records')

    # Define columns with proper formatting
    columns = []
    for col in available_cols:
        col_def = {
            'name': _format_column_name(col, primary_company),
            'id': col
        }

        # Format competitor columns as percentages
        if col in competitor_cols:
            col_def['type'] = 'numeric'
            col_def['format'] = {'specifier': '.0%'}
        # Format numeric columns
        elif col in ['Clicks', 'Search Volume']:
            col_def['type'] = 'numeric'
            col_def['format'] = {'specifier': ','}

        columns.append(col_def)

    return html.Div([
        html.H3("Keywords Summary", style={
            'fontSize': '18px',
            'fontWeight': '600',
            'color': '#2c3e50',
            'marginBottom': '20px',
            'padding': '0 30px'
        }),

        dash_table.DataTable(
            data=formatted_data,
            columns=columns,
            style_table={
                'overflowX': 'auto',
                'marginBottom': '30px'
            },
            style_header={
                'backgroundColor': '#5c6bc0',
                'color': 'white',
                'fontWeight': '600',
                'fontSize': '13px',
                'padding': '12px',
                'textAlign': 'left',
                'borderBottom': '2px solid #3f51b5'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '12px 15px',
                'fontSize': '13px',
                'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                'border': 'none',
                'borderBottom': '1px solid #e0e0e0'
            },
            style_data={
                'backgroundColor': 'white',
                'color': '#2c3e50'
            },
            style_data_conditional=[
                # Alternate row colors
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                },
                # Highlight primary company column
                {
                    'if': {'column_id': primary_company} if primary_company else {},
                    'backgroundColor': '#e8eaf6',
                    'fontWeight': '600'
                }
            ],
            page_size=20,
            sort_action='native',
            sort_mode='multi'
        )
    ], style={
        'background': 'white',
        'borderRadius': '8px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.08)',
        'padding': '20px 0'
    })


def _format_column_name(col: str, primary_company: str = None) -> str:
    """Format column name for display."""
    if col == 'Search Volume':
        return 'Search Volume'
    elif col == 'Clicks':
        return 'Total Clicks'
    elif '.' in col:
        # Extract company name from domain
        name = col.split('.')[0]
        # Mark primary company
        if col == primary_company:
            return f"{name.upper()} (You)"
        return name.title()
    return col


def create_keyword_traffic_share_chart(keywords_df: pd.DataFrame,
                                       primary_company: str = None,
                                       top_n: int = 20) -> dcc.Graph:
    """
    Creates stacked bar chart showing keyword traffic share by competitor.

    Args:
        keywords_df: DataFrame with keyword data
        primary_company: Primary company domain
        top_n: Number of keywords to show

    Returns:
        dcc.Graph - Stacked bar chart
    """
    if keywords_df is None or keywords_df.empty:
        return html.Div()

    # Identify competitor columns
    competitor_cols = [col for col in keywords_df.columns
                      if '.' in col and 'Unnamed' not in col]

    if not competitor_cols:
        return html.Div()

    # Get top N keywords by total traffic
    top_keywords = keywords_df.head(top_n).copy()

    # Create figure
    fig = go.Figure()

    # Color palette matching VortexMini style
    colors = {
        'primary': '#5c6bc0',  # Indigo
        'competitor_1': '#66bb6a',  # Green
        'competitor_2': '#42a5f5',  # Blue
        'competitor_3': '#ab47bc',  # Purple
        'competitor_4': '#26c6da',  # Cyan
        'competitor_5': '#ffa726',  # Orange
        'competitor_6': '#ec407a',  # Pink
        'other': '#bdbdbd'  # Gray
    }

    # Add traces for each competitor
    for i, competitor_col in enumerate(competitor_cols):
        if competitor_col not in top_keywords.columns:
            continue

        # Determine color
        if competitor_col == primary_company:
            color = colors['primary']
            name = f"{competitor_col.split('.')[0].upper()} (You)"
        else:
            color_key = f'competitor_{min(i, 6)}'
            color = colors.get(color_key, colors['other'])
            name = competitor_col.split('.')[0].title()

        fig.add_trace(go.Bar(
            name=name,
            x=top_keywords.get('Keyword', top_keywords.index),
            y=top_keywords[competitor_col],
            marker_color=color,
            hovertemplate='<b>%{x}</b><br>' + name + ': %{y:.1%}<extra></extra>',
            opacity=0.85
        ))

    # Update layout
    fig.update_layout(
        title={
            'text': f'Organic Keyword Traffic Share: Top {top_n} Keywords',
            'font': {'size': 16, 'color': '#2c3e50', 'family': 'Arial, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        barmode='stack',
        height=450,
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#e0e0e0',
            borderwidth=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=40, t=80, b=120),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=11),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='#e0e0e0'
        ),
        yaxis=dict(
            title='Traffic Share (%)',
            tickformat='.0%',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            showline=True,
            linewidth=1,
            linecolor='#e0e0e0'
        )
    )

    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={
            'background': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 1px 3px rgba(0,0,0,0.08)',
            'padding': '20px',
            'marginBottom': '30px'
        }
    )


def create_keywords_page_layout(keywords_df: pd.DataFrame,
                               keyword_type: str = 'Organic',
                               primary_company: str = None) -> html.Div:
    """
    Creates complete keywords page layout matching VortexMini style.

    Args:
        keywords_df: DataFrame with keyword data
        keyword_type: 'Organic' or 'Paid'
        primary_company: Primary company domain

    Returns:
        html.Div - Complete page layout
    """
    return html.Div([
        # Page Title
        html.H2(f"Top Keywords - {keyword_type} Breakdown", style={
            'fontSize': '24px',
            'fontWeight': '600',
            'color': '#2c3e50',
            'marginBottom': '30px',
            'padding': '0 30px'
        }),

        # Stacked Bar Chart
        html.Div([
            create_keyword_traffic_share_chart(keywords_df, primary_company, top_n=20)
        ], style={'padding': '0 30px', 'marginBottom': '40px'}),

        # Keywords Summary Table
        html.Div([
            create_keywords_summary_table(keywords_df, primary_company)
        ], style={'padding': '0'})

    ], style={
        'padding': '30px 0',
        'background': '#fafafa',
        'minHeight': '100vh'
    })


def create_simple_keywords_table(keywords: List[str],
                                 clicks: List[int],
                                 search_volumes: List[int]) -> html.Div:
    """
    Creates simplified keyword table for quick display.

    Args:
        keywords: List of keyword strings
        clicks: List of click values
        search_volumes: List of search volume values

    Returns:
        html.Div - Simple table
    """
    return html.Div([
        html.Table([
            # Header
            html.Thead([
                html.Tr([
                    html.Th('Keyword', style=_table_header_style()),
                    html.Th('Clicks', style=_table_header_style()),
                    html.Th('Search Volume', style=_table_header_style())
                ])
            ]),

            # Body
            html.Tbody([
                html.Tr([
                    html.Td(keyword, style=_table_cell_style()),
                    html.Td(f"{clicks[i]:,}", style=_table_cell_style()),
                    html.Td(f"{search_volumes[i]:,}", style=_table_cell_style())
                ], style={'background': '#f8f9fa' if i % 2 else 'white'})
                for i, keyword in enumerate(keywords)
            ])
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'fontSize': '13px',
            'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        })
    ], style={
        'background': 'white',
        'borderRadius': '8px',
        'boxShadow': '0 1px 3px rgba(0,0,0,0.08)',
        'overflow': 'hidden',
        'marginTop': '20px'
    })


def _table_header_style() -> Dict:
    """Header style for simple tables."""
    return {
        'backgroundColor': '#5c6bc0',
        'color': 'white',
        'fontWeight': '600',
        'padding': '12px 15px',
        'textAlign': 'left',
        'borderBottom': '2px solid #3f51b5'
    }


def _table_cell_style() -> Dict:
    """Cell style for simple tables."""
    return {
        'padding': '12px 15px',
        'borderBottom': '1px solid #e0e0e0',
        'color': '#2c3e50'
    }
