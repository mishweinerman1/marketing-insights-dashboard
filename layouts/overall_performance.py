"""
Overall Performance layout with traffic and engagement analysis.
Matches PDF pages 10-13.
"""

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from components.charts import (
    create_traffic_scale_scatter,
    create_traffic_sources_chart,
    create_engagement_scatter,
    create_web_vitals_chart
)


def create_layout(data=None):
    """
    Creates overall performance analysis page.

    Args:
        data: dict - Processed data with traffic, engagement, web vitals

    Returns:
        html.Div - Overall performance layout
    """
    return html.Div([
        # Page title
        html.Div([
            html.H1("Overall Performance Analysis", style={
                'color': '#2c3e50',
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px'
            }),
            html.P(
                "Digital footprint analysis and competitive positioning",
                style={
                    'color': '#7f8c8d',
                    'fontSize': '16px',
                    'marginBottom': '30px'
                }
            )
        ], style={'padding': '0 40px'}),

        # Traffic scale scatter plot
        html.Div([
            html.H2("Traffic Scale Analysis", style={
                'color': '#2c3e50',
                'fontSize': '24px',
                'fontWeight': '700',
                'marginBottom': '15px'
            }),
            html.Div([
                create_traffic_scale_scatter(data.get('traffic_data') if data else None)
            ], style={
                'background': '#ffffff',
                'borderRadius': '15px',
                'padding': '20px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                'marginBottom': '30px'
            }),
            html.Div([
                html.H4("📊 Key Takeaway", style={'color': '#2c3e50', 'marginBottom': '10px'}),
                html.P(
                    "Dossier sits in the 'large, shrinking' quadrant with strong monthly traffic (~780K visits) "
                    "and negative year-over-year growth (-45%). This signals a clear opportunity to scale reach "
                    "through paid acquisition, SEO expansion, and partnership-driven traffic growth.",
                    style={'color': '#7f8c8d', 'lineHeight': 1.6}
                )
            ], style={
                'background': '#f8f9fa',
                'padding': '20px',
                'borderRadius': '10px',
                'borderLeft': '4px solid #667eea'
            })
        ], style={'padding': '0 40px', 'marginBottom': '40px'}),

        # Traffic sources breakdown
        html.Div([
            html.H2("Traffic Sources Breakdown", style={
                'color': '#2c3e50',
                'fontSize': '24px',
                'fontWeight': '700',
                'marginBottom': '15px'
            }),
            html.Div([
                create_traffic_sources_chart(data.get('traffic_data') if data else None)
            ], style={
                'background': '#ffffff',
                'borderRadius': '15px',
                'padding': '20px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                'marginBottom': '30px'
            }),
            html.Div([
                html.H4("📊 Key Takeaway", style={'color': '#2c3e50', 'marginBottom': '10px'}),
                html.P(
                    "Dossier drives 42% of traffic from direct sources and 38% from organic search—totaling 79% "
                    "from direct and organic sources (well above category average of 67%). This indicates strong "
                    "brand awareness and SEO equity. However, paid search accounts for just 7% of traffic, "
                    "trailing competitors like Le Labo (22%) and Sol de Janeiro (21%), suggesting missed "
                    "opportunity in scalable, intent-driven acquisition.",
                    style={'color': '#7f8c8d', 'lineHeight': 1.6}
                )
            ], style={
                'background': '#f8f9fa',
                'padding': '20px',
                'borderRadius': '10px',
                'borderLeft': '4px solid #2ecc71'
            })
        ], style={'padding': '0 40px', 'marginBottom': '40px'}),

        # Site engagement analysis
        html.Div([
            html.H2("Site Engagement Analysis", style={
                'color': '#2c3e50',
                'fontSize': '24px',
                'fontWeight': '700',
                'marginBottom': '15px'
            }),
            html.Div([
                create_engagement_scatter(data.get('traffic_data') if data else None)
            ], style={
                'background': '#ffffff',
                'borderRadius': '15px',
                'padding': '20px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                'marginBottom': '30px'
            }),
            html.Div([
                html.H4("📊 Key Takeaway", style={'color': '#2c3e50', 'marginBottom': '10px'}),
                html.P(
                    "Dossier sits in the 'enticing, not engaging' quadrant with a low bounce rate (43%) and "
                    "above-average visit duration (3.0 minutes) compared to peers. This signals strong site "
                    "content and user interest. However, Core Web Vitals analysis indicates room for technical "
                    "improvements that could drive even higher conversion rates.",
                    style={'color': '#7f8c8d', 'lineHeight': 1.6}
                )
            ], style={
                'background': '#f8f9fa',
                'padding': '20px',
                'borderRadius': '10px',
                'borderLeft': '4px solid #f39c12'
            })
        ], style={'padding': '0 40px', 'marginBottom': '40px'}),

        # Core Web Vitals
        html.Div([
            html.H2("Core Web Vitals", style={
                'color': '#2c3e50',
                'fontSize': '24px',
                'fontWeight': '700',
                'marginBottom': '15px'
            }),
            html.Div([
                create_web_vitals_chart(data.get('web_vitals') if data else None)
            ], style={
                'background': '#ffffff',
                'borderRadius': '15px',
                'padding': '20px',
                'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                'marginBottom': '30px'
            }),
            html.Div([
                html.H4("⚠️ Conversion Impact", style={'color': '#2c3e50', 'marginBottom': '10px'}),
                html.P(
                    "Dossier's Core Web Vitals score of 61/100 (mobile) indicates technical performance issues "
                    "that may be costing conversions. Low scores correlate with higher bounce rates and lower "
                    "conversion rates. Improvements to page speed, largest contentful paint (LCP), and "
                    "first contentful paint (FCP) could unlock 5-10% conversion rate lift.",
                    style={'color': '#7f8c8d', 'lineHeight': 1.6}
                )
            ], style={
                'background': '#f8f9fa',
                'padding': '20px',
                'borderRadius': '10px',
                'borderLeft': '4px solid #e74c3c'
            })
        ], style={'padding': '0 40px', 'marginBottom': '40px'})

    ], style={'padding': '30px 0'})
