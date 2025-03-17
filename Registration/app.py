from flask import Flask, request, jsonify, send_from_directory
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_cors import CORS  # For handling CORS
import os


app = Flask(__name__)
CORS(app)  # Enabling CORS globally


# Set up the Sheets API with OAuth credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"intra-sports-competition-api-325f110d4e0c.json", scope)
client = gspread.authorize(creds)


# Open the sheet by key (replace with your Google Sheets key)
sheet = client.open_by_key('1zDQjBu-2WIosSBh2sUzbJZxqoLPPshuEUHRJ98Tuu8Y').sheet1


@app.route('/')
def home():
    return send_from_directory(os.getcwd(), 'index.html')


@app.route('/submit', methods=['POST'])
@app.route('/submit', methods=['POST'])
@app.route('/submit', methods=['POST'])
@app.route('/submit', methods=['POST'])
@app.route('/submit', methods=['POST'])
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Use JSON payload

    # Common fields
    player_type = data['playerType']  # "individual" or "team"
    name = data['name']
    roll_no = data['rollNo']
    email = data['email']
    sports = data['sports']  # List of selected sports
    team_id = data['teamId']

    max_sports = 5
    fixed_columns = 22

    if player_type == 'individual':
        # Schema: [playerType, name, rollNo, email, teamId, sport1, sport2, sport3, sport4, sport5]
        sports_data = sports[:max_sports]
        sports_data += [""] * (max_sports - len(sports_data))
        row = [player_type, name, roll_no, email, team_id] + sports_data
        # Pad to fixed_columns
        row += [""] * (fixed_columns - len(row))
    elif player_type == 'team':
        # Schema: [playerType, name, rollNo, email, teamId, teamName, teamLeader,
        #          member1,...,member10, sport1, sport2, sport3, sport4, sport5]
        team_name = data.get('teamName', '')
        team_leader = data.get('teamLeader', '')
        members = [data.get(f'member{i}', '') for i in range(1, 11)]
        sports_data = sports[:max_sports]
        sports_data += [""] * (max_sports - len(sports_data))
        row = [player_type, name, roll_no, email, team_id, team_name, team_leader] + members + sports_data
        # This row should be exactly 22 columns
    else:
        return jsonify({"status": "error", "message": "Invalid player type"}), 400

    # Helper function to insert row starting at column A
    def append_row_fixed(row):
        values = sheet.get_all_values()
        next_row = len(values) + 1
        cell_range = f"A{next_row}:V{next_row}"  # Columns A to V (22 columns)
        sheet.update(cell_range, [row])

    # Append the row so that it always starts from column A
    append_row_fixed(row)
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
