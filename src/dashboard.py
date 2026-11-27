from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


# --- Create Dash application ---

app = Dash(__name__)
app.title = "MarketPulse"


# --- Load shared snapshot ---

snapshot = build_market_snapshot()

provider = snapshot["provider"]
access_mode = snapshot.get("access_mode", "")
lookback = snapshot["lookback"]
interval = snapshot["interval"]

instrument = snapshot["instrument"]
benchmark = snapshot["benchmark"]

instrument_return = snapshot["instrument_return"]
benchmark_return = snapshot["benchmark_return"]
relative_performance = snapshot["relative_performance"]

instrument_base_100 = snapshot["instrument_base_100"]
benchmark_base_100 = snapshot["benchmark_base_100"]


# --- Market context ---

context = html.Div([
    html.H2("Market Context"),

    html.P(f"Provider: {provider}"),
    html.P(f"Access mode: {access_mode}"),

    html.P(
        f"Instrument: {instrument['ticker']} - "
        f"{instrument['name']}"
    ),

    html.P(
        f"Benchmark: {benchmark['ticker']} - "
        f"{benchmark['name']}"
    ),

    html.P(f"Lookback: {lookback}"),
    html.P(f"Interval: {interval}"),
])


# --- Performance indicators ---

performance = html.Div([
    html.H2("Market Performance"),

    html.Div([
        html.H3("Instrument Return"),
        html.P(f"{instrument_return:+.2f}%"),
    ]),

    html.Div([
        html.H3("Benchmark Return"),
        html.P(f"{benchmark_return:+.2f}%"),
    ]),

    html.Div([
        html.H3("Relative Performance"),
        html.P(f"{relative_performance:+.2f} pts"),
    ]),
])


# --- Base-100 comparison chart ---

figure = go.Figure()

figure.add_trace(
    go.Scatter(
        x=[row["date"] for row in instrument_base_100],
        y=[row["value"] for row in instrument_base_100],
        mode="lines",
        name=instrument["ticker"],
    )
)

figure.add_trace(
    go.Scatter(
        x=[row["date"] for row in benchmark_base_100],
        y=[row["value"] for row in benchmark_base_100],
        mode="lines",
        name=benchmark["ticker"],
    )
)

figure.update_layout(
    title="Instrument vs Benchmark - Base 100",
    xaxis_title="Date",
    yaxis_title="Base 100",
    template="plotly_white",
    height=500,
)


# --- Final dashboard layout ---

app.layout = html.Div(
    [
        html.H1("MarketPulse"),

        html.P(
            "Instrument vs Benchmark market comparison"
        ),

        html.Hr(),

        context,

        html.Hr(),

        performance,

        html.Hr(),

        dcc.Graph(
            id="base-100-chart",
            figure=figure
        ),
    ],
    style={
        "fontFamily": "Arial",
        "maxWidth": "1200px",
        "margin": "auto",
        "padding": "30px",
    }
)


# --- Start server ---

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8050,
        debug=False
    )