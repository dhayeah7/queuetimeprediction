from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import subprocess
import os

from prediction import calculate_worst_case_wait_time  # Assuming this function exists in prediction.py

app = Flask(__name__)
CORS(app)

# Define paths
CSV_FILE = 'waittime.xlsx'
TRACKING_SCRIPTS = {
    "dinosaur": "tracking1.py",
    "iceCream": "tracking2.py",
    "paintPalette": "tracking3.py",
    "volcano": "tracking4.py"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-tracking', methods=['POST'])
def run_tracking():
    """Execute specified tracking script to generate waittime.xlsx file."""
    tracking_id = request.json.get("tracking_id")  # Get tracking ID from the request body
    script_path = TRACKING_SCRIPTS.get(tracking_id)
    
    if not script_path:
        return jsonify({"status": "error", "message": "Invalid tracking ID."})
    
    try:
        # Run the appropriate tracking script to generate or update waittime.xlsx
        subprocess.run(['python', script_path], check=True)
        
        return jsonify({"status": "success", "message": f"Tracking data updated for {tracking_id}."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/predict-wait-time', methods=['GET'])
def predict_wait_time():
    """Calculate and return the worst-case wait time."""
    if not os.path.exists(CSV_FILE):
        return jsonify({"status": "error", "message": "Excel file not found. Run tracking first."})

    # Load data using read_excel for Excel files
    df = pd.read_excel(CSV_FILE)
    worst_case_time = calculate_worst_case_wait_time(df)
    return jsonify({"status": "success", "worst_case_wait_time": worst_case_time})

if __name__ == "__main__":
    app.run(debug=True)
