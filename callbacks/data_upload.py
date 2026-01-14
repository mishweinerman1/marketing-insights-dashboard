"""
Data upload callback for Excel file processing.
Handles file upload, validation, and data storage.
"""

from dash import Input, Output, State, html
import io
import logging

from data.loader import ExcelDataLoader
from data.validators import DataValidator
from data.processor import DataProcessor

logger = logging.getLogger(__name__)


def register_callbacks(app):
    """
    Register data upload callbacks.

    Args:
        app: Dash app instance
    """

    @app.callback(
        [Output('data-store', 'data'),
         Output('upload-status', 'children'),
         Output('data-status-indicator', 'children'),
         Output('data-status-indicator', 'style')],
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def upload_file(contents, filename):
        """
        Handle Excel file upload and process all sheets.

        Args:
            contents: str - Base64 encoded file contents
            filename: str - Original filename

        Returns:
            tuple: (processed_data, status_message, indicator_text, indicator_style)
        """
        if contents is None:
            return (
                None,
                html.Div([
                    html.I(className='fas fa-upload', style={'marginRight': '10px', 'fontSize': '24px'}),
                    html.Span("No file uploaded yet")
                ], style={'color': '#95a5a6', 'fontSize': '16px'}),
                [html.I(className='fas fa-exclamation-circle', style={'marginRight': '8px'}),
                 html.Span('No Data')],
                {
                    'padding': '10px 20px',
                    'background': 'rgba(255,255,255,0.2)',
                    'borderRadius': '8px',
                    'color': '#ffffff',
                    'display': 'flex',
                    'alignItems': 'center'
                }
            )

        try:
            import base64

            # Decode the uploaded file
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            excel_file = io.BytesIO(decoded)

            logger.info(f"Processing uploaded file: {filename}")

            # Validate file structure
            is_valid, error_msg, warnings = DataValidator.validate_excel_structure(excel_file)

            if not is_valid:
                return (
                    None,
                    html.Div([
                        html.I(className='fas fa-exclamation-triangle', style={
                            'marginRight': '10px',
                            'fontSize': '20px'
                        }),
                        html.Div([
                            html.Strong(f"Error: {error_msg}", style={'display': 'block', 'marginBottom': '5px'}),
                            html.Span(f"File: {filename}", style={'fontSize': '13px'})
                        ])
                    ], style={'color': '#e74c3c', 'padding': '15px'}),
                    [html.I(className='fas fa-times-circle', style={'marginRight': '8px'}),
                     html.Span('Error')],
                    {
                        'padding': '10px 20px',
                        'background': 'rgba(231,76,60,0.2)',
                        'borderRadius': '8px',
                        'color': '#ffffff',
                        'display': 'flex',
                        'alignItems': 'center'
                    }
                )

            # Reset file pointer
            excel_file.seek(0)

            # Load and process data
            loader = ExcelDataLoader(excel_file)
            sheets = loader.load_all_sheets()

            processor = DataProcessor()
            processed_data = processor.process_all_data(sheets)

            # Convert DataFrames to dictionaries for JSON storage
            serializable_data = {}
            for key, value in processed_data.items():
                if hasattr(value, 'to_dict'):  # pandas DataFrame
                    serializable_data[key] = value.to_dict('records')
                else:
                    serializable_data[key] = value

            # Create success message
            summary = loader.summary()
            success_msg = html.Div([
                html.I(className='fas fa-check-circle', style={
                    'marginRight': '10px',
                    'fontSize': '24px',
                    'color': '#27ae60'
                }),
                html.Div([
                    html.Strong(f"✓ Successfully loaded: {filename}", style={
                        'display': 'block',
                        'marginBottom': '8px',
                        'color': '#27ae60',
                        'fontSize': '16px'
                    }),
                    html.Div([
                        html.Span(f"📊 {summary['loaded_sheets']}/{summary['total_sheets']} sheets loaded", style={
                            'marginRight': '15px',
                            'fontSize': '13px',
                            'color': '#7f8c8d'
                        }),
                        html.Span(f"✅ Data processed successfully", style={
                            'fontSize': '13px',
                            'color': '#7f8c8d'
                        })
                    ])
                ])
            ], style={'padding': '15px', 'background': '#d4edda', 'borderRadius': '8px', 'border': '1px solid #c3e6cb'})

            # Add warnings if any
            if warnings:
                warnings_div = html.Div([
                    html.I(className='fas fa-info-circle', style={'marginRight': '8px'}),
                    html.Span(warning)
                ], style={'marginTop': '10px', 'fontSize': '12px', 'color': '#856404'})
                success_msg = html.Div([success_msg, warnings_div])

            logger.info(f"✓ Successfully processed {filename}")

            return (
                serializable_data,
                success_msg,
                [html.I(className='fas fa-check-circle', style={'marginRight': '8px'}),
                 html.Span('Data Loaded')],
                {
                    'padding': '10px 20px',
                    'background': 'rgba(46,204,113,0.3)',
                    'borderRadius': '8px',
                    'color': '#ffffff',
                    'display': 'flex',
                    'alignItems': 'center'
                }
            )

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}", exc_info=True)

            return (
                None,
                html.Div([
                    html.I(className='fas fa-times-circle', style={
                        'marginRight': '10px',
                        'fontSize': '20px'
                    }),
                    html.Div([
                        html.Strong(f"Error processing file", style={'display': 'block', 'marginBottom': '5px'}),
                        html.Span(f"Details: {str(e)}", style={'fontSize': '13px', 'fontFamily': 'monospace'})
                    ])
                ], style={'color': '#e74c3c', 'padding': '15px', 'background': '#f8d7da', 'borderRadius': '8px'}),
                [html.I(className='fas fa-exclamation-triangle', style={'marginRight': '8px'}),
                 html.Span('Error')],
                {
                    'padding': '10px 20px',
                    'background': 'rgba(231,76,60,0.2)',
                    'borderRadius': '8px',
                    'color': '#ffffff',
                    'display': 'flex',
                    'alignItems': 'center'
                }
            )
