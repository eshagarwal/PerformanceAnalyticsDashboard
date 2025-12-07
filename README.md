# Amazon Diwali Sales 2025 Dashboard

A interactive analytics dashboard for visualizing Amazon sales data during Diwali 2025.

<!-- ## Demo Link -> <https://28ff7ed7-4257-4098-9cb2-bf156c235b54.plotly.app/> -->

## Features

- **Real-time KPIs**: Total revenue, orders, average ratings, and top category
- **Sales Trends**: Daily sales performance tracking
- **Payment Analysis**: Distribution of payment methods
- **Product Insights**: Category and product breakdown with sunburst chart
- **Geographic View**: Sales by state with interactive map
- **Customer Satisfaction**: Rating distribution across categories
- **Logistics Tracking**: Delivery status monitoring

## Installation

1. Clone the repository
2. Install dependencies using [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
uv sync
```

## Usage

Run the dashboard:

```bash
uv run app/app.py
```

Open your browser to `http://127.0.0.1:8050`

## Data Source

Uses the Amazon Product Sales 2025 dataset from Kaggle (anandshaw2001/amazon-product-sales-2025)

## Technologies

- Dash & Plotly for visualizations
- Pandas for data processing
- VADER for sentiment analysis
- Bootstrap (Flatly theme) for styling


## Video Demo

https://github.com/user-attachments/assets/6612a49c-ed6f-4983-a228-4be369f7252f

