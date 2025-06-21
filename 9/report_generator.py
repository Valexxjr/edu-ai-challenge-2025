"""
Report Generator Module

Generates comprehensive markdown-formatted reports from service analysis data,
including business, technical, and user-focused perspectives.
"""

from typing import Dict, List, Optional
from datetime import datetime
from service_analyzer import ServiceInfo


class ReportGenerator:
    """Generates comprehensive markdown reports from service analysis."""
    
    def __init__(self):
        """Initialize the report generator."""
        pass
    
    def generate_report(self, input_data: str, input_type: str) -> str:
        """Generate a comprehensive markdown report."""
        from service_analyzer import ServiceAnalyzer
        
        # Analyze the input
        analyzer = ServiceAnalyzer()
        
        if input_type == "service_name":
            service_info = analyzer.analyze_service_name(input_data)
        else:
            service_info = analyzer.analyze_description(input_data)
        
        # Generate the markdown report
        return self._format_report(service_info)
    
    def _format_report(self, service_info: ServiceInfo) -> str:
        """Format service information into a comprehensive markdown report."""
        report = []
        
        # Header
        report.append(f"# {service_info.name} - Comprehensive Service Analysis")
        report.append("")
        report.append(f"*Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")
        report.append("")
        report.append("---")
        report.append("")
        
        # Executive Summary
        report.append("## 📋 Executive Summary")
        report.append("")
        report.append(service_info.description)
        report.append("")
        
        # Brief History
        report.append("## 📅 Brief History")
        report.append("")
        if service_info.founding_year and service_info.founding_year != "Unknown":
            report.append(f"**Founded:** {service_info.founding_year}")
            report.append("")
            report.append("### Key Milestones")
            report.append("- Initial launch and market entry")
            report.append("- User base growth and expansion")
            report.append("- Feature development and platform evolution")
            report.append("- Market positioning and competitive response")
        else:
            report.append("*Historical information not available for this service.*")
        report.append("")
        
        # Target Audience
        report.append("## 🎯 Target Audience")
        report.append("")
        if service_info.target_audience:
            report.append("### Primary User Segments")
            for audience in service_info.target_audience:
                report.append(f"- **{audience}**")
            report.append("")
            report.append("### User Demographics")
            report.append("- Age range: 18-45 (primary)")
            report.append("- Tech-savvy individuals and professionals")
            report.append("- Both individual and organizational users")
        else:
            report.append("*Target audience information not available.*")
        report.append("")
        
        # Core Features
        report.append("## ⚡ Core Features")
        report.append("")
        if service_info.core_features:
            report.append("### Key Functionalities")
            for i, feature in enumerate(service_info.core_features, 1):
                report.append(f"{i}. **{feature}**")
            report.append("")
            report.append("### Feature Highlights")
            report.append("- User-friendly interface design")
            report.append("- Cross-platform compatibility")
            report.append("- Real-time synchronization")
            report.append("- Robust security measures")
        else:
            report.append("*Core features information not available.*")
        report.append("")
        
        # Unique Selling Points
        report.append("## 🌟 Unique Selling Points")
        report.append("")
        if service_info.unique_selling_points:
            report.append("### Key Differentiators")
            for usp in service_info.unique_selling_points:
                report.append(f"- {usp}")
        else:
            report.append("### Competitive Advantages")
            report.append("- Innovative approach to user needs")
            report.append("- Strong market positioning")
            report.append("- Quality user experience")
        report.append("")
        
        # Business Model
        report.append("## 💼 Business Model")
        report.append("")
        if service_info.business_model:
            report.append(f"**Revenue Strategy:** {service_info.business_model}")
            report.append("")
        else:
            report.append("**Revenue Strategy:** Subscription-based or freemium model")
            report.append("")
        
        report.append("### Revenue Streams")
        report.append("- **Subscription Plans:** Premium features and advanced capabilities")
        report.append("- **Freemium Model:** Basic features free, premium features paid")
        report.append("- **Enterprise Solutions:** Custom solutions for large organizations")
        report.append("- **Partnerships:** Strategic collaborations and integrations")
        report.append("")
        
        # Tech Stack Insights
        report.append("## 🔧 Tech Stack Insights")
        report.append("")
        if service_info.tech_stack:
            report.append("### Technology Stack")
            for tech in service_info.tech_stack:
                report.append(f"- **{tech}**")
            report.append("")
        else:
            report.append("### Technology Stack")
            report.append("- **Frontend:** Modern web frameworks (React, Vue, Angular)")
            report.append("- **Backend:** Scalable server technologies")
            report.append("- **Database:** Cloud-based data storage solutions")
            report.append("- **Infrastructure:** Cloud computing platforms")
            report.append("")
        
        report.append("### Technical Architecture")
        report.append("- **Scalability:** Cloud-native architecture")
        report.append("- **Security:** Enterprise-grade security measures")
        report.append("- **Performance:** Optimized for speed and reliability")
        report.append("- **Integration:** API-first approach for third-party connections")
        report.append("")
        
        # Perceived Strengths
        report.append("## ✅ Perceived Strengths")
        report.append("")
        if service_info.strengths:
            report.append("### Positive Attributes")
            for strength in service_info.strengths:
                report.append(f"- {strength}")
        else:
            report.append("### Positive Attributes")
            report.append("- Strong market presence")
            report.append("- User-friendly interface")
            report.append("- Reliable service delivery")
            report.append("- Continuous innovation")
        report.append("")
        
        # Perceived Weaknesses
        report.append("## ⚠️ Perceived Weaknesses")
        report.append("")
        if service_info.weaknesses:
            report.append("### Areas for Improvement")
            for weakness in service_info.weaknesses:
                report.append(f"- {weakness}")
        else:
            report.append("### Potential Limitations")
            report.append("- Market competition")
            report.append("- Feature complexity for new users")
            report.append("- Dependency on internet connectivity")
            report.append("- Data privacy concerns")
        report.append("")
        
        # Market Analysis
        report.append("## 📊 Market Analysis")
        report.append("")
        report.append("### Market Position")
        report.append("- **Competitive Landscape:** Operating in a dynamic, competitive market")
        report.append("- **Market Share:** Established presence with growth potential")
        report.append("- **Growth Trajectory:** Positive market adoption trends")
        report.append("")
        
        report.append("### Opportunities")
        report.append("- **Market Expansion:** Potential for geographic and demographic growth")
        report.append("- **Feature Development:** Continuous innovation opportunities")
        report.append("- **Partnerships:** Strategic collaboration possibilities")
        report.append("- **Technology Advancement:** Leveraging emerging technologies")
        report.append("")
        
        # Recommendations
        report.append("## 💡 Strategic Recommendations")
        report.append("")
        report.append("### For Users")
        report.append("- Evaluate feature requirements against available capabilities")
        report.append("- Consider integration needs with existing workflows")
        report.append("- Assess pricing plans for long-term value")
        report.append("- Review security and privacy policies")
        report.append("")
        
        report.append("### For Investors")
        report.append("- Strong market positioning with growth potential")
        report.append("- Established user base and revenue streams")
        report.append("- Technology-driven competitive advantages")
        report.append("- Scalable business model")
        report.append("")
        
        report.append("### For Competitors")
        report.append("- Focus on unique value propositions")
        report.append("- Invest in user experience and innovation")
        report.append("- Build strong community and ecosystem")
        report.append("- Maintain competitive pricing strategies")
        report.append("")
        
        # Footer
        report.append("---")
        report.append("")
        report.append("*This analysis is based on available information and market research. For the most current and detailed information, please refer to official sources and recent updates.*")
        report.append("")
        report.append(f"*Report generated by Service Analysis Tool - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(report)
    
    def _format_list(self, items: List[str], bullet: str = "-") -> List[str]:
        """Format a list of items with consistent bullet points."""
        return [f"{bullet} {item}" for item in items]
    
    def _format_table(self, headers: List[str], rows: List[List[str]]) -> List[str]:
        """Format data as a markdown table."""
        table = []
        
        # Header row
        table.append("| " + " | ".join(headers) + " |")
        
        # Separator row
        table.append("| " + " | ".join(["---"] * len(headers)) + " |")
        
        # Data rows
        for row in rows:
            table.append("| " + " | ".join(row) + " |")
        
        return table 