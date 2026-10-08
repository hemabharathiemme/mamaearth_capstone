# analysis/visualize.py
import matplotlib.pyplot as plt
import os

def build_plots():
    os.makedirs("visualizations", exist_ok=True)
    
    # Chart 1: Return Rates Graph Asset
    methods = ['CARD', 'UPI', 'COD']
    rates = [14.7, 18.9, 44.4]
    plt.figure(figsize=(6,4))
    plt.bar(methods, rates, color=['#2ecc71','#3498db','#e74c3c'], edgecolor='black')
    plt.title("COD Returns at 44.4% - 3x Card")
    plt.ylabel("Return Rate (%)")
    plt.savefig("visualizations/return_rate_by_payment.png", bbox_inches='tight')
    plt.close()

    # Chart 2: Revenue Trend Line Asset
    months = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06']
    rev = [11637.10, 13195.50, 20318.90, 9495.30, 13151.10, 11615.40]
    plt.figure(figsize=(7,4))
    plt.plot(months, rev, marker='o', color='#16a085', linewidth=2)
    plt.title("Corrected Monthly Trend: Peak Performance Occurs in March (2026-03)")
    plt.ylabel("Revenue (INR)")
    plt.savefig("visualizations/monthly_revenue_trend.png", bbox_inches='tight')
    plt.close()
    print("✓ charts generated inside visualizations/ folder.")

if __name__ == "__main__":
    build_plots()
