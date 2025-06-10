import json
import pandas as pd
from dataclasses import dataclass
from typing import Literal, Optional
from fastapi_htmx.core.service.content.chart import htmlContentChart


@dataclass
class SeriesConfig:
    column: str
    type: Optional[Literal["bar", "line", "dash"]] = "bar"
    color: Optional[str] = "rgba(54, 162, 235, 0.5)"
    width: Optional[int] = 1


def htmlContentPandaChartTimeSerie(
    df: pd.DataFrame, axe_index: str, series: list[SeriesConfig]
):
    """

    series = [
        {
            "column": "ColumnName",   # Required: name of the column in the DataFrame to plot
            "type": "bar",            # Optional: "bar", "line", or "dash"
            "color": "rgba(255, 99, 132, 0.5)",  # Optional: CSS rgba or hex color
            "width": 2                # Optional: Line or bar border width (default is 1)
        },
        ...
    ]

    """

    # --------------
    # Create Labels of the Chart
    if pd.api.types.is_datetime64_any_dtype(df[axe_index]):
        # if axe column is datetime
        labels = df[axe_index].dt.strftime("%Y-%m-%d").tolist()
        df[axe_index] = df[axe_index].dt.strftime("%Y-%m-%d")
    else:
        labels = df[axe_index].astype(str).tolist()

    dataset_configs = []
    # --------------
    # Build DataSets , Using DF , and Serie Configuration
    for serie in series:
        serie_type = serie.type
        axe_column = serie.column

        dataset = {
            "label": axe_column,
            "data": df[axe_column].tolist(),
            "type": "bar",
            "borderColor": "rgba(54, 162, 235, 1)",
            "borderWidth": 1,
        }
        match serie_type:
            case "bar":
                dataset["backgroundColor"] = ("rgba(54, 162, 235, 0.5)",)
            case "line":
                dataset["type"] = "line"
                dataset["tension"] = 0.3
            case "dash":
                dataset["type"] = "line"
                dataset["tension"] = 0.3
                dataset["borderDash"] = [5, 5]

        # Color Option
        color = serie.color
        if color:
            dataset["borderColor"] = (color,)
            dataset["backgroundColor"] = (color,)

        # Width Option
        width = serie.width
        dataset["borderWidth"] = (width,)

        # Add DataSet to Configuration list
        dataset_configs.append(dataset)
        # -- End Loop

    chart_config = {
        "type": "bar",  # top-level 'type' can be overridden by dataset-level types
        "data": {"labels": labels, "datasets": dataset_configs},
        "options": {
            "responsive": True,
            # "interaction": {
            #     "mode": "index",
            #     "intersect": False
            # },
            "scales": {
                "x": {"title": {"display": True, "text": axe_index}, "stacked": False},
                "y": {"stacked": False, "title": {"display": True, "text": "Values"}},
            },
        },
    }
    """

    # If time series, modify x scale type
    if time_series:
        chart_config["options"]["scales"]["x"]["type"] = "time"
        chart_config["options"]["scales"]["x"]["time"] = {
            "unit": "day",
            "tooltipFormat": "yyyy-MM-dd"
        }

    """

    return htmlContentChart(chart_config)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlContentPandaChartTimeSerie_exemple():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01"]),
            "sales": [100, 120, 140],
            "revenue": [200, 240, 300],
            "profit": [50, 60, 80],
            "profit2": [55, 65, 85],
        }
    )

    return htmlContentPandaChartTimeSerie(
        df,
        "date",
        [
            SeriesConfig(column="sales", type="bar"),
            SeriesConfig(column="sales", type="dash", width=5),
            SeriesConfig(column="revenue", type="line"),
            SeriesConfig(column="profit", type="line", color="hsla(38, 40%, 50%, 1)"),
            SeriesConfig(
                column="profit2", type="line", color="hsla(158, 40%, 50%, 1)", width=5
            ),
        ],
    )
