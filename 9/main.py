#!/usr/bin/env python3
"""
Service Analysis Console Application

A lightweight console application that generates comprehensive markdown reports
for services or products from multiple viewpoints including business, technical,
and user-focused perspectives.
"""

import argparse
import sys
import os
from typing import Optional
from service_analyzer import ServiceAnalyzer
from report_generator import ReportGenerator


def main():
    """Main entry point for the console application."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive service analysis reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --service "Spotify"
  python main.py --text "A music streaming service that allows users to listen to millions of songs"
  python main.py --service "Notion" --output report.md
  python main.py --text "A productivity app for notes and collaboration" --output analysis.md
        """
    )
    
    parser.add_argument(
        "--service", "-s",
        type=str,
        help="Name of a known service (e.g., 'Spotify', 'Notion')"
    )
    
    parser.add_argument(
        "--text", "-t",
        type=str,
        help="Raw service description text"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path for the markdown report (default: prints to console)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not args.service and not args.text:
        print("Error: You must provide either --service or --text")
        parser.print_help()
        sys.exit(1)
    
    if args.service and args.text:
        print("Error: Please provide either --service OR --text, not both")
        sys.exit(1)
    
    try:
        # Initialize the service analyzer
        analyzer = ServiceAnalyzer()
        
        # Get input data
        if args.service:
            input_data = args.service
            input_type = "service_name"
        else:
            input_data = args.text
            input_type = "description"
        
        if args.verbose:
            print(f"Analyzing {input_type}: {input_data}")
        
        # Generate the report
        report_generator = ReportGenerator()
        report = report_generator.generate_report(input_data, input_type)
        
        # Output the report
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {args.output}")
        else:
            print("\n" + "="*80)
            print("SERVICE ANALYSIS REPORT")
            print("="*80)
            print(report)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 