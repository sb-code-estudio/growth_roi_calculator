# Growth ROI Calculator

An interactive tool that goes beyond traditional LTV:CAC metrics to provide deeper insights into growth economics by incorporating churn risk, expansion revenue, and referral impact.

Try it out here! 
[https://marketing-growth-roi-calculator.streamlit.app/]

## Overview

This calculator helps growth teams and founders make better decisions by visualizing how different factors affect their true ROI. Unlike simple LTV:CAC calculations, this tool considers:

- **Customer Acquisition Cost (CAC)**: The cost to acquire a new customer
- **Customer Lifetime Value (LTV)**: The revenue generated from a customer
- **Churn Rate**: How it erodes potential revenue
- **Expansion Revenue**: Additional revenue from existing customers
- **Referral Impact**: The multiplier effect of organic growth

## Features

- **True Growth ROI Calculation**: Accurate measurement incorporating all growth factors
- **Break-Even CAC Analysis**: Know exactly what you can afford to pay for acquisition
- **Revenue Composition Visualization**: See where your revenue comes from and goes
- **Sensitivity Analysis**: Understand how changes to different metrics impact your ROI
- **Strategic Recommendations**: Get actionable insights based on your metrics

## Getting Started

### Prerequisites
- Python 3.7+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- NumPy

### Installation

```bash
# Clone the repository
git clone https://github.com/sebastians-estudio/growth-roi-calculator.git

# Navigate to the project directory
cd growth-roi-calculator

# Install dependencies
pip install streamlit pandas matplotlib seaborn numpy

# Run the application
streamlit run growth_roi_calculator.py

Usage

Input your financial metrics in the sidebar:

Customer Acquisition Cost (CAC)
Customer Lifetime Value (LTV)
Total Ad Spend
Retention Costs
Product & Engineering Costs


Set your performance metrics:

Churn Rate
Conversion Rate
Expansion Revenue
Referral Revenue Impact


The dashboard will automatically calculate and display:

True Growth ROI
Break-Even CAC
Traditional LTV:CAC Ratio
Revenue composition analysis
Sensitivity to CAC and churn changes
Strategic recommendations


License
MIT License# Repo Updated
