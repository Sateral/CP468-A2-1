from flask import Flask, request, jsonify
from flask_cors import CORS
from sudoku_validator import solve_sudoku

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/check', methods=['POST'])
def check_sudoku():
    data = request.json
    grid = data.get('grid')
    is_valid, solvedGrid, message = solve_sudoku(grid)
    return jsonify({'valid': is_valid, 'solvedGrid': solvedGrid, 'message': message})

if __name__ == '__main__':
    app.run(debug=True)