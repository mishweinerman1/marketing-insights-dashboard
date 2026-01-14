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
        # Header with gradient background
        html.Div([
            html.I(className=f'fas {icon}', style={
                'marginRight': '14px',
                'fontSize': '26px',
                'color': '#ffffff'
            }),
            html.Span(title, style={
                'fontSize': '22px',
                'fontWeight': '800',
                'color': '#ffffff',
                'letterSpacing': '0.5px'
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '0px',
            'padding': '20px 24px',
            'background': f'linear-gradient(135deg, {color} 0%, {color}dd 100%)',
            'borderRadius': '12px 12px 0 0',
            'marginTop': '-24px',
            'marginLeft': '-24px',
            'marginRight': '-24px'
        }),

        # Insights list with more prominence
        html.Div([
            html.Div([
                html.I(className='fas fa-arrow-right', style={
                    'color': color,
                    'marginRight': '14px',
                    'fontSize': '16px',
                    'marginTop': '4px',
                    'fontWeight': 'bold'
                }),
                html.Span(insight, style={
                    'color': '#2c3e50',
                    'fontSize': '15px',
                    'lineHeight': '1.7',
                    'flex': '1',
                    'fontWeight': '500'
                })
            ], style={
                'display': 'flex',
                'marginBottom': '16px',
                'alignItems': 'flex-start',
                'padding': '12px',
                'background': '#f8f9fa',
                'borderRadius': '8px',
                'borderLeft': f'4px solid {color}'
            })
            for insight in insights
        ], style={'marginTop': '24px'})
    ], style={
        'background': '#ffffff',
        'padding': '24px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 16px rgba(0,0,0,0.12)',
        'border': f'2px solid {color}',
        'height': '100%',
        'transition': 'transform 0.2s ease, box-shadow 0.2s ease'
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
        # Icon with gradient background
        html.Div([
            html.I(className=f'fas {icon}', style={
                'fontSize': '32px',
                'color': '#ffffff'
            })
        ], style={
            'marginBottom': '16px',
            'padding': '20px',
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'borderRadius': '50%',
            'width': '70px',
            'height': '70px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'margin': '0 auto',
            'boxShadow': '0 4px 12px rgba(102, 126, 234, 0.3)'
        }),

        # Value
        html.Div(value, style={
            'fontSize': '42px',
            'fontWeight': '800',
            'color': '#2c3e50',
            'marginBottom': '10px',
            'lineHeight': '1',
            'letterSpacing': '-1px'
        }),

        # Label
        html.Div(label, style={
            'fontSize': '15px',
            'color': '#7f8c8d',
            'marginBottom': '12px',
            'fontWeight': '600',
            'textTransform': 'uppercase',
            'letterSpacing': '1px'
        }),

        # Change indicator with background
        html.Div([
            html.I(className=f'fas {change_icon}', style={
                'marginRight': '8px',
                'fontSize': '14px'
            }),
            html.Span(change, style={
                'fontSize': '16px',
                'fontWeight': '700'
            })
        ], style={
            'color': change_color,
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'padding': '8px 16px',
            'background': f'{change_color}15',
            'borderRadius': '20px',
            'display': 'inline-flex',
            'margin': '0 auto'
        }) if change else None
    ], style={
        'background': '#ffffff',
        'padding': '30px 24px',
        'borderRadius': '16px',
        'boxShadow': '0 4px 16px rgba(0,0,0,0.1)',
        'border': '2px solid #e8e8e8',
        'textAlign': 'center',
        'height': '100%',
        'transition': 'transform 0.2s ease, box-shadow 0.2s ease',
        'cursor': 'pointer'
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
        # Header with gradient
        html.Div([
            html.I(className='fas fa-key', style={
                'marginRight': '14px',
                'fontSize': '26px',
                'color': '#ffffff'
            }),
            html.Span('Keyword Insights', style={
                'fontSize': '22px',
                'fontWeight': '800',
                'color': '#ffffff',
                'letterSpacing': '0.5px'
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '0px',
            'padding': '20px 24px',
            'background': 'linear-gradient(135deg, #f39c12 0%, #e67e22 100%)',
            'borderRadius': '12px 12px 0 0',
            'marginTop': '-24px',
            'marginLeft': '-24px',
            'marginRight': '-24px'
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
