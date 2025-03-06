from datetime import datetime
import requests
from bs4 import BeautifulSoup;


results = []

def check_sql_injection(url):
    payload = " ' OR '1' = '1 "
    response = requests.get(f"{url}?id={payload}")
    if"mysql" in response.text.lower() or "syntax" in response.text.lower():
        results.append(('SQL Injection', url, True))
    else:
        results.append(('SQL Injection', url, False))
        
def check_xss(url):
    payload = "<script>alert('XSS')</script>"
    response = requests.get(f"{url}?q={payload}")
    if payload in response.text:
        results.append(('XSS', url, True))

    else:
        results.append(('XSS', url, False))


def generate_html_report(results):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"relatorio_{timestamp}.html"
    with open(filename, "w") as f:
        f.write("""
        <html>
        <head>
            <title>Relatório de Vulnerabilidades</title>
            <style>
                body { font-family: Arial, sans-serif; }
                table { border-collapse: collapse; width: 100%; }
                th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
                th { background-color: #4CAF50; color: white; }
                .vulnerable { color: red; }
                .safe { color: green; }
            </style>
        </head>
        <body>
            <h1>Relatório de Vulnerabilidades</h1>
            <table>
                <tr>
                    <th>Vulnerabilidade</th>
                    <th>URL</th>
                    <th>Status</th>
                </tr>
        """)
        for vulnerability, url, status in results:
            status_class = "vulnerable" if status else "safe"
            status_text = "Vulnerável" if status else "Seguro"
            f.write(f"""
                <tr>
                    <td>{vulnerability}</td>
                    <td><a href="{url}" target="_blank">{url}</a></td>
                    <td class="{status_class}">{status_text}</td>
                </tr>
            """)
        f.write("""
            </table>
        </body>
        </html>
        """)
    print(f"[+] Relatório gerado: {filename}")
    
    
def main():
    url = input("Digite a URL do site: ")
    check_sql_injection(url)
    check_xss(url)
    generate_html_report(results)

    
if __name__ == "__main__":
    main()