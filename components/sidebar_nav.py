"""
Professional Sidebar Navigation Component
Matches VortexMini-style clean, hierarchical navigation design.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_sidebar_nav(current_page='/'):
    """
    Creates professional left sidebar navigation.

    Args:
        current_page: str - Current active page path

    Returns:
        html.Div - Sidebar navigation component
    """
    return html.Div([
        # Logo Section
        html.Div([
            html.Img(src='/assets/logo.png', style={
                'height': '40px',
                'marginBottom': '5px'
            }) if False else None,  # Set to True when logo exists
            html.Div([
                html.Span('Marketing', style={'fontWeight': '700', 'fontSize': '18px'}),
                html.Span('Insights', style={'fontWeight': '300', 'fontSize': '14px', 'marginLeft': '5px'})
            ], style={'color': '#2c3e50'})
        ], style={
            'padding': '20px 15px',
            'borderBottom': '1px solid #e0e0e0',
            'marginBottom': '10px'
        }),

        # User/Report Section
        html.Div([
            html.I(className='fas fa-chart-bar', style={
                'fontSize': '20px',
                'color': '#95a5a6',
                'marginRight': '10px'
            }),
            html.Span('Report', style={'fontSize': '14px', 'color': '#7f8c8d', 'fontWeight': '500'})
        ], style={
            'padding': '15px',
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '20px'
        }),

        # Navigation Sections
        create_nav_section('Overview', [
            {'label': 'Executive Summary', 'path': '/', 'icon': 'fa-home'},
            {'label': 'Overall Performance', 'path': '/performance', 'icon': 'fa-chart-line'},
            {'label': 'Tactics Matrix', 'path': '/tactics', 'icon': 'fa-th'}
        ], current_page),

        create_nav_section('Competitive Analysis', [
            {'label': 'Competitive Breakdown', 'path': '/competitive', 'icon': 'fa-users'},
            {'label': 'Market Position', 'path': '/market-position', 'icon': 'fa-trophy'}
        ], current_page),

        create_nav_section('Search & Keywords', [
            {'label': 'Paid Search (PPC)', 'path': '/paid-search', 'icon': 'fa-dollar-sign'},
            {'label': 'Organic Search (SEO)', 'path': '/seo', 'icon': 'fa-search'},
            {'label': 'Top Keywords - Organic', 'path': '/keywords-organic', 'icon': 'fa-key'},
            {'label': 'Top Keywords - Paid', 'path': '/keywords-paid', 'icon': 'fa-key'}
        ], current_page),

        create_nav_section('Conversion', [
            {'label': 'CRO Analysis', 'path': '/cro', 'icon': 'fa-funnel-dollar'},
            {'label': 'User Experience', 'path': '/ux', 'icon': 'fa-smile'}
        ], current_page),

        create_nav_section('Social & Email', [
            {'label': 'Paid Social', 'path': '/paid-social', 'icon': 'fa-facebook'},
            {'label': 'CRM / Email', 'path': '/crm', 'icon': 'fa-envelope'}
        ], current_page),

        # Bottom Actions
        html.Div([
            html.Hr(style={'margin': '20px 0', 'borderColor': '#e0e0e0'}),

            create_action_button('Refresh Data', 'fa-sync-alt', 'refresh-data-btn'),
            create_action_button('Export Report', 'fa-file-export', 'export-report-btn'),
            create_action_button('Settings', 'fa-cog', 'settings-btn')
        ], style={'position': 'absolute', 'bottom': '20px', 'width': 'calc(100% - 30px)'})

    ], style={
        'width': '220px',
        'height': '100vh',
        'position': 'fixed',
        'left': '0',
        'top': '0',
        'background': '#f8f9fa',
        'borderRight': '1px solid #e0e0e0',
        'overflowY': 'auto',
        'overflowX': 'hidden',
        'zIndex': '1000',
        'fontFamily': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    })


def create_nav_section(title, items, current_page):
    """Create a navigation section with title and items."""
    return html.Div([
        # Section Title
        html.Div(title, style={
            'fontSize': '12px',
            'fontWeight': '700',
            'color': '#2c3e50',
            'textTransform': 'uppercase',
            'letterSpacing': '0.5px',
            'padding': '8px 15px',
            'marginTop': '15px',
            'marginBottom': '5px'
        }),

        # Section Items
        html.Div([
            create_nav_item(item['label'], item['path'], item.get('icon'), current_page)
            for item in items
        ])
    ])


def create_nav_item(label, path, icon=None, current_page='/'):
    """Create individual navigation item."""
    is_active = current_page == path

    return dcc.Link([
        html.I(className=f'fas {icon}', style={
            'fontSize': '13px',
            'marginRight': '10px',
            'color': '#667eea' if is_active else '#95a5a6',
            'width': '16px'
        }) if icon else None,
        html.Span(label, style={
            'fontSize': '14px',
            'fontWeight': '500' if is_active else '400'
        })
    ], href=path, style={
        'display': 'flex',
        'alignItems': 'center',
        'padding': '10px 15px',
        'color': '#2c3e50' if is_active else '#7f8c8d',
        'textDecoration': 'none',
        'background': '#e8eaf6' if is_active else 'transparent',
        'borderLeft': '3px solid #667eea' if is_active else '3px solid transparent',
        'transition': 'all 0.2s ease',
        ':hover': {
            'background': '#f0f0f0',
            'color': '#2c3e50'
        }
    })


def create_action_button(label, icon, button_id):
    """Create action button for sidebar."""
    return html.Div([
        html.I(className=f'fas {icon}', style={
            'fontSize': '14px',
            'marginRight': '8px',
            'color': '#7f8c8d'
        }),
        html.Span(label, style={'fontSize': '13px'})
    ], id=button_id, style={
        'display': 'flex',
        'alignItems': 'center',
        'padding': '10px 15px',
        'color': '#7f8c8d',
        'cursor': 'pointer',
        'borderRadius': '6px',
        'marginBottom': '5px',
        'transition': 'all 0.2s ease',
        ':hover': {
            'background': '#e8eaf6',
            'color': '#667eea'
        }
    })


def create_top_header(report_title='Marketing Insights Report', client_name='Dossier', is_complete=True):
    """
    Creates dark top header bar matching VortexMini style.

    Args:
        report_title: str - Report title
        client_name: str - Client name
        is_complete: bool - Whether analysis is complete

    Returns:
        html.Div - Top header component
    """
    return html.Div([
        # Left side - Menu and title
        html.Div([
            html.I(className='fas fa-bars', style={
                'fontSize': '20px',
                'color': '#ffffff',
                'marginRight': '20px',
                'cursor': 'pointer'
            }),
            html.Span(f'Report: {report_title}', style={
                'fontSize': '16px',
                'fontWeight': '600',
                'color': '#ffffff'
            })
        ], style={'display': 'flex', 'alignItems': 'center'}),

        # Right side - Status and logout
        html.Div([
            html.Div([
                html.I(className='fas fa-check-circle', style={
                    'fontSize': '14px',
                    'marginRight': '6px',
                    'color': '#4caf50'
                }) if is_complete else html.I(className='fas fa-clock', style={
                    'fontSize': '14px',
                    'marginRight': '6px',
                    'color': '#ffa726'
                }),
                html.Span('Analysis complete' if is_complete else 'Analyzing...', style={
                    'fontSize': '13px',
                    'color': '#ffffff'
                })
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'background': 'rgba(255,255,255,0.1)',
                'padding': '6px 12px',
                'borderRadius': '4px',
                'marginRight': '15px'
            }),

            html.Button('LOGOUT', style={
                'background': 'transparent',
                'border': 'none',
                'color': '#ffffff',
                'fontSize': '12px',
                'fontWeight': '600',
                'cursor': 'pointer',
                'letterSpacing': '0.5px'
            })
        ], style={'display': 'flex', 'alignItems': 'center'})

    ], style={
        'position': 'fixed',
        'top': '0',
        'left': '220px',
        'right': '0',
        'height': '60px',
        'background': '#4a4a4a',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'space-between',
        'padding': '0 30px',
        'zIndex': '999',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    })


def create_breadcrumb_nav(client='Clients', category='Analytics', report='Marketing Insights'):
    """
    Creates breadcrumb navigation bar.

    Args:
        client: str - Client/organization name
        category: str - Category level
        report: str - Current report name

    Returns:
        html.Div - Breadcrumb navigation
    """
    return html.Div([
        dcc.Link(client, href='/clients', style={
            'color': '#7f8c8d',
            'textDecoration': 'none',
            'fontSize': '14px',
            ':hover': {'color': '#667eea'}
        }),
        html.Span(' / ', style={'color': '#bdc3c7', 'margin': '0 8px', 'fontSize': '14px'}),

        dcc.Link(category, href='/analytics', style={
            'color': '#7f8c8d',
            'textDecoration': 'none',
            'fontSize': '14px',
            ':hover': {'color': '#667eea'}
        }),
        html.Span(' / ', style={'color': '#bdc3c7', 'margin': '0 8px', 'fontSize': '14px'}),

        html.Span(report, style={
            'color': '#2c3e50',
            'fontSize': '14px',
            'fontWeight': '500'
        })
    ], style={
        'position': 'fixed',
        'top': '60px',
        'left': '220px',
        'right': '0',
        'padding': '15px 30px',
        'background': '#ffffff',
        'borderBottom': '1px solid #e0e0e0',
        'zIndex': '998',
        'display': 'flex',
        'alignItems': 'center'
    })


def create_competitor_pills(competitors, current_filter='All'):
    """
    Creates competitor filter pills matching VortexMini style.

    Args:
        competitors: list - List of competitor names
        current_filter: str - Currently selected filter

    Returns:
        html.Div - Competitor filter pills
    """
    # Color palette for competitors
    colors = [
        '#e0e0e0',  # Gray for All/TARGET
        '#ffcccc',  # Light red
        '#ffe0b2',  # Light orange
        '#fff9c4',  # Light yellow
        '#c8e6c9',  # Light green
        '#b3e5fc',  # Light blue
        '#e1bee7'   # Light purple
    ]

    all_filters = ['All'] + list(competitors)

    return html.Div([
        html.Button([
            html.I(className='fas fa-user', style={'marginRight': '6px', 'fontSize': '12px'}),
            filter_name
        ], style={
            'background': colors[i % len(colors)],
            'border': '2px solid #bdbdbd' if filter_name == current_filter else '1px solid #e0e0e0',
            'borderRadius': '20px',
            'padding': '8px 16px',
            'marginRight': '10px',
            'fontSize': '13px',
            'fontWeight': '600' if filter_name == current_filter else '500',
            'color': '#2c3e50',
            'cursor': 'pointer',
            'transition': 'all 0.2s ease',
            ':hover': {
                'transform': 'translateY(-2px)',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.15)'
            }
        })
        for i, filter_name in enumerate(all_filters)
    ], style={
        'position': 'fixed',
        'top': '110px',
        'left': '220px',
        'right': '0',
        'padding': '15px 30px',
        'background': '#ffffff',
        'borderBottom': '1px solid #e0e0e0',
        'zIndex': '997',
        'display': 'flex',
        'alignItems': 'center',
        'overflowX': 'auto',
        'whiteSpace': 'nowrap'
    })
