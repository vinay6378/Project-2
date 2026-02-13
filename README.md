# Career Progression and Promotion Gap Analysis for Retention Optimization

## Project Overview

This comprehensive data science project analyzes career progression patterns and promotion gaps at Palo Alto Networks to identify retention opportunities and optimize talent management strategies. Unlike traditional attrition models that predict who might leave, this analysis explains why employees may eventually disengage by uncovering promotion gaps and career stagnation patterns.

## 🎯 Project Objectives

- Develop a data-driven view of career progression patterns
- Identify employees experiencing promotion stagnation
- Provide early signals of retention opportunities before disengagement
- Enable targeted, personalized retention interventions
- Transform from reactive to proactive career-centric workforce management

## 📊 Dataset

- **Source:** Palo Alto Networks Employee Records
- **Size:** 1,470 employees, 31 features
- **Key Features:** Demographics, career progression, compensation, satisfaction metrics, behavioral indicators

## 🔬 Methodology

### Feature Engineering
Created 7 key career progression metrics:
1. **Promotion Gap Ratio** = YearsSinceLastPromotion / YearsAtCompany
2. **Role Stagnation Index** = YearsInCurrentRole / YearsAtCompany
3. **Training Intensity Score** = TrainingTimesLastYear / YearsAtCompany
4. **Manager Stability Indicator** = YearsWithCurrManager / YearsAtCompany
5. **Career Velocity Score** = JobLevel / YearsAtCompany
6. **Income Growth Potential** = MonthlyIncome / (YearsAtCompany + 1)
7. **Experience Utilization** = TotalWorkingYears / Age

### Clustering Analysis
- **Algorithm:** K-Means clustering (optimal k=3, silhouette score: 0.180)
- **Validation:** Hierarchical clustering for cluster validation
- **Clusters Identified:** Fast-Track Performers, Promotion-Stalled Employees, Early-Career Explorers

### Risk Scoring System
- **High Risk:** Score ≥ 7 points (7.5% of employees)
- **Medium Risk:** Score 4-6 points (40.1% of employees)
- **Low Risk:** Score ≤ 3 points (52.4% of employees)

## 📈 Key Findings

### Career Clusters
- **Fast-Track Performers:** 61.7% of employees, moderate attrition risk (19.1%)
- **Promotion-Stalled Employees:** 35.4% of employees, low immediate risk but high long-term risk (9.4%)
- **Early-Career Explorers:** 2.9% of employees, high attrition risk (34.9%)

### Retention Opportunities
- **224 employees** (15.2% of workforce) identified for career intervention
- **47 high-priority employees** requiring immediate action
- **156 employees** need training programs
- **89 employees** ready for promotion review
- **67 employees** need role rotation

### Business Impact
- **Potential savings:** $2.2M - $2.9M in replacement costs
- **ROI:** 300-400% on intervention investments
- **Productivity improvement:** 15-20% expected

## 🛠️ Project Structure

```
Second Project/
├── Palo Alto Networks.csv          # Original dataset
├── career_progression_analysis.py  # Main analysis script
├── streamlit_dashboard.py          # Interactive dashboard
├── requirements.txt                # Python dependencies
├── research_paper.md               # Comprehensive research paper
├── executive_summary.md            # Executive summary for stakeholders
├── README.md                       # This file
├── career_progression_results.csv  # Analysis results
├── cluster_analysis.csv            # Cluster analysis results
├── retention_opportunities.csv    # Retention opportunities
└── cluster_analysis.png            # Cluster optimization visualization
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone or download the project files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis:**
   ```bash
   python career_progression_analysis.py
   ```

4. **Launch the dashboard:**
   ```bash
   streamlit run streamlit_dashboard.py
   ```

### Dependencies

- pandas==2.1.4
- numpy==1.24.3
- scikit-learn==1.3.2
- matplotlib==3.7.1
- seaborn==0.12.2
- plotly==5.17.0
- streamlit==1.29.0
- scipy==1.11.4
- joblib==1.3.2

## 📱 Dashboard Features

### Career Path Clustering Dashboard
- Cluster distribution visualization
- Career pattern summaries
- Cluster comparison analysis
- Interactive cluster explorer

### Promotion Gap Monitor
- Risk distribution charts
- High-risk employee identification
- Role-level stagnation insights
- Adjustable promotion gap thresholds

### Retention Opportunity Panel
- Employees needing career intervention
- Suggested actions (training, rotation, promotion review)
- Priority-based employee recommendations
- Detailed intervention strategies

### Managerial Insight Dashboard
- Manager tenure vs career growth analysis
- Team-level stagnation signals
- Manager effectiveness metrics
- Leadership recommendations

### Interactive Filters
- Department and role selection
- Career stage filtering
- Promotion gap risk level selector
- Real-time data updates

## 📋 Key Deliverables

1. **Research Paper** (`research_paper.md`)
   - Comprehensive EDA and methodology
   - Detailed findings and insights
   - Business impact analysis
   - Strategic recommendations

2. **Streamlit Dashboard** (`streamlit_dashboard.py`)
   - Live analytics interface
   - Interactive visualizations
   - Real-time filtering capabilities
   - Export functionality

3. **Executive Summary** (`executive_summary.md`)
   - High-level insights for stakeholders
   - Business case and ROI analysis
   - Implementation roadmap
   - Success metrics

4. **Analysis Results** (CSV files)
   - Complete dataset with engineered features
   - Cluster assignments and analysis
   - Retention opportunity identification
   - Risk scoring results

## 🎯 Business Applications

### HR & Talent Management
- Proactive retention strategies
- Career path planning
- Promotion readiness assessment
- Training program optimization

### Leadership Development
- Manager effectiveness monitoring
- Team composition optimization
- Succession planning
- Leadership training needs

### Strategic Workforce Planning
- Talent risk assessment
- Workforce composition analysis
- Skills gap identification
- Organizational design insights

## 📊 Key Performance Indicators

### Career Intelligence KPIs
- **Career Cluster Distribution:** Employee career trajectory types
- **Promotion Gap Score:** Risk of stagnation assessment
- **Retention Opportunity Index:** Intervention priority scoring
- **Training Need Indicator:** Development planning metrics
- **Manager Stability Impact:** Leadership effectiveness insights

### Success Metrics
- **Attrition Reduction:** 15-20% decrease in voluntary turnover
- **Satisfaction Improvement:** 20-25% increase in employee satisfaction
- **Career Velocity:** 25% improvement in advancement speed
- **ROI Achievement:** 300-400% return on investments

## 🔧 Technical Implementation

### Data Processing Pipeline
1. **Data Loading & Exploration**
2. **Feature Engineering** (7 career metrics)
3. **Data Preprocessing** (normalization, encoding, outlier handling)
4. **Clustering Analysis** (K-means with optimal k determination)
5. **Risk Scoring** (multi-factor risk assessment)
6. **Opportunity Identification** (retervention candidate selection)

### Analytics Framework
- **Unsupervised Learning:** Career trajectory clustering
- **Risk Modeling:** Multi-factor promotion gap scoring
- **Opportunity Analysis:** Retention intervention identification
- **Visualization:** Interactive dashboard with real-time analytics

## 🚀 Future Enhancements

### Advanced Analytics
- Predictive attrition modeling
- Machine learning for career path optimization
- Natural language processing for career sentiment analysis
- Network analysis for career mobility patterns

### Integration Opportunities
- HRIS system integration
- Learning management system connectivity
- Performance management system alignment
- Compensation planning integration

### Scalability Considerations
- Real-time data processing
- Automated risk alerting
- Mobile application development
- API development for system integration

## 📞 Contact

**Project Lead:** Vinay Sharma, Data Science Intern  
**Program:** Unified Mentor  
**Date:** February 2026  
**Dataset:** Palo Alto Networks Employee Records

## 📄 License

This project is for educational and demonstration purposes as part of the Unified Mentor Data Science Internship program.

## 🙏 Acknowledgments

- Unified Mentor for the internship opportunity and guidance
- Palo Alto Networks for providing the dataset
- Data science community for inspiration and best practices

---

**Note:** This project demonstrates the application of data science techniques to solve real-world business challenges in talent management and employee retention.
