import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# =============================================================================
# 1. DATA LOADING & PROCESSING
# =============================================================================
file_path = "amazon_sales_2025_INR.csv"

# Load the dataset
df = kagglehub.dataset_load(
    KaggleDatasetAdapter.PANDAS,
    "anandshaw2001/amazon-product-sales-2025",
    file_path,
)

# Load and Merge Geo Data
geo_df = pd.read_csv("states_geo.csv")
df = df.merge(geo_df, on="State", how="left")
del geo_df

# --- Sentiment Analysis Setup ---
analyzer = SentimentIntensityAnalyzer()


def classify_sentiment(text):
    if not isinstance(text, str) or not text.strip():
        return "Unknown"
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


# Apply Sentiment Analysis
df["Sentiment_Class"] = df["Review_Text"].apply(classify_sentiment)

# =============================================================================
# 2. APP SETUP & THEME
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

colors = {
    "background": "#ecf0f1",
    "text": "#2c3e50",
    "primary": "#2c3e50",
    "card_bg": "#ffffff",
}

# =============================================================================
# 3. LAYOUT DEFINITIONS (TABS)
# =============================================================================

# --- Header ---
header = dbc.Row(
    [
        dbc.Col(
            html.Div(
                [
                    html.H1("Amazon Diwali Sales 2025", className="display-4"),
                    html.P(
                        "Performance & Sentiment Analytics Dashboard", className="lead"
                    ),
                    html.Hr(),
                    # kaggle dataset link
                    html.P(
                        [
                            "Dataset Source: ",
                            html.A(
                                "Kaggle - Amazon Product Sales 2025",
                                href="https://www.kaggle.com/datasets/anandshaw2001/amazon-product-sales-2025",
                                target="_blank",
                            ),
                        ]
                    ),
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
)

# --- TAB 1 CONTENT: ORIGINAL SALES DASHBOARD ---
sales_tab_content = [
    # Row 1: KPIs
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
    # Row 2: Trend & Payment
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Daily Sales Trend", className="font-weight-bold"
                        ),
                        dbc.CardBody(dcc.Graph(id="trend-line")),
                    ]
                ),
                width=8,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Payment Methods", className="font-weight-bold"),
                        dbc.CardBody(dcc.Graph(id="payment-donut")),
                    ]
                ),
                width=4,
            ),
        ],
        className="mb-4",
    ),
    # Row 3: Sunburst & Geo
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Category & Product Breakdown", className="font-weight-bold"
                        ),
                        dbc.CardBody(dcc.Graph(id="product-sunburst")),
                    ]
                ),
                width=6,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Sales by Region (State)", className="font-weight-bold"
                        ),
                        dbc.CardBody(dcc.Graph(id="state-bar")),
                    ]
                ),
                width=6,
            ),
        ],
        className="mb-4",
    ),
    # Row 4: Ratings & Logistics
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Customer Satisfaction Distribution",
                            className="font-weight-bold",
                        ),
                        dbc.CardBody(dcc.Graph(id="rating-box")),
                    ]
                ),
                width=6,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Logistics & Delivery Status", className="font-weight-bold"
                        ),
                        dbc.CardBody(dcc.Graph(id="delivery-stack")),
                    ]
                ),
                width=6,
            ),
        ],
        className="mb-4",
    ),
]

# --- TAB 2 CONTENT: SENTIMENT ANALYSIS ---
sentiment_tab_content = [
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Sentiment Analysis Methodology",
                            className="font-weight-bold",
                        ),
                        dbc.CardBody(
                            children=[
                                html.P(
                                    "Sentiment is derived from customer reviews' text using the VADER lexicon.",
                                    className="card-text",
                                ),
                                html.P(
                                    "Scores >= 0.05 are Positive, <= -0.05 are Negative, others are Neutral.",
                                    className="card-text",
                                ),
                            ],
                        ),
                    ],
                    className="mb-4",
                ),
                width=12,
            )
        ]
    ),
    dbc.Row(
        [
            # Sentiment Donut Chart
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Overall Sentiment Distribution",
                            className="font-weight-bold text-center",
                        ),
                        dbc.CardBody(dcc.Graph(id="sentiment-donut-chart")),
                    ],
                    style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                ),
                width=6,
            ),
            # Sentiment by Category (Bar Chart)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Sentiment by Product Category",
                            className="font-weight-bold text-center",
                        ),
                        dbc.CardBody(dcc.Graph(id="sentiment-category-bar")),
                    ],
                    style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                ),
                width=6,
            ),
        ]
    ),
    dbc.Row(
        [
            # Sentiment vs. Rating (Box Plot)
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Sentiment vs. Customer Ratings",
                            className="font-weight-bold text-center",
                        ),
                        dbc.CardBody(dcc.Graph(id="sentiment-rating-box")),
                    ],
                    style={"boxShadow": "0px 2px 5px rgba(0,0,0,0.05)"},
                ),
                width=12,
            ),
        ]
    ),
]

# --- MAIN LAYOUT ASSEMBLY ---
app.layout = dbc.Container(
    [
        header,
        dbc.Tabs(
            [
                dbc.Tab(sales_tab_content, label="Sales Dashboard", tab_id="tab-sales"),
                dbc.Tab(
                    sentiment_tab_content,
                    label="Sentiment Analysis",
                    tab_id="tab-sentiment",
                ),
            ],
            id="tabs",
            active_tab="tab-sales",
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
        Output("sentiment-donut-chart", "figure"),
        Output("sentiment-category-bar", "figure"),
        Output("sentiment-rating-box", "figure"),
    ],
    [Input("tabs", "active_tab")],  # Trigger on tab change or load
)
def update_charts(_):
    clean_template = "plotly_white"

    # --- EXISTING CHARTS ---

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

    # 2. Payment Donut
    fig_donut = px.pie(
        df,
        names="Payment_Method",
        values="Total_Sales_INR",
        hole=0.4,
        template=clean_template,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    # 3. Sunburst
    fig_sun = px.sunburst(
        df,
        path=["Product_Category", "Product_Name"],
        values="Total_Sales_INR",
        template=clean_template,
        color="Total_Sales_INR",
        color_continuous_scale="Blues",
    )

    # 4. Geo Map
    fig_geo = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Total_Sales_INR",
        hover_name="State",
        template=clean_template,
        color_continuous_scale="Viridis",
    )
    fig_geo.update_geos(center=dict(lat=20.5937, lon=78.9629), projection_scale=10)

    # 5. Box Plot
    fig_box = px.box(
        df,
        x="Product_Category",
        y="Review_Rating",
        color="Product_Category",
        template=clean_template,
    )

    # 6. Delivery Stack
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

    # --- NEW SENTIMENT CHARTS ---

    # 7. Sentiment Donut
    # We count the occurrences of each sentiment class
    sentiment_counts = df["Sentiment_Class"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    fig_sent_donut = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        hole=0.5,
        template=clean_template,
        color="Sentiment",
        # Specific colors for sentiments
        color_discrete_map={
            "Positive": "#2ecc71",  # Green
            "Neutral": "#95a5a6",  # Grey
            "Negative": "#e74c3c",  # Red
        },
    )
    fig_sent_donut.update_traces(textinfo="percent+label")

    # 8. Sentiment by Category Bar
    sent_cat = (
        df.groupby(["Product_Category", "Sentiment_Class"])
        .size()
        .reset_index(name="Count")
    )
    fig_sent_bar = px.bar(
        sent_cat,
        x="Product_Category",
        y="Count",
        color="Sentiment_Class",
        template=clean_template,
        barmode="group",
        color_discrete_map={
            "Positive": "#2ecc71",
            "Neutral": "#95a5a6",
            "Negative": "#e74c3c",
        },
    )

    # 9. Sentiment vs. Rating Box Plot
    fig_sentiment_rating_box = px.box(
        df,
        x="Review_Rating",
        y="Sentiment_Class",
        color="Sentiment_Class",
        template=clean_template,
        color_discrete_map={
            "Positive": "#2ecc71",
            "Neutral": "#95a5a6",
            "Negative": "#e74c3c",
        },
    )

    return (
        fig_line,
        fig_donut,
        fig_sun,
        fig_geo,
        fig_box,
        fig_stack,
        fig_sent_donut,
        fig_sent_bar,
        fig_sentiment_rating_box,
    )


if __name__ == "__main__":
    app.run(debug=True)
