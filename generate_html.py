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

