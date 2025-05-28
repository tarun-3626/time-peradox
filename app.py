from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from generate_timetable import generate_timetable

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        csv_file = request.files.get('csv_file')
        if csv_file and csv_file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(csv_file.filename))
            csv_file.save(filepath)
            data = generate_timetable(filepath)
            if data:
                return render_template('timetable.html',
                                       sections=data['sections'],
                                       days=data['days'],
                                       slots=data['slots_per_day'],
                                       timetable=data['timetable'])
            else:
                return "❌ No feasible timetable found.", 400
        return "❌ Please upload a valid CSV file.", 400
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
