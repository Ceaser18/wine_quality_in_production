########################################
# app.py
########################################
from flask import Flask, request, flash, redirect, url_for, render_template_string
import os
import numpy as np
import pandas as pd
# Update to match your pipeline import
from src.datascience.pipeline.prediction_pipeline import PredictionPipeline

# -------------- Inline Templates --------------
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Wine Quality Predictor</title>
  <!-- Bootstrap 5 CSS -->
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
  />
  <style>
    body {
      background: #f4f4f4;
    }
    h1 {
      margin-top: 30px;
      font-weight: bold;
      text-shadow: 1px 1px #ccc;
    }
    .form-label {
      font-weight: 600;
    }
    .card {
      border-radius: 12px;
    }
    .nav-link {
      color: #fff !important;
    }
  </style>
</head>
<body>

<!-- Navigation Bar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="{{ url_for('homePage') }}">Wine Quality Predictor</a>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
      aria-controls="navbarNav"
      aria-expanded="false"
      aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('homePage') }}">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('training') }}">Train Model</a>
        </li>
      </ul>
    </div>
  </div>
</nav>


<div class="container my-5">
  <h1 class="text-center">Predict Your Wine's Quality</h1>

  <!-- Flashed messages -->
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="mt-4">
        {% for category, msg in messages %}
          <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
            {{ msg }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}

  <!-- Prediction Form -->
  <div class="row justify-content-center">
    <div class="col-md-8">
      <div class="card shadow p-4">
        <form method="POST" action="{{ url_for('predict_wine') }}">
          
          <!-- Form Fields -->
          <div class="mb-3">
            <label for="fixed_acidity" class="form-label">Fixed Acidity</label>
            <input type="number" class="form-control" name="fixed_acidity" id="fixed_acidity" required step="any">
          </div>
          <div class="mb-3">
            <label for="volatile_acidity" class="form-label">Volatile Acidity</label>
            <input type="number" class="form-control" name="volatile_acidity" id="volatile_acidity" required step="any">
          </div>
          <div class="mb-3">
            <label for="citric_acid" class="form-label">Citric Acid</label>
            <input type="number" class="form-control" name="citric_acid" id="citric_acid" required step="any">
          </div>
          <div class="mb-3">
            <label for="residual_sugar" class="form-label">Residual Sugar</label>
            <input type="number" class="form-control" name="residual_sugar" id="residual_sugar" required step="any">
          </div>
          <div class="mb-3">
            <label for="chlorides" class="form-label">Chlorides</label>
            <input type="number" class="form-control" name="chlorides" id="chlorides" required step="any">
          </div>
          <div class="mb-3">
            <label for="free_sulfur_dioxide" class="form-label">Free Sulfur Dioxide</label>
            <input type="number" class="form-control" name="free_sulfur_dioxide" id="free_sulfur_dioxide" required step="any">
          </div>
          <div class="mb-3">
            <label for="total_sulfur_dioxide" class="form-label">Total Sulfur Dioxide</label>
            <input type="number" class="form-control" name="total_sulfur_dioxide" id="total_sulfur_dioxide" required step="any">
          </div>
          <div class="mb-3">
            <label for="density" class="form-label">Density</label>
            <input type="number" class="form-control" name="density" id="density" required step="any">
          </div>
          <div class="mb-3">
            <label for="pH" class="form-label">pH</label>
            <input type="number" class="form-control" name="pH" id="pH" required step="any">
          </div>
          <div class="mb-3">
            <label for="sulphates" class="form-label">Sulphates</label>
            <input type="number" class="form-control" name="sulphates" id="sulphates" required step="any">
          </div>
          <div class="mb-3">
            <label for="alcohol" class="form-label">Alcohol</label>
            <input type="number" class="form-control" name="alcohol" id="alcohol" required step="any">
          </div>

          <!-- Buttons -->
          <div class="d-grid gap-2 d-sm-flex justify-content-sm-end">
            <button type="submit" class="btn btn-primary btn-lg">Predict Quality</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

<!-- Bootstrap 5 JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

RESULTS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Wine Prediction Result</title>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
  />
  <style>
    body {
      background: #f4f4f4;
    }
    .card {
      border-radius: 12px;
    }
    .btn-custom {
      background-color: #333;
      color: #fff;
      border-radius: 20px;
    }
    .btn-custom:hover {
      background-color: #555;
    }
  </style>
</head>
<body>

<div class="container my-5">
  <div class="card mx-auto shadow p-4" style="max-width: 600px;">
    <h1 class="text-center text-primary mb-4">Wine Quality Result</h1>
    <hr/>
    <div class="alert alert-info fs-4 text-center" role="alert">
      The predicted wine quality is: <strong>{{ prediction }}</strong>
    </div>
    <div class="text-center">
      <a href="{{ url_for('homePage') }}" class="btn btn-custom btn-lg">Go Back</a>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# -------------- Flask App --------------
app = Flask(__name__)
app.secret_key = "ANY_RANDOM_SECRET_KEY"

@app.route('/', methods=['GET'])
def homePage():
    """Renders the main (home) page."""
    return render_template_string(INDEX_HTML)

@app.route('/train', methods=['GET'])
def training():
    """
    Trigger training by calling main.py (synchronously).
    Once done, flash message & redirect to home.
    """
    try:
        os.system("python main.py")  # <--- Update if needed
        flash("Training Successful!", "success")
    except Exception as e:
        flash(f"Training Failed: {e}", "danger")
    return redirect(url_for('homePage'))

@app.route('/predict', methods=['POST', 'GET'])
def predict_wine():
    """
    On POST: gather form data, run model, show results.
    On GET: just show the home page.
    """
    if request.method == 'POST':
        try:
            # Extract form fields
            fixed_acidity         = float(request.form['fixed_acidity'])
            volatile_acidity      = float(request.form['volatile_acidity'])
            citric_acid           = float(request.form['citric_acid'])
            residual_sugar        = float(request.form['residual_sugar'])
            chlorides             = float(request.form['chlorides'])
            free_sulfur_dioxide   = float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide  = float(request.form['total_sulfur_dioxide'])
            density               = float(request.form['density'])
            pH                    = float(request.form['pH'])
            sulphates             = float(request.form['sulphates'])
            alcohol               = float(request.form['alcohol'])

            # Prepare data for prediction
            data = np.array([
                fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density,
                pH, sulphates, alcohol
            ]).reshape(1, -1)

            # Predict
            pipeline = PredictionPipeline()
            prediction_result = pipeline.predict(data)

            return render_template_string(RESULTS_HTML, prediction=str(prediction_result))

        except Exception as e:
            flash(f"Something went wrong: {e}", "danger")
            return redirect(url_for('homePage'))
    
    return redirect(url_for('homePage'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
