"""
Excel data loader for marketing insights dashboard.
Handles file upload parsing and extraction of all 17 sheets.
"""

import pandas as pd
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExcelDataLoader:
    """
    Loads and parses Excel files with marketing analysis data.
    Handles all 17 expected sheets and provides error handling.
    """

    # Mapping of internal keys to Excel sheet names
    SHEET_MAPPING = {
        'inputs': 'Inputs',
        'dash_view': 'dash view',
        'benchmarks': 'Benchmarks',
        'traffic_data': 'Similarweb Lead Enrichment',
        'ppc_spend': 'Similarweb PPC Spend',
        'da_backlinks': 'Semrush DA & Backlinks Overview',
        'tactics': 'Low Hanging Fruit',
        'varos_benchmarks': 'Varos Benchmarks',
        'web_vitals': 'Core Web Vitals',
        'cro_vitals': 'CRO Vitals',
        'meta_ads': 'Meta Ads',
        'ie_matrix': 'IE Matrix',
        'backlinks': 'Semrush Backlinks Overview',
        'landing_pages': 'Similarweb Keywords - Landing P',
        'keywords_paid': 'Similarweb Keyword Report - pai',
        'keywords_organic': 'Similarweb Keyword Report - org'
    }

    def __init__(self, excel_file):
        """
        Initialize loader with Excel file.

        Args:
            excel_file: file-like object, bytes, or path to Excel file
        """
        self.excel_file = excel_file
        self.sheets = {}
        self.raw_sheets = {}  # Store raw DataFrames for debugging

    def load_all_sheets(self):
        """
        Load all available sheets from Excel file.

        Returns:
            dict: Dictionary of DataFrames keyed by internal names
        """
        logger.info("Loading Excel sheets...")

        for key, sheet_name in self.SHEET_MAPPING.items():
            try:
                df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
                self.raw_sheets[key] = df.copy()  # Store raw data
                self.sheets[key] = df
                logger.info(f"✓ Loaded {sheet_name}: {df.shape[0]} rows × {df.shape[1]} columns")
            except Exception as e:
                logger.warning(f"⚠ Could not load {sheet_name}: {str(e)}")
                self.sheets[key] = None

        return self.sheets

    def get_sheet(self, key):
        """
        Get a specific sheet by key.

        Args:
            key: str - Internal key name (e.g., 'traffic_data', 'ppc_spend')

        Returns:
            pandas.DataFrame or None
        """
        return self.sheets.get(key)

    def get_available_sheets(self):
        """
        Get list of successfully loaded sheets.

        Returns:
            list: List of sheet keys that were loaded
        """
        return [key for key, df in self.sheets.items() if df is not None and not df.empty]

    def get_sheet_info(self):
        """
        Get information about all sheets (loaded and missing).

        Returns:
            dict: Sheet information with names, shapes, and status
        """
        info = {}

        for key, sheet_name in self.SHEET_MAPPING.items():
            df = self.sheets.get(key)

            if df is not None and not df.empty:
                info[key] = {
                    'name': sheet_name,
                    'status': 'loaded',
                    'rows': df.shape[0],
                    'columns': df.shape[1],
                    'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB"
                }
            else:
                info[key] = {
                    'name': sheet_name,
                    'status': 'missing',
                    'rows': 0,
                    'columns': 0,
                    'memory_usage': '0 KB'
                }

        return info

    @staticmethod
    def from_upload(contents, filename):
        """
        Create loader from Dash upload component contents.

        Args:
            contents: str - Base64 encoded file contents from dcc.Upload
            filename: str - Original filename

        Returns:
            ExcelDataLoader instance
        """
        import base64

        # Decode the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        excel_file = io.BytesIO(decoded)

        logger.info(f"Processing uploaded file: {filename}")

        return ExcelDataLoader(excel_file)

    def summary(self):
        """
        Get summary of loaded data.

        Returns:
            dict: Summary statistics
        """
        available = self.get_available_sheets()

        return {
            'total_sheets': len(self.SHEET_MAPPING),
            'loaded_sheets': len(available),
            'missing_sheets': len(self.SHEET_MAPPING) - len(available),
            'available_keys': available,
            'sheet_details': self.get_sheet_info()
        }
