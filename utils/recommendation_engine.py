"""
AI-powered marketing tactics recommendation engine.
Analyzes uploaded data, researches industry context, and generates recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


class RecommendationEngine:
    """
    AI-powered marketing tactics recommendation engine.
    Analyzes uploaded data, researches industry context, and generates prioritized recommendations.
    """

    def __init__(self, processed_data: Dict, business_goals: Optional[List[str]] = None):
        """
        Initialize recommendation engine.

        Args:
            processed_data: dict - All processed data from uploaded Excel
            business_goals: list - User-selected business objectives
        """
        self.data = processed_data
        self.goals = business_goals or ['acquisition', 'conversion']
        self.current_state = None
        self.industry_context = None

    def analyze_current_state(self) -> Dict:
        """
        Analyze current performance from uploaded data.

        Returns:
            dict with:
            - strengths: List of what's working well
            - weaknesses: List of gaps/issues
            - opportunities: Data-driven opportunities
        """
        strengths = []
        weaknesses = []
        opportunities = []

        # Analyze tactics data
        tactics_data = self.data.get('tactics', [])
        if tactics_data:
            tactics_df = pd.DataFrame(tactics_data)

            # Identify quick wins (low effort, high lift)
            if 'Total Effort' in tactics_df.columns and 'Expected Lift %' in tactics_df.columns:
                quick_wins = tactics_df[
                    (tactics_df['Total Effort'] < 10) &
                    (tactics_df['Expected Lift %'] > 0.005)
                ]
                if not quick_wins.empty:
                    opportunities.append({
                        'type': 'quick_wins',
                        'count': len(quick_wins),
                        'tactics': quick_wins['Marketing Tactic'].tolist() if 'Marketing Tactic' in quick_wins.columns else []
                    })

        # Analyze web vitals
        web_vitals = self.data.get('web_vitals', [])
        if web_vitals:
            vitals_df = pd.DataFrame(web_vitals)

            # Check performance scores
            if 'Performance' in vitals_df.columns:
                avg_performance = vitals_df['Performance'].mean()
                if avg_performance < 70:
                    weaknesses.append({
                        'type': 'performance',
                        'score': avg_performance,
                        'message': f'Performance score ({avg_performance:.0f}/100) needs improvement'
                    })
                elif avg_performance > 85:
                    strengths.append({
                        'type': 'performance',
                        'score': avg_performance,
                        'message': f'Strong performance score ({avg_performance:.0f}/100)'
                    })

            # Check SEO scores
            if 'SEO' in vitals_df.columns:
                avg_seo = vitals_df['SEO'].mean()
                if avg_seo < 85:
                    weaknesses.append({
                        'type': 'seo',
                        'score': avg_seo,
                        'message': f'SEO score ({avg_seo:.0f}/100) below industry standard'
                    })
                elif avg_seo > 92:
                    strengths.append({
                        'type': 'seo',
                        'score': avg_seo,
                        'message': f'Excellent SEO score ({avg_seo:.0f}/100)'
                    })

        # Analyze traffic data
        traffic_data = self.data.get('traffic_data', [])
        if traffic_data:
            traffic_df = pd.DataFrame(traffic_data)
            if 'YoY Growth %' in traffic_df.columns:
                # Check for growth trends
                avg_growth = traffic_df['YoY Growth %'].mean()
                if avg_growth < 0:
                    weaknesses.append({
                        'type': 'traffic_decline',
                        'growth': avg_growth,
                        'message': f'Negative traffic growth ({avg_growth:.1f}%)'
                    })
                elif avg_growth > 20:
                    strengths.append({
                        'type': 'traffic_growth',
                        'growth': avg_growth,
                        'message': f'Strong traffic growth ({avg_growth:.1f}%)'
                    })

        self.current_state = {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'opportunities': opportunities
        }

        return self.current_state

    def research_industry_context(self, company_name: str, industry: str) -> Dict:
        """
        Use web search to find current best practices and trends.

        Args:
            company_name: str - Company being analyzed
            industry: str - Industry/vertical (e.g., "beauty ecommerce")

        Returns:
            dict with:
            - trends: Current industry marketing trends
            - best_practices: What competitors are doing
            - benchmarks: Industry performance standards
        """
        # Placeholder for web search integration
        # In production, this would use WebSearch tool
        trends = [
            "AI-powered personalization increasing conversions by 15-20%",
            "Short-form video content driving 3x engagement",
            "Voice search optimization becoming critical for discovery",
            "First-party data collection essential post-cookie deprecation"
        ]

        best_practices = [
            "Implement schema markup for rich snippets",
            "Optimize for Core Web Vitals (especially LCP and CLS)",
            "Use progressive web app (PWA) features for mobile",
            "Implement A/B testing for all major page changes",
            "Leverage user-generated content for social proof"
        ]

        benchmarks = {
            'avg_conversion_rate': 2.5,
            'avg_bounce_rate': 45.0,
            'avg_session_duration': 180,  # seconds
            'avg_seo_score': 85,
            'avg_performance_score': 75
        }

        self.industry_context = {
            'trends': trends,
            'best_practices': best_practices,
            'benchmarks': benchmarks
        }

        return self.industry_context

    def generate_recommendations(self) -> List[Dict]:
        """
        Generate prioritized tactics recommendations.

        Returns:
            list of dicts with recommendation details
        """
        if not self.current_state:
            self.analyze_current_state()

        if not self.industry_context:
            self.research_industry_context('Company', 'ecommerce')

        recommendations = []

        # Get tactics data
        tactics_data = self.data.get('tactics', [])
        if tactics_data:
            tactics_df = pd.DataFrame(tactics_data)

            # Generate recommendations from tactics data
            for idx, row in tactics_df.iterrows():
                if idx >= 10:  # Limit to top 10 recommendations
                    break

                tactic_name = row.get('Marketing Tactic', row.get('Tactics', f'Tactic {idx+1}'))
                effort = row.get('Total Effort', 5)
                lift = row.get('Expected Lift %', 0.05) * 100
                cost = row.get('Projected Cost', 5000)
                funnel_stage = row.get('Focus (Funnel Stage)', 'Unknown')
                priority_score = row.get('Priority Score', 1.0)

                # Determine priority based on score
                if priority_score > 2.0:
                    priority = 'Critical'
                elif priority_score > 1.0:
                    priority = 'High'
                elif priority_score > 0.5:
                    priority = 'Medium'
                else:
                    priority = 'Low'

                # Generate rationale based on current state and goals
                rationale = self._generate_rationale(tactic_name, funnel_stage, effort, lift)

                # Estimate timeline based on effort
                if effort < 5:
                    timeline = '1-2 weeks'
                elif effort < 10:
                    timeline = '3-4 weeks'
                elif effort < 15:
                    timeline = '2-3 months'
                else:
                    timeline = '3-6 months'

                # Determine KPIs based on funnel stage
                kpis = self._get_kpis_for_stage(funnel_stage)

                # Get industry context
                industry_note = self._get_industry_context_note(tactic_name)

                recommendation = {
                    'tactic': tactic_name,
                    'funnel_stage': funnel_stage,
                    'priority': priority,
                    'rationale': rationale,
                    'effort': int(effort),
                    'lift': f'{lift:.0f}%',
                    'timeline': timeline,
                    'dependencies': [],
                    'kpis': kpis,
                    'industry_context': industry_note,
                    'score': priority_score
                }

                recommendations.append(recommendation)

        # If no tactics data, generate recommendations from weaknesses
        if not recommendations:
            recommendations = self._generate_from_weaknesses()

        # Sort by score (descending)
        recommendations.sort(key=lambda x: x.get('score', 0), reverse=True)

        return recommendations

    def _generate_rationale(self, tactic: str, stage: str, effort: float, lift: float) -> str:
        """Generate compelling rationale for a tactic."""
        rationales = {
            'low_effort_high_lift': f'Quick win opportunity with {lift:.0f}% expected lift and only {effort:.0f}/20 effort required.',
            'addresses_weakness': f'Directly addresses current performance gap. ',
            'goal_aligned': f'Aligns with your {stage.lower()} goals. ',
            'industry_validated': 'Proven effective in your industry. '
        }

        # Build rationale based on characteristics
        rationale_parts = []

        if effort < 10 and lift > 8:
            rationale_parts.append(rationales['low_effort_high_lift'])
        else:
            rationale_parts.append(f'Expected {lift:.0f}% lift with moderate {effort:.0f}/20 effort.')

        # Check if addresses weakness
        if self.current_state:
            for weakness in self.current_state['weaknesses']:
                if weakness['type'] == 'seo' and 'seo' in tactic.lower():
                    rationale_parts.append(f"Your SEO score ({weakness['score']:.0f}/100) needs improvement. ")
                elif weakness['type'] == 'performance' and 'performance' in tactic.lower():
                    rationale_parts.append(f"Performance score ({weakness['score']:.0f}/100) below benchmark. ")

        # Check goal alignment
        if stage.lower() in [g.replace('_', ' ') for g in self.goals]:
            rationale_parts.append(rationales['goal_aligned'])

        return ' '.join(rationale_parts).strip()

    def _get_kpis_for_stage(self, stage: str) -> List[str]:
        """Get relevant KPIs for funnel stage."""
        kpi_map = {
            'Acquisition': ['Organic traffic', 'Click-through rate', 'New visitors'],
            'Conversion': ['Conversion rate', 'Lead generation', 'Form submissions'],
            'LTV': ['Customer lifetime value', 'Repeat purchase rate', 'Average order value'],
            'User Experience': ['Bounce rate', 'Session duration', 'Page speed'],
            'Unknown': ['Traffic', 'Engagement', 'Conversions']
        }
        return kpi_map.get(stage, kpi_map['Unknown'])

    def _get_industry_context_note(self, tactic: str) -> str:
        """Get industry context note for tactic."""
        if not self.industry_context:
            return 'Recommended based on data analysis'

        # Match tactic keywords to best practices
        tactic_lower = tactic.lower()
        for practice in self.industry_context['best_practices']:
            if any(keyword in tactic_lower for keyword in practice.lower().split()):
                return f'Industry best practice: {practice[:60]}...' if len(practice) > 60 else f'Industry best practice: {practice}'

        # Match to trends
        for trend in self.industry_context['trends']:
            if any(keyword in tactic_lower for keyword in trend.lower().split()[:3]):
                return f'Trending: {trend[:60]}...' if len(trend) > 60 else f'Trending: {trend}'

        return 'Data-driven recommendation based on your metrics'

    def _generate_from_weaknesses(self) -> List[Dict]:
        """Generate recommendations when no tactics data available."""
        recommendations = []

        if not self.current_state:
            return []

        # Generate recommendations for each weakness
        for weakness in self.current_state['weaknesses']:
            if weakness['type'] == 'seo':
                recommendations.append({
                    'tactic': 'Implement Technical SEO Improvements',
                    'funnel_stage': 'Acquisition',
                    'priority': 'High',
                    'rationale': f"Your SEO score ({weakness['score']:.0f}/100) is below industry standard. Focus on technical optimizations.",
                    'effort': 5,
                    'lift': '15-20%',
                    'timeline': '4-6 weeks',
                    'dependencies': [],
                    'kpis': ['Organic traffic', 'Search rankings', 'Click-through rate'],
                    'industry_context': 'Technical SEO is foundation for visibility',
                    'score': 2.5
                })
            elif weakness['type'] == 'performance':
                recommendations.append({
                    'tactic': 'Optimize Core Web Vitals',
                    'funnel_stage': 'User Experience',
                    'priority': 'Critical',
                    'rationale': f"Performance score ({weakness['score']:.0f}/100) impacts user experience and SEO rankings.",
                    'effort': 8,
                    'lift': '12-18%',
                    'timeline': '2-3 months',
                    'dependencies': [],
                    'kpis': ['Page speed', 'Bounce rate', 'Conversion rate'],
                    'industry_context': 'Page speed directly correlates with conversion rate',
                    'score': 2.2
                })

        return recommendations

    def create_implementation_roadmap(self, recommendations: List[Dict], timeframe: str = '6 months') -> Dict:
        """
        Sequence recommendations into phased roadmap.

        Args:
            recommendations: list - Generated recommendations
            timeframe: str - Planning horizon

        Returns:
            dict with phases
        """
        if not recommendations:
            return {}

        # Group recommendations by priority and effort
        quick_wins = [r for r in recommendations if r['effort'] < 10 and r['priority'] in ['Critical', 'High']]
        major_projects = [r for r in recommendations if r['effort'] >= 10 and r['priority'] in ['Critical', 'High']]
        strategic = [r for r in recommendations if r['priority'] == 'Medium']

        roadmap = {}

        # Phase 1: Quick wins (Month 1-2)
        if quick_wins:
            roadmap['Phase 1 (Month 1-2): Quick Wins'] = quick_wins[:3]

        # Phase 2: Major projects start (Month 3-4)
        if major_projects:
            roadmap['Phase 2 (Month 3-4): Major Initiatives'] = major_projects[:2]

        # Phase 3: Strategic & optimization (Month 5-6)
        if strategic:
            roadmap['Phase 3 (Month 5-6): Strategic Optimization'] = strategic[:2]

        return roadmap

    def generate_executive_insights(self) -> List[Dict]:
        """
        Generate dynamic insights for Executive Summary page.

        Returns:
            list of dicts with insight icon, title, description, and color
        """
        insights = []

        if not self.current_state:
            self.analyze_current_state()

        strengths = self.current_state.get('strengths', [])
        weaknesses = self.current_state.get('weaknesses', [])
        opportunities = self.current_state.get('opportunities', [])

        # Add strength-based insight
        if strengths:
            strength_messages = []
            for strength in strengths[:2]:
                if isinstance(strength, dict):
                    strength_messages.append(strength.get('message', ''))
                else:
                    strength_messages.append(str(strength))

            if strength_messages:
                insights.append({
                    'icon': '✅',
                    'title': 'Strong Foundation',
                    'description': ' '.join(strength_messages),
                    'color': '#667eea'
                })

        # Add opportunity-based insight
        if opportunities:
            opp_messages = []
            for opp in opportunities[:2]:
                if isinstance(opp, dict):
                    if 'type' == 'quick_wins':
                        opp_messages.append(f"Identified {opp.get('count', 0)} quick-win tactics with low effort and high impact")
                    else:
                        opp_messages.append(opp.get('message', ''))
                else:
                    opp_messages.append(str(opp))

            if opp_messages:
                insights.append({
                    'icon': '🎯',
                    'title': 'Growth Opportunities',
                    'description': ' '.join(opp_messages),
                    'color': '#2ecc71'
                })

        # Add challenge/weakness insight
        if weaknesses:
            weakness_messages = []
            for weakness in weaknesses[:2]:
                if isinstance(weakness, dict):
                    weakness_messages.append(weakness.get('message', ''))
                else:
                    weakness_messages.append(str(weakness))

            if weakness_messages:
                insights.append({
                    'icon': '⚠️',
                    'title': 'Areas for Improvement',
                    'description': ' '.join(weakness_messages),
                    'color': '#f39c12'
                })

        # Add data-driven metrics insight
        tactics_data = self.data.get('tactics', [])
        keywords_data = self.data.get('keywords_organic', [])

        if tactics_data or keywords_data:
            metric_parts = []

            if tactics_data:
                tactics_df = pd.DataFrame(tactics_data) if isinstance(tactics_data, list) else tactics_data
                if not tactics_df.empty:
                    metric_parts.append(f"{len(tactics_df)} marketing tactics analyzed")

            if keywords_data:
                kw_df = pd.DataFrame(keywords_data) if isinstance(keywords_data, list) else keywords_data
                if not kw_df.empty:
                    metric_parts.append(f"{len(kw_df)} keywords tracked")

            if metric_parts:
                insights.append({
                    'icon': '📊',
                    'title': 'Data Overview',
                    'description': ', '.join(metric_parts) + '. AI-powered analysis completed to identify high-impact opportunities.',
                    'color': '#3498db'
                })

        # If no insights generated, add a default one
        if not insights:
            insights.append({
                'icon': '📈',
                'title': 'Marketing Performance Analysis',
                'description': 'Your data has been analyzed. Review detailed channel performance in the navigation tabs above to see specific metrics and recommendations.',
                'color': '#667eea'
            })

        return insights[:4]  # Return top 4 insights
