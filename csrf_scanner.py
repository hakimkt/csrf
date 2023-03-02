import sys
import re
import httplib2

# Check if URL is provided as command line argument
if len(sys.argv) < 2:
    print("Usage: python3 csrf_scanner.py <url>")
    sys.exit(1)

# Retrieve URL from command line argument
url = sys.argv[1]

# Create HTTP client
http = httplib2.Http()

# Retrieve HTML content from URL
response, content = http.request(url)

# Extract all forms from HTML content
forms = re.findall(r'<form.*?>(.*?)</form>', content.decode('utf-8'), re.DOTALL)

# Flag to indicate whether a CSRF vulnerability was found
csrf_found = False

# Check each form for potential CSRF vulnerability
for form in forms:
    # Check if form contains a CSRF token field
    if re.search(r'<input.*?name=["\']csrf_token["\']', form):
        # Check if form does not have a method attribute or if it uses POST
        if not re.search(r'method=["\'].*?["\']', form) or re.search(r'method=["\']post["\']', form):
            # Check if form action URL is different from current URL
            if not re.search(r'action=["\']{}["\']'.format(url), form):
                print("Potential CSRF vulnerability found:")
                print(form)
                csrf_found = True

# If no CSRF vulnerabilities were found, notify the user
if not csrf_found:
    print("No CSRF vulnerabilities found.")
