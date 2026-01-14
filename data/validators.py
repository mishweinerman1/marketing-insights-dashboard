"""
Data validation functions for Excel file uploads.
Ensures uploaded files have required sheets and correct structure.
"""

import pandas as pd
import io


class DataValidator:
    """Validates Excel file structure and data integrity"""

    # Minimum required sheets for dashboard to function
    REQUIRED_SHEETS = [
        'dash view',
        'Similarweb Lead Enrichment',
        'Low Hanging Fruit'
    ]

    # All expected sheets (optional but recommended)
    EXPECTED_SHEETS = [
        'Inputs',
        'dash view',
        'Benchmarks',
        'Similarweb Lead Enrichment',
        'Similarweb PPC Spend',
        'Semrush DA & Backlinks Overview',
        'Low Hanging Fruit',
        'Varos Benchmarks',
        'Core Web Vitals',
        'CRO Vitals',
        'Meta Ads',
        'IE Matrix',
        'Semrush Backlinks Overview',
        'Similarweb Keywords - Landing P',
        'Similarweb Keyword Report - pai',
        'Similarweb Keyword Report - org'
    ]

    @classmethod
    def validate_excel_structure(cls, excel_file):
        """
        Validate that Excel file has required sheets.

        Args:
            excel_file: file-like object or path to Excel file

        Returns:
            tuple: (is_valid: bool, error_message: str or None, warnings: list)
        """
        try:
            xl_file = pd.ExcelFile(excel_file)
            available_sheets = xl_file.sheet_names

            # Check for missing required sheets
            missing_required = [s for s in cls.REQUIRED_SHEETS if s not in available_sheets]

            if missing_required:
                error_msg = f"Missing required sheets: {', '.join(missing_required)}"
                return False, error_msg, []

            # Check for missing optional sheets (warnings only)
            missing_optional = [s for s in cls.EXPECTED_SHEETS
                              if s not in available_sheets and s not in cls.REQUIRED_SHEETS]

            warnings = []
            if missing_optional:
                warnings.append(f"Missing optional sheets (some features may be limited): {', '.join(missing_optional[:3])}")

            return True, None, warnings

        except Exception as e:
            return False, f"Error reading Excel file: {str(e)}", []

    @classmethod
    def validate_sheet_data(cls, df, sheet_name):
        """
        Validate that a sheet contains data.

        Args:
            df: pandas DataFrame
            sheet_name: str - Name of sheet

        Returns:
            tuple: (is_valid: bool, error_message: str or None)
        """
        if df is None:
            return False, f"{sheet_name} is None"

        if df.empty:
            return False, f"{sheet_name} is empty"

        # Check if sheet is just headers
        if len(df) <= 1:
            return False, f"{sheet_name} has no data rows (only headers)"

        return True, None

    @classmethod
    def get_validation_summary(cls, excel_file):
        """
        Get comprehensive validation summary for uploaded file.

        Args:
            excel_file: file-like object or path to Excel file

        Returns:
            dict: Validation results with status, errors, warnings, and sheet info
        """
        is_valid, error, warnings = cls.validate_excel_structure(excel_file)

        summary = {
            'is_valid': is_valid,
            'error': error,
            'warnings': warnings,
            'sheets_found': [],
            'sheets_missing': []
        }

        if not is_valid:
            return summary

        # Get detailed sheet information
        try:
            xl_file = pd.ExcelFile(excel_file)
            available_sheets = xl_file.sheet_names

            for sheet in cls.EXPECTED_SHEETS:
                if sheet in available_sheets:
                    summary['sheets_found'].append(sheet)
                else:
                    summary['sheets_missing'].append(sheet)

        except Exception as e:
            summary['warnings'].append(f"Could not read sheet details: {str(e)}")

        return summary
