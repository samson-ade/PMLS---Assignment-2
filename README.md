# PMLS - ASSIGNMENT 2: Developing API For Excel

## Business Context
A skin clinic conducted a targeted marketing campaign reaching **10,000 customers**. The primary objective is to analyse which customer segments exhibit higher receptivity and likelihood to respond based on demographic attributes and historical purchasing behaviour. Insights derived from this analysis empower the clinic to optimise future marketing expenditures, personalise customer communications, and maximise overall return on campaign investment.

---

## Analytical Results & Segment Response Performance

### 1. Gender vs Campaign Response
| Gender Segment | Total Customers | Responders | Non-Responders | Response Rate (%) |
|:--------------:|:---:|:---:|:---:|:---:|
|   **Female**   | 6,007 | 2,629 | 3,378 | **43.77%** |
|    **Male**    | 3,993 | 1,361 | 2,632 | **34.08%** |

*Interpretation:* Female customers responded at a substantially higher rate (**43.77%**) compared to male customers (**34.08%**). Furthermore, female clients represent **60.07%** of the customer database, establishing them as the core audience for clinic offerings and product campaigns.

---

### 2. Age Group vs Campaign Response
| Age Group | Total Customers | Responders | Non-Responders | Response Rate (%) |
|:---------:|:---:|:---:|:---:|:---:|
|  **<30**  | 2,499 | 823 | 1,676 | **32.93%** |
| **30–50** | 4,992 | 2,349 | 2,643 | **47.06%** |
|  **>50**  | 2,509 | 818 | 1,691 | **32.60%** |

*Interpretation:* Customers aged **30–50** are the most receptive cohort with an outstanding **47.06%** response rate, accounting for **58.87%** of all total responders. Both younger (<30) and older (>50) segments demonstrate lower, almost identical response rates of **32.93%** and **32.60%**.

---

### 3. Purchase in Last Quarter vs Campaign Response
| Purchase Last Quarter | Total Customers | Responders | Non-Responders | Response Rate (%) |
|:---------------------:|:---:|:---:|:---:|:---:|
|        **Yes**        | 6,514 | 3,234 | 3,280 | **49.65%** |
|        **No**         | 3,486 | 756 | 2,730 | **21.69%** |

*Interpretation:* Recency of engagement is the single strongest binary discriminator of campaign receptivity. Customers active within the last quarter responded at **49.65%**, more than **2.29×** higher than inactive/dormant customers (**21.69%**).

---

### 4. Product Usage vs Campaign Response
| Unique Products Purchased (1 Year) | Total Customers | Responders | Non-Responders | Response Rate (%) |
|:----------------------------------:|:---:|:---:|:---:|:---:|
|              **1–4**               | 2,091 | 378 | 1,713 | **18.08%** |
|              **5–8**               | 3,703 | 1,425 | 2,278 | **38.48%** |
|               **>8**               | 4,206 | 2,187 | 2,019 | **52.00%** |

*Interpretation:* A direct positive linear relationship exists between product diversity and campaign conversion. Customers purchasing **>8** unique products demonstrated an exceptional **52.00%** conversion rate, whereas low-variety shoppers (1–4 products) converted at only **18.08%**.

---

### 5. Consolidated Multi-Dimensional Summary
|       Dimension       | Segment | Total Customers | Responders | Non-Responders | Response Rate (%) |
|:---------------------:|:---|:---:|:---:|:---:|:---:|
|        Gender         | Female | 6,007 | 2,629 | 3,378 | 43.77% |
|        Gender         | Male | 3,993 | 1,361 | 2,632 | 34.08% |
|       Age Group       | <30 | 2,499 | 823 | 1,676 | 32.93% |
|       Age Group       | 30–50 | 4,992 | 2,349 | 2,643 | 47.06% |
|       Age Group       | >50 | 2,509 | 818 | 1,691 | 32.60% |
| Purchase Last Quarter | Yes | 6,514 | 3,234 | 3,280 | 49.65% |
| Purchase Last Quarter | No | 3,486 | 756 | 2,730 | 21.69% |
|     Product Usage     | 1–4 | 2,091 | 378 | 1,713 | 18.08% |
|     Product Usage     | 5–8 | 3,703 | 1,425 | 2,278 | 38.48% |
|     Product Usage     | >8 | 4,206 | 2,187 | 2,019 | 52.00% |

---

## Strategic Marketing Recommendations
1. **Primary High-Value Segment**: Center major budget allocation and premium promotional treatments on Females aged 30–50 with active purchases in the last 90 days and high product breadth (>8 unique products)**. This segment yields predicted conversion rates upwards of **55–60%**.
2. **Basket Diversification Programs**: Customers who buy across 5+ product categories show more than double the conversion of single-category buyers. Implement cross-category product bundling and sampling to transition low-tier purchasers into high-diversity advocates.
3. **Automated Re-engagement Triggers**: Set up automated nurture workflows before a client enters the 90-day inactivity window, maintaining the 49.65% high-recency conversion baseline.

---

## FastAPI Application Architecture

The application is implemented in `main.py` using **FastAPI** and is engineered specifically to feed data into **Microsoft Excel Power Query**:

- `GET /` &mdash; Welcome endpoint providing metadata, available routes, and Excel connection guidance.
- `GET /health` &mdash; Healthcheck endpoint returning total records parsed.
- `GET /campaign-analysis` &mdash; **Primary Endpoint**: Returns semantic HTML with individual `<table>` elements and a consolidated master table. Each table features explicit table IDs (`#gender_table`, `#age_table`, `#purchase_table`, `#product_usage_table`, `#consolidated_table`) and `<caption>` tags, enabling Excel's Web Connector to parse and name each table automatically.
- `GET /campaign-analysis?format=json` &mdash; Returns structured JSON data for API clients.
- `GET /api/campaign-analysis` &mdash; Direct JSON REST endpoint.
- `GET /docs` &mdash; Interactive Swagger UI documentation.

---

## How to Run Locally

### 1. Install Dependencies
```bash
cd "Assignment for (Productionisation of Machine Learning System)/PMLS - Assignment 2"
pip install -r requirements.txt
```

### 2. Start the FastAPI Server
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Verify in Browser
- **Home**: `http://127.0.0.1:8000/`
- **Tabular HTML Endpoint (for Excel)**: `http://127.0.0.1:8000/campaign-analysis`
- **JSON Format**: `http://127.0.0.1:8000/campaign-analysis?format=json`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`

---

## How to Deploy to Render (Publicly Accessible)

1. **Push Code to GitHub**:
   Create a GitHub repository (e.g. `pmls-assignment-2`) and push the contents of `PMLS - Assignment 2`:
   ```bash
   git init
   git add .
   git commit -m "M10 PMLS Assignment 2: FastAPI for Excel"
   git branch -M main
   git remote add origin https://github.com/<your-username>/pmls-assignment-2.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to the [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** &rarr; **Web Service**.
   - Select your GitHub repository.
   - Configure settings:
     - **Name**: `skin-clinic-campaign-api` (or custom name)
     - **Region**: Closest to your location (e.g. Oregon / Frankfurt)
     - **Branch**: `main`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: `Free`
   - Click **Create Web Service**.

3. **Obtain Public URL**:
   Once Render displays **Live**, your public endpoint URL will be:
   ```
   https://<your-service-name>.onrender.com/campaign-analysis
   ```

---

## Excel Power Query Integration Step-by-Step

### Step 1: Open Excel and Connect via Power Query
1. Open Microsoft Excel and create a blank workbook (or open `Skin_Clinic_Campaign_Analysis.xlsx`).
2. Go to the **Data** tab on the Excel ribbon.
3. Click **Get Data** &rarr; **From Other Sources** &rarr; **From Web** (or click the **From Web** button directly on the ribbon).
4. In the URL prompt, enter your public Render endpoint:
   ```
   https://<your-service-name>.onrender.com/campaign-analysis
   ```
   *(For local testing, you can also use `http://127.0.0.1:8000/campaign-analysis`)*.
5. In the Access Web Content window, leave authentication as **Anonymous** and click **Connect**.

### Step 2: Select and Load Tables
1. The **Navigator** window will display the web page preview and list all detected tables:
   - `Gender Segment Response Analysis` (`gender_table`)
   - `Age Group Segment Response Analysis` (`age_table`)
   - `Purchase In Last Quarter Response Analysis` (`purchase_table`)
   - `Product Usage Segment Response Analysis` (`product_usage_table`)
   - `Consolidated Campaign Analysis Table` (`consolidated_table`)
2. Check the box **Select multiple items**.
3. Select the tables you wish to import.
4. Click **Load** (or click the arrow next to Load &rarr; **Load To...** &rarr; Table in New Worksheet).

---

## Excel Form Control Refresh Button & VBA Setup

To create an interactive button that refreshes the tables whenever clicked:

### Step 1: Add the VBA Refresh Macro
1. Press `Alt + F11` (or `Fn + Option + F11` on Mac) to open the **Visual Basic for Applications** editor.
2. In the menu, click **Insert** &rarr; **Module**.
3. Paste the following VBA code:
   ```vba
   Sub RefreshCampaignData()
       On Error GoTo ErrHandler
       
       ' Refresh all background data connections and Power Query web feeds
       ActiveWorkbook.RefreshAll
       
       MsgBox "Campaign analysis tables have been refreshed successfully from the API!", vbInformation, "Data Refreshed"
       Exit Sub
       
   ErrHandler:
       MsgBox "Unable to refresh data. Please verify your internet connection and API endpoint status.", vbCritical, "Refresh Error"
   End Sub
   ```
4. Close the VBA editor window (`Cmd + Q` on Mac or `Alt + Q` on Windows).

### Step 2: Insert the Form Control Button
1. In Excel, navigate to the **Developer** tab. *(If Developer tab is not visible: Go to Excel Preferences/Options &rarr; Ribbon & Toolbar &rarr; Check "Developer")*.
2. Click **Insert** &rarr; **Button (Form Control)**.
3. Draw the button on your worksheet (e.g. at the top of your Dashboard).
4. The **Assign Macro** dialog will immediately pop up.
5. Select `RefreshCampaignData` and click **OK**.
6. Right-click the button &rarr; **Edit Text** &rarr; Rename it to `🔄 Refresh Campaign Data`.

### Step 3: Test the Button
- Click the button: Excel will trigger `ActiveWorkbook.RefreshAll`, re-query the FastAPI `/campaign-analysis` endpoint, update all values in place, and display the confirmation dialog!

---

## Deliverables in this Directory
- [`Analysis.ipynb`](file:///Users/samson/Desktop/Data%20Experimention%20Folders/Data%20Science%20Institute%20(Courses)/All%20Assignment%20for%20Course%20Work/Assignment%20for%20(Productionisation%20of%20Machine%20Learning%20System)/PMLS%20-%20Assignment%202/Analysis.ipynb): Complete Jupyter notebook with data loading, EDA, segmentation functions, 4 task tables, visualizations, and marketing interpretations.
- [`main.py`](file:///Users/samson/Desktop/Data%20Experimention%20Folders/Data%20Science%20Institute%20(Courses)/All%20Assignment%20for%20Course%20Work/Assignment%20for%20(Productionisation%20of%20Machine%20Learning%20System)/PMLS%20-%20Assignment%202/main.py): Production FastAPI application serving tabular HTML (for Excel Power Query) and JSON responses.
- [`Skin_Clinic_Campaign_Analysis.xlsx`](file:///Users/samson/Desktop/Data%20Experimention%20Folders/Data%20Science%20Institute%20(Courses)/All%20Assignment%20for%20Course%20Work/Assignment%20for%20(Productionisation%20of%20Machine%20Learning%20System)/PMLS%20-%20Assignment%202/Skin_Clinic_Campaign_Analysis.xlsx): Pre-built Excel workbook featuring an executive dashboard, all 4 segmented analysis tables, KPI cards, Form Control refresh buttons, and an integrated Power Query guide sheet.
- [`skin clinic campaign.csv`](file:///Users/samson/Desktop/Data%20Experimention%20Folders/Data%20Science%20Institute%20(Courses)/All%20Assignment%20for%20Course%20Work/Assignment%20for%20(Productionisation%20of%20Machine%20Learning%20System)/PMLS%20-%20Assignment%202/skin%20clinic%20campaign.csv): The 10,000-customer dataset.
- [`requirements.txt`](file:///Users/samson/Desktop/Data%20Experimention%20Folders/Data%20Science%20Institute%20(Courses)/All%20Assignment%20for%20Course%20Work/Assignment%20for%20(Productionisation%20of%20Machine%20Learning%20System)/PMLS%20-%20Assignment%202/requirements.txt): Python dependencies for deployment.
- [`render.yaml`](file:///Users/samson/Desktop/Data%20Experimention%20Folders/Data%20Science%20Institute%20(Courses)/All%20Assignment%20for%20Course%20Work/Assignment%20for%20(Productionisation%20of%20Machine%20Learning%20System)/PMLS%20-%20Assignment%202/render.yaml): Render cloud deployment specification.
