#!/usr/bin/env python3
"""
Simple test script for the Service Analysis Console Application
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from service_analyzer import ServiceAnalyzer
from report_generator import ReportGenerator


def test_known_service():
    """Test analysis of a known service."""
    print("Testing known service analysis...")
    
    analyzer = ServiceAnalyzer()
    service_info = analyzer.analyze_service_name("Spotify")
    
    assert service_info.name == "Spotify"
    assert service_info.founding_year == "2006"
    assert len(service_info.core_features) > 0
    
    print("✅ Known service analysis test passed")


def test_description_analysis():
    """Test analysis of service description."""
    print("Testing description analysis...")
    
    analyzer = ServiceAnalyzer()
    description = "A music streaming service that allows users to listen to millions of songs"
    service_info = analyzer.analyze_description(description)
    
    assert service_info.name is not None
    assert len(service_info.description) > 0
    
    print("✅ Description analysis test passed")


def test_report_generation():
    """Test report generation."""
    print("Testing report generation...")
    
    generator = ReportGenerator()
    report = generator.generate_report("Spotify", "service_name")
    
    assert "# Spotify - Comprehensive Service Analysis" in report
    assert "## 📋 Executive Summary" in report
    assert "## 📅 Brief History" in report
    assert "## 🎯 Target Audience" in report
    assert "## ⚡ Core Features" in report
    assert "## 🌟 Unique Selling Points" in report
    assert "## 💼 Business Model" in report
    assert "## 🔧 Tech Stack Insights" in report
    assert "## ✅ Perceived Strengths" in report
    assert "## ⚠️ Perceived Weaknesses" in report
    
    print("✅ Report generation test passed")


def test_unknown_service():
    """Test analysis of unknown service."""
    print("Testing unknown service analysis...")
    
    analyzer = ServiceAnalyzer()
    service_info = analyzer.analyze_service_name("UnknownService123")
    
    assert service_info.name == "UnknownService123"
    assert service_info.founding_year == "Unknown"
    
    print("✅ Unknown service analysis test passed")


def main():
    """Run all tests."""
    print("🧪 Running Service Analysis Application Tests")
    print("=" * 50)
    
    try:
        test_known_service()
        test_description_analysis()
        test_report_generation()
        test_unknown_service()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed successfully!")
        print("\nYou can now run the application with:")
        print("  python main.py --service \"Spotify\"")
        print("  python main.py --text \"A productivity app for teams\"")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 