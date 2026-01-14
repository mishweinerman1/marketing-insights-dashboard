"""
Branded header component with gradient background.
Displays client name, logo, and dashboard title.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime


def create_header(client_name='AUX Insights', theme=None, subtitle='Outside-In Analysis'):
    """
    Creates branded gradient header for dashboard.

    Args:
        client_name: str - Client company name
        theme: dict - Theme configuration from branding.py
        subtitle: str - Subtitle for header

    Returns:
        html.Div - Header component
    """
    if theme is None:
        from config.branding import ClientBranding
        theme = ClientBranding.get_theme()

    current_date = datetime.now().strftime('%B %d, %Y')

    return html.Div([
        html.Div([
            # Left side: Logo and title
            html.Div([
                html.Div([
                    html.H1(
                        [
                            html.Span('AUX', style={
                                'fontWeight': '700',
                                'marginRight': '10px'
                            }),
                            html.Span('INSIGHTS', style={
                                'fontWeight': '300',
                                'letterSpacing': '2px'
                            })
                        ],
                        style={
                            'color': '#ffffff',
                            'margin': 0,
                            'fontSize': '28px',
                            'marginBottom': '5px'
                        }
                    ),
                    html.H2(
                        f"{client_name} - {subtitle}",
                        style={
                            'color': '#ffffff',
                            'margin': 0,
                            'fontSize': '32px',
                            'fontWeight': '700',
                            'marginBottom': '8px'
                        }
                    ),
                    html.P(
                        f"Marketing Insights Dashboard · {current_date}",
                        style={
                            'color': 'rgba(255,255,255,0.85)',
                            'margin': 0,
                            'fontSize': '14px',
                            'fontWeight': '400'
                        }
                    )
                ])
            ], style={'flex': 1}),

            # Right side: Status indicator
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className='fas fa-check-circle', style={
                            'marginRight': '8px',
                            'fontSize': '20px'
                        }),
                        html.Span('Data Loaded', style={
                            'fontSize': '14px',
                            'fontWeight': '500'
                        })
                    ], id='data-status-indicator', style={
                        'padding': '10px 20px',
                        'background': 'rgba(255,255,255,0.2)',
                        'borderRadius': '8px',
                        'color': '#ffffff',
                        'display': 'flex',
                        'alignItems': 'center'
                    })
                ])
            ], style={'textAlign': 'right'})
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between'
        })
    ], style={
        'background': theme['gradient'],
        'padding': '30px 40px',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
        'marginBottom': '0'
    })


def create_navigation_tabs(active_tab='executive'):
    """
    Creates navigation tabs for dashboard sections.

    Args:
        active_tab: str - Currently active tab ID

    Returns:
        html.Div - Navigation tabs component
    """
    tabs = [
        {'id': 'executive', 'label': 'Executive Summary', 'icon': 'fa-chart-pie'},
        {'id': 'performance', 'label': 'Overall Performance', 'icon': 'fa-chart-line'},
        {'id': 'paid-search', 'label': 'Paid Search', 'icon': 'fa-search-dollar'},
        {'id': 'paid-social', 'label': 'Paid Social', 'icon': 'fa-share-alt'},
        {'id': 'seo', 'label': 'SEO', 'icon': 'fa-search'},
        {'id': 'crm', 'label': 'CRM', 'icon': 'fa-envelope'},
        {'id': 'cro', 'label': 'CRO', 'icon': 'fa-chart-bar'},
        {'id': 'tactics', 'label': 'Tactics Matrix', 'icon': 'fa-th'}
    ]

    tab_elements = []

    for tab in tabs:
        is_active = tab['id'] == active_tab

        tab_style = {
            'padding': '15px 25px',
            'cursor': 'pointer',
            'borderBottom': f"3px solid {'#667eea' if is_active else 'transparent'}",
            'color': '#667eea' if is_active else '#7f8c8d',
            'fontWeight': '600' if is_active else '500',
            'fontSize': '14px',
            'transition': 'all 0.3s ease',
            'display': 'inline-block',
            'textDecoration': 'none'
        }

        tab_elements.append(
            dcc.Link([
                html.I(className=f'fas {tab["icon"]}', style={'marginRight': '8px'}),
                html.Span(tab['label'])
            ], href=f'/{tab["id"]}', style=tab_style, id=f'tab-{tab["id"]}')
        )

    return html.Div(
        tab_elements,
        style={
            'background': '#ffffff',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
            'padding': '0 40px',
            'marginBottom': '30px'
        }
    )


def create_breadcrumb(path=['Home', 'Executive Summary']):
    """
    Creates breadcrumb navigation.

    Args:
        path: list - List of breadcrumb items

    Returns:
        html.Div - Breadcrumb component
    """
    breadcrumb_items = []

    for i, item in enumerate(path):
        breadcrumb_items.append(
            html.Span(item, style={
                'color': '#667eea' if i == len(path) - 1 else '#7f8c8d',
                'fontWeight': '600' if i == len(path) - 1 else '400'
            })
        )

        if i < len(path) - 1:
            breadcrumb_items.append(
                html.Span(' / ', style={'margin': '0 10px', 'color': '#bdc3c7'})
            )

    return html.Div(
        breadcrumb_items,
        style={
            'padding': '15px 40px',
            'fontSize': '13px',
            'background': '#f8f9fa'
        }
    )
