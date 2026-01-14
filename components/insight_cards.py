"""
Insight cards component for displaying key findings and recommendations.
"""

from dash import html


def create_insight_card(title, insights, icon='fa-lightbulb', color='#667eea'):
    """
    Creates an insight card with title and bullet points.

    Args:
        title: str - Card title
        insights: list - List of insight strings
        icon: str - FontAwesome icon class
        color: str - Accent color

    Returns:
        html.Div - Insight card
    """
    return html.Div([
        # Header
        html.Div([
            html.I(className=f'fas {icon}', style={
                'marginRight': '12px',
                'fontSize': '20px',
                'color': color
            }),
            html.Span(title, style={
                'fontSize': '18px',
                'fontWeight': '700',
                'color': '#2c3e50'
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '16px',
            'paddingBottom': '12px',
            'borderBottom': f'2px solid {color}'
        }),

        # Insights list
        html.Div([
            html.Div([
                html.I(className='fas fa-check-circle', style={
                    'color': color,
                    'marginRight': '10px',
                    'fontSize': '14px',
                    'marginTop': '2px'
                }),
                html.Span(insight, style={
                    'color': '#34495e',
                    'fontSize': '14px',
                    'lineHeight': '1.6',
                    'flex': '1'
                })
            ], style={
                'display': 'flex',
                'marginBottom': '12px',
                'alignItems': 'flex-start'
            })
            for insight in insights
        ])
    ], style={
        'background': '#ffffff',
        'padding': '24px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
        'border': f'1px solid {color}20',
        'height': '100%'
    })


def create_metric_card(label, value, change=None, icon='fa-chart-line', good_direction='up'):
    """
    Creates a metric card with value and optional change indicator.

    Args:
        label: str - Metric label
        value: str - Metric value
        change: str - Change value (e.g., "+15%")
        icon: str - FontAwesome icon class
        good_direction: str - 'up' or 'down' for what direction is good

    Returns:
        html.Div - Metric card
    """
    # Determine if change is positive or negative
    is_positive = None
    if change:
        is_positive = '+' in change
        if good_direction == 'down':
            is_positive = not is_positive

    change_color = '#27ae60' if is_positive else '#e74c3c' if is_positive is False else '#95a5a6'
    change_icon = 'fa-arrow-up' if is_positive else 'fa-arrow-down' if is_positive is False else 'fa-minus'

    return html.Div([
        # Icon
        html.Div([
            html.I(className=f'fas {icon}', style={
                'fontSize': '24px',
                'color': '#667eea'
            })
        ], style={
            'marginBottom': '12px'
        }),

        # Value
        html.Div(value, style={
            'fontSize': '32px',
            'fontWeight': '700',
            'color': '#2c3e50',
            'marginBottom': '8px',
            'lineHeight': '1'
        }),

        # Label
        html.Div(label, style={
            'fontSize': '14px',
            'color': '#7f8c8d',
            'marginBottom': '8px'
        }),

        # Change indicator
        html.Div([
            html.I(className=f'fas {change_icon}', style={
                'marginRight': '6px',
                'fontSize': '12px'
            }),
            html.Span(change, style={
                'fontSize': '14px',
                'fontWeight': '600'
            })
        ], style={
            'color': change_color,
            'display': 'flex',
            'alignItems': 'center'
        }) if change else None
    ], style={
        'background': '#ffffff',
        'padding': '24px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
        'border': '1px solid #e0e0e0',
        'textAlign': 'center',
        'height': '100%'
    })


def create_keyword_insight_card(keywords_df):
    """
    Creates keyword insights card with top keywords and trends.

    Args:
        keywords_df: DataFrame - Keywords data

    Returns:
        html.Div - Keyword insights card
    """
    if keywords_df is None or keywords_df.empty:
        return html.Div("No keyword data available")

    # Get top keywords
    top_keywords = []
    if 'Keyword' in keywords_df.columns:
        top_5 = keywords_df.head(5)
        for idx, row in top_5.iterrows():
            keyword = row.get('Keyword', 'Unknown')
            clicks = row.get('Clicks', 0)
            top_keywords.append({
                'keyword': keyword,
                'clicks': f"{clicks:,.0f}" if clicks else "N/A"
            })

    # Calculate insights
    total_keywords = len(keywords_df)
    avg_position = keywords_df['Position'].mean() if 'Position' in keywords_df.columns else None

    return html.Div([
        # Header
        html.Div([
            html.I(className='fas fa-key', style={
                'marginRight': '12px',
                'fontSize': '20px',
                'color': '#f39c12'
            }),
            html.Span('Keyword Insights', style={
                'fontSize': '18px',
                'fontWeight': '700',
                'color': '#2c3e50'
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '16px',
            'paddingBottom': '12px',
            'borderBottom': '2px solid #f39c12'
        }),

        # Stats row
        html.Div([
            html.Div([
                html.Div(str(total_keywords), style={
                    'fontSize': '24px',
                    'fontWeight': '700',
                    'color': '#2c3e50'
                }),
                html.Div('Total Keywords', style={
                    'fontSize': '12px',
                    'color': '#7f8c8d',
                    'marginTop': '4px'
                })
            ], style={'flex': '1', 'textAlign': 'center'}),

            html.Div([
                html.Div(f"{avg_position:.1f}" if avg_position else "N/A", style={
                    'fontSize': '24px',
                    'fontWeight': '700',
                    'color': '#2c3e50'
                }),
                html.Div('Avg Position', style={
                    'fontSize': '12px',
                    'color': '#7f8c8d',
                    'marginTop': '4px'
                })
            ], style={'flex': '1', 'textAlign': 'center', 'borderLeft': '1px solid #e0e0e0'})
        ], style={
            'display': 'flex',
            'marginBottom': '20px',
            'padding': '16px',
            'background': '#f8f9fa',
            'borderRadius': '8px'
        }),

        # Top keywords
        html.Div('Top Performing Keywords:', style={
            'fontSize': '14px',
            'fontWeight': '600',
            'color': '#2c3e50',
            'marginBottom': '12px'
        }),

        html.Div([
            html.Div([
                html.Div([
                    html.Span(f"{idx+1}.", style={
                        'fontWeight': '700',
                        'color': '#667eea',
                        'marginRight': '8px',
                        'fontSize': '14px'
                    }),
                    html.Span(kw['keyword'], style={
                        'flex': '1',
                        'fontSize': '13px',
                        'color': '#34495e'
                    }),
                    html.Span(kw['clicks'], style={
                        'fontSize': '13px',
                        'fontWeight': '600',
                        'color': '#667eea'
                    })
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'padding': '8px 0',
                    'borderBottom': '1px solid #ecf0f1' if idx < len(top_keywords)-1 else 'none'
                })
            ])
            for idx, kw in enumerate(top_keywords)
        ])
    ], style={
        'background': '#ffffff',
        'padding': '24px',
        'borderRadius': '12px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
        'border': '1px solid #f39c1220',
        'height': '100%'
    })
