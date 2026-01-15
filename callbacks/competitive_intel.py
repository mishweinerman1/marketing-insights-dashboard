"""
Competitive Intelligence Callbacks
Generates and displays competitive analysis based on keyword overlap data.
"""

from dash import Input, Output, html
from utils.competitive_intelligence import CompetitiveIntelligence
from components.competitive_intel_panel import create_competitive_intel_panel
import logging

logger = logging.getLogger(__name__)


def register_competitive_intel_callbacks(app):
    """
    Register callbacks for competitive intelligence generation.

    Args:
        app: Dash app instance
    """

    @app.callback(
        Output('competitive-intel-panel', 'children'),
        [Input('data-store', 'data')]
    )
    def generate_competitive_intel(data):
        """
        Generate competitive intelligence when data is uploaded.

        Args:
            data: dict - Processed data from data-store

        Returns:
            html.Div - Competitive intelligence panel
        """
        if data is None:
            return html.Div()  # Return empty div when no data

        try:
            # Initialize competitive intelligence engine
            ci_engine = CompetitiveIntelligence(processed_data=data)

            # Identify competitors
            competitors = ci_engine.identify_competitors_from_keywords()

            if not competitors:
                logger.info("No competitors identified from keyword data")
                return html.Div([
                    html.Div([
                        html.I(className='fas fa-info-circle', style={
                            'fontSize': '36px',
                            'color': '#95a5a6',
                            'marginBottom': '12px'
                        }),
                        html.H4("No Competitor Data Available", style={
                            'color': '#7f8c8d',
                            'marginBottom': '8px'
                        }),
                        html.P(
                            "Competitive analysis requires keyword data with multiple domain columns. "
                            "Please ensure your Excel file contains keyword sheets with competitor traffic data.",
                            style={'color': '#95a5a6', 'fontSize': '14px', 'lineHeight': '1.6'}
                        )
                    ], style={
                        'textAlign': 'center',
                        'padding': '50px 40px',
                        'background': '#f8f9fa',
                        'borderRadius': '15px',
                        'marginTop': '30px'
                    })
                ])

            # Analyze keyword gaps
            keyword_gaps = ci_engine.analyze_keyword_gaps()

            # Generate competitive tactics
            competitive_tactics = ci_engine.generate_competitive_tactics(top_n=5)

            # Get comprehensive summary
            competitive_summary = ci_engine.get_competitive_summary()

            logger.info(f"Generated competitive intelligence: {len(competitors)} competitors, {len(keyword_gaps)} gaps")

            # Render competitive intelligence panel
            return create_competitive_intel_panel(
                competitive_summary=competitive_summary,
                competitive_tactics=competitive_tactics
            )

        except Exception as e:
            logger.error(f"Error generating competitive intelligence: {str(e)}")
            import traceback
            traceback.print_exc()

            return html.Div([
                html.Div([
                    html.I(className='fas fa-exclamation-triangle', style={
                        'fontSize': '36px',
                        'color': '#e74c3c',
                        'marginBottom': '12px'
                    }),
                    html.H4("Error Generating Competitive Intelligence", style={
                        'color': '#e74c3c',
                        'marginBottom': '8px'
                    }),
                    html.P(
                        f"An error occurred while analyzing competitive data: {str(e)}",
                        style={'color': '#95a5a6', 'fontSize': '14px'}
                    )
                ], style={
                    'textAlign': 'center',
                    'padding': '50px 40px',
                    'background': '#fff5f5',
                    'borderRadius': '15px',
                    'border': '1px solid #e74c3c',
                    'marginTop': '30px'
                })
            ])
