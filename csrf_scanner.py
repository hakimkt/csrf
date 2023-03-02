import argparse
import requests
from bs4 import BeautifulSoup

def check_csrf(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print("Error: Unable to access the URL")
        return

    # Parse the HTML content of the webpage using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all forms in the HTML code
    forms = soup.find_all('form')

    # Check each form for CSRF protection
    for form in forms:
        # Check if the form contains a CSRF token
        csrf_token = form.find('input', {'name': 'csrf_token'})
        if csrf_token is None:
            # CSRF token not found, possible CSRF attack
            print(f"Possible CSRF attack detected in form {form}")
        else:
            # CSRF token found, check its value
            if csrf_token.get('value') == '':
                # Empty CSRF token value, possible CSRF attack
                print(f"Possible CSRF attack detected in form {form}")

if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Scan a URL for possible CSRF attacks')
    parser.add_argument('url', type=str, help='The URL to be scanned')
    args = parser.parse_args()

    # Call the check_csrf function with the provided URL
    check_csrf(args.url)
