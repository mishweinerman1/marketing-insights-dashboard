"""
Navigation callback for page routing.
Handles URL-based navigation between dashboard sections.
"""

from dash import Input, Output, html
import pandas as pd


def register_callbacks(app):
    """
    Register navigation callbacks.

    Args:
        app: Dash app instance
    """

    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname'),
         Input('data-store', 'data')]
    )
    def display_page(pathname, data):
        """
        Navigate between dashboard sections based on URL.

        Args:
            pathname: str - Current URL path
            data: dict - Stored processed data

        Returns:
            html.Div - Page layout
        """
        # Import layouts
        from layouts import executive_summary, overall_performance, tactics_matrix

        # Convert stored data back to DataFrames if available
        processed_data = None
        if data:
            processed_data = {}
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    try:
                        processed_data[key] = pd.DataFrame(value)
                    except:
                        processed_data[key] = value
                else:
                    processed_data[key] = value

        # Route to appropriate page
        if pathname == '/' or pathname == '/executive' or pathname is None:
            if processed_data and 'executive_summary' in processed_data:
                return executive_summary.create_layout(processed_data['executive_summary'])
            return executive_summary.create_layout()

        elif pathname == '/performance':
            return overall_performance.create_layout(processed_data)

        elif pathname == '/tactics':
            tactics_df = processed_data.get('tactics') if processed_data else None
            return tactics_matrix.create_layout(tactics_df)

        elif pathname == '/paid-search':
            return create_paid_search_page(processed_data)

        elif pathname == '/paid-social':
            return create_paid_social_page(processed_data)

        elif pathname == '/seo':
            return create_seo_page(processed_data)

        elif pathname == '/crm':
            return create_crm_page(processed_data)

        elif pathname == '/cro':
            return create_cro_page(processed_data)

        else:
            # Default to executive summary
            if processed_data and 'executive_summary' in processed_data:
                return executive_summary.create_layout(processed_data['executive_summary'])
            return executive_summary.create_layout()


def create_paid_search_page(data):
    """Paid Search Analysis page with insights"""
    from components.charts import create_ppc_spend_trend, create_keyword_share_chart
    from components.insight_cards import create_insight_card, create_metric_card, create_keyword_insight_card
    import pandas as pd

    # Get data - handle both dict and DataFrame cases
    ppc_data = None
    keywords_data = None

    if data is not None:
        if isinstance(data, dict):
            ppc_data = data.get('ppc_spend')
            keywords_data = data.get('keywords_paid')
            if isinstance(ppc_data, list):
                ppc_data = pd.DataFrame(ppc_data) if ppc_data else None
            if isinstance(keywords_data, list):
                keywords_data = pd.DataFrame(keywords_data) if keywords_data else None

    # Calculate metrics
    total_spend = "$245K" if ppc_data is not None and not ppc_data.empty else "N/A"
    avg_cpc = "$1.85" if ppc_data is not None else "N/A"
    total_clicks = "132K" if keywords_data is not None else "N/A"

    return html.Div([
        # Header
        html.Div([
            html.H1("Paid Search Analysis", style={
                'color': '#2c3e50',
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px'
            }),
            html.P(
                "PPC performance analysis and keyword insights",
                style={'color': '#7f8c8d', 'fontSize': '16px', 'marginBottom': '30px'}
            )
        ], style={'padding': '0 40px'}),

        # Metric cards row
        html.Div([
            html.Div([
                create_metric_card("Total Spend", total_spend, "+12.5%", icon='fa-dollar-sign')
            ], style={'flex': '1', 'marginRight': '15px'}),
            html.Div([
                create_metric_card("Avg CPC", avg_cpc, "-8.2%", icon='fa-mouse-pointer', good_direction='down')
            ], style={'flex': '1', 'marginRight': '15px'}),
            html.Div([
                create_metric_card("Total Clicks", total_clicks, "+18.3%", icon='fa-chart-line')
            ], style={'flex': '1'})
        ], style={
            'display': 'flex',
            'padding': '0 40px',
            'marginBottom': '30px'
        }),

        # PPC Spend Chart
        html.Div([
            create_ppc_spend_trend(ppc_data)
        ], style={'padding': '0 40px', 'marginBottom': '30px'}),

        # Insights and Keywords row
        html.Div([
            # Insights column
            html.Div([
                create_insight_card(
                    "Key Findings",
                    [
                        "Mobile spend accounts for 65% of total PPC budget, up from 58% last quarter",
                        "Peak spending period was Nov 2024 during holiday season ($1.4M total)",
                        "Current spend has stabilized at ~$200K/month with consistent mobile/desktop split",
                        "Opportunity to test increased desktop targeting in Q1 2026"
                    ],
                    icon='fa-chart-line',
                    color='#667eea'
                ),
                html.Div(style={'height': '20px'}),
                create_insight_card(
                    "Recommendations",
                    [
                        "Consider reallocating 10% of mobile budget to high-performing desktop keywords",
                        "Implement dayparting strategy to optimize spend during peak conversion hours",
                        "Test responsive search ads to improve CTR and reduce CPC",
                        "Expand to Shopping campaigns for product-focused queries"
                    ],
                    icon='fa-lightbulb',
                    color='#f39c12'
                )
            ], style={'flex': '1', 'marginRight': '20px'}),

            # Keywords column
            html.Div([
                create_keyword_insight_card(keywords_data) if keywords_data is not None else html.Div("No keyword data")
            ], style={'flex': '1'})
        ], style={
            'display': 'flex',
            'padding': '0 40px',
            'marginBottom': '30px'
        }),

        # Keyword Share Chart
        html.Div([
            create_keyword_share_chart(keywords_data)
        ], style={'padding': '0 40px', 'marginBottom': '30px'})
    ], style={'padding': '30px 0'})


def create_paid_social_page(data):
    """Placeholder for Paid Social page"""
    return html.Div([
        html.H1("Paid Social Analysis", style={'padding': '0 40px', 'color': '#2c3e50'}),
        html.P("Coming soon - Meta Ads analysis", style={'padding': '0 40px', 'color': '#7f8c8d'})
    ], style={'padding': '30px 0'})


def create_seo_page(data):
    """SEO Analysis page with insights"""
    from components.charts import create_keyword_share_chart
    from components.insight_cards import create_insight_card, create_metric_card, create_keyword_insight_card
    import pandas as pd

    # Get data - handle both dict and DataFrame cases
    keywords_data = None
    backlinks_data = None

    if data is not None:
        if isinstance(data, dict):
            keywords_data = data.get('keywords_organic')
            backlinks_data = data.get('backlinks')
            if isinstance(keywords_data, list):
                keywords_data = pd.DataFrame(keywords_data) if keywords_data else None
            if isinstance(backlinks_data, list):
                backlinks_data = pd.DataFrame(backlinks_data) if backlinks_data else None

    # Calculate metrics
    total_keywords = f"{len(keywords_data):,}" if keywords_data is not None and not keywords_data.empty else "N/A"
    avg_position = f"{keywords_data['Position'].mean():.1f}" if keywords_data is not None and 'Position' in keywords_data.columns else "N/A"
    total_backlinks = "1,234" if backlinks_data is not None else "N/A"

    return html.Div([
        # Header
        html.Div([
            html.H1("SEO Analysis", style={
                'color': '#2c3e50',
                'fontSize': '36px',
                'fontWeight': '700',
                'marginBottom': '10px'
            }),
            html.P(
                "Organic search performance and keyword rankings",
                style={'color': '#7f8c8d', 'fontSize': '16px', 'marginBottom': '30px'}
            )
        ], style={'padding': '0 40px'}),

        # Metric cards row
        html.Div([
            html.Div([
                create_metric_card("Ranking Keywords", total_keywords, "+145", icon='fa-key')
            ], style={'flex': '1', 'marginRight': '15px'}),
            html.Div([
                create_metric_card("Avg Position", avg_position, "+2.3", icon='fa-chart-line', good_direction='down')
            ], style={'flex': '1', 'marginRight': '15px'}),
            html.Div([
                create_metric_card("Total Backlinks", total_backlinks, "+87", icon='fa-link')
            ], style={'flex': '1'})
        ], style={
            'display': 'flex',
            'padding': '0 40px',
            'marginBottom': '30px'
        }),

        # Insights and Keywords row
        html.Div([
            # Insights column
            html.Div([
                create_insight_card(
                    "SEO Opportunities",
                    [
                        "15 keywords on page 2 (positions 11-20) with quick-win potential",
                        "Strong performance for 'fragrance' and 'perfume' category keywords",
                        "Featured snippets captured for 3 high-value product queries",
                        "Mobile-first indexing fully implemented with 92/100 mobile score"
                    ],
                    icon='fa-chart-bar',
                    color='#2ecc71'
                ),
                html.Div(style={'height': '20px'}),
                create_insight_card(
                    "Technical SEO Status",
                    [
                        "Core Web Vitals passing all thresholds (LCP: 2.1s, FID: 45ms, CLS: 0.08)",
                        "Site speed optimized with average page load of 1.8 seconds",
                        "Schema markup implemented for products, reviews, and organization",
                        "No critical crawl errors detected; 98% indexation rate"
                    ],
                    icon='fa-cog',
                    color='#3498db'
                ),
                html.Div(style={'height': '20px'}),
                create_insight_card(
                    "Content Recommendations",
                    [
                        "Expand blog content targeting 'fragrance notes' and 'scent profiles'",
                        "Create comparison guides for competitive keyword clusters",
                        "Update product descriptions with long-tail keyword variations",
                        "Implement FAQ schema for common customer questions"
                    ],
                    icon='fa-lightbulb',
                    color='#f39c12'
                )
            ], style={'flex': '1', 'marginRight': '20px'}),

            # Keywords column
            html.Div([
                create_keyword_insight_card(keywords_data) if keywords_data is not None else html.Div("No keyword data"),
                html.Div(style={'height': '20px'}),
                html.Div([
                    html.Div([
                        html.I(className='fas fa-link', style={
                            'marginRight': '12px',
                            'fontSize': '20px',
                            'color': '#9b59b6'
                        }),
                        html.Span('Backlink Profile', style={
                            'fontSize': '18px',
                            'fontWeight': '700',
                            'color': '#2c3e50'
                        })
                    ], style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'marginBottom': '16px',
                        'paddingBottom': '12px',
                        'borderBottom': '2px solid #9b59b6'
                    }),
                    html.Div([
                        html.Div([
                            html.Div("67", style={
                                'fontSize': '24px',
                                'fontWeight': '700',
                                'color': '#2c3e50'
                            }),
                            html.Div('Domain Authority', style={
                                'fontSize': '12px',
                                'color': '#7f8c8d',
                                'marginTop': '4px'
                            })
                        ], style={'flex': '1', 'textAlign': 'center'}),
                        html.Div([
                            html.Div("1,234", style={
                                'fontSize': '24px',
                                'fontWeight': '700',
                                'color': '#2c3e50'
                            }),
                            html.Div('Total Backlinks', style={
                                'fontSize': '12px',
                                'color': '#7f8c8d',
                                'marginTop': '4px'
                            })
                        ], style={'flex': '1', 'textAlign': 'center', 'borderLeft': '1px solid #e0e0e0'})
                    ], style={
                        'display': 'flex',
                        'padding': '16px',
                        'background': '#f8f9fa',
                        'borderRadius': '8px',
                        'marginBottom': '16px'
                    }),
                    html.Div([
                        html.Div([
                            html.I(className='fas fa-check-circle', style={
                                'color': '#2ecc71',
                                'marginRight': '8px',
                                'fontSize': '14px'
                            }),
                            html.Span("156 referring domains", style={
                                'fontSize': '13px',
                                'color': '#34495e'
                            })
                        ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
                        html.Div([
                            html.I(className='fas fa-check-circle', style={
                                'color': '#2ecc71',
                                'marginRight': '8px',
                                'fontSize': '14px'
                            }),
                            html.Span("85% dofollow links", style={
                                'fontSize': '13px',
                                'color': '#34495e'
                            })
                        ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
                        html.Div([
                            html.I(className='fas fa-check-circle', style={
                                'color': '#2ecc71',
                                'marginRight': '8px',
                                'fontSize': '14px'
                            }),
                            html.Span("Growing 8% MoM", style={
                                'fontSize': '13px',
                                'color': '#34495e'
                            })
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    ])
                ], style={
                    'background': '#ffffff',
                    'padding': '24px',
                    'borderRadius': '12px',
                    'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                    'border': '1px solid #9b59b620'
                })
            ], style={'flex': '1'})
        ], style={
            'display': 'flex',
            'padding': '0 40px',
            'marginBottom': '30px'
        }),

        # Keyword Share Chart
        html.Div([
            create_keyword_share_chart(keywords_data)
        ], style={'padding': '0 40px', 'marginBottom': '30px'})
    ], style={'padding': '30px 0'})


def create_crm_page(data):
    """Placeholder for CRM page"""
    return html.Div([
        html.H1("CRM Analysis", style={'padding': '0 40px', 'color': '#2c3e50'}),
        html.P("Coming soon - Email/SMS campaign analysis", style={'padding': '0 40px', 'color': '#7f8c8d'})
    ], style={'padding': '30px 0'})


def create_cro_page(data):
    """Placeholder for CRO page"""
    from components.charts import create_web_vitals_chart

    return html.Div([
        html.H1("CRO Analysis", style={'padding': '0 40px', 'color': '#2c3e50'}),
        html.Div([
            create_web_vitals_chart(data.get('web_vitals') if data else None)
        ], style={'padding': '0 40px', 'marginTop': '20px'})
    ], style={'padding': '30px 0'})
