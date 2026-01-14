"""
Callbacks for AI recommendations generation.
"""

from dash import Input, Output, html
import pandas as pd
from utils.recommendation_engine import RecommendationEngine
from components.recommendations_panel import create_recommendations_panel, create_loading_state


def register_recommendations_callbacks(app):
    """
    Register callbacks for AI recommendations generation.

    Args:
        app: Dash app instance
    """

    @app.callback(
        Output('recommendations-panel', 'children'),
        [Input('data-store', 'data'),
         Input('business-goals', 'value')]
    )
    def generate_recommendations(data, business_goals):
        """
        Generate AI recommendations when data is uploaded.

        Args:
            data: dict - Processed data from data-store
            business_goals: list - Selected business objectives

        Returns:
            html.Div - Recommendations panel
        """
        if data is None:
            return html.Div([
                html.I(className='fas fa-info-circle', style={
                    'fontSize': '48px',
                    'color': '#95a5a6',
                    'marginBottom': '15px'
                }),
                html.H4("Upload Data to See Recommendations", style={
                    'color': '#7f8c8d',
                    'marginBottom': '10px'
                }),
                html.P(
                    "AI-powered recommendations will appear here after uploading your Excel file",
                    style={'color': '#95a5a6', 'fontSize': '14px'}
                )
            ], style={
                'textAlign': 'center',
                'padding': '60px 40px',
                'background': '#f8f9fa',
                'borderRadius': '15px',
                'marginTop': '40px'
            })

        try:
            # Extract company name and industry from inputs sheet
            inputs = data.get('inputs', [])
            company_name = 'Dossier'  # Default
            industry = 'beauty ecommerce'  # Default

            if inputs and len(inputs) > 0:
                try:
                    inputs_df = pd.DataFrame(inputs)
                    # Try to extract company/industry from inputs sheet
                    # This depends on your Excel structure - adjust as needed
                    if 'Company' in inputs_df.columns:
                        company_name = inputs_df['Company'].iloc[0]
                    if 'Industry' in inputs_df.columns:
                        industry = inputs_df['Industry'].iloc[0]
                except Exception as e:
                    print(f"Could not extract company/industry from inputs: {e}")

            # Initialize recommendation engine
            engine = RecommendationEngine(
                processed_data=data,
                business_goals=business_goals or ['acquisition', 'conversion']
            )

            # Analyze current state
            current_state = engine.analyze_current_state()

            # Research industry context
            industry_context = engine.research_industry_context(
                company_name=company_name,
                industry=industry
            )

            # Generate recommendations
            recommendations = engine.generate_recommendations()

            if not recommendations:
                return html.Div([
                    html.I(className='fas fa-exclamation-circle', style={
                        'fontSize': '48px',
                        'color': '#f39c12',
                        'marginBottom': '15px'
                    }),
                    html.H4("No Recommendations Available", style={
                        'color': '#7f8c8d',
                        'marginBottom': '10px'
                    }),
                    html.P(
                        "Unable to generate recommendations from the uploaded data. Please ensure your file contains tactics data.",
                        style={'color': '#95a5a6', 'fontSize': '14px'}
                    )
                ], style={
                    'textAlign': 'center',
                    'padding': '60px 40px',
                    'background': '#f8f9fa',
                    'borderRadius': '15px',
                    'marginTop': '40px'
                })

            # Create implementation roadmap
            roadmap = engine.create_implementation_roadmap(recommendations)

            # Render recommendations panel
            return create_recommendations_panel(recommendations, roadmap)

        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            import traceback
            traceback.print_exc()

            return html.Div([
                html.I(className='fas fa-exclamation-triangle', style={
                    'fontSize': '48px',
                    'color': '#e74c3c',
                    'marginBottom': '15px'
                }),
                html.H4("Error Generating Recommendations", style={
                    'color': '#e74c3c',
                    'marginBottom': '10px'
                }),
                html.P(
                    f"An error occurred: {str(e)}",
                    style={'color': '#95a5a6', 'fontSize': '14px'}
                ),
                html.P(
                    "Please check your data format and try again.",
                    style={'color': '#95a5a6', 'fontSize': '12px', 'marginTop': '10px'}
                )
            ], style={
                'textAlign': 'center',
                'padding': '60px 40px',
                'background': '#fff5f5',
                'borderRadius': '15px',
                'marginTop': '40px',
                'border': '1px solid #e74c3c'
            })
