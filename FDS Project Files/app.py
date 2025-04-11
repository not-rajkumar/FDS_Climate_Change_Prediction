import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go

# Load data
df = pd.read_csv("citywise_forecast_rmse.csv")

# Add dummy MAE columns (remove if actual MAE values are available)
df["ARIMA_MAE"] = df["ARIMA_RMSE"] * 0.8
df["LSTM_Residual_MAE"] = df["LSTM_Residual_RMSE"] * 0.8
df["Hybrid_MAE"] = df["Hybrid_RMSE"] * 0.8

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "T-Climate Dashboard"

# Layout
app.layout = html.Div([
    html.H1("🌍 T-Climate Forecast Error Dashboard", style={"textAlign": "center"}),

    # City dropdown for individual chart
    html.Div([
        html.Label("Select a city to view RMSEs:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{"label": city, "value": city} for city in df["City"]],
            placeholder="Choose a city",
            style={"width": "50%"}
        )
    ], style={"padding": "20px"}),

    dcc.Graph(id="rmse-bar-chart"),

    html.Hr(),

    # Top 5 performance selection
    html.Div([
        html.Label("🔎 Show Top 5 Cities by Hybrid RMSE:"),
        dcc.Dropdown(
            id="performance-type",
            options=[
                {"label": "Top 5 Best (Lowest Error)", "value": "best"},
                {"label": "Top 5 Worst (Highest Error)", "value": "worst"}
            ],
            value="best",
            style={"width": "50%"}
        )
    ], style={"padding": "20px"}),

    dcc.Graph(id="rmse-mae-bar-chart"),

    html.Hr(),

    html.H2("📌 Citywise Hybrid RMSE Scatter Plot", style={"textAlign": "center"}),

    dcc.Graph(
        id="rmse-scatter",
        figure=px.scatter(
            df,
            x="City",
            y="Hybrid_RMSE",
            color="Hybrid_RMSE",
            hover_data=["ARIMA_RMSE", "LSTM_Residual_RMSE"],
            title="All Cities - Hybrid Model RMSE",
            color_continuous_scale="Viridis",
        ).update_layout(xaxis_tickangle=-45, height=500, margin={"r":20, "t":50, "l":20, "b":150})
    )
])

# Callback for city-specific RMSE bar chart
@app.callback(
    Output("rmse-bar-chart", "figure"),
    Input("city-dropdown", "value")
)
def update_city_chart(selected_city):
    if selected_city:
        row = df[df["City"] == selected_city].iloc[0]
        return {
            "data": [
                go.Bar(
                    x=["ARIMA", "LSTM Residual", "Hybrid"],
                    y=[row["ARIMA_RMSE"], row["LSTM_Residual_RMSE"], row["Hybrid_RMSE"]],
                    marker_color=["#636EFA", "#EF553B", "#00CC96"]
                )
            ],
            "layout": go.Layout(
                title=f"RMSEs for {selected_city}",
                yaxis_title="RMSE",
                xaxis_title="Model Type"
            )
        }
    else:
        return go.Figure()

# Callback for top 5 RMSE+MAE grouped bar chart
@app.callback(
    Output("rmse-mae-bar-chart", "figure"),
    Input("performance-type", "value")
)
def update_bar_chart(performance_type):
    if performance_type == "best":
        df_sorted = df.nsmallest(5, "Hybrid_RMSE")
        title = "Top 5 Best Performing Cities (Lowest Hybrid RMSE)"
    else:
        df_sorted = df.nlargest(5, "Hybrid_RMSE")
        title = "Top 5 Worst Performing Cities (Highest Hybrid RMSE)"

    fig = px.bar(
        df_sorted,
        x="City",
        y=["ARIMA_RMSE", "LSTM_Residual_RMSE", "Hybrid_RMSE", "ARIMA_MAE", "LSTM_Residual_MAE", "Hybrid_MAE"],
        barmode="group",
        title=title,
        labels={"value": "Error", "variable": "Metric"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(xaxis_tickangle=-45, height=500, margin={"r":20, "t":50, "l":20, "b":150})
    return fig

# Run server
if __name__ == "__main__":
    app.run(debug=True)
