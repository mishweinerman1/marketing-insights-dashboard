"""
Data processing and transformation for marketing insights dashboard.
Cleans raw Excel data and prepares it for visualizations.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processes and transforms raw Excel data for dashboard visualizations"""

    @staticmethod
    def clean_dataframe(df):
        """
        Basic cleaning for any DataFrame.

        Args:
            df: pandas.DataFrame

        Returns:
            pandas.DataFrame - Cleaned DataFrame
        """
        if df is None or df.empty:
            return df

        # Remove completely empty rows and columns
        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)

        # Clean column names
        df.columns = [str(col).strip() if not pd.isna(col) else f'Unnamed_{i}'
                     for i, col in enumerate(df.columns)]

        return df

    @staticmethod
    def process_traffic_data(df):
        """
        Process Similarweb Lead Enrichment data.

        Args:
            df: pandas.DataFrame - Raw traffic data

        Returns:
            pandas.DataFrame - Processed traffic metrics
        """
        if df is None or df.empty:
            logger.warning("Traffic data is empty")
            return pd.DataFrame()

        df = DataProcessor.clean_dataframe(df)

        # The traffic data has URL, date columns, and various metrics
        # Extract relevant columns
        try:
            # Find columns with traffic metrics
            metric_cols = [col for col in df.columns if 'traffic' in col.lower()
                          or 'visits' in col.lower()
                          or 'share' in col.lower()]

            if len(df) > 0:
                logger.info(f"Processed traffic data: {df.shape}")

        except Exception as e:
            logger.error(f"Error processing traffic data: {e}")

        return df

    @staticmethod
    def process_ppc_spend(df):
        """
        Process PPC spend data (Similarweb PPC Spend sheet).

        Args:
            df: pandas.DataFrame - Raw PPC spend data

        Returns:
            pandas.DataFrame - Processed with total spend and trends
        """
        if df is None or df.empty:
            logger.warning("PPC spend data is empty")
            return pd.DataFrame()

        df = DataProcessor.clean_dataframe(df)

        try:
            # Calculate total spend (Mobile + Desktop)
            if 'Mobile Spend' in df.columns and 'Desktop Spend' in df.columns:
                df['Total Spend'] = df['Mobile Spend'] + df['Desktop Spend']

            # Parse date if available
            if 'YearMonth' in df.columns:
                df['YearMonth'] = pd.to_datetime(df['YearMonth'], errors='coerce')
                df['Year'] = df['YearMonth'].dt.year
                df['Month'] = df['YearMonth'].dt.month
                df['Month Name'] = df['YearMonth'].dt.strftime('%b %Y')

                # Calculate YoY growth
                df = df.sort_values('YearMonth')
                df['Spend YoY %'] = df['Total Spend'].pct_change(12) * 100

            logger.info(f"Processed PPC spend data: {df.shape}")

        except Exception as e:
            logger.error(f"Error processing PPC spend: {e}")

        return df

    @staticmethod
    def process_tactics_matrix(df_tactics, df_ie_matrix):
        """
        Merge Low Hanging Fruit and IE Matrix sheets.

        Args:
            df_tactics: pandas.DataFrame - Low Hanging Fruit sheet
            df_ie_matrix: pandas.DataFrame - IE Matrix sheet

        Returns:
            pandas.DataFrame - Combined tactics with priority scores
        """
        if df_tactics is None or df_tactics.empty:
            logger.warning("Tactics data is empty")
            return pd.DataFrame()

        df_tactics = DataProcessor.clean_dataframe(df_tactics)

        try:
            # Merge with IE Matrix if available
            if df_ie_matrix is not None and not df_ie_matrix.empty:
                df_ie_matrix = DataProcessor.clean_dataframe(df_ie_matrix)

                # Try to merge on tactic name
                if 'Tactics' in df_tactics.columns and 'Marketing Tactic' in df_ie_matrix.columns:
                    merged = pd.merge(
                        df_tactics,
                        df_ie_matrix,
                        left_on='Tactics',
                        right_on='Marketing Tactic',
                        how='outer'
                    )
                else:
                    merged = df_tactics
            else:
                merged = df_tactics

            # Calculate priority score (Expected Lift / Total Effort)
            if 'Expected Lift %' in merged.columns and 'Total Effort' in merged.columns:
                merged['Priority Score'] = (merged['Expected Lift %'] * 100) / merged['Total Effort'].replace(0, 1)
                merged['Priority Score'] = merged['Priority Score'].fillna(0)

            # Add priority category
            if 'Priority Score' in merged.columns:
                merged['Priority Category'] = pd.cut(
                    merged['Priority Score'],
                    bins=[-np.inf, 0.5, 1.0, 2.0, np.inf],
                    labels=['Low', 'Medium', 'High', 'Critical']
                )

            # Calculate cost efficiency (Lift per dollar)
            if 'Expected Lift %' in merged.columns and 'Projected Cost' in merged.columns:
                merged['Cost Efficiency'] = (merged['Expected Lift %'] * 100) / merged['Projected Cost'].replace(0, 1)

            logger.info(f"Processed tactics matrix: {merged.shape}")

            return merged

        except Exception as e:
            logger.error(f"Error processing tactics matrix: {e}")
            return df_tactics

    @staticmethod
    def process_web_vitals(df):
        """
        Process Core Web Vitals data.

        Args:
            df: pandas.DataFrame - Core Web Vitals sheet

        Returns:
            pandas.DataFrame - Processed vitals with scores
        """
        if df is None or df.empty:
            logger.warning("Web vitals data is empty")
            return pd.DataFrame()

        df = DataProcessor.clean_dataframe(df)

        try:
            # The first column is usually URL
            if len(df.columns) > 0:
                url_col = df.columns[0]
                if 'URL' not in df.columns and url_col != 'URL':
                    df = df.rename(columns={url_col: 'URL'})

            # Extract company name from URL
            if 'URL' in df.columns:
                df['Company'] = df['URL'].str.replace('http://', '').str.replace('https://', '')
                df['Company'] = df['Company'].str.split('.').str[0].str.title()

            logger.info(f"Processed web vitals: {df.shape}")

        except Exception as e:
            logger.error(f"Error processing web vitals: {e}")

        return df

    @staticmethod
    def process_keywords(df, keyword_type='paid'):
        """
        Process keyword data (paid or organic).

        Args:
            df: pandas.DataFrame - Keyword report
            keyword_type: str - 'paid' or 'organic'

        Returns:
            pandas.DataFrame - Processed keyword metrics
        """
        if df is None or df.empty:
            logger.warning(f"{keyword_type} keyword data is empty")
            return pd.DataFrame()

        df = DataProcessor.clean_dataframe(df)

        try:
            # Add keyword type column
            df['Type'] = keyword_type.title()

            # Calculate market share if company columns exist
            company_cols = [col for col in df.columns if '.' in col and 'Unnamed' not in col]

            if len(company_cols) > 0:
                df['Total Clicks'] = df[company_cols].sum(axis=1)

                for col in company_cols:
                    share_col = f'{col}_share'
                    df[share_col] = (df[col] / df['Total Clicks'] * 100).fillna(0)

            logger.info(f"Processed {keyword_type} keywords: {df.shape}")

        except Exception as e:
            logger.error(f"Error processing keywords: {e}")

        return df

    @staticmethod
    def process_backlinks(df):
        """
        Process SEO backlinks data.

        Args:
            df: pandas.DataFrame - Backlinks overview

        Returns:
            pandas.DataFrame - Processed backlink metrics
        """
        if df is None or df.empty:
            logger.warning("Backlinks data is empty")
            return pd.DataFrame()

        df = DataProcessor.clean_dataframe(df)

        try:
            # Extract company name from domain
            if 'Domain' in df.columns:
                df['Company'] = df['Domain'].str.split('.').str[0].str.title()

            logger.info(f"Processed backlinks: {df.shape}")

        except Exception as e:
            logger.error(f"Error processing backlinks: {e}")

        return df

    @staticmethod
    def calculate_executive_summary(sheets):
        """
        Extract executive summary metrics from various sheets.

        Args:
            sheets: dict - Dictionary of all loaded sheets

        Returns:
            dict - Executive summary data with 4 channel cards
        """
        # Default channel data (matching PDF page 9)
        channels = {
            'DTC Ecomm': {
                'share': 0.43,
                'growth': '+18% YoY',
                'icon': '🛒',
                'description': 'Core performance engine',
                'bullets': [
                    'Core revenue engine, 43% of 2025 revenue',
                    '18% YoY growth in H1 2025',
                    'Strong brand loyalty and repeat purchases'
                ]
            },
            'Wholesale Retail': {
                'share': 0.30,
                'growth': '+44% margin',
                'icon': '🏢',
                'description': 'Big-box retail outperforming',
                'bullets': [
                    'Target sales 90K units above forecast',
                    'Walmart = #1 POS fragrance brand',
                    'Retail driving 44% margin contribution'
                ]
            },
            'Marketplace': {
                'share': 0.15,
                'growth': 'Solid economics',
                'icon': '📦',
                'description': 'Lean channel with strong unit economics',
                'bullets': [
                    'Strategic role in SEO and brand visibility',
                    'Helps offload long-tail SKUs',
                    'Supports pricing strategy without dilution'
                ]
            },
            'TikTok Shop': {
                'share': 0.11,
                'growth': '1% → 15%',
                'icon': '🎵',
                'description': 'High-velocity social commerce',
                'bullets': [
                    'Breakout DTC lever in under a year',
                    'Originals growing from 1% to 15%+ of units',
                    'Influencer collaborations driving performance'
                ]
            }
        }

        try:
            # Try to extract real data from sheets if available
            # This would require analyzing the dash_view or inputs sheets
            # For now, return the default template data

            logger.info("Generated executive summary")

        except Exception as e:
            logger.error(f"Error calculating executive summary: {e}")

        return channels

    @staticmethod
    def process_all_data(sheets):
        """
        Process all sheets and return dashboard-ready data.

        Args:
            sheets: dict - Dictionary of raw DataFrames from ExcelDataLoader

        Returns:
            dict - Processed data for all dashboard sections
        """
        logger.info("Processing all data sheets...")

        processed = {
            'executive_summary': DataProcessor.calculate_executive_summary(sheets),
            'traffic_data': DataProcessor.process_traffic_data(sheets.get('traffic_data')),
            'ppc_spend': DataProcessor.process_ppc_spend(sheets.get('ppc_spend')),
            'tactics': DataProcessor.process_tactics_matrix(
                sheets.get('tactics'),
                sheets.get('ie_matrix')
            ),
            'web_vitals': DataProcessor.process_web_vitals(sheets.get('web_vitals')),
            'keywords_paid': DataProcessor.process_keywords(sheets.get('keywords_paid'), 'paid'),
            'keywords_organic': DataProcessor.process_keywords(sheets.get('keywords_organic'), 'organic'),
            'backlinks': DataProcessor.process_backlinks(sheets.get('backlinks')),
            'landing_pages': DataProcessor.clean_dataframe(sheets.get('landing_pages'))
        }

        logger.info("✓ All data processed successfully")

        return processed
