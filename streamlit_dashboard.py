import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from career_progression_analysis import CareerProgressionAnalyzer

# Set page configuration
st.set_page_config(
    page_title="Career Progression & Promotion Gap Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data and analysis
@st.cache_data
def load_analysis():
    analyzer = CareerProgressionAnalyzer('d:/UFO PROJECTS/Second Project/Palo Alto Networks.csv')
    analyzer.load_data()
    analyzer.feature_engineering()
    analyzer.preprocess_data()
    
    # Use optimal clusters from analysis
    analyzer.perform_clustering(3)
    analyzer.interpret_clusters()
    analyzer.calculate_promotion_gap_risk_score()
    analyzer.identify_retention_opportunities()
    
    return analyzer

def main():
    # Load analysis
    analyzer = load_analysis()
    df = analyzer.processed_df
    
    # Main header
    st.markdown('<h1 class="main-header">📊 Career Progression & Promotion Gap Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Palo Alto Networks - Retention Optimization Dashboard</p>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.markdown("### 🔍 Filters & Controls")
    
    # Department filter
    departments = ['All'] + list(df['Department'].unique())
    selected_dept = st.sidebar.selectbox('Department', departments)
    
    # Job Role filter
    roles = ['All'] + list(df['JobRole'].unique())
    selected_role = st.sidebar.selectbox('Job Role', roles)
    
    # Career Stage filter
    career_stages = ['All', 'Early Career (0-3 years)', 'Mid Career (4-7 years)', 'Senior Career (8+ years)']
    selected_career_stage = st.sidebar.selectbox('Career Stage', career_stages)
    
    # Promotion Gap Risk Level filter
    risk_levels = ['All'] + list(df['PromotionGapRiskLevel'].unique())
    selected_risk = st.sidebar.selectbox('Promotion Gap Risk Level', risk_levels)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
    
    if selected_role != 'All':
        filtered_df = filtered_df[filtered_df['JobRole'] == selected_role]
    
    if selected_career_stage != 'All':
        if selected_career_stage == 'Early Career (0-3 years)':
            filtered_df = filtered_df[filtered_df['YearsAtCompany'] <= 3]
        elif selected_career_stage == 'Mid Career (4-7 years)':
            filtered_df = filtered_df[(filtered_df['YearsAtCompany'] >= 4) & (filtered_df['YearsAtCompany'] <= 7)]
        else:  # Senior Career
            filtered_df = filtered_df[filtered_df['YearsAtCompany'] >= 8]
    
    if selected_risk != 'All':
        filtered_df = filtered_df[filtered_df['PromotionGapRiskLevel'] == selected_risk]
    
    # Key Metrics Dashboard
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_employees = len(filtered_df)
        st.metric("Total Employees", f"{total_employees:,}")
    
    with col2:
        high_risk_count = len(filtered_df[filtered_df['PromotionGapRiskLevel'] == 'High'])
        high_risk_pct = (high_risk_count / total_employees * 100) if total_employees > 0 else 0
        st.metric("High Risk Employees", f"{high_risk_count} ({high_risk_pct:.1f}%)")
    
    with col3:
        avg_promotion_gap = filtered_df['PromotionGapRatio'].mean()
        st.metric("Avg Promotion Gap", f"{avg_promotion_gap:.3f}")
    
    with col4:
        attrition_rate = filtered_df['Attrition'].mean() * 100
        st.metric("Attrition Rate", f"{attrition_rate:.1f}%")
    
    # Tab-based navigation
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Career Clustering", "⚠️ Promotion Gap Monitor", "💡 Retention Opportunities", "👥 Managerial Insights"])
    
    with tab1:
        st.markdown("### Career Path Clustering Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cluster distribution pie chart
            cluster_counts = filtered_df['CareerCluster'].value_counts()
            cluster_labels = [analyzer.cluster_labels[i] for i in cluster_counts.index]
            
            fig_pie = px.pie(
                values=cluster_counts.values,
                names=cluster_labels,
                title="Career Cluster Distribution"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Cluster characteristics
            st.markdown("#### Career Pattern Summaries")
            
            for cluster_id in analyzer.cluster_analysis.keys():
                if cluster_id in filtered_df['CareerCluster'].values:
                    cluster_data = filtered_df[filtered_df['CareerCluster'] == cluster_id]
                    label = analyzer.cluster_labels[cluster_id]
                    size = len(cluster_data)
                    
                    with st.expander(f"{label} ({size} employees)"):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.metric("Avg Years at Company", f"{cluster_data['YearsAtCompany'].mean():.1f}")
                            st.metric("Avg Promotion Gap", f"{cluster_data['PromotionGapRatio'].mean():.3f}")
                            st.metric("Career Velocity", f"{cluster_data['CareerVelocityScore'].mean():.2f}")
                        
                        with col_b:
                            st.metric("Avg Job Level", f"{cluster_data['JobLevel'].mean():.1f}")
                            st.metric("Role Stagnation", f"{cluster_data['RoleStagnationIndex'].mean():.3f}")
                            st.metric("Attrition Rate", f"{cluster_data['Attrition'].mean()*100:.1f}%")
        
        # Cluster comparison chart
        st.markdown("#### Cluster Comparison Analysis")
        
        cluster_comparison = filtered_df.groupby('CareerCluster').agg({
            'PromotionGapRatio': 'mean',
            'RoleStagnationIndex': 'mean',
            'CareerVelocityScore': 'mean',
            'TrainingIntensityScore': 'mean'
        }).reset_index()
        
        cluster_comparison['ClusterLabel'] = cluster_comparison['CareerCluster'].map(analyzer.cluster_labels)
        
        fig_radar = go.Figure()
        
        metrics = ['PromotionGapRatio', 'RoleStagnationIndex', 'CareerVelocityScore', 'TrainingIntensityScore']
        
        for _, row in cluster_comparison.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row[metric] for metric in metrics],
                theta=metrics,
                fill='toself',
                name=row['ClusterLabel']
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, cluster_comparison[metrics].max().max()]
                )),
            showlegend=True,
            title="Career Cluster Profiles Comparison"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab2:
        st.markdown("### Promotion Gap Monitor")
        
        # Risk distribution
        col1, col2 = st.columns(2)
        
        with col1:
            risk_counts = filtered_df['PromotionGapRiskLevel'].value_counts()
            
            fig_risk = px.bar(
                x=risk_counts.index,
                y=risk_counts.values,
                title="Promotion Gap Risk Distribution",
                color=risk_counts.index,
                color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
            )
            fig_risk.update_xaxes(title="Risk Level")
            fig_risk.update_yaxes(title="Number of Employees")
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            # High-risk employee identification
            high_risk_employees = filtered_df[filtered_df['PromotionGapRiskLevel'] == 'High']
            
            if len(high_risk_employees) > 0:
                st.markdown("#### High-Risk Employees (Top 10)")
                
                top_high_risk = high_risk_employees.nlargest(10, 'PromotionGapRiskScore')
                
                display_cols = ['Department', 'JobRole', 'YearsAtCompany', 'YearsSinceLastPromotion', 
                               'PromotionGapRatio', 'RoleStagnationIndex']
                
                st.dataframe(
                    top_high_risk[display_cols].round(3),
                    use_container_width=True
                )
            else:
                st.info("No high-risk employees in the current filter selection.")
        
        # Role-level stagnation insights
        st.markdown("#### Role-Level Stagnation Analysis")
        
        role_stagnation = filtered_df.groupby('JobRole').agg({
            'PromotionGapRatio': 'mean',
            'RoleStagnationIndex': 'mean',
            'YearsSinceLastPromotion': 'mean',
            'Attrition': 'mean'
        }).round(3)
        
        role_stagnation.columns = ['Avg Promotion Gap', 'Avg Role Stagnation', 'Avg Years Since Promotion', 'Attrition Rate']
        role_stagnation = role_stagnation.sort_values('Avg Promotion Gap', ascending=False)
        
        st.dataframe(role_stagnation, use_container_width=True)
        
        # Promotion gap threshold analysis
        st.markdown("#### Promotion Gap Threshold Analysis")
        
        gap_threshold = st.slider("Promotion Gap Ratio Threshold", 0.0, 1.0, 0.4, 0.05)
        
        above_threshold = filtered_df[filtered_df['PromotionGapRatio'] >= gap_threshold]
        below_threshold = filtered_df[filtered_df['PromotionGapRatio'] < gap_threshold]
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric(f"Above Threshold (≥{gap_threshold})", 
                     f"{len(above_threshold)} ({len(above_threshold)/len(filtered_df)*100:.1f}%)")
            st.metric("Avg Attrition (Above)", f"{above_threshold['Attrition'].mean()*100:.1f}%")
        
        with col_b:
            st.metric(f"Below Threshold (<{gap_threshold})", 
                     f"{len(below_threshold)} ({len(below_threshold)/len(filtered_df)*100:.1f}%)")
            st.metric("Avg Attrition (Below)", f"{below_threshold['Attrition'].mean()*100:.1f}%")
    
    with tab3:
        st.markdown("### Retention Opportunity Panel")
        
        # Get retention opportunities for filtered data
        retention_candidates = filtered_df[
            (filtered_df['Attrition'] == 0) & 
            (filtered_df['PromotionGapRiskLevel'].isin(['Medium', 'High'])) & 
            (filtered_df['JobSatisfaction'] >= 3) & 
            (filtered_df['EnvironmentSatisfaction'] >= 3)
        ].copy()
        
        # Calculate retention opportunity index
        retention_candidates['RetentionOpportunityIndex'] = (
            retention_candidates['PromotionGapRiskScore'] * 0.4 +
            (5 - retention_candidates['JobSatisfaction']) * 0.2 +
            (5 - retention_candidates['EnvironmentSatisfaction']) * 0.2 +
            retention_candidates['RoleStagnationIndex'] * 10 * 0.2
        )
        
        retention_candidates = retention_candidates.sort_values('RetentionOpportunityIndex', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Employees Needing Career Intervention", f"{len(retention_candidates)}")
            
            if len(retention_candidates) > 0:
                high_priority = retention_candidates[retention_candidates['RetentionOpportunityIndex'] >= 5.0]
                st.metric("High Priority (Index ≥ 5.0)", f"{len(high_priority)}")
        
        with col2:
            if len(retention_candidates) > 0:
                avg_opportunity_index = retention_candidates['RetentionOpportunityIndex'].mean()
                st.metric("Avg Opportunity Index", f"{avg_opportunity_index:.2f}")
                
                # Suggested actions distribution
                training_needed = len(retention_candidates[retention_candidates['TrainingIntensityScore'] < 0.2])
                promotion_review = len(retention_candidates[retention_candidates['PromotionGapRatio'] > 0.5])
                role_rotation = len(retention_candidates[retention_candidates['RoleStagnationIndex'] > 0.6])
                
                st.markdown("**Suggested Actions:**")
                st.write(f"• Training Needed: {training_needed} employees")
                st.write(f"• Promotion Review: {promotion_review} employees")
                st.write(f"• Role Rotation: {role_rotation} employees")
        
        if len(retention_candidates) > 0:
            # Detailed retention opportunities table
            st.markdown("#### Detailed Retention Opportunities")
            
            display_cols = ['Department', 'JobRole', 'YearsAtCompany', 'YearsSinceLastPromotion',
                           'PromotionGapRiskLevel', 'JobSatisfaction', 'EnvironmentSatisfaction',
                           'RetentionOpportunityIndex']
            
            # Show top 20 opportunities
            top_opportunities = retention_candidates.head(20)
            
            st.dataframe(
                top_opportunities[display_cols].round(3),
                use_container_width=True
            )
            
            # Action recommendations
            st.markdown("#### Recommended Interventions")
            
            selected_employee = st.selectbox(
                "Select an employee for detailed recommendations:",
                options=top_opportunities.index,
                format_func=lambda x: f"Employee {x} - {top_opportunities.loc[x, 'JobRole']}"
            )
            
            if selected_employee:
                employee_data = top_opportunities.loc[selected_employee]
                
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown(f"**Employee {selected_employee} - {employee_data['JobRole']}**")
                
                recommendations = []
                
                if employee_data['PromotionGapRatio'] > 0.5:
                    recommendations.append("🎯 **Promotion Review**: Consider for advancement based on tenure and performance")
                
                if employee_data['TrainingIntensityScore'] < 0.2:
                    recommendations.append("📚 **Training Program**: Enroll in skill development programs to enhance capabilities")
                
                if employee_data['RoleStagnationIndex'] > 0.6:
                    recommendations.append("🔄 **Role Rotation**: Consider lateral move to new team or project")
                
                if employee_data['ManagerStabilityIndicator'] < 0.3:
                    recommendations.append("👥 **Manager Assignment**: Review manager-employee fit and consider reassignment")
                
                if employee_data['JobSatisfaction'] < 4:
                    recommendations.append("💬 **Career Discussion**: Schedule career development conversation")
                
                for rec in recommendations:
                    st.markdown(f"• {rec}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No retention opportunities identified in the current filter selection.")
    
    with tab4:
        st.markdown("### Managerial Insight Dashboard")
        
        # Manager tenure vs career growth
        col1, col2 = st.columns(2)
        
        with col1:
            # Manager stability impact
            manager_impact = filtered_df.groupby('YearsWithCurrManager').agg({
                'PromotionGapRatio': 'mean',
                'CareerVelocityScore': 'mean',
                'Attrition': 'mean',
                'JobSatisfaction': 'mean'
            }).round(3)
            
            manager_impact.columns = ['Avg Promotion Gap', 'Avg Career Velocity', 'Attrition Rate', 'Avg Job Satisfaction']
            
            fig_manager = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Promotion Gap vs Manager Tenure', 'Career Velocity vs Manager Tenure',
                              'Attrition vs Manager Tenure', 'Job Satisfaction vs Manager Tenure'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            fig_manager.add_trace(
                go.Scatter(x=manager_impact.index, y=manager_impact['Avg Promotion Gap'], 
                          mode='lines+markers', name='Promotion Gap'),
                row=1, col=1
            )
            
            fig_manager.add_trace(
                go.Scatter(x=manager_impact.index, y=manager_impact['Avg Career Velocity'], 
                          mode='lines+markers', name='Career Velocity'),
                row=1, col=2
            )
            
            fig_manager.add_trace(
                go.Scatter(x=manager_impact.index, y=manager_impact['Attrition Rate'], 
                          mode='lines+markers', name='Attrition Rate'),
                row=2, col=1
            )
            
            fig_manager.add_trace(
                go.Scatter(x=manager_impact.index, y=manager_impact['Avg Job Satisfaction'], 
                          mode='lines+markers', name='Job Satisfaction'),
                row=2, col=2
            )
            
            fig_manager.update_layout(height=600, showlegend=False, 
                                     title_text="Manager Tenure Impact on Career Metrics")
            
            st.plotly_chart(fig_manager, use_container_width=True)
        
        with col2:
            # Team-level stagnation signals
            st.markdown("#### Team-Level Stagnation Signals")
            
            # Create team identifier (Department + JobRole combination)
            filtered_df['Team'] = filtered_df['Department'] + ' - ' + filtered_df['JobRole']
            
            team_analysis = filtered_df.groupby('Team').agg({
                'PromotionGapRatio': 'mean',
                'RoleStagnationIndex': 'mean',
                'Attrition': 'mean',
                'YearsWithCurrManager': 'mean'
            }).round(3)
            
            team_analysis.columns = ['Avg Promotion Gap', 'Avg Role Stagnation', 'Attrition Rate', 'Avg Manager Tenure']
            
            # Identify high-risk teams
            team_analysis['RiskScore'] = (
                team_analysis['Avg Promotion Gap'] * 0.4 +
                team_analysis['Avg Role Stagnation'] * 0.3 +
                team_analysis['Attrition Rate'] * 0.3
            )
            
            high_risk_teams = team_analysis.sort_values('RiskScore', ascending=False).head(10)
            
            st.dataframe(high_risk_teams, use_container_width=True)
            
            # Manager effectiveness insights
            st.markdown("#### Manager Effectiveness Insights")
            
            manager_effectiveness = filtered_df.groupby('YearsWithCurrManager').agg({
                'JobSatisfaction': 'mean',
                'EnvironmentSatisfaction': 'mean',
                'PerformanceRating': 'mean'
            }).round(2)
            
            manager_effectiveness.columns = ['Avg Job Satisfaction', 'Avg Environment Satisfaction', 'Avg Performance Rating']
            
            # Find optimal manager tenure range
            optimal_satisfaction = manager_effectiveness['Avg Job Satisfaction'].idxmax()
            optimal_performance = manager_effectiveness['Avg Performance Rating'].idxmax()
            
            st.markdown(f"**Optimal Manager-Employee Relationship Duration:**")
            st.markdown(f"• For Job Satisfaction: {optimal_satisfaction} years")
            st.markdown(f"• For Performance: {optimal_performance} years")
            
            # Manager stability recommendations
            st.markdown("**Manager Stability Recommendations:**")
            
            if optimal_satisfaction < 2:
                st.write("• Consider more frequent manager check-ins for early-career employees")
            elif optimal_satisfaction > 5:
                st.write("• Long-term manager relationships show positive impact on satisfaction")
            
            low_manager_tenure = filtered_df[filtered_df['YearsWithCurrManager'] < 1]
            if len(low_manager_tenure) > 0:
                st.write(f"• {len(low_manager_tenure)} employees have new managers (< 1 year) - monitor transition")
    
    # Footer insights
    st.markdown("---")
    st.markdown("### 💡 Key Insights & Recommendations")
    
    # Generate dynamic insights based on filtered data
    insights = []
    
    # Cluster insights
    largest_cluster = filtered_df['CareerCluster'].value_counts().index[0]
    largest_cluster_label = analyzer.cluster_labels[largest_cluster]
    insights.append(f"Primary career pattern: '{largest_cluster_label}' ({filtered_df['CareerCluster'].value_counts().iloc[0]} employees)")
    
    # Risk insights
    high_risk_pct = len(filtered_df[filtered_df['PromotionGapRiskLevel'] == 'High']) / len(filtered_df) * 100
    insights.append(f"{high_risk_pct:.1f}% of employees at high promotion stagnation risk")
    
    # Training insights
    low_training_pct = len(filtered_df[filtered_df['TrainingIntensityScore'] < 0.1]) / len(filtered_df) * 100
    insights.append(f"{low_training_pct:.1f}% have very low training intensity")
    
    # Manager stability insights
    avg_manager_tenure = filtered_df['YearsWithCurrManager'].mean()
    insights.append(f"Average manager-employee relationship: {avg_manager_tenure:.1f} years")
    
    # Display insights
    col1, col2 = st.columns(2)
    
    with col1:
        for i, insight in enumerate(insights[:2]):
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    with col2:
        for i, insight in enumerate(insights[2:]):
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    # Export functionality
    st.markdown("---")
    st.markdown("### 📊 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Filtered Data"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="career_progression_filtered.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export Retention Opportunities"):
            if len(retention_candidates) > 0:
                csv = retention_candidates.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="retention_opportunities.csv",
                    mime="text/csv"
                )
    
    with col3:
        if st.button("Export Cluster Analysis"):
            cluster_data = filtered_df.groupby('CareerCluster').agg({
                'PromotionGapRatio': 'mean',
                'RoleStagnationIndex': 'mean',
                'CareerVelocityScore': 'mean',
                'Attrition': 'mean'
            }).round(3)
            csv = cluster_data.to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="cluster_analysis.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
