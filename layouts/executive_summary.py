"""
Executive Summary layout with 4 channel cards.
Matches PDF page 9 - channel revenue breakdown.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from components.metric_cards import create_channel_card
from components.charts import create_donut_chart
from config.branding import ClientBranding
from typing import List, Dict


def create_layout(channel_data=None, theme=None):
    """
    Creates executive summary page layout.

    Args:
        channel_data: dict - Channel metrics and details
        theme: dict - Theme configuration

    Returns:
        html.Div - Executive summary layout
    """
    if theme is None:
        theme = ClientBranding.get_theme('dossier')

    if channel_data is None:
        # Default channel data matching PDF
        channel_data = {
            'DTC Ecomm': {
                'share': 0.43,
                'growth': '+18% YoY',
                'icon': '🛒',
                'description': 'Core performance engine',
                'bullets': [
                    'Core revenue engine, accounting for 43% of 2025 revenue',
                    '+18% YoY growth in H1 2025',
                    'Strong brand loyalty and repeat customer base'
                ]
            },
            'Wholesale Retail': {
                'share': 0.30,
                'growth': '+44% margin',
                'icon': '🏢',
                'description': 'Big-box retail outperforming',
                'bullets': [
                    'Target sales 90K units above forecast',
                    'Walmart = #1 POS fragrance brand',
                    'Retail driving 44% margin contribution in wholesale'
                ]
            },
            'Marketplace': {
                'share': 0.15,
                'growth': 'Solid economics',
                'icon': '📦',
                'description': 'Lean channel with strong unit economics',
                'bullets': [
                    'Strategic role in SEO, brand visibility, and non-DTC discovery',
                    'Helps offload long-tail SKUs with limited overhead',
                    'Supports pricing and review strategy without brand dilution'
                ]
            },
            'TikTok Shop': {
                'share': 0.11,
                'growth': '1% → 15%',
                'icon': '🎵',
                'description': 'High-velocity social commerce engine',
                'bullets': [
                    'Breakout DTC lever with Originals growing from 1% to 15%+ of units in under a year',
                    'Influencer collaborations driving outsized performance',
                    'Gen Z discovery and engagement platform'
                ]
            }
        }

    return html.Div([
        # Page title
        html.Div([
            html.H1("Executive Summary", style={
                'color': '#2c3e50',
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px'
            }),
            html.P(
                "Omni-channel business showing strong growth in retail and TikTok Shop channels",
                style={
                    'color': '#7f8c8d',
                    'fontSize': '16px',
                    'marginBottom': '30px'
                }
            )
        ], style={'padding': '0 40px'}),

        # 4 Channel cards
        html.Div([
            html.Div([
                create_channel_card(
                    channel_name,
                    data,
                    ClientBranding.get_channel_colors(channel_name)
                )
                for channel_name, data in channel_data.items()
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))',
                'gap': '25px',
                'marginBottom': '40px'
            })
        ], style={'padding': '0 40px'}),

        # Revenue mix donut chart
        html.Div([
            html.H2("Revenue Mix by Channel", style={
                'color': '#2c3e50',
                'fontSize': '24px',
                'fontWeight': '700',
                'marginBottom': '20px'
            }),
            html.Div([
                create_donut_chart(
                    {
                        'DTC Ecomm': 43,
                        'Wholesale Retail': 30,
                        'Marketplace': 15,
                        'TikTok Shop': 11,
                        'Other': 1
                    },
                    title=None
                )
            ], style={
                'background': '#ffffff',
                'borderRadius': '15px',
                'padding': '20px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'
            })
        ], style={'padding': '0 40px', 'marginBottom': '40px'}),

        # Key insights section - Dynamic content container
        html.Div(id='executive-insights', style={'padding': '0 40px', 'marginBottom': '40px'})

    ], style={'padding': '30px 0'})


def create_dynamic_insights(insights: List[Dict]) -> html.Div:
    """
    Create dynamic insights section from AI-generated insights.

    Args:
        insights: list of dicts with keys: icon, title, description, color

    Returns:
        html.Div - Insights section
    """
    if not insights:
        # Return default placeholder insights
        insights = [
            {
                'icon': '🎯',
                'title': 'Upload Data for Insights',
                'description': 'Upload your marketing data Excel file to see AI-powered insights based on your performance metrics.',
                'color': '#667eea'
            }
        ]

    return html.Div([
        html.H2("Key Insights", style={
            'color': '#2c3e50',
            'fontSize': '24px',
            'fontWeight': '700',
            'marginBottom': '20px'
        }),
        html.Div([
            html.Div([
                html.H4(f"{insight['icon']} {insight['title']}", style={
                    'color': '#2c3e50',
                    'marginBottom': '10px'
                }),
                html.P(
                    insight['description'],
                    style={'color': '#7f8c8d', 'lineHeight': 1.6}
                )
            ], style={
                'background': '#f8f9fa',
                'padding': '20px',
                'borderRadius': '10px',
                'borderLeft': f"4px solid {insight['color']}",
                'marginBottom': '15px'
            })
            for insight in insights
        ])
    ])
