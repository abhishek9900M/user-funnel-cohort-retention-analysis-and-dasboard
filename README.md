# Product Funnel & Retention Analysis And Dashboard

A data analytics project designed to understand user acquisition, engagement, conversion, and retention through event-level user data.

The project uses Python to generate user activity data and supports SQL-based analysis and Power BI visualization to identify funnel drop-offs and user retention patterns.

## Project Objectives

- Generate realistic daily user activity data.
- Track user journeys from app visits to purchases.
- Analyze conversion rates across funnel stages.
- Identify where users drop off during the journey.
- Measure daily and weekly user retention.
- Analyze user behavior across different cohorts.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | User data generation and processing |
| SQL Server | Data storage and querying |
| Power BI | Dashboard and data visualization |
| Excel / CSV | Data storage and reporting |

## Project Workflow

1. **Data Generation:** Generate simulated users and their activities using Python.
2. **Data Processing:** Organize user events with timestamps and user IDs.
3. **Database Storage:** Store generated user activity data in SQL Server.
4. **Data Analysis:** Use SQL to calculate funnel conversion, drop-offs, and retention.
5. **Visualization:** Build interactive Power BI dashboards to analyze user behavior.

## Key Analytics

### 1. User Funnel Analysis

Track users through these stages:

- App Visit
- Search Used
- Signup
- Activation
- Wishlist Used
- Purchase

Analyze the number of users reaching each stage and calculate conversion and drop-off rates.

### 2. Cohort Analysis

Group users based on their first activity date and track their return behavior over subsequent days.

Key metrics:
- Daily Retained Users
- Daily Retention Rate
- Cohort Retention
- Returning Users
- New Users

### 3. User Activity Analysis

Analyze:
- Daily new users
- Daily active users
- Feature adoption
- User engagement
- Purchase activity

## Sample Project Structure

```text
Product-Funnel-Retention-Dashboard/
│
├── users.csv
├── data.sql
├── main.py
├── requirements.txt
├── README.md
│
├── database/
│   └── database_queries.sql
│
└── dashboard/
    └── PowerBI_Dashboard.pbix
```

*Update this structure to match your actual repository files.*

## Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Product-Funnel-Retention-Dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Python Project

```bash
python main.py
```

### 4. Database Setup

- Open SQL Server.
- Execute the SQL scripts in `data.sql`.
- Configure your database connection.
- Load the generated user activity data.

### 5. Power BI Dashboard

Open the Power BI project file and connect it to your SQL Server database to explore user analytics.

## Expected Outcomes

- Understand the complete user journey.
- Identify conversion bottlenecks.
- Measure user retention across cohorts.
- Monitor daily user activity.
- Support data-driven product decisions.

## Project Type

**End-to-End Data Analytics Project**

Python | SQL Server | Power BI | Excel

---

**Disclaimer:** This project uses simulated user activity data for educational and analytical purposes.
