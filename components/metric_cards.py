"""
Metric cards for executive summary and KPI displays.
Reusable card components with customizable colors and values.
"""

from dash import html
import dash_bootstrap_components as dbc


def create_metric_card(title, value, subtitle=None, icon=None, color='#667eea', change=None):
    """
    Creates a single metric card.

    Args:
        title: str - Card title
        value: str or number - Main metric value
        subtitle: str - Optional subtitle text
        icon: str - Optional emoji or icon
        color: str - Primary color for the card
        change: str - Optional change indicator (e.g., "+18% YoY")

    Returns:
        html.Div - Metric card component
    """
    return html.Div([
        # Icon section
        html.Div([
            html.Span(icon if icon else '📊', style={
                'fontSize': '48px',
                'display': 'block',
                'marginBottom': '15px'
            })
        ]) if icon else None,

        # Title
        html.H3(title, style={
            'color': '#2c3e50',
            'fontSize': '18px',
            'fontWeight': '600',
            'marginBottom': '15px',
            'marginTop': '10px'
        }),

        # Main value
        html.Div([
            html.Span(value, style={
                'fontSize': '42px',
                'fontWeight': '700',
                'color': color,
                'lineHeight': 1
            }),
            html.Span(subtitle if subtitle else '', style={
                'fontSize': '14px',
                'color': '#7f8c8d',
                'marginLeft': '10px',
                'fontWeight': '400'
            }) if subtitle else None
        ], style={'marginBottom': '15px'}),

        # Change indicator
        html.Div(change, style={
            'fontSize': '16px',
            'color': color,
            'fontWeight': '600',
            'marginTop': '10px'
        }) if change else None

    ], style={
        'background': '#ffffff',
        'padding': '30px',
        'borderRadius': '15px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.08)',
        'borderTop': f'5px solid {color}',
        'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
        'cursor': 'pointer',
        'height': '100%',
        'minHeight': '250px'
    }, className='metric-card-hover')


def create_channel_card(channel_name, data, colors):
    """
    Creates executive summary channel card (matches PDF page 9).

    Args:
        channel_name: str - Channel name ('DTC Ecomm', 'Wholesale Retail', etc.)
        data: dict - Channel data with share, growth, description, bullets
        colors: dict - Color scheme with bg, accent, light

    Returns:
        html.Div - Channel card component
    """
    return html.Div([
        # Icon
        html.Div(data['icon'], style={
            'fontSize': '56px',
            'marginBottom': '20px',
            'textAlign': 'center'
        }),

        # Channel name
        html.H2(channel_name, style={
            'color': '#2c3e50',
            'fontSize': '22px',
            'fontWeight': '700',
            'marginBottom': '10px',
            'textAlign': 'center'
        }),

        # Share of revenue
        html.Div([
            html.Div([
                html.Span(f"{int(data['share']*100)}", style={
                    'fontSize': '64px',
                    'fontWeight': '800',
                    'color': colors['bg'],
                    'lineHeight': 1
                }),
                html.Span('%', style={
                    'fontSize': '32px',
                    'fontWeight': '700',
                    'color': colors['bg'],
                    'marginLeft': '5px'
                })
            ], style={'display': 'flex', 'alignItems': 'baseline', 'justifyContent': 'center'}),
            html.Div('of 2025 Revenue', style={
                'fontSize': '14px',
                'color': '#7f8c8d',
                'textAlign': 'center',
                'marginTop': '8px'
            })
        ], style={'marginBottom': '20px'}),

        # Growth metric
        html.Div(data['growth'], style={
            'padding': '10px 20px',
            'background': colors['light'],
            'borderRadius': '8px',
            'color': colors['accent'],
            'fontWeight': '700',
            'fontSize': '18px',
            'textAlign': 'center',
            'marginBottom': '20px'
        }),

        # Description
        html.Div(data['description'], style={
            'fontSize': '16px',
            'color': '#34495e',
            'fontWeight': '600',
            'marginBottom': '15px',
            'textAlign': 'center'
        }),

        # Bullet points
        html.Ul([
            html.Li(bullet, style={
                'marginBottom': '10px',
                'fontSize': '13px',
                'lineHeight': 1.5
            }) for bullet in data.get('bullets', [])
        ], style={
            'textAlign': 'left',
            'color': '#34495e',
            'paddingLeft': '20px'
        })

    ], style={
        'background': '#ffffff',
        'padding': '35px 30px',
        'borderRadius': '15px',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.08)',
        'borderTop': f'6px solid {colors["bg"]}',
        'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
        'height': '100%',
        'minHeight': '500px'
    }, className='channel-card-hover')


def create_insight_card(title, finding, recommendation):
    """
    Creates insight/recommendation card.

    Args:
        title: str - Insight title (with emoji)
        finding: str - Key finding
        recommendation: str - Recommended action

    Returns:
        html.Div - Insight card component
    """
    return html.Div([
        html.H4(title, style={
            'color': '#2c3e50',
            'fontSize': '18px',
            'fontWeight': '700',
            'marginBottom': '15px'
        }),
        html.Div([
            html.Strong('Finding: ', style={'color': '#34495e'}),
            html.Span(finding, style={'color': '#7f8c8d'})
        ], style={'marginBottom': '12px', 'fontSize': '14px'}),
        html.Div([
            html.Strong('Action: ', style={'color': '#667eea'}),
            html.Span(recommendation, style={'color': '#34495e', 'fontWeight': '500'})
        ], style={'fontSize': '14px'})
    ], style={
        'background': '#f8f9fa',
        'padding': '20px',
        'borderRadius': '10px',
        'borderLeft': '4px solid #667eea',
        'marginBottom': '15px'
    })


def create_stat_row(stats):
    """
    Creates a row of small stat cards.

    Args:
        stats: list - List of dicts with label, value, change

    Returns:
        html.Div - Row of stat cards
    """
    stat_cards = []

    for stat in stats:
        card = html.Div([
            html.Div(stat['label'], style={
                'fontSize': '12px',
                'color': '#7f8c8d',
                'fontWeight': '500',
                'marginBottom': '8px',
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px'
            }),
            html.Div(stat['value'], style={
                'fontSize': '28px',
                'fontWeight': '700',
                'color': '#2c3e50',
                'marginBottom': '5px'
            }),
            html.Div(stat.get('change', ''), style={
                'fontSize': '13px',
                'color': '#2ecc71' if '+' in str(stat.get('change', '')) else '#e74c3c',
                'fontWeight': '600'
            }) if stat.get('change') else None
        ], style={
            'background': '#ffffff',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
            'flex': '1',
            'margin': '0 10px',
            'minWidth': '200px'
        })

        stat_cards.append(card)

    return html.Div(stat_cards, style={
        'display': 'flex',
        'gap': '20px',
        'marginBottom': '30px',
        'flexWrap': 'wrap'
    })


def create_kpi_card(label, current, target, unit='%'):
    """
    Creates KPI card with current vs target.

    Args:
        label: str - KPI label
        current: number - Current value
        target: number - Target value
        unit: str - Unit symbol

    Returns:
        html.Div - KPI card with progress indicator
    """
    progress = (current / target * 100) if target > 0 else 0
    progress_color = '#2ecc71' if progress >= 100 else '#f39c12' if progress >= 75 else '#e74c3c'

    return html.Div([
        html.Div(label, style={
            'fontSize': '14px',
            'color': '#7f8c8d',
            'fontWeight': '600',
            'marginBottom': '10px'
        }),
        html.Div([
            html.Span(f"{current}{unit}", style={
                'fontSize': '32px',
                'fontWeight': '700',
                'color': '#2c3e50'
            }),
            html.Span(f" / {target}{unit}", style={
                'fontSize': '18px',
                'color': '#95a5a6',
                'marginLeft': '8px'
            })
        ], style={'marginBottom': '15px'}),
        html.Div([
            html.Div(style={
                'width': f'{min(progress, 100)}%',
                'height': '100%',
                'background': progress_color,
                'borderRadius': '6px',
                'transition': 'width 0.5s ease'
            })
        ], style={
            'width': '100%',
            'height': '10px',
            'background': '#ecf0f1',
            'borderRadius': '6px',
            'overflow': 'hidden'
        })
    ], style={
        'background': '#ffffff',
        'padding': '25px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'
    })
