from flask import Flask, render_template, request, jsonify
import threading
import time
from simulation import run_simulation  # Import the run_simulation function from simulation.py

app = Flask(__name__)

# Landing page route
@app.route('/')
def landing_page():
    return render_template('landing.html')

# Start simulation route
@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    # Run the simulation in a separate thread to avoid blocking the web server
    simulation_thread = threading.Thread(target=run_simulation)
    simulation_thread.start()

    # Return a response to inform the client that the simulation has started
    return jsonify({'status': 'Simulation started'})

if __name__ == '__main__':
    app.run(debug=True)
