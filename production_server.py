from waitress import serve
from app import app
import os

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Pulmonologist Website - Production Server")
    print("=" * 60)
    print("📍 Local URL: http://localhost:8080")
    print("🌐 Network URL: http://0.0.0.0:8080 (Accessible on LAN)")
    print("=" * 60)
    print("✨ Press CTRL+C to stop the server")
    print("=" * 60)
    
    # Run the server on port 8080
    serve(app, host='0.0.0.0', port=8080)
