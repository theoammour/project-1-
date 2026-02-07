from flask import Flask, render_template_string
import redis
import os
import random
import socket

app = Flask(__name__)

# Connect to Redis
redis_host = os.environ.get('REDIS_HOST', 'redis')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def home():
    # Simulate some metrics
    hits = r.incr('hits')
    
    # Simulate server statuses
    servers = [
        {"name": "Web-Server-01", "status": "Online", "cpu": random.randint(10, 40)},
        {"name": "Web-Server-02", "status": "Online", "cpu": random.randint(15, 45)},
        {"name": "Database-Primary", "status": "Online", "cpu": random.randint(20, 60)},
        {"name": "Cache-Node", "status": "Maintenance", "cpu": 0},
    ]
    
    hostname = socket.gethostname()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DevOps Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #1a1a1a; color: #fff; text-align: center; padding: 50px; }
            .container { max-width: 800px; margin: 0 auto; }
            .card { background-color: #2d2d2d; padding: 20px; margin: 10px; border-radius: 8px; text-align: left; display: flex; justify-content: space-between; }
            .status { font-weight: bold; }
            .online { color: #4caf50; }
            .maintenance { color: #ff9800; }
            h1 { color: #00bcd4; }
            .footer { margin-top: 50px; color: #888; font-size: 0.8em; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🖥️ System Status Dashboard</h1>
            <p>Served by Container ID: <strong>{{ hostname }}</strong></p>
            <p>Total Views: <strong>{{ hits }}</strong></p>
            
            {% for server in servers %}
            <div class="card">
                <div>
                    <strong>{{ server.name }}</strong>
                    <br>
                    <small>CPU Usage: {{ server.cpu }}%</small>
                </div>
                <div class="status {{ server.status.lower() }}">
                    ● {{ server.status }}
                </div>
            </div>
            {% endfor %}
            
            <div class="footer">
                <p>Powered by Docker Compose & Redis</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, hits=hits, servers=servers, hostname=hostname)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
