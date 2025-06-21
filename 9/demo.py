#!/usr/bin/env python3
"""
Demonstration script for the Service Analysis Console Application

This script showcases all the capabilities of the application
by running various examples and generating sample reports.
"""

import os
import sys
from datetime import datetime


def run_demo():
    """Run a comprehensive demonstration of the application."""
    print("🚀 Service Analysis Console Application - Demo")
    print("=" * 60)
    print()
    
    # Demo 1: Known service analysis
    print("📊 Demo 1: Analyzing Known Service (Spotify)")
    print("-" * 40)
    os.system('python main.py --service "Spotify" --output demo_spotify.md')
    print("✅ Spotify analysis completed and saved to demo_spotify.md")
    print()
    
    # Demo 2: Service description analysis
    print("📝 Demo 2: Analyzing Service Description")
    print("-" * 40)
    description = "A video conferencing platform that enables remote meetings and webinars"
    os.system(f'python main.py --text "{description}" --output demo_videoconf.md')
    print("✅ Video conferencing analysis completed and saved to demo_videoconf.md")
    print()
    
    # Demo 3: Another known service
    print("📋 Demo 3: Analyzing Another Known Service (GitHub)")
    print("-" * 40)
    os.system('python main.py --service "GitHub" --output demo_github.md')
    print("✅ GitHub analysis completed and saved to demo_github.md")
    print()
    
    # Demo 4: Console output
    print("🖥️  Demo 4: Console Output (Slack)")
    print("-" * 40)
    print("Running: python main.py --service 'Slack'")
    print()
    os.system('python main.py --service "Slack"')
    print()
    
    # Summary
    print("📈 Demo Summary")
    print("=" * 60)
    print("Generated reports:")
    print("  • demo_spotify.md - Spotify analysis")
    print("  • demo_videoconf.md - Video conferencing analysis")
    print("  • demo_github.md - GitHub analysis")
    print("  • Console output - Slack analysis")
    print()
    print("🎯 Key Features Demonstrated:")
    print("  ✅ Known service analysis")
    print("  ✅ Service description analysis")
    print("  ✅ File output capability")
    print("  ✅ Console output capability")
    print("  ✅ Comprehensive report structure")
    print()
    print("📋 Report Sections Included:")
    sections = [
        "Executive Summary", "Brief History", "Target Audience",
        "Core Features", "Unique Selling Points", "Business Model",
        "Tech Stack Insights", "Perceived Strengths", "Perceived Weaknesses",
        "Market Analysis", "Strategic Recommendations"
    ]
    for i, section in enumerate(sections, 1):
        print(f"  {i:2d}. {section}")
    print()
    print("🎉 Demo completed successfully!")
    print()
    print("💡 Try your own analysis:")
    print("  python main.py --service \"YourService\"")
    print("  python main.py --text \"Your service description\"")
    print("  python main.py --help")


if __name__ == "__main__":
    run_demo() 