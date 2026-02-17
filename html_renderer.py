import json
from pathlib import Path


INPUT_JSON = Path("data/ui_balance_sheet.json")
OUTPUT_HTML = Path("data/balance_sheet.html")


# ----------------------------------------
# Color logic
# ----------------------------------------

def trend_class(signal):
    if signal == "positive":
        return "positive"
    if signal == "negative":
        return "negative"
    return "neutral"


# ----------------------------------------
# Section HTML Builder
# ----------------------------------------

def build_section_html(section):
    rows = ""

    for metric in section["metrics"]:
        rows += f"""
        <tr>
            <td class="metric">{metric['label']}</td>
            <td>{metric['current']}</td>
            <td>{metric['previous']}</td>
            <td class="{trend_class(metric['signal'])}">
                {metric['change_pct']}
            </td>
        </tr>
        """

    return f"""
    <div class="section">
        <h2>{section['section_title']}</h2>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Current</th>
                    <th>Previous</th>
                    <th>Change</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    """


# ----------------------------------------
# Main HTML Builder
# ----------------------------------------

def build_html(data):

    sections_html = ""
    for section in data["sections"]:
        sections_html += build_section_html(section)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Balance Sheet - {data['company']['name']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f4f6f9;
            }}

            h1 {{
                margin-bottom: 5px;
            }}

            .company-info {{
                margin-bottom: 30px;
                color: #555;
            }}

            .section {{
                margin-bottom: 40px;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}

            th, td {{
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }}

            th {{
                background-color: #fafafa;
            }}

            .metric {{
                font-weight: 600;
            }}

            .positive {{
                color: green;
                font-weight: bold;
            }}

            .negative {{
                color: red;
                font-weight: bold;
            }}

            .neutral {{
                color: #555;
            }}

            .footer {{
                margin-top: 40px;
                font-size: 12px;
                color: #888;
            }}
        </style>
    </head>
    <body>

        <h1>{data['company']['name']}</h1>

        <div class="company-info">
            Ticker: {data['company']['ticker']} <br>
            Currency: {data['company']['currency']} <br>
            Period: {data['periods']['current']} vs {data['periods']['previous']}
        </div>

        {sections_html}

        <div class="footer">
            Generated via Automated Balance Sheet Engine
        </div>

    </body>
    </html>
    """

    return html


# ----------------------------------------
# Entry Point
# ----------------------------------------

def main():
    if not INPUT_JSON.exists():
        raise FileNotFoundError("UI JSON not found.")

    with open(INPUT_JSON, "r") as f:
        data = json.load(f)

    html_content = build_html(data)

    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Balance sheet HTML generated → {OUTPUT_HTML}")


if __name__ == "__main__":
    main()