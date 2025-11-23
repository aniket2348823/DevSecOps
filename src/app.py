from flask import Flask, request

app = Flask(__name__)

# Vulnerability 1: Hardcoded Secret (Triggers Bandit)
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"

@app.route('/greet/<name>')
def greet(name):
    # Vulnerability 2: XSS (Triggers OWASP ZAP)
    # Returning the user input directly without sanitization
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DevSecOps Demo</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .container {{ background-color: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }}
            h1 {{ color: #1a73e8; }}
            p {{ font-size: 1.2em; color: #333; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DevSecOps Demo</h1>
            <p>Hello {name}</p>
        </div>
    </body>
    </html>
    """


@app.route('/')
def home():
    return "Welcome to the DevSecOps Demo! Go to /greet/YourName to test."

@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /", 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    return "<urlset><url><loc>http://localhost:5000/</loc></url></urlset>", 200, {'Content-Type': 'application/xml'}

@app.after_request
def add_security_headers(response):
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
