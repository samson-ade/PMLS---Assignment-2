import os
from typing import Optional
import pandas as pd
import numpy as np

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(
    title= "Skin Clinic Campaign Analysis API",
    description= "API for marketing campaign segmentation and response analysis, optimised for Microsoft Excel Power Query integration.",
    version= "2.0.0"
)

# Load dataset
file_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(file_dir, "skin clinic campaign.csv")
data = pd.read_csv(data_path)

# Categorise customers based on unique products purchased in the last year
data['Product_Usage'] = pd.cut(
    data['Unique_Products_Purchased'],
    bins= [0, 4, 8, np.inf],
    labels= ['1-4', '5-8', '>8']
)

def calculate_response_rate(df: pd.DataFrame, column: str, category_order: Optional[list] = None) -> pd.DataFrame:
    """Calculate campaign response rates across customer segments."""
    categories = category_order if category_order else list(df[column].dropna().unique())
    results = []
    
    for category in categories:
        category_data = df[df[column] == category]
        total_customers = len(category_data)
        responders = int((category_data['Response_to_Campaign'] == 'Yes').sum())
        non_responders = total_customers - responders
        response_rate = round((responders / total_customers * 100), 2) if total_customers > 0 else 0.0
        
        results.append({
            "segment": str(category),
            "total_customers": total_customers,
            "responders": responders,
            "non_responders": non_responders,
            "response_rate_pct": response_rate
        })
        
    return pd.DataFrame(results)

# Generate tables for each customer segment
gender_table = calculate_response_rate(data, "Gender", category_order= ["Female", "Male"])
age_table = calculate_response_rate(data, "AgeGroup", category_order= ["<30", "30-50", ">50"])
purchase_table = calculate_response_rate(data, "Purchase_Last_Quarter", category_order= ["Yes", "No"])
product_usage_table = calculate_response_rate(data, "Product_Usage", category_order= ["1-4", "5-8", ">8"])

# Generate consolidated summary table
consolidated_list = []
for dim_name, df_dim in [
    ("Gender", gender_table),
    ("Age Group", age_table),
    ("Purchase Last Quarter", purchase_table),
    ("Product Usage", product_usage_table)
]:
    df_copy = df_dim.copy()
    df_copy.insert(0, "dimension", dim_name)
    consolidated_list.append(df_copy)
consolidated_table = pd.concat(consolidated_list, ignore_index= True)


@app.get("/")
def home():
    return {
        "title": "Skin Clinic Campaign Analysis API",
        "version": "2.0.0",
        "description": "API designed to power Microsoft Excel Power Query and web dashboards.",
        "endpoints": {
            "/campaign-analysis": "Tabular HTML output for Excel Power Query (Get Data -> From Web)",
            "/campaign-analysis?format=json": "JSON formatted campaign analysis data",
            "/api/campaign-analysis": "Direct JSON endpoint with all segmentation tables",
            "/docs": "Interactive FastAPI Swagger documentation"
        },
        "excel_instructions": "In Excel, go to Data -> Get Data -> From Web, paste your hosted endpoint URL (/campaign-analysis), select the tables, and click Load."
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "total_records_loaded": len(data)}


@app.get("/api/campaign-analysis")
def get_campaign_analysis_json():
    return {
        "gender_analysis": gender_table.to_dict(orient= "records"),
        "age_group_analysis": age_table.to_dict(orient= "records"),
        "purchase_last_quarter_analysis": purchase_table.to_dict(orient= "records"),
        "product_usage_analysis": product_usage_table.to_dict(orient= "records"),
        "consolidated_summary": consolidated_table.to_dict(orient= "records")
    }


@app.get("/campaign-analysis", response_class= HTMLResponse)
def get_campaign_analysis(request: Request, format: Optional[str] = None):
    # Support JSON requests via query param or Accept header
    accept_header = request.headers.get("accept", "")
    if format == "json" or "application/json" in accept_header and "text/html" not in accept_header:
        return JSONResponse(content= get_campaign_analysis_json())

    # Build clean HTML tables for Excel Power Query
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skin Clinic Campaign Analysis</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: #ffffff;
            padding: 36px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #0f172a;
            margin-top: 0;
            font-size: 26px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 12px;
        }}
        .subtitle {{
            color: #64748b;
            font-size: 15px;
            margin-bottom: 25px;
        }}
        .notice {{
            background: #ecfdf5;
            border-left: 4px solid #10b981;
            padding: 14px 18px;
            border-radius: 6px;
            margin-bottom: 30px;
            font-size: 14px;
            color: #065f46;
        }}
        h2 {{
            color: #1e3a8a;
            font-size: 19px;
            margin-top: 32px;
            margin-bottom: 12px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 28px;
            font-size: 14px;
        }}
        caption {{
            caption-side: top;
            text-align: left;
            font-weight: 600;
            color: #475569;
            margin-bottom: 8px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{
            background-color: #f1f5f9;
            color: #334155;
            font-weight: 600;
            border-top: 1px solid #cbd5e1;
            border-bottom: 2px solid #cbd5e1;
        }}
        tr:hover {{
            background-color: #f8fafc;
        }}
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
            background: #e0f2fe;
            color: #0369a1;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
            font-size: 12px;
            color: #94a3b8;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Skin Clinic Marketing Campaign Analysis</h1>
        <p class="subtitle">API Endpoint serving customer segmentation & response performance for Excel Power Query</p>

        <div class="notice">
            <strong>Power Query Quick Connect:</strong> In Excel, navigate to <em>Data &rarr; Get Data &rarr; From Web</em>, paste this endpoint URL, and select the desired tables from the navigator to import directly into your spreadsheet.
        </div>

        <h2>1. Gender vs Campaign Response</h2>
        <table id="gender_table">
            <caption>Gender Segment Response Analysis</caption>
            <thead>
                <tr>
                    <th>Segment</th>
                    <th>Total Customers</th>
                    <th>Responders</th>
                    <th>Non-Responders</th>
                    <th>Response Rate (%)</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f"<tr><td><strong>{row['segment']}</strong></td><td>{row['total_customers']:,}</td><td>{row['responders']:,}</td><td>{row['non_responders']:,}</td><td><span class='badge'>{row['response_rate_pct']}%</span></td></tr>" for _, row in gender_table.iterrows())}
            </tbody>
        </table>

        <h2>2. Age Group vs Campaign Response</h2>
        <table id="age_table">
            <caption>Age Group Segment Response Analysis</caption>
            <thead>
                <tr>
                    <th>Segment</th>
                    <th>Total Customers</th>
                    <th>Responders</th>
                    <th>Non-Responders</th>
                    <th>Response Rate (%)</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f"<tr><td><strong>{row['segment']}</strong></td><td>{row['total_customers']:,}</td><td>{row['responders']:,}</td><td>{row['non_responders']:,}</td><td><span class='badge'>{row['response_rate_pct']}%</span></td></tr>" for _, row in age_table.iterrows())}
            </tbody>
        </table>

        <h2>3. Purchase in Last Quarter vs Campaign Response</h2>
        <table id="purchase_table">
            <caption>Purchase In Last Quarter Response Analysis</caption>
            <thead>
                <tr>
                    <th>Segment</th>
                    <th>Total Customers</th>
                    <th>Responders</th>
                    <th>Non-Responders</th>
                    <th>Response Rate (%)</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f"<tr><td><strong>{row['segment']}</strong></td><td>{row['total_customers']:,}</td><td>{row['responders']:,}</td><td>{row['non_responders']:,}</td><td><span class='badge'>{row['response_rate_pct']}%</span></td></tr>" for _, row in purchase_table.iterrows())}
            </tbody>
        </table>

        <h2>4. Product Usage vs Campaign Response</h2>
        <table id="product_usage_table">
            <caption>Product Usage Segment Response Analysis</caption>
            <thead>
                <tr>
                    <th>Segment</th>
                    <th>Total Customers</th>
                    <th>Responders</th>
                    <th>Non-Responders</th>
                    <th>Response Rate (%)</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f"<tr><td><strong>{row['segment']}</strong></td><td>{row['total_customers']:,}</td><td>{row['responders']:,}</td><td>{row['non_responders']:,}</td><td><span class='badge'>{row['response_rate_pct']}%</span></td></tr>" for _, row in product_usage_table.iterrows())}
            </tbody>
        </table>

        <h2>5. Consolidated Summary (All Segments)</h2>
        <table id="consolidated_table">
            <caption>Consolidated Campaign Analysis Table</caption>
            <thead>
                <tr>
                    <th>Dimension</th>
                    <th>Segment</th>
                    <th>Total Customers</th>
                    <th>Responders</th>
                    <th>Non-Responders</th>
                    <th>Response Rate (%)</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f"<tr><td>{row['dimension']}</td><td><strong>{row['segment']}</strong></td><td>{row['total_customers']:,}</td><td>{row['responders']:,}</td><td>{row['non_responders']:,}</td><td><span class='badge'>{row['response_rate_pct']}%</span></td></tr>" for _, row in consolidated_table.iterrows())}
            </tbody>
        </table>

        <footer>
            Skin Clinic Campaign Intelligence API &bull; M10 PMLS Assignment 2 &bull; Developed for Excel Power Query
        </footer>
    </div>
</body>
</html>
"""
    return html_content
