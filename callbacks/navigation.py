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
    """Placeholder for Paid Search page"""
    from components.charts import create_ppc_spend_trend, create_keyword_share_chart

    return html.Div([
        html.H1("Paid Search Analysis", style={'padding': '0 40px', 'color': '#2c3e50'}),
        html.Div([
            create_ppc_spend_trend(data.get('ppc_spend') if data else None)
        ], style={'padding': '0 40px', 'marginTop': '20px'}),
        html.Div([
            create_keyword_share_chart(data.get('keywords_paid') if data else None)
        ], style={'padding': '0 40px', 'marginTop': '20px'})
    ], style={'padding': '30px 0'})


def create_paid_social_page(data):
    """Placeholder for Paid Social page"""
    return html.Div([
        html.H1("Paid Social Analysis", style={'padding': '0 40px', 'color': '#2c3e50'}),
        html.P("Coming soon - Meta Ads analysis", style={'padding': '0 40px', 'color': '#7f8c8d'})
    ], style={'padding': '30px 0'})


def create_seo_page(data):
    """Placeholder for SEO page"""
    from components.charts import create_keyword_share_chart

    return html.Div([
        html.H1("SEO Analysis", style={'padding': '0 40px', 'color': '#2c3e50'}),
        html.Div([
            create_keyword_share_chart(data.get('keywords_organic') if data else None)
        ], style={'padding': '0 40px', 'marginTop': '20px'})
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
