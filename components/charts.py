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
    # Mock data (TODO: Parse actual traffic scale data from Excel)
    companies = ['Dossier', 'Phlur', 'Le Labo', 'ALT', 'Glossier', 'Sol de Janeiro']
    monthly_visits = [780000, 230000, 1050000, 530000, 1100000, 1300000]
    yoy_growth = [-45, 2, -8, -5, -55, 28]

    fig = go.Figure()

    # Set reasonable axis ranges based on data
    max_visits = max(monthly_visits) * 1.1
    min_growth = min(yoy_growth) - 10
    max_growth = max(yoy_growth) + 10
    mid_visits = max_visits / 2

    # Add quadrant backgrounds with better visibility
    # Small, Growing (top left) - light green
    fig.add_shape(type="rect", x0=0, x1=mid_visits, y0=0, y1=max_growth,
                  fillcolor="rgba(46,204,113,0.15)", line_width=0, layer="below")

    # Large, Growing (top right) - darker green
    fig.add_shape(type="rect", x0=mid_visits, x1=max_visits, y0=0, y1=max_growth,
                  fillcolor="rgba(39,174,96,0.2)", line_width=0, layer="below")

    # Small, Shrinking (bottom left) - light orange
    fig.add_shape(type="rect", x0=0, x1=mid_visits, y0=min_growth, y1=0,
                  fillcolor="rgba(230,126,34,0.15)", line_width=0, layer="below")

    # Large, Shrinking (bottom right) - red
    fig.add_shape(type="rect", x0=mid_visits, x1=max_visits, y0=min_growth, y1=0,
                  fillcolor="rgba(231,76,60,0.2)", line_width=0, layer="below")

    # Add divider lines
    fig.add_hline(y=0, line_dash="solid", line_color="rgba(44,62,80,0.4)", line_width=2)
    fig.add_vline(x=mid_visits, line_dash="solid", line_color="rgba(44,62,80,0.4)", line_width=2)

    # Add scatter points with better styling
    colors = ['#667eea' if c.lower() == company_focus.lower() else '#7f8c8d' for c in companies]
    sizes = [20 if c.lower() == company_focus.lower() else 14 for c in companies]

    fig.add_trace(go.Scatter(
        x=monthly_visits,
        y=yoy_growth,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2, color='white'),
            opacity=0.9
        ),
        text=companies,
        textposition='top center',
        textfont=dict(
            size=11,
            color='#2c3e50',
            family='Arial, sans-serif',
            weight='bold'
        ),
        hovertemplate='<b>%{text}</b><br>Monthly Visits: %{x:,.0f}<br>YoY Growth: %{y:.1f}%<extra></extra>'
    ))

    # Add quadrant labels in better positions
    fig.add_annotation(
        text="<b>Small,<br>Growing</b>",
        x=mid_visits*0.5,
        y=max_growth*0.7,
        showarrow=False,
        font=dict(size=13, color='#27ae60', family='Arial, sans-serif'),
        bgcolor='rgba(255,255,255,0.8)',
        borderpad=8
    )
    fig.add_annotation(
        text="<b>Large,<br>Growing</b>",
        x=mid_visits*1.5,
        y=max_growth*0.7,
        showarrow=False,
        font=dict(size=13, color='#27ae60', family='Arial, sans-serif'),
        bgcolor='rgba(255,255,255,0.8)',
        borderpad=8
    )
    fig.add_annotation(
        text="<b>Small,<br>Shrinking</b>",
        x=mid_visits*0.5,
        y=min_growth*0.7,
        showarrow=False,
        font=dict(size=13, color='#e67e22', family='Arial, sans-serif'),
        bgcolor='rgba(255,255,255,0.8)',
        borderpad=8
    )
    fig.add_annotation(
        text="<b>Large,<br>Shrinking</b>",
        x=mid_visits*1.5,
        y=min_growth*0.7,
        showarrow=False,
        font=dict(size=13, color='#c0392b', family='Arial, sans-serif'),
        bgcolor='rgba(255,255,255,0.8)',
        borderpad=8
    )

    fig.update_layout(
        title={
            'text': "Traffic Scale Analysis",
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'}
        },
        xaxis_title="Monthly Visits",
        yaxis_title="YoY Growth (%)",
        height=550,
        template='plotly_white',
        hovermode='closest',
        showlegend=False,
        plot_bgcolor='#f8f9fa',
        margin=dict(l=80, r=40, t=80, b=60)
    )

    fig.update_xaxes(
        tickformat=',',
        range=[0, max_visits],
        gridcolor='rgba(0,0,0,0.05)',
        showline=True,
        linewidth=1,
        linecolor='#ddd'
    )
    fig.update_yaxes(
        ticksuffix='%',
        range=[min_growth, max_growth],
        zeroline=False,
        gridcolor='rgba(0,0,0,0.05)',
        showline=True,
        linewidth=1,
        linecolor='#ddd'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_traffic_sources_chart(df):
    """
    Creates stacked bar chart showing traffic channel mix (PDF page 12).

    Args:
        df: pandas.DataFrame - Traffic sources data

    Returns:
        dcc.Graph - Stacked bar chart
    """
    # Mock data (TODO: Parse actual traffic sources from Excel data)
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

    # Better color scheme with distinct, professional colors
    colors = {
        'Direct': '#667eea',
        'Organic Search': '#2ecc71',
        'Paid Search': '#f39c12',
        'Social': '#e74c3c',
        'Referrals': '#9b59b6',
        'Email': '#3498db',
        'Display Ads': '#1abc9c'
    }

    channels = [col for col in df.columns if col != 'Company']

    for channel in channels:
        if channel in df.columns:
            fig.add_trace(go.Bar(
                name=channel,
                x=df['Company'],
                y=df[channel],
                marker_color=colors.get(channel, '#95a5a6'),
                marker_line_color='white',
                marker_line_width=0.5,
                hovertemplate='<b>%{x}</b><br>' + channel + ': %{y}%<extra></extra>',
                text=df[channel],
                textposition='inside',
                textfont=dict(size=10, color='white'),
                texttemplate='%{text}%'
            ))

    fig.update_layout(
        title={
            'text': "Traffic Sources Breakdown",
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'}
        },
        xaxis_title="Company",
        yaxis_title="Traffic Share (%)",
        barmode='stack',
        height=450,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#ddd',
            borderwidth=1
        ),
        plot_bgcolor='#f8f9fa',
        margin=dict(l=60, r=40, t=80, b=60)
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='#ddd',
        gridcolor='rgba(0,0,0,0.05)'
    )
    fig.update_yaxes(
        ticksuffix='%',
        range=[0, 100],
        showline=True,
        linewidth=1,
        linecolor='#ddd',
        gridcolor='rgba(0,0,0,0.05)'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


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
    # Mock data (TODO: Parse actual engagement metrics from Excel data)
    companies = ['Dossier', 'Phlur', 'Le Labo', 'ALT', 'Glossier', 'Sol de Janeiro']
    bounce_rate = [43, 47, 50, 49, 42, 49]
    dwell_time = [3.0, 2.1, 1.9, 1.85, 2.3, 2.1]

    fig = go.Figure()

    # Calculate median values for dividers
    median_bounce = 45
    median_dwell = 2.2

    # Add quadrant backgrounds with better visibility
    # Enticing, Engaging (low bounce, high dwell) - green
    fig.add_shape(type="rect", x0=0, x1=median_bounce, y0=median_dwell, y1=3.5,
                  fillcolor="rgba(39,174,96,0.15)", line_width=0, layer="below")

    # Enticing, Brief (low bounce, low dwell) - light blue
    fig.add_shape(type="rect", x0=0, x1=median_bounce, y0=0, y1=median_dwell,
                  fillcolor="rgba(52,152,219,0.15)", line_width=0, layer="below")

    # Unenticing, Engaging (high bounce, high dwell) - light orange
    fig.add_shape(type="rect", x0=median_bounce, x1=60, y0=median_dwell, y1=3.5,
                  fillcolor="rgba(230,126,34,0.15)", line_width=0, layer="below")

    # Unenticing, Brief (high bounce, low dwell) - light red
    fig.add_shape(type="rect", x0=median_bounce, x1=60, y0=0, y1=median_dwell,
                  fillcolor="rgba(231,76,60,0.15)", line_width=0, layer="below")

    # Add divider lines
    fig.add_hline(y=median_dwell, line_dash="solid", line_color="rgba(44,62,80,0.4)", line_width=2)
    fig.add_vline(x=median_bounce, line_dash="solid", line_color="rgba(44,62,80,0.4)", line_width=2)

    # Determine if each company is the focus (Dossier)
    colors = ['#667eea' if c == 'Dossier' else '#7f8c8d' for c in companies]
    sizes = [16 if c == 'Dossier' else 12 for c in companies]

    fig.add_trace(go.Scatter(
        x=bounce_rate,
        y=dwell_time,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(width=2, color='white'),
            opacity=0.9
        ),
        text=companies,
        textposition='top center',
        textfont=dict(size=10, color='#2c3e50', family='Arial, sans-serif', weight='bold'),
        hovertemplate='<b>%{text}</b><br>Bounce Rate: %{x}%<br>Visit Duration: %{y:.2f} min<extra></extra>'
    ))

    # Add quadrant labels with better positioning
    fig.add_annotation(
        text="<b>Enticing,<br>Engaging</b>",
        x=median_bounce*0.5,
        y=2.9,
        showarrow=False,
        font=dict(size=12, color='#27ae60', family='Arial, sans-serif'),
        bgcolor='rgba(255,255,255,0.8)',
        borderpad=6
    )
    fig.add_annotation(
        text="<b>Unenticing,<br>Engaging</b>",
        x=median_bounce*1.4,
        y=2.9,
        showarrow=False,
        font=dict(size=12, color='#e67e22', family='Arial, sans-serif'),
        bgcolor='rgba(255,255,255,0.8)',
        borderpad=6
    )
    fig.add_annotation(
        text="<b>Enticing,<br>Brief</b>",
        x=median_bounce*0.5,
        y=1.0,
        showarrow=False,
        font=dict(size=12, color='#3498db', family='Arial, sans-serif'),
        bgcolor='rgba(255,255,255,0.8)',
        borderpad=6
    )
    fig.add_annotation(
        text="<b>Unenticing,<br>Brief</b>",
        x=median_bounce*1.4,
        y=1.0,
        showarrow=False,
        font=dict(size=12, color='#c0392b', family='Arial, sans-serif'),
        bgcolor='rgba(255,255,255,0.8)',
        borderpad=6
    )

    fig.update_layout(
        title={
            'text': "Site Engagement Analysis",
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'}
        },
        xaxis_title="Bounce Rate (%)",
        yaxis_title="Visit Duration (minutes)",
        height=550,
        template='plotly_white',
        hovermode='closest',
        showlegend=False,
        plot_bgcolor='#f8f9fa',
        margin=dict(l=80, r=40, t=80, b=60)
    )

    fig.update_xaxes(
        ticksuffix='%',
        range=[35, 55],
        gridcolor='rgba(0,0,0,0.05)',
        showline=True,
        linewidth=1,
        linecolor='#ddd'
    )
    fig.update_yaxes(
        ticksuffix=' min',
        range=[1.5, 3.2],
        gridcolor='rgba(0,0,0,0.05)',
        showline=True,
        linewidth=1,
        linecolor='#ddd'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_web_vitals_chart(df):
    """
    Creates Core Web Vitals grouped bar chart (PDF page 13).

    Args:
        df: pandas.DataFrame - Core Web Vitals data

    Returns:
        dcc.Graph - Grouped bar chart
    """
    # Mock data (TODO: Parse actual Core Web Vitals from Excel data)
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
    colors = ['#667eea', '#2ecc71', '#f39c12', '#3498db']

    fig = go.Figure()

    for i, metric in enumerate(metrics):
        if metric in df.columns:
            fig.add_trace(go.Bar(
                name=metric,
                x=df['Company'] if 'Company' in df.columns else df.index,
                y=df[metric],
                marker_color=colors[i],
                marker_line_color='white',
                marker_line_width=0.5,
                text=df[metric],
                textposition='outside',
                textfont=dict(size=10),
                hovertemplate='<b>%{x}</b><br>' + metric + ': <b>%{y}/100</b><extra></extra>'
            ))

    # Add benchmark lines
    fig.add_hline(y=90, line_dash="dash", line_color="rgba(39,174,96,0.3)", line_width=2,
                  annotation_text="Excellent (90+)", annotation_position="right",
                  annotation_font_size=11, annotation_font_color="#27ae60")
    fig.add_hline(y=70, line_dash="dash", line_color="rgba(243,156,18,0.3)", line_width=2,
                  annotation_text="Good (70+)", annotation_position="right",
                  annotation_font_size=11, annotation_font_color="#f39c12")

    fig.update_layout(
        title={
            'text': "Core Web Vitals Scores",
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'}
        },
        xaxis_title="Company",
        yaxis_title="Score (out of 100)",
        barmode='group',
        height=450,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#ddd',
            borderwidth=1
        ),
        plot_bgcolor='#f8f9fa',
        margin=dict(l=60, r=40, t=80, b=60),
        bargap=0.15,
        bargroupgap=0.1
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='#ddd',
        gridcolor='rgba(0,0,0,0.05)'
    )
    fig.update_yaxes(
        range=[0, 105],
        showline=True,
        linewidth=1,
        linecolor='#ddd',
        gridcolor='rgba(0,0,0,0.05)'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_ppc_spend_trend(df):
    """
    Creates PPC spend trend line chart.

    Args:
        df: pandas.DataFrame - PPC spend data with YearMonth, Mobile Spend, Desktop Spend

    Returns:
        dcc.Graph - Line chart
    """
    if df is None or df.empty or 'Mobile Spend' not in df.columns:
        return create_empty_chart("PPC spend data not available")

    fig = go.Figure()

    try:
        # Create stacked area chart
        if 'Mobile Spend' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['YearMonth'] if 'YearMonth' in df.columns else df.index,
                y=df['Mobile Spend'],
                name='Mobile',
                mode='lines',
                line=dict(color='#667eea', width=0),
                fillcolor='rgba(102, 126, 234, 0.5)',
                fill='tozeroy',
                stackgroup='one',
                hovertemplate='<b>Mobile</b><br>$%{y:,.0f}<extra></extra>'
            ))

        if 'Desktop Spend' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['YearMonth'] if 'YearMonth' in df.columns else df.index,
                y=df['Desktop Spend'],
                name='Desktop',
                mode='lines',
                line=dict(color='#f39c12', width=0),
                fillcolor='rgba(243, 156, 18, 0.5)',
                fill='tonexty',
                stackgroup='one',
                hovertemplate='<b>Desktop</b><br>$%{y:,.0f}<extra></extra>'
            ))
    except Exception as e:
        return create_empty_chart(f"Error rendering PPC data: {str(e)}")

    fig.update_layout(
        title={
            'text': "PPC Spend Trend (Mobile + Desktop)",
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'}
        },
        xaxis_title="Month",
        yaxis_title="Spend ($)",
        height=450,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#ddd',
            borderwidth=1
        ),
        plot_bgcolor='#f8f9fa',
        margin=dict(l=70, r=40, t=80, b=60)
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor='#ddd',
        gridcolor='rgba(0,0,0,0.05)'
    )
    fig.update_yaxes(
        tickprefix='$',
        tickformat=',',
        rangemode='tozero',
        showline=True,
        linewidth=1,
        linecolor='#ddd',
        gridcolor='rgba(0,0,0,0.05)'
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


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

    # Check for required columns
    required_cols = ['Total Effort', 'Expected Lift %']
    if not all(col in df.columns for col in required_cols):
        return create_empty_chart("Tactics data missing required columns")

    fig = go.Figure()

    # Color mapping by funnel stage
    color_map = {
        'Conversion': '#667eea',
        'Acquisition': '#2ecc71',
        'LTV': '#f39c12',
        'User Experience': '#e74c3c'
    }

    try:
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

        # Get data ranges for better positioning
        if 'Total Effort' in df.columns and 'Expected Lift %' in df.columns:
            max_effort = df['Total Effort'].max()
            max_lift = (df['Expected Lift %'] * 100).max()
            min_lift = (df['Expected Lift %'] * 100).min()
            mid_effort = max_effort / 2
            mid_lift = (max_lift + min_lift) / 2
        else:
            max_effort = 20
            max_lift = 20
            min_lift = 0
            mid_effort = 10
            mid_lift = 10

        # Add quadrant backgrounds
        # Quick Wins (low effort, high impact) - green
        fig.add_shape(type="rect", x0=0, x1=mid_effort, y0=mid_lift, y1=max_lift*1.1,
                      fillcolor="rgba(39,174,96,0.15)", line_width=0, layer="below")

        # Major Projects (high effort, high impact) - orange
        fig.add_shape(type="rect", x0=mid_effort, x1=max_effort*1.1, y0=mid_lift, y1=max_lift*1.1,
                      fillcolor="rgba(243,156,18,0.15)", line_width=0, layer="below")

        # Strategic (low effort, low impact) - blue
        fig.add_shape(type="rect", x0=0, x1=mid_effort, y0=min_lift, y1=mid_lift,
                      fillcolor="rgba(52,152,219,0.15)", line_width=0, layer="below")

        # Low Priority (high effort, low impact) - red
        fig.add_shape(type="rect", x0=mid_effort, x1=max_effort*1.1, y0=min_lift, y1=mid_lift,
                      fillcolor="rgba(231,76,60,0.15)", line_width=0, layer="below")

        # Add divider lines
        fig.add_hline(y=mid_lift, line_dash="solid", line_color="rgba(44,62,80,0.4)", line_width=2)
        fig.add_vline(x=mid_effort, line_dash="solid", line_color="rgba(44,62,80,0.4)", line_width=2)

        # Add quadrant labels
        fig.add_annotation(
            text="<b>Quick Wins</b>",
            x=mid_effort*0.5,
            y=max_lift*0.9,
            showarrow=False,
            font=dict(size=13, color='#27ae60', family='Arial, sans-serif'),
            bgcolor='rgba(255,255,255,0.8)',
            borderpad=8
        )
        fig.add_annotation(
            text="<b>Major Projects</b>",
            x=mid_effort*1.5,
            y=max_lift*0.9,
            showarrow=False,
            font=dict(size=13, color='#e67e22', family='Arial, sans-serif'),
            bgcolor='rgba(255,255,255,0.8)',
            borderpad=8
        )
        fig.add_annotation(
            text="<b>Strategic</b>",
            x=mid_effort*0.5,
            y=min_lift*1.5,
            showarrow=False,
            font=dict(size=13, color='#3498db', family='Arial, sans-serif'),
            bgcolor='rgba(255,255,255,0.8)',
            borderpad=8
        )
        fig.add_annotation(
            text="<b>Low Priority</b>",
            x=mid_effort*1.5,
            y=min_lift*1.5,
            showarrow=False,
            font=dict(size=13, color='#c0392b', family='Arial, sans-serif'),
            bgcolor='rgba(255,255,255,0.8)',
            borderpad=8
        )

        fig.update_layout(
            title={
                'text': "Marketing Tactics: Effort vs. Impact",
                'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'}
            },
            xaxis_title="Total Effort (People + Cost)",
            yaxis_title="Expected Lift (%)",
            height=650,
            template='plotly_white',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#ddd',
                borderwidth=1
            ),
            plot_bgcolor='#f8f9fa',
            margin=dict(l=80, r=40, t=80, b=60)
        )

        fig.update_xaxes(
            range=[0, max_effort*1.1],
            gridcolor='rgba(0,0,0,0.05)',
            showline=True,
            linewidth=1,
            linecolor='#ddd'
        )
        fig.update_yaxes(
            range=[min_lift-2, max_lift*1.1],
            gridcolor='rgba(0,0,0,0.05)',
            showline=True,
            linewidth=1,
            linecolor='#ddd'
        )
    except Exception as e:
        return create_empty_chart(f"Error rendering tactics matrix: {str(e)}")

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


def create_keyword_share_chart(df, top_n=15):
    """
    Creates horizontal bar chart for keyword traffic share.

    Args:
        df: pandas.DataFrame - Keyword data
        top_n: int - Number of top keywords to show

    Returns:
        dcc.Graph - Horizontal bar chart
    """
    if df is None or df.empty or 'Keyword' not in df.columns:
        return create_empty_chart("Keyword data not available")

    try:
        # Take top N keywords by clicks
        if 'Clicks' in df.columns:
            df_top = df.nlargest(top_n, 'Clicks').sort_values('Clicks', ascending=True)
        else:
            df_top = df.head(top_n)

        # Create gradient colors from light to dark
        max_clicks = df_top['Clicks'].max() if 'Clicks' in df_top.columns else 100
        colors = [f'rgba(102, 126, 234, {0.4 + (val/max_clicks * 0.6)})'
                  for val in (df_top['Clicks'] if 'Clicks' in df_top.columns else range(len(df_top)))]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=df_top['Keyword'] if 'Keyword' in df_top.columns else df_top.index,
            x=df_top['Clicks'] if 'Clicks' in df_top.columns else range(len(df_top)),
            orientation='h',
            marker_color=colors,
            marker_line_color='white',
            marker_line_width=0.5,
            text=df_top['Clicks'] if 'Clicks' in df_top.columns else range(len(df_top)),
            textposition='outside',
            texttemplate='%{text:,.0f}',
            textfont=dict(size=10),
            hovertemplate='<b>%{y}</b><br>Clicks: <b>%{x:,.0f}</b><extra></extra>'
        ))
    except Exception as e:
        return create_empty_chart(f"Error rendering keyword data: {str(e)}")

    fig.update_layout(
        title={
            'text': f"Top {top_n} Keywords by Traffic",
            'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'}
        },
        xaxis_title="Clicks",
        yaxis_title="",
        height=550,
        template='plotly_white',
        plot_bgcolor='#f8f9fa',
        margin=dict(l=200, r=60, t=80, b=60)
    )

    fig.update_xaxes(
        tickformat=',',
        showline=True,
        linewidth=1,
        linecolor='#ddd',
        gridcolor='rgba(0,0,0,0.05)'
    )
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor='#ddd',
        tickfont=dict(size=11)
    )

    return dcc.Graph(figure=fig, config={'displayModeBar': False})


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
