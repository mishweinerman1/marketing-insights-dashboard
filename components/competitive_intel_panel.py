"""
Competitive Intelligence UI Panel
Displays competitor analysis, gap insights, and competitive tactics.
"""

from dash import html, dcc
import plotly.graph_objects as go
from typing import Dict, List


def create_competitive_intel_panel(competitive_summary: Dict, competitive_tactics: List[Dict]) -> html.Div:
    """
    Creates comprehensive competitive intelligence panel.

    Args:
        competitive_summary: dict - Summary of competitive analysis
        competitive_tactics: list - Generated competitive tactics

    Returns:
        html.Div - Competitive intelligence panel
    """
    if not competitive_summary or not competitive_summary.get('top_competitors'):
        return html.Div([
            html.I(className='fas fa-info-circle', style={
                'fontSize': '48px',
                'color': '#95a5a6',
                'marginBottom': '15px'
            }),
            html.H4("Upload Data for Competitive Analysis", style={
                'color': '#7f8c8d',
                'marginBottom': '10px'
            }),
            html.P(
                "Competitive intelligence will appear here after uploading your Excel file with keyword data",
                style={'color': '#95a5a6', 'fontSize': '14px'}
            )
        ], style={
            'textAlign': 'center',
            'padding': '60px 40px',
            'background': '#f8f9fa',
            'borderRadius': '15px',
            'marginTop': '40px'
        })

    return html.Div([
        # Header Section
        html.Div([
            html.Div([
                html.I(className='fas fa-chart-network', style={
                    'fontSize': '32px',
                    'color': '#ffffff',
                    'marginRight': '15px'
                }),
                html.H2("Competitive Intelligence", style={
                    'color': '#ffffff',
                    'margin': '0',
                    'fontSize': '28px',
                    'fontWeight': '700'
                })
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'marginBottom': '15px'
            }),
            html.P(
                f"Analyzed {competitive_summary.get('competitor_count', 0)} competitors using keyword overlap and traffic data",
                style={'color': '#ffffff', 'margin': '0', 'fontSize': '15px', 'opacity': '0.9'}
            )
        ], style={
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'padding': '30px 40px',
            'borderRadius': '15px 15px 0 0',
            'marginBottom': '0'
        }),

        # Key Metrics Row
        html.Div([
            create_metric_box(
                icon='fa-users',
                value=str(competitive_summary.get('competitor_count', 0)),
                label='Competitors Identified',
                color='#667eea'
            ),
            create_metric_box(
                icon='fa-search',
                value=f"{competitive_summary.get('total_keyword_gaps', 0):,}",
                label='Keyword Gaps Found',
                color='#f39c12'
            ),
            create_metric_box(
                icon='fa-chart-line',
                value=f"{competitive_summary.get('total_gap_potential_volume', 0):,}",
                label='Monthly Search Volume Gap',
                color='#e74c3c'
            ),
            create_metric_box(
                icon='fa-fire',
                value=f"{competitive_summary.get('avg_competitive_intensity', 0):.0f}",
                label='Competitive Intensity',
                color='#9b59b6'
            )
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(4, 1fr)',
            'gap': '20px',
            'padding': '30px 40px',
            'background': '#ffffff'
        }),

        # Top Competitors Section
        html.Div([
            html.H3([
                html.I(className='fas fa-trophy', style={'marginRight': '10px', 'color': '#f39c12'}),
                'Top Competitors'
            ], style={'color': '#2c3e50', 'marginBottom': '20px', 'fontSize': '22px'}),

            html.Div([
                create_competitor_card(comp, rank=i+1)
                for i, comp in enumerate(competitive_summary.get('top_competitors', [])[:5])
            ], style={'display': 'grid', 'gap': '15px'})
        ], style={'padding': '30px 40px', 'background': '#f8f9fa'}),

        # Competitive Tactics Section
        html.Div([
            html.H3([
                html.I(className='fas fa-bullseye', style={'marginRight': '10px', 'color': '#e74c3c'}),
                'Top 5 Competitive Gap Tactics'
            ], style={'color': '#2c3e50', 'marginBottom': '20px', 'fontSize': '22px'}),

            html.P(
                "AI-generated tactics based on competitive gap analysis and keyword overlap",
                style={'color': '#7f8c8d', 'marginBottom': '25px', 'fontSize': '14px'}
            ),

            html.Div([
                create_competitive_tactic_card(tactic, rank=i+1)
                for i, tactic in enumerate(competitive_tactics[:5])
            ], style={'display': 'grid', 'gap': '20px'})
        ], style={'padding': '30px 40px', 'background': '#ffffff'})

    ], style={
        'background': '#ffffff',
        'borderRadius': '15px',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.1)',
        'marginTop': '30px',
        'overflow': 'hidden'
    })


def create_metric_box(icon: str, value: str, label: str, color: str) -> html.Div:
    """Create a metric box for key competitive metrics."""
    return html.Div([
        html.Div([
            html.I(className=f'fas {icon}', style={
                'fontSize': '24px',
                'color': color
            })
        ], style={
            'marginBottom': '12px'
        }),
        html.Div(value, style={
            'fontSize': '32px',
            'fontWeight': '800',
            'color': '#2c3e50',
            'marginBottom': '5px',
            'lineHeight': '1'
        }),
        html.Div(label, style={
            'fontSize': '13px',
            'color': '#7f8c8d',
            'fontWeight': '600',
            'textTransform': 'uppercase',
            'letterSpacing': '0.5px'
        })
    ], style={
        'textAlign': 'center',
        'padding': '25px 20px',
        'background': '#f8f9fa',
        'borderRadius': '12px',
        'border': f'2px solid {color}20',
        'transition': 'transform 0.2s ease',
        ':hover': {'transform': 'translateY(-5px)'}
    })


def create_competitor_card(competitor: Dict, rank: int) -> html.Div:
    """Create a competitor analysis card."""
    intensity = competitor.get('competitive_intensity', 0)

    # Determine intensity level and color
    if intensity > 70:
        intensity_label = 'Very High'
        intensity_color = '#e74c3c'
    elif intensity > 50:
        intensity_label = 'High'
        intensity_color = '#f39c12'
    elif intensity > 30:
        intensity_label = 'Moderate'
        intensity_color = '#3498db'
    else:
        intensity_label = 'Low'
        intensity_color = '#2ecc71'

    return html.Div([
        # Rank Badge
        html.Div(f"#{rank}", style={
            'position': 'absolute',
            'top': '15px',
            'left': '15px',
            'background': intensity_color,
            'color': 'white',
            'borderRadius': '50%',
            'width': '35px',
            'height': '35px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'fontWeight': 'bold',
            'fontSize': '16px',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.2)'
        }),

        # Content
        html.Div([
            # Company Name
            html.H4(competitor.get('company_name', 'Unknown'), style={
                'color': '#2c3e50',
                'marginBottom': '15px',
                'paddingLeft': '50px',
                'fontSize': '20px',
                'fontWeight': '700'
            }),

            # Metrics Grid
            html.Div([
                html.Div([
                    html.Div([
                        html.Span('Keyword Overlap:', style={'fontWeight': '600', 'fontSize': '12px', 'color': '#7f8c8d'}),
                        html.Span(f" {competitor.get('keyword_overlap_pct', 0):.1f}%", style={'fontWeight': '700', 'fontSize': '14px', 'color': '#2c3e50'})
                    ], style={'marginBottom': '8px'}),
                    html.Div([
                        html.Span('Traffic Share:', style={'fontWeight': '600', 'fontSize': '12px', 'color': '#7f8c8d'}),
                        html.Span(f" {competitor.get('traffic_share_on_overlap', 0):.1f}%", style={'fontWeight': '700', 'fontSize': '14px', 'color': '#2c3e50'})
                    ])
                ], style={'flex': '1'}),

                html.Div([
                    html.Div([
                        html.Span('Gap Keywords:', style={'fontWeight': '600', 'fontSize': '12px', 'color': '#7f8c8d'}),
                        html.Span(f" {competitor.get('gap_keywords_count', 0)}", style={'fontWeight': '700', 'fontSize': '14px', 'color': '#e74c3c'})
                    ], style={'marginBottom': '8px'}),
                    html.Div([
                        html.Span('Gap Volume:', style={'fontWeight': '600', 'fontSize': '12px', 'color': '#7f8c8d'}),
                        html.Span(f" {competitor.get('gap_potential_volume', 0):,}", style={'fontWeight': '700', 'fontSize': '14px', 'color': '#e74c3c'})
                    ])
                ], style={'flex': '1'})
            ], style={'display': 'flex', 'gap': '30px', 'marginBottom': '15px'}),

            # Competitive Intensity Badge
            html.Div([
                html.Span('Competitive Intensity: ', style={'fontSize': '13px', 'color': '#7f8c8d', 'marginRight': '8px'}),
                html.Span(f"{intensity_label} ({intensity:.0f}/100)", style={
                    'background': f'{intensity_color}15',
                    'color': intensity_color,
                    'padding': '4px 12px',
                    'borderRadius': '12px',
                    'fontSize': '13px',
                    'fontWeight': '700'
                })
            ], style={'marginTop': '10px'})
        ])
    ], style={
        'position': 'relative',
        'background': '#ffffff',
        'padding': '20px 25px',
        'borderRadius': '12px',
        'border': f'2px solid {intensity_color}30',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
        'transition': 'all 0.3s ease',
        ':hover': {'boxShadow': '0 4px 16px rgba(0,0,0,0.12)', 'transform': 'translateY(-2px)'}
    })


def create_competitive_tactic_card(tactic: Dict, rank: int) -> html.Div:
    """Create a competitive tactic recommendation card."""
    priority = tactic.get('priority', 'Medium')

    # Priority colors
    priority_colors = {
        'Critical': '#e74c3c',
        'High': '#f39c12',
        'Medium': '#3498db',
        'Low': '#95a5a6'
    }

    priority_color = priority_colors.get(priority, '#95a5a6')

    return html.Div([
        # Header with rank and priority
        html.Div([
            html.Div(f"#{rank}", style={
                'background': '#667eea',
                'color': 'white',
                'borderRadius': '8px',
                'padding': '8px 15px',
                'fontWeight': 'bold',
                'fontSize': '18px',
                'marginRight': '15px'
            }),
            html.Div([
                html.H4(tactic.get('tactic', ''), style={
                    'color': '#2c3e50',
                    'margin': '0 0 5px 0',
                    'fontSize': '19px',
                    'fontWeight': '700'
                }),
                html.Div([
                    html.Span(priority, style={
                        'background': priority_color,
                        'color': 'white',
                        'padding': '3px 10px',
                        'borderRadius': '12px',
                        'fontSize': '12px',
                        'fontWeight': '600',
                        'marginRight': '10px'
                    }),
                    html.Span(tactic.get('category', ''), style={
                        'background': '#f8f9fa',
                        'color': '#7f8c8d',
                        'padding': '3px 10px',
                        'borderRadius': '12px',
                        'fontSize': '12px',
                        'fontWeight': '600'
                    })
                ])
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '20px'}),

        # Rationale
        html.Div([
            html.Div([
                html.I(className='fas fa-info-circle', style={'marginRight': '8px', 'color': '#667eea'}),
                html.Strong('Why This Matters:')
            ], style={'marginBottom': '8px', 'color': '#2c3e50', 'fontSize': '14px'}),
            html.P(tactic.get('rationale', ''), style={
                'color': '#34495e',
                'fontSize': '14px',
                'lineHeight': '1.6',
                'margin': '0 0 15px 0',
                'paddingLeft': '24px'
            })
        ]),

        # Competitive Context Highlight
        html.Div([
            html.I(className='fas fa-chart-line', style={'marginRight': '8px', 'color': '#f39c12'}),
            html.Strong('Competitive Context: ', style={'color': '#2c3e50'}),
            html.Span(tactic.get('competitive_context', ''), style={'color': '#7f8c8d'})
        ], style={
            'background': '#fff9e6',
            'padding': '12px 15px',
            'borderRadius': '8px',
            'borderLeft': '4px solid #f39c12',
            'fontSize': '13px',
            'marginBottom': '15px'
        }),

        # Metrics Row
        html.Div([
            html.Div([
                html.I(className='fas fa-dumbbell', style={'marginRight': '5px'}),
                html.Span(f"Effort: {tactic.get('effort', 'N/A')}/10")
            ], style={'fontSize': '13px', 'color': '#7f8c8d'}),
            html.Div([
                html.I(className='fas fa-clock', style={'marginRight': '5px'}),
                html.Span(f"Timeline: {tactic.get('timeline', 'N/A')}")
            ], style={'fontSize': '13px', 'color': '#7f8c8d'}),
            html.Div([
                html.I(className='fas fa-rocket', style={'marginRight': '5px'}),
                html.Span(f"Expected: {tactic.get('expected_lift', 'N/A')}")
            ], style={'fontSize': '13px', 'color': '#27ae60', 'fontWeight': '600'})
        ], style={
            'display': 'flex',
            'gap': '25px',
            'paddingTop': '15px',
            'borderTop': '1px solid #e0e0e0',
            'marginTop': '15px'
        }),

        # KPIs
        html.Div([
            html.Strong('Track: ', style={'fontSize': '12px', 'color': '#7f8c8d', 'marginRight': '8px'}),
            ', '.join(tactic.get('kpis', []))
        ], style={'fontSize': '12px', 'color': '#95a5a6', 'marginTop': '12px'})

    ], style={
        'background': '#ffffff',
        'padding': '25px',
        'borderRadius': '12px',
        'border': f'2px solid {priority_color}20',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.08)',
        'transition': 'all 0.3s ease',
        ':hover': {'boxShadow': '0 4px 16px rgba(0,0,0,0.12)'}
    })


def create_competitor_comparison_chart(competitors: List[Dict]) -> dcc.Graph:
    """Create a visual comparison chart of competitors."""
    if not competitors:
        return html.Div()

    # Prepare data
    names = [c.get('company_name', '') for c in competitors[:5]]
    overlaps = [c.get('keyword_overlap_pct', 0) for c in competitors[:5]]
    intensities = [c.get('competitive_intensity', 0) for c in competitors[:5]]
    gaps = [c.get('gap_keywords_count', 0) for c in competitors[:5]]

    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Bar(
        name='Keyword Overlap %',
        x=names,
        y=overlaps,
        marker_color='#667eea',
        text=[f"{v:.1f}%" for v in overlaps],
        textposition='auto'
    ))

    fig.add_trace(go.Bar(
        name='Competitive Intensity',
        x=names,
        y=intensities,
        marker_color='#f39c12',
        text=[f"{v:.0f}" for v in intensities],
        textposition='auto'
    ))

    fig.update_layout(
        title='Competitor Comparison',
        barmode='group',
        height=400,
        template='plotly_white',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})
