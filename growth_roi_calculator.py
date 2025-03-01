import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set page config
st.set_page_config(
    page_title="Smarter Growth ROI Calculator",
    page_icon="📈",
    layout="wide"
)

# Clear CSS that works in both light and dark mode
st.markdown("""
<style>
/* Make delta values more visible */
[data-testid="stMetricDelta"] {
    font-weight: bold !important;
}
[data-testid="stMetricDelta"] svg {
    margin-right: 2px !important;
}
/* Positive values - green */
[data-testid="stMetricDelta"][data-direction="up"] {
    color: #28a745 !important;
    background-color: rgba(40, 167, 69, 0.1) !important;
    padding: 2px 6px;
    border-radius: 4px;
}
/* Negative values - red */
[data-testid="stMetricDelta"][data-direction="down"] {
    color: #dc3545 !important;
    background-color: rgba(220, 53, 69, 0.1) !important;
    padding: 2px 6px;
    border-radius: 4px;
}
/* Neutral values */
[data-testid="stMetricDelta"][data-direction="right"] {
    color: #6c757d !important;
    background-color: rgba(108, 117, 125, 0.1) !important;
    padding: 2px 6px;
    border-radius: 4px;
}
/* Improve metric visuals */
[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: bold !important;
}
/* Make code more readable */
[data-testid="stCodeBlock"] {
    line-height: 1.5 !important;
}
/* Highlight box styling */
.highlight {
    padding: 12px 15px;
    margin-bottom: 15px;
    border-radius: 4px;
    border-left: 4px solid #007bff;
}
/* Recommendation boxes */
.recommendation-box {
    padding: 15px;
    border-radius: 6px;
    margin-bottom: 15px;
}
.recommendation-good {
    border-left: 4px solid #28a745;
    background-color: rgba(40, 167, 69, 0.05);
}
.recommendation-neutral {
    border-left: 4px solid #007bff;
    background-color: rgba(0, 123, 255, 0.05);
}
.recommendation-bad {
    border-left: 4px solid #dc3545;
    background-color: rgba(220, 53, 69, 0.05);
}
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("Smarter Growth ROI Calculator: Go Beyond LTV vs. CAC")
st.markdown("""
This calculator provides deeper insights into your digital growth strategy's ROI by incorporating churn risk, 
upsell potential, and organic/referral growth impact beyond traditional LTV vs. CAC metrics.
""")

# Sidebar with inputs
st.sidebar.header("Growth Metrics Inputs")

# Financial inputs
with st.sidebar.expander("Financial Metrics", expanded=True):
    cac = st.number_input("Customer Acquisition Cost (CAC) ($)", min_value=0.0, value=200.0, step=10.0)
    ltv = st.number_input("Customer Lifetime Value (LTV) ($)", min_value=0.0, value=600.0, step=50.0)
    total_ad_spend = st.number_input("Total Ad Spend ($)", min_value=0.0, value=10000.0, step=1000.0)
    retention_costs = st.number_input("Retention Costs ($)", min_value=0.0, value=5000.0, step=500.0,
                                      help="Costs for support, loyalty, and re-engagement programs")
    product_engineering_costs = st.number_input("Product & Engineering Costs ($)", min_value=0.0, value=15000.0, step=1000.0,
                                                help="Costs for growth-related features, AI/automation, etc.")

# Performance metrics inputs
with st.sidebar.expander("Performance Metrics", expanded=True):
    churn_rate = st.slider("Churn Rate (%)", min_value=0.0, max_value=50.0, value=5.0, step=0.5) / 100
    conversion_rate = st.slider("Conversion Rate (%)", min_value=0.0, max_value=30.0, value=2.5, step=0.1) / 100
    expansion_revenue = st.slider("Expansion Revenue (%)", min_value=0.0, max_value=30.0, value=10.0, step=0.5) / 100
    referral_revenue_impact = st.slider("Referral Revenue Impact (%)", min_value=0.0, max_value=50.0, value=15.0, step=0.5) / 100

# Calculate key metrics
new_customers = total_ad_spend * conversion_rate / cac if cac > 0 else 0
base_revenue = new_customers * ltv
expansion_impact = base_revenue * expansion_revenue
referral_impact = base_revenue * referral_revenue_impact
churn_loss = base_revenue * churn_rate
total_revenue = base_revenue + expansion_impact + referral_impact - churn_loss
total_growth_investment = total_ad_spend + retention_costs + product_engineering_costs
acquisition_retention_costs = total_ad_spend + retention_costs
growth_roi = ((total_revenue - acquisition_retention_costs) / total_growth_investment) * 100 if total_growth_investment else 0
break_even_cac = ltv * (1 + expansion_revenue + referral_revenue_impact - churn_rate) if churn_rate < 1 else 0
profitable_revenue_from_ads = total_ad_spend * conversion_rate

# Main content
st.header("ROI Analysis")

col1, col2, col3 = st.columns([1.618, 1, 1])
with col1:
    st.metric(
        label="True Growth ROI", 
        value=f"{growth_roi:.2f}%",
        delta="Beyond simple LTV:CAC" if growth_roi > 0 else "Needs improvement",
        delta_color="normal" if growth_roi > 20 else "off" if growth_roi > 0 else "inverse"
    )
    st.markdown("""
    <div class="highlight">
    <small>Formula: ((Net Revenue - Acquisition & Retention Costs) / Total Growth Investment) × 100</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric(
        label="Break-Even CAC", 
        value=f"${break_even_cac:.2f}",
        delta=f"{'Below' if cac < break_even_cac else 'Above'} current CAC (${cac:.2f})",
        delta_color="normal" if cac < break_even_cac else "inverse"
    )
    st.markdown("""
    <div class="highlight">
    <small>Maximum CAC before becoming unprofitable, accounting for all factors</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    ltv_cac_ratio = ltv / cac if cac else 0
    st.metric(
        label="Traditional LTV:CAC Ratio", 
        value=f"{ltv_cac_ratio:.2f}",
        delta=f"{'Good' if ltv_cac_ratio >= 3 else 'Needs improvement'}",
        delta_color="normal" if ltv_cac_ratio >= 3 else "inverse"
    )
    st.markdown("""
    <div class="highlight">
    <small>Target ratio is typically 3:1 or higher</small>
    </div>
    """, unsafe_allow_html=True)

st.subheader("Detailed Performance Metrics")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    churn_delta_color = "inverse" if churn_rate > 0.05 else "normal"
    st.metric(
        label="Revenue Lost to Churn", 
        value=f"${churn_loss:.2f}",
        delta=f"{churn_rate*100:.1f}% of potential revenue",
        delta_color=churn_delta_color
    )

with col2:
    expansion_delta_color = "normal" if expansion_revenue >= 0.1 else "off"
    st.metric(
        label="Expansion Revenue Impact", 
        value=f"${expansion_impact:.2f}",
        delta=f"{expansion_revenue*100:.1f}% increase",
        delta_color=expansion_delta_color
    )

with col3:
    referral_delta_color = "normal" if referral_revenue_impact >= 0.15 else "off"
    st.metric(
        label="Referral Revenue Impact", 
        value=f"${referral_impact:.2f}",
        delta=f"{referral_revenue_impact*100:.1f}% of revenue",
        delta_color=referral_delta_color
    )

with col4:
    conversion_delta_color = "normal" if conversion_rate >= 0.02 else "off"
    st.metric(
        label="Profitable Ad Revenue", 
        value=f"${profitable_revenue_from_ads:.2f}",
        delta=f"{conversion_rate*100:.2f}% conversion rate",
        delta_color=conversion_delta_color
    )

# Revenue Composition Analysis
st.subheader("Revenue Composition Analysis")
revenue_data = {
    'Category': ['Base Revenue', 'Expansion Impact', 'Referral Impact', 'Churn Loss'],
    'Value': [base_revenue, expansion_impact, referral_impact, -churn_loss]
}
revenue_df = pd.DataFrame(revenue_data)
revenue_df = revenue_df[revenue_df['Value'] != 0]

fig, ax = plt.subplots(figsize=(12, 6))
# High contrast colors for accessibility
colors = []
for val in revenue_df['Value']:
    if val == base_revenue:
        colors.append('#000080')  # Dark blue
    elif val == expansion_impact:
        colors.append('#006400')  # Dark green
    elif val == referral_impact:
        colors.append('#4B0082')  # Dark purple
    else:
        colors.append('#8B0000')  # Dark red for negative

bars = ax.bar(revenue_df['Category'], revenue_df['Value'], color=colors, width=0.7)

# Bar labels with high contrast
for bar in bars:
    height = bar.get_height()
    if height < 0:
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            0,
            f'${abs(height):,.2f}',
            ha='center', va='bottom',
            color='#000000',
            fontweight='bold',
            fontsize=11
        )
    else:
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'${height:,.2f}',
            ha='center', va='bottom',
            color='#000000',
            fontweight='bold',
            fontsize=11
        )

ax.set_title('Revenue Components Breakdown', fontsize=16, pad=20, fontweight='bold', color='#000000')
ax.set_ylabel('Revenue ($)', fontsize=12, labelpad=15, fontweight='bold', color='#000000')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#000000')
ax.spines['bottom'].set_color('#000000')
ax.tick_params(axis='both', labelsize=11, colors='#000000')
ax.grid(axis='y', linestyle='--', alpha=0.3, color='#000000')
ax.set_axisbelow(True)

total_positive = base_revenue + expansion_impact + referral_impact
plt.annotate(
    f'Total Positive Impact: ${total_positive:,.2f}',
    xy=(0.6, 0.92), xycoords='axes fraction',
    bbox=dict(boxstyle="round,pad=0.5", fc="#FFFFFF", ec="#006400", alpha=1.0),
    fontsize=11, ha='center', color='#000000'
)
plt.annotate(
    f'Churn Loss: ${churn_loss:,.2f} ({(churn_loss / total_positive * 100):.1f}% of positive revenue)',
    xy=(0.6, 0.84), xycoords='axes fraction',
    bbox=dict(boxstyle="round,pad=0.5", fc="#FFFFFF", ec="#8B0000", alpha=1.0),
    fontsize=11, ha='center', color='#000000'
)

plt.tight_layout()
st.pyplot(fig)

# Sensitivity Analysis
st.subheader("Sensitivity Analysis")
st.markdown("""
<div class="highlight">
    <p style="margin: 0; font-size: 16px;">Explore how changes in key metrics affect your Growth ROI. 
    This analysis helps you understand which factors have the biggest impact on your business performance.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.618, 1])
with col1:
    cac_changes = np.linspace(cac * 0.5, cac * 1.5, 10)
    roi_at_cac = []
    for test_cac in cac_changes:
        new_customers_test = total_ad_spend * conversion_rate / test_cac if test_cac > 0 else 0
        base_revenue_test = new_customers_test * ltv
        expansion_impact_test = base_revenue_test * expansion_revenue
        referral_impact_test = base_revenue_test * referral_revenue_impact
        churn_loss_test = base_revenue_test * churn_rate
        total_revenue_test = base_revenue_test + expansion_impact_test + referral_impact_test - churn_loss_test
        roi_test = ((total_revenue_test - acquisition_retention_costs) / total_growth_investment) * 100 if total_growth_investment else 0
        roi_at_cac.append(roi_test)

    sensitivity_cac = pd.DataFrame({
        'CAC ($)': cac_changes,
        'Growth ROI (%)': roi_at_cac
    })

    fig_cac, ax_cac = plt.subplots(figsize=(12, 7))
    # Using a high contrast colormap
    points = ax_cac.scatter(
        sensitivity_cac['CAC ($)'],
        sensitivity_cac['Growth ROI (%)'],
        c=sensitivity_cac['Growth ROI (%)'],
        cmap='viridis',
        s=80,
        alpha=0.8,
        zorder=5
    )
    sns.lineplot(
        data=sensitivity_cac,
        x='CAC ($)',
        y='Growth ROI (%)',
        ax=ax_cac,
        color='#000080',  # Dark blue for better contrast
        linewidth=2.5,
        alpha=0.7,
        zorder=4
    )
    ax_cac.axhline(y=0, color='#8B0000', linestyle='--', alpha=0.8, linewidth=1.5, zorder=3, label='Break-even point')
    ax_cac.axvline(x=cac, color='#006400', linestyle='--', alpha=0.8, linewidth=1.5, zorder=3, label=f'Current CAC (${cac:.2f})')
    ax_cac.axvline(x=break_even_cac, color='#FF8C00', linestyle='--', alpha=0.8, linewidth=1.5, zorder=3, label=f'Break-even CAC (${break_even_cac:.2f})')

    ax_cac.set_title('Growth ROI Sensitivity to CAC Changes', fontsize=16, pad=20, fontweight='bold', color='#000000')
    ax_cac.set_xlabel('Customer Acquisition Cost ($)', fontsize=12, labelpad=10, fontweight='bold', color='#000000')
    ax_cac.set_ylabel('Growth ROI (%)', fontsize=12, labelpad=10, fontweight='bold', color='#000000')
    ax_cac.spines['top'].set_visible(False)
    ax_cac.spines['right'].set_visible(False)
    ax_cac.spines['left'].set_color('#000000')
    ax_cac.spines['bottom'].set_color('#000000')
    ax_cac.tick_params(axis='both', labelsize=10, colors='#000000')
    ax_cac.grid(True, linestyle='--', alpha=0.3, color='#000000')

    cbar = fig_cac.colorbar(points, ax=ax_cac, pad=0.01)
    cbar.set_label('Growth ROI (%)', rotation=270, labelpad=20, fontweight='bold', color='#000000')
    cbar.ax.tick_params(colors='#000000')
    ax_cac.legend(loc='lower right', frameon=True, framealpha=0.9, facecolor='#FFFFFF', edgecolor='#000000')

    plt.tight_layout()
    st.pyplot(fig_cac)

    highest_roi_cac = sensitivity_cac.loc[sensitivity_cac['Growth ROI (%)'].idxmax(), 'CAC ($)']
    is_optimum_lower = highest_roi_cac < cac
    insight_class = "recommendation-good" if is_optimum_lower else "recommendation-bad"
    
    st.markdown(f"""
    <div class="{insight_class} recommendation-box">
        <p style="margin: 0; font-size: 15px;">
            <strong>Key Insight:</strong> Your optimum CAC for maximum ROI is 
            <strong>${highest_roi_cac:.2f}</strong>. 
            {"This is <strong>"
             + f"${(cac - highest_roi_cac):.2f} less</strong> than your current CAC." 
             if is_optimum_lower else 
             "This is <strong>"
             + f"${(highest_roi_cac - cac):.2f} more</strong> than your current CAC."}
        </p>
    </div>
    """, unsafe_allow_html=True)

# Growth Strategy Recommendations
st.subheader("Growth Strategy Recommendations")

overall_health_score = 0
health_factors = 0

ltv_cac_health = "Good" if ltv_cac_ratio >= 3 else "Needs Improvement"
if ltv_cac_health == "Good":
    overall_health_score += 1
health_factors += 1

growth_roi_health = "Good" if growth_roi >= 20 else "Needs Improvement"
if growth_roi_health == "Good":
    overall_health_score += 1
health_factors += 1

churn_health = "Good" if churn_rate <= 0.05 else "Needs Improvement"
if churn_health == "Good":
    overall_health_score += 1
health_factors += 1

expansion_health = "Good" if expansion_revenue >= 0.1 else "Needs Improvement"
if expansion_health == "Good":
    overall_health_score += 1
health_factors += 1

referral_health = "Good" if referral_revenue_impact >= 0.15 else "Needs Improvement"
if referral_health == "Good":
    overall_health_score += 1
health_factors += 1

overall_health_percentage = (overall_health_score / health_factors) * 100

if overall_health_percentage >= 80:
    recommendation_message = (
        "Your growth strategy is robust. Consider reinvesting in high-performing channels "
        "and further optimizing upsell and referral programs."
    )
    recommendation_class = "recommendation-good"
    border_color = "#006400"
elif overall_health_percentage >= 50:
    recommendation_message = (
        "Your metrics are moderately healthy. Focus on improving churn and conversion rates, "
        "and consider targeted investments in product improvements."
    )
    recommendation_class = ""
    border_color = "#000000"
else:
    recommendation_message = (
        "Your current metrics indicate significant room for improvement. Reassess your customer acquisition strategy, "
        "churn management, and invest in product enhancements."
    )
    recommendation_class = "recommendation-bad"
    border_color = "#8B0000"

if overall_health_percentage >= 80:
    recommendation_class = "recommendation-good"
elif overall_health_percentage >= 50:
    recommendation_class = "recommendation-neutral"
else:
    recommendation_class = "recommendation-bad"

st.markdown(f"""
<div class="{recommendation_class} recommendation-box">
    <p style="margin: 0; font-size: 15px;">
        <strong>Overall Health Score:</strong> {overall_health_score}/{health_factors} ({overall_health_percentage:.0f}%)
    </p>
    <p style="margin-top: 10px; font-size: 15px;">{recommendation_message}</p>
</div>
""", unsafe_allow_html=True)

# Add a spacer at the bottom for better layout
st.markdown("<br><br>", unsafe_allow_html=True)