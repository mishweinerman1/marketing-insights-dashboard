"""
Competitive Intelligence Engine
Analyzes competitor data from keyword overlap, identifies gaps, and generates data-driven tactics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class CompetitiveIntelligence:
    """
    Analyzes competitive landscape using keyword overlap and multi-source data.
    Generates gap-based tactics recommendations backed by competitive intelligence.
    """

    def __init__(self, processed_data: Dict):
        """
        Initialize competitive intelligence engine.

        Args:
            processed_data: dict - All processed data from uploaded Excel
        """
        self.data = processed_data
        self.primary_company = None
        self.competitors = []
        self.competitive_gaps = []
        self.keyword_overlaps = {}

    def identify_primary_company(self, keywords_df: pd.DataFrame) -> str:
        """
        Identify the primary company (client) from keyword data.

        Args:
            keywords_df: DataFrame with company domain columns

        Returns:
            str - Primary company domain
        """
        # Find all domain columns (contain '.')
        domain_cols = [col for col in keywords_df.columns
                      if '.' in col and 'Unnamed' not in col and col != 'Search Volume']

        if not domain_cols:
            return 'dossier.co'  # Default

        # Primary company is usually the one with most data/highest average traffic
        company_traffic = {}
        for col in domain_cols:
            company_traffic[col] = keywords_df[col].sum()

        if company_traffic:
            primary = max(company_traffic.items(), key=lambda x: x[1])[0]
            self.primary_company = primary
            logger.info(f"Identified primary company: {primary}")
            return primary

        return domain_cols[0]

    def identify_competitors_from_keywords(self) -> List[Dict]:
        """
        Identify competitors based on keyword overlap analysis.

        Returns:
            list of dicts with competitor info and overlap metrics
        """
        competitors = []

        # Get keyword data
        keywords_paid = self.data.get('keywords_paid', [])
        keywords_organic = self.data.get('keywords_organic', [])

        # Combine paid and organic
        all_keywords = []
        if keywords_paid:
            kw_paid_df = pd.DataFrame(keywords_paid) if isinstance(keywords_paid, list) else keywords_paid
            if not kw_paid_df.empty:
                all_keywords.append(kw_paid_df)

        if keywords_organic:
            kw_org_df = pd.DataFrame(keywords_organic) if isinstance(keywords_organic, list) else keywords_organic
            if not kw_org_df.empty:
                all_keywords.append(kw_org_df)

        if not all_keywords:
            logger.warning("No keyword data available for competitor identification")
            return []

        # Combine all keyword data
        combined_kw = pd.concat(all_keywords, ignore_index=True)

        # Identify primary company
        primary = self.identify_primary_company(combined_kw)

        # Find all competitor domains
        domain_cols = [col for col in combined_kw.columns
                      if '.' in col and 'Unnamed' not in col and col != primary]

        for competitor_domain in domain_cols:
            # Calculate keyword overlap
            total_keywords = len(combined_kw)

            # Keywords where both companies have traffic
            both_present = combined_kw[
                (combined_kw[primary] > 0) &
                (combined_kw[competitor_domain] > 0)
            ]
            overlap_count = len(both_present)
            overlap_pct = (overlap_count / total_keywords * 100) if total_keywords > 0 else 0

            # Calculate traffic share on overlapping keywords
            if not both_present.empty:
                primary_traffic = both_present[primary].sum()
                competitor_traffic = both_present[competitor_domain].sum()
                total_overlap_traffic = primary_traffic + competitor_traffic

                competitor_share = (competitor_traffic / total_overlap_traffic * 100) if total_overlap_traffic > 0 else 0
            else:
                competitor_share = 0

            # Keywords where competitor has traffic but primary doesn't (gap keywords)
            gap_keywords = combined_kw[
                (combined_kw[primary] == 0) &
                (combined_kw[competitor_domain] > 0)
            ]
            gap_count = len(gap_keywords)

            # Calculate potential impact (search volume of gap keywords)
            if 'Search Volume' in combined_kw.columns and not gap_keywords.empty:
                gap_potential = gap_keywords['Search Volume'].sum()
            else:
                gap_potential = gap_count * 1000  # Estimate

            competitor_info = {
                'domain': competitor_domain,
                'company_name': self._extract_company_name(competitor_domain),
                'keyword_overlap_count': overlap_count,
                'keyword_overlap_pct': round(overlap_pct, 1),
                'traffic_share_on_overlap': round(competitor_share, 1),
                'gap_keywords_count': gap_count,
                'gap_potential_volume': int(gap_potential),
                'competitive_intensity': self._calculate_competitive_intensity(
                    overlap_pct, competitor_share, gap_count
                ),
                'top_gap_keywords': gap_keywords.head(10)['Keyword'].tolist() if 'Keyword' in gap_keywords.columns else []
            }

            competitors.append(competitor_info)

        # Sort by competitive intensity
        competitors.sort(key=lambda x: x['competitive_intensity'], reverse=True)

        self.competitors = competitors
        logger.info(f"Identified {len(competitors)} competitors")

        return competitors

    def _extract_company_name(self, domain: str) -> str:
        """Extract clean company name from domain."""
        # Remove TLD and clean up
        name = domain.split('.')[0]
        # Handle hyphens and underscores
        name = name.replace('-', ' ').replace('_', ' ')
        # Capitalize
        return name.title()

    def _calculate_competitive_intensity(self, overlap_pct: float,
                                        traffic_share: float,
                                        gap_count: int) -> float:
        """
        Calculate competitive intensity score (0-100).

        Factors:
        - 40%: Keyword overlap (higher = more direct competitor)
        - 30%: Traffic share on overlap (higher = stronger competitor)
        - 30%: Gap keywords (higher = more opportunity)
        """
        overlap_score = min(overlap_pct / 80 * 40, 40)  # 80% overlap = max score
        traffic_score = min(traffic_share / 50 * 30, 30)  # 50% share = max score
        gap_score = min(gap_count / 20 * 30, 30)  # 20+ gaps = max score

        return round(overlap_score + traffic_score + gap_score, 1)

    def analyze_keyword_gaps(self) -> List[Dict]:
        """
        Deep analysis of keyword gaps - which keywords competitors rank for that you don't.

        Returns:
            list of keyword gap opportunities
        """
        keyword_gaps = []

        if not self.competitors:
            self.identify_competitors_from_keywords()

        # Get keyword data
        keywords_paid = self.data.get('keywords_paid', [])
        keywords_organic = self.data.get('keywords_organic', [])

        all_keywords = []
        if keywords_paid:
            kw_paid_df = pd.DataFrame(keywords_paid) if isinstance(keywords_paid, list) else keywords_paid
            if not kw_paid_df.empty:
                kw_paid_df['Type'] = 'Paid'
                all_keywords.append(kw_paid_df)

        if keywords_organic:
            kw_org_df = pd.DataFrame(keywords_organic) if isinstance(keywords_organic, list) else keywords_organic
            if not kw_org_df.empty:
                kw_org_df['Type'] = 'Organic'
                all_keywords.append(kw_org_df)

        if not all_keywords:
            return keyword_gaps

        combined_kw = pd.concat(all_keywords, ignore_index=True)

        # For each top competitor, find high-value gap keywords
        for comp in self.competitors[:5]:  # Top 5 competitors
            competitor_domain = comp['domain']

            if competitor_domain in combined_kw.columns and self.primary_company in combined_kw.columns:
                # Find gaps
                gaps = combined_kw[
                    (combined_kw[self.primary_company] == 0) &
                    (combined_kw[competitor_domain] > 0)
                ]

                if not gaps.empty and 'Search Volume' in gaps.columns:
                    # Sort by search volume
                    gaps = gaps.sort_values('Search Volume', ascending=False)

                    # High-value gaps (top volume)
                    high_value = gaps.head(10)

                    for _, row in high_value.iterrows():
                        keyword_gaps.append({
                            'keyword': row.get('Keyword', ''),
                            'search_volume': row.get('Search Volume', 0),
                            'competitor': comp['company_name'],
                            'competitor_traffic': row.get(competitor_domain, 0),
                            'type': row.get('Type', 'Organic'),
                            'opportunity_score': self._calculate_keyword_opportunity_score(row, competitor_domain)
                        })

        # Sort by opportunity score
        keyword_gaps.sort(key=lambda x: x['opportunity_score'], reverse=True)

        self.competitive_gaps = keyword_gaps
        return keyword_gaps[:20]  # Return top 20 opportunities

    def _calculate_keyword_opportunity_score(self, row: pd.Series, competitor_domain: str) -> float:
        """Calculate opportunity score for a keyword gap."""
        volume = row.get('Search Volume', 0)
        competitor_traffic = row.get(competitor_domain, 0)

        # Higher volume + higher competitor success = higher opportunity
        volume_score = min(volume / 10000 * 50, 50)  # 10K volume = 50 points
        traffic_score = min(competitor_traffic / 1000 * 50, 50)  # 1K traffic = 50 points

        return volume_score + traffic_score

    def generate_competitive_tactics(self, top_n: int = 5) -> List[Dict]:
        """
        Generate top N tactics based on competitive gap analysis.

        Args:
            top_n: Number of tactics to generate

        Returns:
            list of tactic recommendations with competitive context
        """
        tactics = []

        # Ensure we have competitors and gaps
        if not self.competitors:
            self.identify_competitors_from_keywords()

        if not self.competitive_gaps:
            self.analyze_keyword_gaps()

        # Tactic 1: Target high-value keyword gaps
        if self.competitive_gaps:
            top_gaps = self.competitive_gaps[:10]
            gap_keywords = [g['keyword'] for g in top_gaps]
            total_volume = sum([g['search_volume'] for g in top_gaps])

            top_competitor = self.competitors[0] if self.competitors else {'company_name': 'competitors'}

            tactics.append({
                'tactic': f"Target '{gap_keywords[0]}' keyword cluster",
                'category': 'SEO/Content',
                'priority': 'Critical',
                'rationale': f"{top_competitor['company_name']} dominates {len(top_gaps)} high-volume keywords where you have no presence. Combined search volume: {total_volume:,}/month.",
                'competitive_context': f"Competitors getting {total_volume:,} monthly searches on keywords you're missing",
                'gap_type': 'Keyword Gap',
                'keywords': gap_keywords[:5],
                'effort': 6,
                'timeline': '2-3 months',
                'expected_lift': f"{int(total_volume * 0.15):,} monthly visits (15% capture rate)",
                'kpis': ['Organic traffic', 'Keyword rankings', 'Content engagement'],
                'implementation_steps': [
                    f"Create comprehensive content for: {', '.join(gap_keywords[:3])}",
                    "Optimize on-page SEO (title tags, meta descriptions, headers)",
                    "Build internal linking structure",
                    "Promote content through owned channels"
                ],
                'competitive_intelligence': f"Analysis of {len(self.competitors)} competitors shows significant opportunity"
            })

        # Tactic 2: Improve on overlapping keywords
        if self.competitors:
            top_comp = self.competitors[0]
            tactics.append({
                'tactic': f"Reclaim traffic from {top_comp['company_name']} on overlapping keywords",
                'category': 'SEO Optimization',
                'priority': 'High',
                'rationale': f"You're losing {top_comp['traffic_share_on_overlap']:.0f}% traffic share to {top_comp['company_name']} on {top_comp['keyword_overlap_count']} shared keywords.",
                'competitive_context': f"{top_comp['company_name']} has {top_comp['traffic_share_on_overlap']:.0f}% share vs your {100-top_comp['traffic_share_on_overlap']:.0f}%",
                'gap_type': 'Share of Voice',
                'effort': 7,
                'timeline': '3-4 months',
                'expected_lift': "15-25% traffic increase on target keywords",
                'kpis': ['Keyword rankings improvement', 'Click-through rate', 'Traffic share']
            })

        return tactics[:top_n]

    def get_competitive_summary(self) -> Dict:
        """
        Generate comprehensive competitive intelligence summary.

        Returns:
            dict with all competitive insights
        """
        if not self.competitors:
            self.identify_competitors_from_keywords()

        if not self.competitive_gaps:
            self.analyze_keyword_gaps()

        # Calculate aggregate metrics
        total_gap_volume = sum([g['search_volume'] for g in self.competitive_gaps])
        avg_intensity = np.mean([c['competitive_intensity'] for c in self.competitors]) if self.competitors else 0

        return {
            'primary_company': self.primary_company,
            'competitor_count': len(self.competitors),
            'top_competitors': self.competitors[:5],
            'total_keyword_gaps': len(self.competitive_gaps),
            'total_gap_potential_volume': total_gap_volume,
            'avg_competitive_intensity': round(avg_intensity, 1)
        }
