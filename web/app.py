from flask import Flask, render_template, request, send_file
from flask import redirect, url_for, flash, session
from user_logging import register_user, login_user, logout_user, get_user_id
from history_db import retrieve_results_from_db, save_result_to_db
from history_db import get_submission_from_id, delete_result_from_db
from upload import handle_upload
from werkzeug.utils import secure_filename
import urllib.parse
import requests
import os
import io
import json
import sys


app = Flask(__name__)
app.secret_key = 'silviasefa'

users_db = {'admin': 'password123'}

app.config['ALLOWED_EXTENSIONS'] = {'txt', 'csv', 'json'}
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def home():
    if 'username' in session:
        # Message displayed when the user is logged in
        flash('Welcome back, {}!'.format(session['username']), 'info')
        return render_template('home.html', username=session['username'])

    # Message displayed when the user is not logged in
    flash('You must log in to access this page.', 'warning')
    return redirect(url_for('login'))


# Route for Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def allowed_file(filename):
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print("Upload, method="+request.method,
          file=sys.stderr)

    if request.method == 'POST':
        if 'generate_random' in request.form:
            api_key = '0d2bfa57-e218-44e8-8af7-74af23327e6c'
            url = 'https://api.random.org/json-rpc/4/invoke'
            bit_sequence = []

            try:
                for i in range(32):
                    headers = {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                    response = requests.post(url, json={
                        "jsonrpc": "2.0",
                        "method": "generateIntegers",
                        "params": {
                            "apiKey": api_key,
                            "n": 32,
                            "min": 0,
                            "max": 1,
                            "replacement": True
                        },
                        "id": i + 1
                    }, headers=headers)

                    data = response.json()
                    if data.get("result") and data["result"].get("random"):
                        bit_sequence.extend(data["result"]["random"]["data"])
                    else:
                        flash('Failed to generate random bits.', 'warning')
                        request.form.pop('generate_random', None)
                        return render_template('upload.html')

                bit_string = ''.join(map(str, bit_sequence))
                return render_template('upload.html',
                                       generated_bit_sequence=bit_string)

            except Exception as e:
                print(e)
                flash('Error while generating random bits.', 'warning')
                return render_template('upload.html')

        bitseq = request.form.get('bit_sequence', None)

        # Verify if the file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                         filename)
                file.save(file_path)

                with open(file_path, 'r') as f:
                    bitseq = f.read().strip()

        test = request.form.get('test_type', None)
        alpha = request.form.get('alpha', None)
        param = request.form.get('parameter')

        if not test:
            flash('Please choose a statistical test.', 'danger')
            return redirect(url_for('upload'))

        if 'username' not in session:
            flash('You must log in.', 'warning')
            return redirect(url_for('login'))

        id = get_user_id(session['username'])

        submission_id, error = handle_upload(user_id=id, bitseq=bitseq,
                                             testtype=test, alpha=alpha,
                                             optional_param=param)

        if not submission_id:
            flash('Failed to run the test. Error: {}'.format(error),
                  'danger')
            return redirect(url_for('upload'))

        return redirect(url_for('results', id=submission_id))

    return render_template('upload.html')


@app.route('/results', methods=['GET'])
def results():
    submission_id = request.args.get('id', None)
    print("Submission ID:", submission_id)

    if submission_id is None:
        flash('Result is not available.', 'info')
        return redirect(url_for('home'))

    result = get_submission_from_id(submission_id)
    print("Result fetched from database:", result)

    return render_template('results.html', result=result)


@app.route('/download-results', methods=['GET'])
def download_results():
    # Get result parameters from the request
    bit_sequence = request.args.get('bit_sequence', '')
    pvalue = request.args.get('pvalue', '0')
    stat = request.args.get('stat', 'FAIL')
    significance = request.args.get('significance', '0.05')

    app.logger.info(f"Received bit_sequence: {bit_sequence}")
    app.logger.info(f"Received pvalue: {pvalue}")
    app.logger.info(f"Received stat: {stat}")
    app.logger.info(f"Received significance: {significance}")

    if not bit_sequence or not pvalue or not stat or not significance:
        app.logger.error("Missing parameters for download.")
        flash("Missing parameters for download.", "error")
        return redirect(url_for('results'))

    # Format the result into a JSON file
    result_data = {
        "bit_sequence": bit_sequence,
        "pvalue": float(pvalue),
        "stat": stat,
        "significance": float(significance)
    }
    result_content = json.dumps(result_data, indent=4)

    # Create an in-memory file for downloading
    output = io.BytesIO()
    output.write(result_content.encode('utf-8'))
    output.seek(0)

    return send_file(output, as_attachment=True,
                     download_name="test_results.json",
                     mimetype="application/json")


# Test routes (will render home.html temporarily)
@app.route('/test/monobit')
def monobit_test():
    return render_template('test/monobit.html')


@app.route('/test/m-bit')
def mbit_test():
    return render_template('test/mbit.html')


@app.route('/test/runs')
def runs_test():
    return render_template('test/runs.html')


@app.route('/test/autocorrelation')
def autocorrelation_test():
    return render_template('test/autocorrelation.html')


@app.route('/test/serial')
def serial_test():
    return render_template('test/serial.html')


@app.route('/history')
def history():
    user_id = None
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)

    if user_id is None:
        flash('You must log in to access this page.', 'warning')
        return redirect(url_for('login'))

    # get the results from the database
    results = retrieve_results_from_db(user_id)
    return render_template('history.html', results=results)


@app.route('/history/filter/', methods=['GET'])
def history_filter():
    required_test = request.args.get('testType', None)
    required_date = request.args.get('date', None)

    if required_date:
        required_date = urllib.parse.unquote(required_date)

    user_id = None
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)

    if user_id is None:
        flash('You must log in to access this page.', 'warning')
        return redirect(url_for('login'))

    # Filter the results based on the filter criteria
    results = retrieve_results_from_db(user_id, required_test, required_date)
    return render_template('history.html', results=results)


@app.route('/delete_result/<int:id_submission>', methods=['POST'])
def delete_result(id_submission):
    user_id = None
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)

    if user_id is None:
        flash('You must log in to access this page.', 'warning')
        return redirect(url_for('login'))

    result = delete_result_from_db(id_submission, user_id)

    if result:
        flash('Result deleted successfully!', 'success')
    else:
        flash('Error deleting result. Please try again.', 'danger')

    return redirect(url_for('history'))


# for testing purposes
@app.route('/insert_sample_data')
def insert_sample_data():
    user_id = None
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)
        flash('User ID: {}'.format(user_id), 'info')
    else:
        flash('You must log in to access this page.', 'warning')
        return redirect(url_for('login'))
    save_result_to_db(user_id, 'monobit', '101010101', 0.01, 0.05, 'SUCCESS')
    save_result_to_db(user_id, 'mbit', '101010101', 0.01, 0.05, 'SUCCESS')
    save_result_to_db(user_id, 'runs', '101010101', 0.01, 0.05, 'SUCCESS')
    save_result_to_db(user_id, 'serial', '101010101', 0.01, 0.05, 'SUCCESS')

    return redirect(url_for('home'))


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
