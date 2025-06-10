import uuid
import json

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlContentChart(chartConf):
    uid = uuid.uuid4()

    return f"""
        <div id="chart-container run-script">
            <canvas id="myChart{uid}"></canvas>
            <script type="text/javascript">
               {{
                Chart.defaults.borderColor = 'hsla(204, 20%, 23%, 90%)';
                Chart.defaults.color = '#FFF';

                const ctx = document.getElementById('myChart{uid}').getContext('2d');
                const myChart = new Chart(ctx, {json.dumps(chartConf)});
                }}
            </script>
        </div>
        """


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def htmlContentChart_exemple():
    chart_config = {
        "type": "bar",
        "data": {
            "labels": ["Red", "Blue", "Yellow"],
            "datasets": [
                {
                    "label": "# of Votes",
                    "data": [12, 19, 3],
                    "backgroundColor": ["red", "blue", "yellow"],
                }
            ],
        },
    }
    return htmlContentChart(chart_config)
