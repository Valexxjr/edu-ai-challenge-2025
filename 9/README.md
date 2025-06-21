# Service Analysis Console Application

A lightweight console application that generates comprehensive markdown-formatted reports for services or products from multiple viewpoints—including business, technical, and user-focused perspectives.

## 🎯 Overview

This application simulates a real-world scenario where product managers, investors, or prospective users want quick, structured insights about a digital service. It uses intelligent analysis to extract and synthesize relevant information from provided text or known service names.

## ✨ Features

- **Dual Input Support**: Accept either known service names or raw service descriptions
- **Comprehensive Analysis**: Generate reports covering 8 key areas:
  - Brief History & Milestones
  - Target Audience Analysis
  - Core Features Overview
  - Unique Selling Points
  - Business Model Insights
  - Tech Stack Analysis
  - Perceived Strengths
  - Perceived Weaknesses
- **Markdown Output**: Beautifully formatted reports for easy reading and sharing
- **Flexible Output**: Display in console or save to file
- **Extensible Design**: Easy to add new services and analysis capabilities

## 🚀 Quick Start

### Installation

1. Clone or download the application files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key as an environment variable** (required for AI-powered analysis):
   - On Windows (PowerShell):
     ```powershell
     $env:OPENAI_API_KEY="sk-...yourkey..."
     ```
   - On macOS/Linux:
     ```bash
     export OPENAI_API_KEY="sk-...yourkey..."
     ```
   - **Never store your API key in the code or repository!**

### Basic Usage

#### Analyze a Known Service
```bash
python main.py --service "Spotify"
```

#### Analyze Service Description
```bash
python main.py --text "A music streaming service that allows users to listen to millions of songs"
```

#### Save Report to File
```bash
python main.py --service "Notion" --output report.md
```

#### Verbose Output
```bash
python main.py --service "GitHub" --verbose
```

## 📋 Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--service` | `-s` | Name of a known service | `--service "Spotify"` |
| `--text` | `-t` | Raw service description | `--text "A productivity app"` |
| `--output` | `-o` | Output file path | `--output report.md` |
| `--verbose` | `-v` | Enable verbose output | `--verbose` |

## 📊 Supported Services

The application includes pre-analyzed data for popular services:

- **Spotify** - Music streaming service
- **Notion** - All-in-one workspace
- **Slack** - Team messaging platform
- **GitHub** - Code hosting and collaboration

For unknown services, the application generates intelligent analysis based on the provided description.

## 📄 Report Structure

Each generated report includes:

### 1. Executive Summary
Brief overview of the service and its purpose.

### 2. Brief History
Founding information and key milestones.

### 3. Target Audience
Primary user segments and demographics.

### 4. Core Features
Top 2-4 key functionalities and capabilities.

### 5. Unique Selling Points
Key differentiators and competitive advantages.

### 6. Business Model
Revenue strategies and monetization approaches.

### 7. Tech Stack Insights
Technology stack and architectural considerations.

### 8. Perceived Strengths
Positive attributes and standout features.

### 9. Perceived Weaknesses
Areas for improvement and potential limitations.

### 10. Market Analysis
Competitive landscape and growth opportunities.

### 11. Strategic Recommendations
Actionable insights for different stakeholders.

## 🔧 Architecture

The application is built with a modular architecture:

```
9/
├── main.py              # Main console application
├── service_analyzer.py  # Service analysis logic
├── report_generator.py  # Markdown report formatting
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Key Components

- **ServiceAnalyzer**: Handles service recognition and data extraction
- **ReportGenerator**: Formats analysis into comprehensive markdown reports
- **ServiceInfo**: Data structure for service information

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 🔮 Future Enhancements

- **AI Integration**: Connect to OpenAI or similar services for enhanced analysis
- **Web Scraping**: Automatically gather information from service websites
- **Real-time Data**: Fetch current market data and statistics
- **Interactive Mode**: Guided analysis with user prompts
- **Export Formats**: Support for PDF, HTML, and other formats
- **Database Integration**: Store and retrieve analysis history

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## 🆘 Support

For issues or questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## ⚠️ Security Note
- **Never commit your OpenAI API key to your repository!**
- Always use environment variables to keep your credentials safe.

---

*Built with ❤️ for comprehensive service analysis* 