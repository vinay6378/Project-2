import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
import warnings
warnings.filterwarnings('ignore')

class CareerProgressionAnalyzer:
    def __init__(self, data_path):
        """Initialize the analyzer with dataset path"""
        self.data_path = data_path
        self.df = None
        self.processed_df = None
        self.scaler = StandardScaler()
        self.kmeans_model = None
        self.clusters = None
        
    def load_data(self):
        """Load and explore the dataset"""
        self.df = pd.read_csv(self.data_path)
        print(f"Dataset loaded with {self.df.shape[0]} employees and {self.df.shape[1]} features")
        print("\nDataset Info:")
        print(self.df.info())
        return self.df
    
    def feature_engineering(self):
        """Create derived career progression metrics"""
        df = self.df.copy()
        
        # Promotion Gap Ratio = YearsSinceLastPromotion / YearsAtCompany
        df['PromotionGapRatio'] = df['YearsSinceLastPromotion'] / (df['YearsAtCompany'] + 1e-6)
        
        # Role Stagnation Index = YearsInCurrentRole / YearsAtCompany
        df['RoleStagnationIndex'] = df['YearsInCurrentRole'] / (df['YearsAtCompany'] + 1e-6)
        
        # Training Intensity Score = TrainingTimesLastYear / YearsAtCompany
        df['TrainingIntensityScore'] = df['TrainingTimesLastYear'] / (df['YearsAtCompany'] + 1e-6)
        
        # Manager Stability Indicator = YearsWithCurrManager / YearsAtCompany
        df['ManagerStabilityIndicator'] = df['YearsWithCurrManager'] / (df['YearsAtCompany'] + 1e-6)
        
        # Career Velocity Score = JobLevel / YearsAtCompany
        df['CareerVelocityScore'] = df['JobLevel'] / (df['YearsAtCompany'] + 1e-6)
        
        # Income Growth Potential = MonthlyIncome / (YearsAtCompany + 1)
        df['IncomeGrowthPotential'] = df['MonthlyIncome'] / (df['YearsAtCompany'] + 1)
        
        # Experience Utilization = TotalWorkingYears / Age
        df['ExperienceUtilization'] = df['TotalWorkingYears'] / (df['Age'] + 1e-6)
        
        self.processed_df = df
        print("Feature engineering completed. New features created:")
        print(['PromotionGapRatio', 'RoleStagnationIndex', 'TrainingIntensityScore', 
              'ManagerStabilityIndicator', 'CareerVelocityScore', 'IncomeGrowthPotential', 
              'ExperienceUtilization'])
        return df
    
    def preprocess_data(self):
        """Preprocess data for clustering"""
        if self.processed_df is None:
            self.feature_engineering()
        
        df = self.processed_df.copy()
        
        # Select career-related features for clustering
        career_features = [
            'Age', 'JobLevel', 'TotalWorkingYears', 'YearsAtCompany', 
            'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
            'PromotionGapRatio', 'RoleStagnationIndex', 'TrainingIntensityScore',
            'ManagerStabilityIndicator', 'CareerVelocityScore', 'IncomeGrowthPotential',
            'ExperienceUtilization'
        ]
        
        # Handle categorical variables
        categorical_cols = ['Department', 'JobRole', 'EducationField', 'Gender', 
                           'MaritalStatus', 'BusinessTravel', 'OverTime']
        
        le_dict = {}
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col + '_Encoded'] = le.fit_transform(df[col].astype(str))
                le_dict[col] = le
                career_features.append(col + '_Encoded')
        
        # Extract features for clustering
        X = df[career_features].copy()
        
        # Handle missing values
        X.fillna(X.median(), inplace=True)
        
        # Remove extreme outliers (late-career edge cases)
        for col in X.columns:
            Q1 = X[col].quantile(0.01)
            Q3 = X[col].quantile(0.99)
            X[col] = np.clip(X[col], Q1, Q3)
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        self.X_scaled = X_scaled
        self.feature_names = career_features
        self.le_dict = le_dict
        
        print(f"Data preprocessing completed. Using {len(career_features)} features for clustering.")
        return X_scaled
    
    def find_optimal_clusters(self, max_clusters=10):
        """Find optimal number of clusters using elbow method and silhouette score"""
        inertias = []
        silhouette_scores = []
        
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(self.X_scaled)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(self.X_scaled, cluster_labels))
        
        # Find optimal k based on silhouette score
        optimal_k = np.argmax(silhouette_scores) + 2
        
        # Plot results
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        ax1.plot(range(2, max_clusters + 1), inertias, 'bo-')
        ax1.set_xlabel('Number of clusters')
        ax1.set_ylabel('Inertia')
        ax1.set_title('Elbow Method')
        ax1.grid(True)
        
        ax2.plot(range(2, max_clusters + 1), silhouette_scores, 'ro-')
        ax2.set_xlabel('Number of clusters')
        ax2.set_ylabel('Silhouette Score')
        ax2.set_title('Silhouette Score Analysis')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('d:/UFO PROJECTS/Second Project/cluster_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Optimal number of clusters: {optimal_k}")
        print(f"Silhouette score: {silhouette_scores[optimal_k-2]:.3f}")
        
        return optimal_k
    
    def perform_clustering(self, n_clusters=5):
        """Perform K-means clustering"""
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.clusters = self.kmeans_model.fit_predict(self.X_scaled)
        
        # Add cluster labels to dataframe
        self.processed_df['CareerCluster'] = self.clusters
        
        silhouette_avg = silhouette_score(self.X_scaled, self.clusters)
        print(f"Clustering completed with silhouette score: {silhouette_avg:.3f}")
        
        return self.clusters
    
    def interpret_clusters(self):
        """Analyze and label clusters based on career patterns"""
        cluster_analysis = {}
        
        for cluster_id in range(len(np.unique(self.clusters))):
            cluster_data = self.processed_df[self.processed_df['CareerCluster'] == cluster_id]
            
            analysis = {
                'size': len(cluster_data),
                'avg_age': cluster_data['Age'].mean(),
                'avg_job_level': cluster_data['JobLevel'].mean(),
                'avg_years_at_company': cluster_data['YearsAtCompany'].mean(),
                'avg_promotion_gap_ratio': cluster_data['PromotionGapRatio'].mean(),
                'avg_role_stagnation': cluster_data['RoleStagnationIndex'].mean(),
                'avg_training_intensity': cluster_data['TrainingIntensityScore'].mean(),
                'avg_career_velocity': cluster_data['CareerVelocityScore'].mean(),
                'attrition_rate': cluster_data['Attrition'].mean() * 100,
                'avg_income': cluster_data['MonthlyIncome'].mean()
            }
            
            cluster_analysis[cluster_id] = analysis
        
        # Create cluster labels based on patterns
        cluster_labels = {}
        for cluster_id, analysis in cluster_analysis.items():
            if analysis['avg_career_velocity'] > 0.5 and analysis['avg_promotion_gap_ratio'] < 0.3:
                cluster_labels[cluster_id] = "Fast-Track Performers"
            elif analysis['avg_years_at_company'] > 10 and analysis['avg_role_stagnation'] < 0.4:
                cluster_labels[cluster_id] = "Stable Long-Term Contributors"
            elif analysis['avg_years_at_company'] < 3:
                cluster_labels[cluster_id] = "Early-Career Explorers"
            elif analysis['avg_promotion_gap_ratio'] > 0.6 and analysis['avg_role_stagnation'] > 0.6:
                cluster_labels[cluster_id] = "High-Risk Stagnation Profiles"
            elif analysis['avg_promotion_gap_ratio'] > 0.4:
                cluster_labels[cluster_id] = "Promotion-Stalled Employees"
            else:
                cluster_labels[cluster_id] = "Career Development Candidates"
        
        self.cluster_analysis = cluster_analysis
        self.cluster_labels = cluster_labels
        
        # Display cluster analysis
        print("\n=== CLUSTER ANALYSIS ===")
        for cluster_id, analysis in cluster_analysis.items():
            label = cluster_labels[cluster_id]
            print(f"\nCluster {cluster_id}: {label}")
            print(f"  Size: {analysis['size']} employees ({analysis['size']/len(self.processed_df)*100:.1f}%)")
            print(f"  Avg Age: {analysis['avg_age']:.1f} years")
            print(f"  Avg Job Level: {analysis['avg_job_level']:.1f}")
            print(f"  Avg Years at Company: {analysis['avg_years_at_company']:.1f}")
            print(f"  Promotion Gap Ratio: {analysis['avg_promotion_gap_ratio']:.3f}")
            print(f"  Role Stagnation: {analysis['avg_role_stagnation']:.3f}")
            print(f"  Career Velocity: {analysis['avg_career_velocity']:.3f}")
            print(f"  Attrition Rate: {analysis['attrition_rate']:.1f}%")
        
        return cluster_analysis, cluster_labels
    
    def calculate_promotion_gap_risk_score(self):
        """Calculate promotion gap risk score for each employee"""
        df = self.processed_df.copy()
        
        # Define risk scoring criteria
        def calculate_risk(row):
            risk_score = 0
            
            # High promotion gap ratio
            if row['PromotionGapRatio'] > 0.6:
                risk_score += 3
            elif row['PromotionGapRatio'] > 0.4:
                risk_score += 2
            elif row['PromotionGapRatio'] > 0.2:
                risk_score += 1
            
            # High role stagnation
            if row['RoleStagnationIndex'] > 0.7:
                risk_score += 3
            elif row['RoleStagnationIndex'] > 0.5:
                risk_score += 2
            elif row['RoleStagnationIndex'] > 0.3:
                risk_score += 1
            
            # Low training intensity
            if row['TrainingIntensityScore'] < 0.1:
                risk_score += 2
            elif row['TrainingIntensityScore'] < 0.2:
                risk_score += 1
            
            # Low career velocity
            if row['CareerVelocityScore'] < 0.1:
                risk_score += 2
            elif row['CareerVelocityScore'] < 0.2:
                risk_score += 1
            
            # Manager instability
            if row['ManagerStabilityIndicator'] < 0.3:
                risk_score += 1
            
            return risk_score
        
        df['PromotionGapRiskScore'] = df.apply(calculate_risk, axis=1)
        
        # Categorize risk levels
        def categorize_risk(score):
            if score >= 7:
                return "High"
            elif score >= 4:
                return "Medium"
            else:
                return "Low"
        
        df['PromotionGapRiskLevel'] = df['PromotionGapRiskScore'].apply(categorize_risk)
        
        self.processed_df = df
        
        # Display risk distribution
        risk_dist = df['PromotionGapRiskLevel'].value_counts()
        print("\n=== PROMOTION GAP RISK DISTRIBUTION ===")
        for risk_level, count in risk_dist.items():
            percentage = count / len(df) * 100
            print(f"{risk_level} Risk: {count} employees ({percentage:.1f}%)")
        
        return df
    
    def identify_retention_opportunities(self):
        """Identify employees who need career intervention"""
        df = self.processed_df.copy()
        
        # Define retention opportunity criteria
        retention_opportunities = df[
            (df['Attrition'] == 0) &  # Not yet disengaged
            (df['PromotionGapRiskLevel'].isin(['Medium', 'High'])) &  # Show career stagnation signals
            (df['JobSatisfaction'] >= 3) &  # Still satisfied with job
            (df['EnvironmentSatisfaction'] >= 3)  # Satisfied with environment
        ].copy()
        
        # Calculate retention opportunity index
        retention_opportunities['RetentionOpportunityIndex'] = (
            retention_opportunities['PromotionGapRiskScore'] * 0.4 +
            (5 - retention_opportunities['JobSatisfaction']) * 0.2 +
            (5 - retention_opportunities['EnvironmentSatisfaction']) * 0.2 +
            retention_opportunities['RoleStagnationIndex'] * 10 * 0.2
        )
        
        # Sort by priority
        retention_opportunities = retention_opportunities.sort_values('RetentionOpportunityIndex', ascending=False)
        
        self.retention_opportunities = retention_opportunities
        
        print(f"\n=== RETENTION OPPORTUNITIES ===")
        print(f"Identified {len(retention_opportunities)} employees for career intervention")
        print(f"Top 10 high-priority employees:")
        
        top_10 = retention_opportunities.head(10)
        for idx, row in top_10.iterrows():
            print(f"  Employee {idx}: Risk Score {row['PromotionGapRiskScore']}, "
                  f"Opportunity Index {row['RetentionOpportunityIndex']:.2f}")
        
        return retention_opportunities
    
    def generate_insights(self):
        """Generate key insights for stakeholders"""
        insights = []
        
        # Cluster insights
        cluster_sizes = self.processed_df['CareerCluster'].value_counts()
        largest_cluster = cluster_sizes.index[0]
        largest_cluster_label = self.cluster_labels[largest_cluster]
        
        insights.append(f"The largest career group is '{largest_cluster_label}' with "
                       f"{cluster_sizes.iloc[0]} employees ({cluster_sizes.iloc[0]/len(self.processed_df)*100:.1f}%)")
        
        # Risk insights
        high_risk_count = len(self.processed_df[self.processed_df['PromotionGapRiskLevel'] == 'High'])
        insights.append(f"{high_risk_count} employees ({high_risk_count/len(self.processed_df)*100:.1f}%) "
                       "are at high risk of promotion stagnation")
        
        # Retention opportunities
        insights.append(f"{len(self.retention_opportunities)} employees show retention opportunities "
                       "through career intervention")
        
        # Department insights
        dept_risk = self.processed_df.groupby('Department')['PromotionGapRiskScore'].mean().sort_values(ascending=False)
        highest_risk_dept = dept_risk.index[0]
        insights.append(f"The '{highest_risk_dept}' department shows the highest average promotion gap risk")
        
        # Training insights
        low_training = len(self.processed_df[self.processed_df['TrainingIntensityScore'] < 0.1])
        insights.append(f"{low_training} employees ({low_training/len(self.processed_df)*100:.1f}%) "
                       "have very low training intensity")
        
        return insights
    
    def save_results(self):
        """Save analysis results"""
        # Save processed dataframe
        self.processed_df.to_csv('d:/UFO PROJECTS/Second Project/career_progression_results.csv', index=False)
        
        # Save cluster analysis
        cluster_df = pd.DataFrame(self.cluster_analysis).T
        cluster_df['ClusterLabel'] = cluster_df.index.map(self.cluster_labels)
        cluster_df.to_csv('d:/UFO PROJECTS/Second Project/cluster_analysis.csv')
        
        # Save retention opportunities
        if hasattr(self, 'retention_opportunities'):
            self.retention_opportunities.to_csv('d:/UFO PROJECTS/Second Project/retention_opportunities.csv', index=False)
        
        print("Results saved to CSV files")

# Main execution
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = CareerProgressionAnalyzer('d:/UFO PROJECTS/Second Project/Palo Alto Networks.csv')
    
    # Load data
    analyzer.load_data()
    
    # Feature engineering
    analyzer.feature_engineering()
    
    # Preprocess data
    analyzer.preprocess_data()
    
    # Find optimal clusters
    optimal_k = analyzer.find_optimal_clusters()
    
    # Perform clustering
    analyzer.perform_clustering(optimal_k)
    
    # Interpret clusters
    analyzer.interpret_clusters()
    
    # Calculate promotion gap risk scores
    analyzer.calculate_promotion_gap_risk_score()
    
    # Identify retention opportunities
    analyzer.identify_retention_opportunities()
    
    # Generate insights
    insights = analyzer.generate_insights()
    
    print("\n=== KEY INSIGHTS FOR STAKEHOLDERS ===")
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    
    # Save results
    analyzer.save_results()
