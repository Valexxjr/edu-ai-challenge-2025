"""
Service Analyzer Module

Handles AI-powered analysis of services and products, including
information extraction and synthesis for comprehensive reports.
"""

import json
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import os
import openai


@dataclass
class ServiceInfo:
    """Data structure for service information."""
    name: str
    description: str
    founding_year: Optional[str] = None
    target_audience: List[str] = None
    core_features: List[str] = None
    unique_selling_points: List[str] = None
    business_model: Optional[str] = None
    tech_stack: List[str] = None
    strengths: List[str] = None
    weaknesses: List[str] = None
    
    def __post_init__(self):
        if self.target_audience is None:
            self.target_audience = []
        if self.core_features is None:
            self.core_features = []
        if self.unique_selling_points is None:
            self.unique_selling_points = []
        if self.tech_stack is None:
            self.tech_stack = []
        if self.strengths is None:
            self.strengths = []
        if self.weaknesses is None:
            self.weaknesses = []


class ServiceAnalyzer:
    """Main service analyzer class that handles AI-powered analysis."""
    
    def __init__(self):
        """Initialize the service analyzer."""
        self.known_services = self._load_known_services()
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if self.openai_api_key:
            print(f"OpenAI API key detected: {self.openai_api_key[:10]}...")
            openai.api_key = self.openai_api_key
        else:
            print("No OpenAI API key found. Using rule-based analysis.")
    
    def _load_known_services(self) -> Dict[str, Dict[str, Any]]:
        """Load known service information from a database."""
        return {
            "spotify": {
                "name": "Spotify",
                "description": "A digital music streaming service that provides access to millions of songs, podcasts, and videos from artists all around the world.",
                "founding_year": "2006",
                "target_audience": ["Music enthusiasts", "Young adults", "Students", "Professionals"],
                "core_features": ["Music streaming", "Playlist creation", "Podcast streaming", "Offline listening"],
                "unique_selling_points": ["Extensive music library", "Personalized recommendations", "Free tier available", "Cross-platform compatibility"],
                "business_model": "Freemium model with premium subscriptions and advertising",
                "tech_stack": ["Python", "Java", "React", "PostgreSQL", "AWS"],
                "strengths": ["Huge music library", "Excellent recommendation algorithm", "User-friendly interface", "Strong brand recognition"],
                "weaknesses": ["Artist compensation concerns", "Limited high-fidelity audio", "Regional content restrictions"]
            },
            "notion": {
                "name": "Notion",
                "description": "An all-in-one workspace for notes, docs, project management, and collaboration.",
                "founding_year": "2013",
                "target_audience": ["Teams and organizations", "Students", "Knowledge workers", "Project managers"],
                "core_features": ["Note-taking", "Database creation", "Project management", "Team collaboration"],
                "unique_selling_points": ["Highly customizable", "All-in-one workspace", "Powerful database features", "Beautiful templates"],
                "business_model": "Freemium model with team and enterprise plans",
                "tech_stack": ["React", "Node.js", "TypeScript", "PostgreSQL", "AWS"],
                "strengths": ["Extremely flexible", "Beautiful design", "Powerful database features", "Great for teams"],
                "weaknesses": ["Steep learning curve", "Can be overwhelming", "Limited offline functionality", "Performance issues with large workspaces"]
            },
            "slack": {
                "name": "Slack",
                "description": "A messaging app for business that connects people to the information they need.",
                "founding_year": "2013",
                "target_audience": ["Business teams", "Remote workers", "Project teams", "Organizations"],
                "core_features": ["Team messaging", "Channel organization", "File sharing", "Integrations"],
                "unique_selling_points": ["Real-time collaboration", "Extensive integrations", "Searchable history", "Mobile-first design"],
                "business_model": "Freemium model with paid plans for teams and enterprises",
                "tech_stack": ["JavaScript", "React", "Node.js", "PostgreSQL", "AWS"],
                "strengths": ["Excellent for team communication", "Rich integrations", "Good search functionality", "Mobile apps"],
                "weaknesses": ["Can be distracting", "Information overload", "Limited free tier", "Privacy concerns"]
            },
            "github": {
                "name": "GitHub",
                "description": "A platform for version control and collaboration that lets people work together on projects.",
                "founding_year": "2008",
                "target_audience": ["Developers", "Open source contributors", "Software teams", "Students"],
                "core_features": ["Git version control", "Code hosting", "Issue tracking", "Pull requests"],
                "unique_selling_points": ["Industry standard", "Large community", "Excellent documentation", "Free for open source"],
                "business_model": "Freemium model with paid plans for private repositories and teams",
                "tech_stack": ["Ruby on Rails", "JavaScript", "MySQL", "Redis", "Git"],
                "strengths": ["Industry standard", "Huge community", "Excellent documentation", "Reliable service"],
                "weaknesses": ["Limited free private repos", "Can be complex for beginners", "Occasional downtime", "Microsoft acquisition concerns"]
            }
        }
    
    def analyze_service_name(self, service_name: str) -> ServiceInfo:
        """Analyze a known service by name."""
        service_name_lower = service_name.lower().strip()
        
        # Try OpenAI API first if available
        if self.openai_api_key:
            print(f"Attempting OpenAI analysis for service: {service_name}")
            try:
                return self._analyze_with_openai(service_name, "service_name")
            except Exception as e:
                print(f"OpenAI API failed: {e}. Falling back to rule-based analysis.")
        
        if service_name_lower in self.known_services:
            service_data = self.known_services[service_name_lower]
            return ServiceInfo(
                name=service_data["name"],
                description=service_data["description"],
                founding_year=service_data["founding_year"],
                target_audience=service_data["target_audience"],
                core_features=service_data["core_features"],
                unique_selling_points=service_data["unique_selling_points"],
                business_model=service_data["business_model"],
                tech_stack=service_data["tech_stack"],
                strengths=service_data["strengths"],
                weaknesses=service_data["weaknesses"]
            )
        else:
            # For unknown services, generate a generic analysis
            return self._generate_generic_analysis(service_name)
    
    def analyze_description(self, description: str) -> ServiceInfo:
        """Analyze a service based on its description text."""
        # Try OpenAI API first if available
        if self.openai_api_key:
            try:
                return self._analyze_with_openai(description, "description")
            except Exception as e:
                print(f"OpenAI API failed: {e}. Falling back to rule-based analysis.")
        
        # Extract service name from description
        service_name = self._extract_service_name(description)
        
        # Generate analysis based on the description
        return self._analyze_description_text(service_name, description)
    
    def _extract_service_name(self, description: str) -> str:
        """Extract a potential service name from description text."""
        # Simple heuristic: look for capitalized words that might be service names
        words = description.split()
        for word in words:
            if word[0].isupper() and len(word) > 2:
                return word
        return "Unknown Service"
    
    def _generate_generic_analysis(self, service_name: str) -> ServiceInfo:
        """Generate a generic analysis for unknown services."""
        return ServiceInfo(
            name=service_name,
            description=f"Analysis of {service_name} based on available information.",
            founding_year="Unknown",
            target_audience=["General users", "Business customers"],
            core_features=["Core functionality", "User interface", "Data management"],
            unique_selling_points=["Competitive features", "User experience", "Market positioning"],
            business_model="Subscription or freemium model",
            tech_stack=["Modern web technologies", "Cloud infrastructure"],
            strengths=["Innovative approach", "User-friendly design", "Market potential"],
            weaknesses=["Limited information available", "Uncertain market position", "Competition risks"]
        )
    
    def _analyze_description_text(self, service_name: str, description: str) -> ServiceInfo:
        """Analyze service description text to extract insights."""
        # This would typically use AI/ML models for text analysis
        # For now, we'll use rule-based extraction
        
        # Extract potential features
        features = self._extract_features(description)
        
        # Extract potential audience
        audience = self._extract_audience(description)
        
        # Generate strengths and weaknesses based on description
        strengths, weaknesses = self._analyze_sentiment(description)
        
        return ServiceInfo(
            name=service_name,
            description=description,
            founding_year="Unknown",
            target_audience=audience,
            core_features=features,
            unique_selling_points=["Based on description analysis"],
            business_model="Likely subscription or freemium",
            tech_stack=["Modern web/mobile technologies"],
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _extract_features(self, description: str) -> List[str]:
        """Extract potential features from description text."""
        features = []
        
        # Look for common feature indicators
        feature_indicators = [
            "allows", "enables", "provides", "offers", "features", "includes",
            "supports", "lets", "can", "capable of", "designed to"
        ]
        
        sentences = description.split('.')
        for sentence in sentences:
            sentence = sentence.lower().strip()
            for indicator in feature_indicators:
                if indicator in sentence:
                    # Extract the feature description
                    parts = sentence.split(indicator)
                    if len(parts) > 1:
                        feature = parts[1].strip()
                        if feature and len(feature) > 5:
                            features.append(feature.capitalize())
        
        return features[:4] if features else ["Core functionality"]
    
    def _extract_audience(self, description: str) -> List[str]:
        """Extract potential target audience from description text."""
        audience = []
        
        # Common audience indicators
        audience_keywords = {
            "users": "General users",
            "business": "Business customers",
            "teams": "Teams and organizations",
            "developers": "Developers",
            "students": "Students",
            "professionals": "Professionals",
            "individuals": "Individual users",
            "organizations": "Organizations"
        }
        
        description_lower = description.lower()
        for keyword, audience_type in audience_keywords.items():
            if keyword in description_lower:
                audience.append(audience_type)
        
        return audience if audience else ["General users"]
    
    def _analyze_sentiment(self, description: str) -> tuple[List[str], List[str]]:
        """Analyze description for strengths and weaknesses."""
        strengths = []
        weaknesses = []
        
        # Positive indicators
        positive_words = ["innovative", "powerful", "excellent", "great", "amazing", "best", "leading", "popular"]
        # Negative indicators
        negative_words = ["limited", "basic", "simple", "restricted", "challenging", "difficult", "complex"]
        
        description_lower = description.lower()
        
        for word in positive_words:
            if word in description_lower:
                strengths.append(f"Positive mention of '{word}'")
        
        for word in negative_words:
            if word in description_lower:
                weaknesses.append(f"Potential limitation: '{word}'")
        
        if not strengths:
            strengths = ["Based on description analysis"]
        if not weaknesses:
            weaknesses = ["Limited information available"]
        
        return strengths, weaknesses
    
    def _analyze_with_openai(self, input_data: str, input_type: str) -> ServiceInfo:
        """Use OpenAI API to analyze the service or description and extract all required fields."""
        prompt = self._build_openai_prompt(input_data, input_type)
        
        # Use only gpt-4.1-mini
        model = "gpt-4.1-mini"
        
        try:
            print(f"Using model: {model}")
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a product analyst generating structured reports. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.4
            )
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from the response
            import json
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                data = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
            
            return ServiceInfo(
                name=data.get("name", "Unknown Service"),
                description=data.get("description", "No description provided."),
                founding_year=data.get("founding_year", "Unknown"),
                target_audience=data.get("target_audience", []),
                core_features=data.get("core_features", []),
                unique_selling_points=data.get("unique_selling_points", []),
                business_model=data.get("business_model", "Unknown"),
                tech_stack=data.get("tech_stack", []),
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", [])
            )
        except Exception as e:
            print(f"Model {model} failed: {e}")
            raise
    
    def _build_openai_prompt(self, input_data: str, input_type: str) -> str:
        """Builds a prompt for OpenAI to extract all required report fields as JSON."""
        if input_type == "service_name":
            intro = f"Analyze the digital service named '{input_data}'."
        else:
            intro = f"Analyze the following digital service description: '{input_data}'."
        
        prompt = f"""
{intro}

Extract comprehensive information and return it as a JSON object with exactly these fields:

{{
    "name": "Service name",
    "description": "Brief description of the service",
    "founding_year": "Year founded (if known, otherwise 'Unknown')",
    "target_audience": ["List", "of", "primary", "user", "segments"],
    "core_features": ["List", "of", "top", "2-4", "key", "functionalities"],
    "unique_selling_points": ["List", "of", "key", "differentiators"],
    "business_model": "How the service makes money",
    "tech_stack": ["List", "of", "technologies", "used"],
    "strengths": ["List", "of", "perceived", "strengths"],
    "weaknesses": ["List", "of", "perceived", "weaknesses"]
}}

Provide realistic, well-researched information. If information is not available, use reasonable estimates based on similar services.
"""
        return prompt 