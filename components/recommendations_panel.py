"""
Recommendations panel component for displaying AI-generated marketing tactics recommendations.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_recommendations_panel(recommendations, roadmap=None):
    """
    Creates recommendations panel with cards and roadmap.

    Args:
        recommendations: list - Generated recommendations
        roadmap: dict - Optional phased implementation plan

    Returns:
        html.Div - Recommendations panel
    """
    if not recommendations:
        return html.Div("No recommendations available", style={
            'textAlign': 'center',
            'padding': '40px',
            'color': '#95a5a6',
            'fontSize': '16px'
        })

    return html.Div([
        # Header
        html.Div([
            html.H3([
                html.I(className='fas fa-lightbulb', style={'marginRight': '10px', 'color': '#f39c12'}),
                'AI-Powered Recommendations'
            ], style={'color': '#2c3e50', 'marginBottom': '10px'}),
            html.P(
                'Prioritized tactics based on your data, industry trends, and business goals.',
                style={'color': '#7f8c8d', 'fontSize': '14px'}
            )
        ], style={'marginBottom': '20px'}),

        # Top 5 Recommendations as cards
        html.Div([
            create_recommendation_card(rec, rank=i+1)
            for i, rec in enumerate(recommendations[:5])
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr', 'gap': '15px', 'marginBottom': '30px'}),

        # Implementation Roadmap (if available)
        create_roadmap_section(roadmap) if roadmap else None

    ], style={
        'background': '#ffffff',
        'padding': '30px',
        'borderRadius': '15px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.08)',
        'marginTop': '40px'
    })


def create_recommendation_card(recommendation, rank):
    """
    Creates individual recommendation card.

    Args:
        recommendation: dict - Recommendation details
        rank: int - Ranking number

    Returns:
        html.Div - Recommendation card
    """
    # Priority badge color
    priority_colors = {
        'Critical': '#e74c3c',
        'High': '#f39c12',
        'Medium': '#3498db',
        'Low': '#95a5a6'
    }

    priority_color = priority_colors.get(recommendation.get('priority', 'Medium'), '#95a5a6')

    return html.Div([
        # Rank badge
        html.Div(f"#{rank}", style={
            'position': 'absolute',
            'top': '15px',
            'left': '15px',
            'background': '#667eea',
            'color': 'white',
            'borderRadius': '50%',
            'width': '32px',
            'height': '32px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'fontWeight': 'bold',
            'fontSize': '14px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'
        }),

        # Priority badge
        html.Div(recommendation.get('priority', 'Medium'), style={
            'position': 'absolute',
            'top': '15px',
            'right': '15px',
            'background': priority_color,
            'color': 'white',
            'padding': '5px 14px',
            'borderRadius': '12px',
            'fontSize': '12px',
            'fontWeight': '600',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'
        }),

        # Content
        html.Div([
            # Tactic name
            html.H5(
                recommendation.get('tactic', 'Unknown Tactic'),
                style={
                    'color': '#2c3e50',
                    'marginBottom': '8px',
                    'paddingTop': '10px',
                    'fontSize': '18px',
                    'fontWeight': '600'
                }
            ),

            # Funnel stage badge
            html.Div(
                recommendation.get('funnel_stage', 'General'),
                style={
                    'display': 'inline-block',
                    'background': '#ecf0f1',
                    'color': '#34495e',
                    'padding': '3px 10px',
                    'borderRadius': '8px',
                    'fontSize': '11px',
                    'fontWeight': '500',
                    'marginBottom': '12px'
                }
            ),

            # Rationale
            html.P(
                recommendation.get('rationale', 'Recommended based on data analysis'),
                style={
                    'color': '#7f8c8d',
                    'fontSize': '14px',
                    'lineHeight': '1.6',
                    'marginBottom': '15px'
                }
            ),

            # Metrics row
            html.Div([
                html.Div([
                    html.Span('Effort: ', style={'fontWeight': '600', 'color': '#34495e'}),
                    html.Span(f"{recommendation.get('effort', 0)}/20", style={'color': '#7f8c8d'})
                ], style={'marginRight': '20px'}),
                html.Div([
                    html.Span('Expected Lift: ', style={'fontWeight': '600', 'color': '#34495e'}),
                    html.Span(recommendation.get('lift', 'N/A'), style={'color': '#27ae60', 'fontWeight': '600'})
                ], style={'marginRight': '20px'}),
                html.Div([
                    html.Span('Timeline: ', style={'fontWeight': '600', 'color': '#34495e'}),
                    html.Span(recommendation.get('timeline', 'TBD'), style={'color': '#7f8c8d'})
                ])
            ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'fontSize': '13px',
                'marginTop': '12px',
                'paddingTop': '12px',
                'borderTop': '1px solid #ecf0f1'
            }),

            # KPIs and Industry Context
            html.Div([
                html.Div([
                    html.Strong('Key Metrics: ', style={'color': '#667eea', 'fontSize': '12px'}),
                    html.Span(
                        ', '.join(recommendation.get('kpis', [])),
                        style={'color': '#7f8c8d', 'fontSize': '12px'}
                    )
                ], style={'marginTop': '10px'}),
                html.Div([
                    html.I(className='fas fa-chart-line', style={'marginRight': '6px', 'color': '#f39c12', 'fontSize': '11px'}),
                    html.Span(
                        recommendation.get('industry_context', ''),
                        style={'color': '#7f8c8d', 'fontSize': '12px', 'fontStyle': 'italic'}
                    )
                ], style={'marginTop': '6px'})
            ])
        ], style={'paddingLeft': '50px', 'paddingRight': '15px', 'paddingBottom': '5px'})
    ], style={
        'position': 'relative',
        'background': '#f8f9fa',
        'padding': '20px',
        'borderRadius': '12px',
        'border': '1px solid #e0e0e0',
        'transition': 'all 0.3s ease',
        'cursor': 'default'
    })


def create_roadmap_section(roadmap):
    """
    Creates implementation roadmap section.

    Args:
        roadmap: dict - Phased implementation plan

    Returns:
        html.Div - Roadmap section
    """
    if not roadmap:
        return None

    return html.Div([
        html.H4('Implementation Roadmap', style={
            'color': '#2c3e50',
            'marginTop': '20px',
            'marginBottom': '20px',
            'fontSize': '20px',
            'fontWeight': '600'
        }),

        html.Div([
            create_roadmap_phase(phase_name, tactics, idx+1)
            for idx, (phase_name, tactics) in enumerate(roadmap.items())
        ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '15px'})
    ])


def create_roadmap_phase(phase_name, tactics, phase_number):
    """
    Creates individual roadmap phase card.

    Args:
        phase_name: str - Phase name
        tactics: list - Tactics in this phase
        phase_number: int - Phase number

    Returns:
        html.Div - Phase card
    """
    phase_colors = ['#667eea', '#f39c12', '#2ecc71']
    phase_color = phase_colors[(phase_number - 1) % len(phase_colors)]

    return html.Div([
        # Phase header
        html.Div([
            html.Div(f"Phase {phase_number}", style={
                'background': phase_color,
                'color': 'white',
                'padding': '6px 14px',
                'borderRadius': '8px',
                'fontSize': '13px',
                'fontWeight': '600',
                'display': 'inline-block',
                'marginBottom': '8px'
            }),
            html.H5(phase_name.split(': ')[1] if ': ' in phase_name else phase_name, style={
                'color': '#2c3e50',
                'fontSize': '16px',
                'fontWeight': '600',
                'marginTop': '5px',
                'marginBottom': '12px'
            }),
            html.P(phase_name.split(': ')[0] if ': ' in phase_name else '', style={
                'color': '#7f8c8d',
                'fontSize': '13px',
                'marginBottom': '15px'
            })
        ]),

        # Tactics list
        html.Div([
            html.Div([
                html.I(className='fas fa-check-circle', style={
                    'color': phase_color,
                    'marginRight': '10px',
                    'fontSize': '14px'
                }),
                html.Span(tactic.get('tactic', 'Unknown'), style={
                    'color': '#34495e',
                    'fontSize': '14px'
                }),
                html.Span(f" ({tactic.get('lift', 'N/A')} lift)", style={
                    'color': '#7f8c8d',
                    'fontSize': '12px',
                    'marginLeft': '8px'
                })
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'})
            for tactic in tactics
        ])
    ], style={
        'background': '#f8f9fa',
        'padding': '20px',
        'borderRadius': '10px',
        'border': f'2px solid {phase_color}',
        'borderLeft': f'6px solid {phase_color}'
    })


def create_loading_state():
    """
    Creates loading state for recommendations.

    Returns:
        html.Div - Loading component
    """
    return html.Div([
        html.Div([
            dcc.Loading(
                id="recommendations-loading",
                type="circle",
                children=html.Div([
                    html.H4("Generating AI Recommendations...", style={
                        'color': '#667eea',
                        'marginTop': '20px',
                        'textAlign': 'center'
                    }),
                    html.P("Analyzing your data, industry trends, and business goals", style={
                        'color': '#7f8c8d',
                        'textAlign': 'center',
                        'fontSize': '14px'
                    })
                ])
            )
        ], style={
            'textAlign': 'center',
            'padding': '60px 20px'
        })
    ], style={
        'background': '#ffffff',
        'padding': '30px',
        'borderRadius': '15px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.08)',
        'marginTop': '40px'
    })
