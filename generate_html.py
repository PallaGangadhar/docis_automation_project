import csv



def generate_html_file(input_file_path, output_file_path):
    print("INPUT FILE PATH =====> ", input_file_path)
    print("OUTPUT FILE PATH =====> ", output_file_path)
# Function to read and parse the test summary file
    def read_test_summary(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter='|')
            # Skip the first few lines that are not part of the actual data
            for _ in range(6):
                next(reader)
            # Read the actual data rows
            rows = []
            for row in reader:
                # Strip whitespace and filter out empty strings
                cleaned_row = [cell.strip() for cell in row if cell.strip()]
                if len(cleaned_row) == 4:
                    rows.append(cleaned_row)
            return rows

    # Function to generate HTML content
    def generate_html(rows):
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Execution Summary</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
                th {
                    background-color: #f2f2f2;
                }
                .pass {
                    color: green;
                }
                .fail {
                    color: red;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h2>TEST EXECUTION SUMMARY</h2>
            <table>
                <tr>
                    <th>Test_Case_Number</th>
                    <th>Test_Case_Status</th>
                    <th>Failed in Test_Steps</th>
                    <th>Execution time in seconds</th>
                </tr>
        """

        for case in rows:
            status_class = "pass" if case[1].upper() == "PASS" else "fail"
            html_content += f"""
                <tr>
                    <td>{case[0]}</td>
                    <td class="{status_class}">{case[1]}</td>
                    <td>{case[2]}</td>
                    <td>{case[3]}</td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        return html_content
    
    rows = read_test_summary(input_file_path)
    html_content = generate_html(rows)
    with open(output_file_path, 'w') as file:
        file.write(html_content)
    print("HTML file generated successfully.")
    return 1

# Main function to read the summary and generate the HTML file
# def main():
#     rows = read_test_summary(input_file_path)
#     html_content = generate_html(rows)
#     with open(output_file_path, 'w') as file:
#         file.write(html_content)
#     print("HTML file generated successfully.")

# # Run the main function
# if __name__ == "__main__":
#     main()

import json
from pathlib import Path

def json_to_html_file(data, output_path, title="Testcase Summary"):
    # Accepts JSON string or Python object (list/dict)
    if isinstance(data, str):
        parsed = json.loads(data)
    else:
        parsed = data


    if not parsed:
        html_table = "<p>No data</p>"
    else:
        # Ensure it's a list
        rows = parsed if isinstance(parsed, list) else [parsed]
        # Collect all columns
        columns = list(rows[0].keys())
        print(columns)
        
        # Build HTML
        html_table = "<table border='1'>\n<tr>"
        html_table += "".join(f"<th>{col}</th>" for col in columns)
        html_table += "</tr>\n"
        for row in rows:
            html_table += "<tr>"
            html_table += "".join(f"<td>{row.get(col,'')}</td>" for col in columns)
            html_table += "</tr>\n"
        html_table += "</table>"

        full_html = f"""<!doctype html>
    <html>
    <head>
    <meta charset="utf-8"/>
    <title>{title}</title>
    </head>
    <body>
    <h2>{title}</h2>
    {html_table}
    </body>
    </html>"""

    Path(output_path).write_text(full_html, encoding="utf-8")
    return output_path