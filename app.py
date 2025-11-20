import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import kagglehub
from kagglehub import KaggleDatasetAdapter

# =============================================================================
# 1. DATA LOADING
# =============================================================================
# Set the path to the file you'd like to load
file_path = "amazon_sales_2025_INR.csv"

# Load the latest version
df = kagglehub.dataset_load(
    KaggleDatasetAdapter.PANDAS,
    "anandshaw2001/amazon-product-sales-2025",
    file_path,
)
geo_df = pd.read_csv("states_geo.csv")
df = df.merge(geo_df, on="State", how="left")
del geo_df

# =============================================================================
# 2. APP SETUP & THEME (CLEAN WHITE)
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Professional Color Palette
colors = {
    "background": "#ecf0f1",  # Very light grey for page background (reduces eye strain)
    "text": "#2c3e50",  # Dark Blue-Grey (Standard for text)
    "primary": "#2c3e50",  # Matching primary color
    "card_bg": "#ffffff",  # Pure white for cards
}

# =============================================================================
# 3. LAYOUT
# =============================================================================
app.layout = dbc.Container(
    [
        # --- Header ---
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H1("Amazon Diwali Sales 2025", className="display-4"),
                            html.P("Performance Analytics Dashboard", className="lead"),
                        ],
                        className="text-center p-4 mb-4",
                        style={
                            "backgroundColor": "white",
                            "boxShadow": "0px 2px 5px rgba(0,0,0,0.1)",
                        },
                    ),
                    width=12,
                )
            ]
        ),
        # --- KPI Cards (Simple, Clean Stats) ---
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Total Revenue", className="text-muted"),
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"₹ {df['Total_Sales_INR'].sum():,.0f}",
                                        className="text-primary font-weight-bold",
                                    )
                                ]
                            ),
                        ],
                        color="light",
                        outline=True,
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Total Orders", className="text-muted"),
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"{len(df):,}",
                                        className="text-success font-weight-bold",
                                    )
                                ]
                            ),
                        ],
                        color="light",
                        outline=True,
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Avg. Rating", className="text-muted"),
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"{df['Review_Rating'].mean():.1f} / 5.0",
                                        className="text-warning font-weight-bold",
                                    )
                                ]
                            ),
                        ],
                        color="light",
                        outline=True,
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Top Category", className="text-muted"),
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"{df['Product_Category'].mode()[0]}",
                                        className="text-danger font-weight-bold",
                                    )
                                ]
                            ),
                        ],
                        color="light",
                        outline=True,
                    ),
                    width=3,
                ),
            ],
            className="mb-4",
        ),
        # --- Row 2: Trend & Payment ---
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Daily Sales Trend", className="font-weight-bold"
                                ),
                                dbc.CardBody(dcc.Graph(id="trend-line")),
                            ],
                            style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                        )
                    ],
                    width=8,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Payment Methods", className="font-weight-bold"
                                ),
                                dbc.CardBody(dcc.Graph(id="payment-donut")),
                            ],
                            style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                        )
                    ],
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        # --- Row 3: Product Hierarchy & States ---
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Category & Product Breakdown",
                                    className="font-weight-bold",
                                ),
                                dbc.CardBody(dcc.Graph(id="product-sunburst")),
                            ],
                            style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Sales by Region (State)",
                                    className="font-weight-bold",
                                ),
                                dbc.CardBody(dcc.Graph(id="state-bar")),
                            ],
                            style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                        )
                    ],
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        # --- Row 4: Ratings & Logistics ---
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Customer Satisfaction Distribution",
                                    className="font-weight-bold",
                                ),
                                dbc.CardBody(dcc.Graph(id="rating-box")),
                            ],
                            style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Logistics & Delivery Status",
                                    className="font-weight-bold",
                                ),
                                dbc.CardBody(dcc.Graph(id="delivery-stack")),
                            ],
                            style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                        )
                    ],
                    width=6,
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
    style={"backgroundColor": colors["background"], "paddingBottom": "50px"},
)


# =============================================================================
# 4. CALLBACKS
# =============================================================================
@app.callback(
    [
        Output("trend-line", "figure"),
        Output("payment-donut", "figure"),
        Output("product-sunburst", "figure"),
        Output("state-bar", "figure"),
        Output("rating-box", "figure"),
        Output("delivery-stack", "figure"),
    ],
    [Input("trend-line", "id")],
)
def update_charts(_):
    clean_template = "plotly_white"

    # 1. Line Chart
    daily_sales = df.groupby("Date")["Total_Sales_INR"].sum().reset_index()
    fig_line = px.line(
        daily_sales,
        x="Date",
        y="Total_Sales_INR",
        template=clean_template,
        markers=True,
    )
    fig_line.update_traces(line_color="#2c3e50", marker=dict(size=8, color="#e74c3c"))
    fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    # 2. Donut Chart
    fig_donut = px.pie(
        df,
        names="Payment_Method",
        values="Total_Sales_INR",
        hole=0.4,
        template=clean_template,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    # 3. Sunburst Chart
    fig_sun = px.sunburst(
        df,
        path=["Product_Category", "Product_Name"],
        values="Total_Sales_INR",
        template=clean_template,
        color="Total_Sales_INR",
        color_continuous_scale="Blues",
    )

    # 4. State Map
    fig_geo = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Total_Sales_INR",
        hover_name="State",
        template=clean_template,
        color_continuous_scale="Viridis",
    )
    india = 20.5937, 78.9629
    fig_geo.update_geos(
        center=dict(lat=india[0], lon=india[1]),
        projection_scale=10,
    )

    # 5. Box Plot
    fig_box = px.box(
        df,
        x="Product_Category",
        y="Review_Rating",
        color="Product_Category",
        template=clean_template,
    )

    # 6. Stacked Bar (Delivery)
    del_stats = (
        df.groupby(["State", "Delivery_Status"]).size().reset_index(name="Count")
    )
    fig_stack = px.bar(
        del_stats,
        x="State",
        y="Count",
        color="Delivery_Status",
        template=clean_template,
        color_discrete_map={
            "Delivered": "#2ecc71",
            "Pending": "#f1c40f",
            "Returned": "#e74c3c",
        },
    )

    return fig_line, fig_donut, fig_sun, fig_geo, fig_box, fig_stack


if __name__ == "__main__":
    app.run(debug=True)
