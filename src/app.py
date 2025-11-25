from flask import Flask, request
from markupsafe import escape
import os

app = Flask(__name__)

# Read secret from environment (do NOT hardcode)
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

@app.route('/greet/<name>')
def greet(name):
    # Escape user input to prevent XSS
    safe_name = escape(name)
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
            <p>Hello {safe_name}</p>
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
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Stricter CSP
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';"
    
    # Remove Server header to prevent version leakage
    # If we delete it, Werkzeug adds its own versioned header.
    # So we set it to a generic value.
    response.headers['Server'] = 'Apache'
    
    # Cache Control
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Spectre / Site Isolation
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    
    return response

if __name__ == '__main__':
    print("--- STARTING SECURE APP V3 ---", flush=True)
    app.run(host='0.0.0.0', port=5000) # nosec
