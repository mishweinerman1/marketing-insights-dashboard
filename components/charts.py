"""
Chart components for marketing insights dashboard.
Plotly-based interactive visualizations for all dashboard sections.
"""

import plotly.graph_objects as go
import plotly.express as px
from dash import dcc
import pandas as pd
import numpy as np


def create_traffic_scale_scatter(df, company_focus='dossier'):
    """
    Creates traffic scale scatter plot with quadrants (PDF page 10).
    X-axis: Monthly Visits
    Y-axis: YoY Growth %

    Args:
        df: pandas.DataFrame - Traffic data with Monthly Visits and YoY Growth %
        company_focus: str - Company to highlight

    Returns:
        dcc.Graph - Plotly scatter plot
    """
    if df is None or df.empty:
        return create_empty_chart("Traffic data not available")

    fig = go.Figure()

    # Add quadrant backgrounds
    max_visits = df.get('Monthly Visits', pd.Series([1400000])).max() if 'Monthly Visits' in df.columns else 1400000
    max_growth = df.get('YoY Growth %', pd.Series([60])).max() if 'YoY Growth %' in df.columns else 60

    # Large, Growing (top right) - green
    fig.add_shape(type="rect", x0=max_visits/2, x1=max_visits, y0=0, y1=max_growth,
                  fillcolor="rgba(46,204,113,0.1)", line_width=0, layer="below")

    # Large, Shrinking (bottom right) - red
    fig.add_shape(type="rect", x0=max_visits/2, x1=max_visits, y0=-60, y1=0,
                  fillcolor="rgba(231,76,60,0.1)", line_width=0, layer="below")

    # Add scatter points (mock data if needed)
    companies = ['Dossier', 'Phlur', 'Le Labo', 'ALT', 'Glossier', 'Sol de Janeiro']
    monthly_visits = [780000, 230000, 1050000, 530000, 1100000, 1300000]
    yoy_growth = [-45, 2, -8, -5, -55, 28]

    fig.add_trace(go.Scatter(
        x=monthly_visits,
        y=yoy_growth,
        mode='markers+text',
        marker=dict(
            size=15,
            color=['#667eea' if c.lower() == company_focus.lower() else '#95a5a6' for c in companies],
            line=dict(width=2, color='white')
        ),
        text=companies,
        textposition='top center',
        textfont=dict(size=12, color='#2c3e50', family='Arial, sans-serif'),
        hovertemplate='<b>%{text}</b><br>Monthly Visits: %{x:,.0f}<br>YoY Growth: %{y:.1f}%<extra></extra>'
    ))

    # Add quadrant labels
    fig.add_annotation(text="Large, Growing", x=max_visits*0.75, y=max_growth*0.5,
                      showarrow=False, font=dict(size=14, color='#27ae60'))
    fig.add_annotation(text="Large, Shrinking", x=max_visits*0.75, y=-30,
                      showarrow=False, font=dict(size=14, color='#c0392b'))
    fig.add_annotation(text="Small, Growing", x=max_visits*0.25, y=max_growth*0.5,
                      showarrow=False, font=dict(size=14, color='#16a085'))
    fig.add_annotation(text="Small, Shrinking", x=max_visits*0.25, y=-30,
                      showarrow=False, font=dict(size=14, color='#e67e22'))

    fig.update_layout(
        title="Traffic Scale Analysis",
        xaxis_title="Monthly Visits",
        yaxis_title="YoY Growth (%)",
        height=500,
        template='plotly_white',
        hovermode='closest',
        showlegend=False
    )

    fig.update_xaxis(tickformat=',')
    fig.update_yaxis(ticksuffix='%', zeroline=True, zerolinewidth=2, zerolinecolor='#34495e')

    return dcc.Graph(figure=fig)


def create_traffic_sources_chart(df):
    """
    Creates stacked bar chart showing traffic channel mix (PDF page 12).

    Args:
        df: pandas.DataFrame - Traffic sources data

    Returns:
        dcc.Graph - Stacked bar chart
    """
    if df is None or df.empty:
        # Create mock data
        companies = ['Dossier', 'Phlur', 'Le Labo', 'ALT', 'Glossier', 'Sol de Janeiro']
        data = {
            'Company': companies,
            'Direct': [42, 38, 48, 52, 42, 38],
            'Organic Search': [38, 42, 28, 22, 38, 35],
            'Paid Search': [7, 8, 22, 13, 8, 21],
            'Social': [12, 10, 0, 8, 10, 5],
            'Referrals': [2, 2, 2, 5, 2, 1]
        }
        df = pd.DataFrame(data)

    fig = go.Figure()

    colors = {
        'Direct': '#0040FF',
        'Organic Search': '#4080FF',
        'Paid Search': '#8080FF',
        'Social': '#00C853',
        'Referrals': '#00E676',
        'Email': '#FFB74D',
        'Display Ads': '#FF6B6B'
    }

    channels = [col for col in df.columns if col != 'Company']

    for channel in channels:
        if channel in df.columns:
            fig.add_trace(go.Bar(
                name=channel,
                x=df['Company'],
                y=df[channel],
                marker_color=colors.get(channel, '#95a5a6'),
                hovertemplate='<b>%{x}</b><br>' + channel + ': %{y}%<extra></extra>'
            ))

    fig.update_layout(
        title="Traffic Sources Breakdown",
        xaxis_title="Company",
        yaxis_title="Traffic Share (%)",
        barmode='stack',
        height=400,
        template='plotly_white',
        hovermode='x',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_yaxis(ticksuffix='%', range=[0, 100])

    return dcc.Graph(figure=fig)


def create_engagement_scatter(df):
    """
    Creates site engagement scatter plot (PDF page 13).
    X-axis: Bounce Rate %
    Y-axis: Dwell Time (minutes)

    Args:
        df: pandas.DataFrame - Engagement metrics

    Returns:
        dcc.Graph - Scatter plot with quadrants
    """
    # Mock data
    companies = ['Dossier', 'Phlur', 'Le Labo', 'ALT', 'Glossier', 'Sol de Janeiro']
    bounce_rate = [43, 47, 50, 49, 42, 49]
    dwell_time = [3.0, 2.1, 1.9, 1.85, 2.3, 2.1]

    fig = go.Figure()

    # Add quadrant backgrounds
    # Enticing, Engaging (low bounce, high dwell) - green
    fig.add_shape(type="rect", x0=0, x1=50, y0=2.0, y1=3.5,
                  fillcolor="rgba(46,204,113,0.1)", line_width=0, layer="below")

    fig.add_trace(go.Scatter(
        x=bounce_rate,
        y=dwell_time,
        mode='markers+text',
        marker=dict(size=12, color='#667eea', line=dict(width=2, color='white')),
        text=companies,
        textposition='top center',
        textfont=dict(size=11),
        hovertemplate='<b>%{text}</b><br>Bounce Rate: %{x}%<br>Dwell Time: %{y:.1f} min<extra></extra>'
    ))

    # Add quadrant labels
    fig.add_annotation(text="Enticing, Engaging", x=25, y=2.7,
                      showarrow=False, font=dict(size=12, color='#27ae60'))
    fig.add_annotation(text="Unenticing, Engaging", x=25, y=1.0,
                      showarrow=False, font=dict(size=12, color='#95a5a6'))

    fig.update_layout(
        title="Site Engagement Analysis",
        xaxis_title="Bounce Rate (%)",
        yaxis_title="Visit Duration (minutes)",
        height=500,
        template='plotly_white',
        hovermode='closest',
        showlegend=False
    )

    fig.update_xaxis(ticksuffix='%', range=[0, 100])
    fig.update_yaxis(range=[0, 3.5])

    return dcc.Graph(figure=fig)


def create_web_vitals_chart(df):
    """
    Creates Core Web Vitals grouped bar chart (PDF page 13).

    Args:
        df: pandas.DataFrame - Core Web Vitals data

    Returns:
        dcc.Graph - Grouped bar chart
    """
    if df is None or df.empty:
        # Mock data
        companies = ['Dossier', 'Phlur', 'Le Labo', 'ALT', 'Glossier', 'Sol de Janeiro']
        data = {
            'Company': companies,
            'Performance': [61, 75, 82, 68, 79, 85],
            'SEO': [88, 92, 95, 85, 90, 93],
            'Accessibility': [85, 88, 90, 83, 87, 91],
            'Best Practices': [78, 82, 85, 80, 83, 87]
        }
        df = pd.DataFrame(data)

    metrics = ['Performance', 'SEO', 'Accessibility', 'Best Practices']
    colors = ['#e74c3c', '#f39c12', '#2ecc71', '#667eea']

    fig = go.Figure()

    for i, metric in enumerate(metrics):
        if metric in df.columns:
            fig.add_trace(go.Bar(
                name=metric,
                x=df['Company'] if 'Company' in df.columns else df.index,
                y=df[metric],
                marker_color=colors[i],
                hovertemplate='<b>%{x}</b><br>' + metric + ': %{y}/100<extra></extra>'
            ))

    fig.update_layout(
        title="Core Web Vitals Scores",
        xaxis_title="Company",
        yaxis_title="Score",
        barmode='group',
        height=400,
        template='plotly_white',
        hovermode='x',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_yaxis(range=[0, 100])

    return dcc.Graph(figure=fig)


def create_ppc_spend_trend(df):
    """
    Creates PPC spend trend line chart.

    Args:
        df: pandas.DataFrame - PPC spend data with YearMonth, Mobile Spend, Desktop Spend

    Returns:
        dcc.Graph - Line chart
    """
    if df is None or df.empty:
        return create_empty_chart("PPC spend data not available")

    fig = go.Figure()

    if 'Mobile Spend' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['YearMonth'] if 'YearMonth' in df.columns else df.index,
            y=df['Mobile Spend'],
            name='Mobile',
            line=dict(color='#667eea', width=3),
            stackgroup='one',
            hovertemplate='Mobile: $%{y:,.0f}<extra></extra>'
        ))

    if 'Desktop Spend' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['YearMonth'] if 'YearMonth' in df.columns else df.index,
            y=df['Desktop Spend'],
            name='Desktop',
            line=dict(color='#f39c12', width=3),
            stackgroup='one',
            hovertemplate='Desktop: $%{y:,.0f}<extra></extra>'
        ))

    fig.update_layout(
        title="PPC Spend Trend",
        xaxis_title="Month",
        yaxis_title="Spend ($)",
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )

    fig.update_yaxis(tickprefix='$', tickformat=',')

    return dcc.Graph(figure=fig)


def create_tactics_matrix_scatter(df):
    """
    Creates IE Matrix scatter plot (bubble chart) for tactics prioritization.
    X-axis: Total Effort
    Y-axis: Expected Lift %
    Bubble size: Projected Cost

    Args:
        df: pandas.DataFrame - Tactics data

    Returns:
        dcc.Graph - Bubble scatter plot
    """
    if df is None or df.empty:
        return create_empty_chart("Tactics data not available")

    fig = go.Figure()

    # Color mapping by funnel stage
    color_map = {
        'Conversion': '#667eea',
        'Acquisition': '#2ecc71',
        'LTV': '#f39c12',
        'User Experience': '#e74c3c'
    }

    if 'Focus (Funnel Stage)' in df.columns:
        for stage in df['Focus (Funnel Stage)'].unique():
            subset = df[df['Focus (Funnel Stage)'] == stage]

            fig.add_trace(go.Scatter(
                x=subset['Total Effort'] if 'Total Effort' in subset.columns else [],
                y=subset['Expected Lift %'] * 100 if 'Expected Lift %' in subset.columns else [],
                mode='markers+text',
                name=stage,
                marker=dict(
                    size=subset['Projected Cost'] / 50 if 'Projected Cost' in subset.columns else 10,
                    color=color_map.get(stage, '#95a5a6'),
                    line=dict(width=2, color='white')
                ),
                text=subset['Marketing Tactic'] if 'Marketing Tactic' in subset.columns else subset.get('Tactics', ''),
                textposition='top center',
                textfont=dict(size=9),
                hovertemplate='<b>%{text}</b><br>Effort: %{x}<br>Lift: %{y:.1f}%<extra></extra>'
            ))

    # Add quadrant lines
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=10, line_dash="dash", line_color="gray", opacity=0.5)

    # Add quadrant labels
    fig.add_annotation(text="Quick Wins", x=5, y=0.6, showarrow=False,
                      font=dict(size=14, color='green'))
    fig.add_annotation(text="Major Projects", x=15, y=0.6, showarrow=False,
                      font=dict(size=14, color='orange'))

    fig.update_layout(
        title="Marketing Tactics: Effort vs. Impact",
        xaxis_title="Total Effort (People + Cost)",
        yaxis_title="Expected Lift (%)",
        height=600,
        template='plotly_white',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return dcc.Graph(figure=fig)


def create_keyword_share_chart(df, top_n=15):
    """
    Creates horizontal bar chart for keyword traffic share.

    Args:
        df: pandas.DataFrame - Keyword data
        top_n: int - Number of top keywords to show

    Returns:
        dcc.Graph - Horizontal bar chart
    """
    if df is None or df.empty:
        return create_empty_chart("Keyword data not available")

    # Take top N keywords by clicks
    if 'Clicks' in df.columns:
        df_top = df.nlargest(top_n, 'Clicks')
    else:
        df_top = df.head(top_n)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df_top['Keyword'] if 'Keyword' in df_top.columns else df_top.index,
        x=df_top['Clicks'] if 'Clicks' in df_top.columns else [],
        orientation='h',
        marker_color='#667eea',
        hovertemplate='<b>%{y}</b><br>Clicks: %{x:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=f"Top {top_n} Keywords by Traffic",
        xaxis_title="Clicks",
        yaxis_title="",
        height=500,
        template='plotly_white'
    )

    fig.update_xaxis(tickformat=',')

    return dcc.Graph(figure=fig)


def create_empty_chart(message="No data available"):
    """
    Creates empty chart placeholder.

    Args:
        message: str - Message to display

    Returns:
        dcc.Graph - Empty chart
    """
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color='#95a5a6')
    )

    fig.update_layout(
        template='plotly_white',
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    return dcc.Graph(figure=fig)


def create_donut_chart(data, title="Revenue by Channel"):
    """
    Creates donut chart for channel mix.

    Args:
        data: dict - Channel names and values
        title: str - Chart title

    Returns:
        dcc.Graph - Donut chart
    """
    labels = list(data.keys())
    values = list(data.values())
    colors = ['#667eea', '#f39c12', '#2ecc71', '#e74c3c']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.5,
        marker_colors=colors,
        hovertemplate='<b>%{label}</b><br>%{value}%<br>%{percent}<extra></extra>'
    )])

    fig.update_layout(
        title=title,
        height=400,
        template='plotly_white',
        showlegend=True
    )

    return dcc.Graph(figure=fig)
