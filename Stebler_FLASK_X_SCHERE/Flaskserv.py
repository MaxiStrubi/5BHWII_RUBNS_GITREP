import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
connection = sqlite3.connect("test.db", check_same_thread=False)
cursor = connection.cursor()

# Stellen Sie sicher, dass die benötigten Tabellen existieren
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Test_SSPS (
        gameId INTEGER PRIMARY KEY, 
        player INTEGER, 
        bot INTEGER, 
        result VARCHAR(20)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS SymbolStatistik (
        symbol TEXT PRIMARY KEY, 
        anzahl INTEGER NOT NULL
    )
""")
connection.commit()


@app.route("/")
def hello_world():
    return "<p>Hallo Seppl</p>"


@app.route("/Data", methods=['GET'])
def look_data():
    cursor.execute("SELECT * FROM Test_SSPS")
    rows = cursor.fetchall()
    return '<br>'.join(str(row) for row in rows)


"""@app.route('/DataSave', methods=['POST'])
def saveStats():
    try:
        stats = request.get_json()
        cursor.execute("INSERT INTO Test_SSPS (gameId, player, bot, result) VALUES (:gameId, :player, :bot, :result)", stats)
        connection.commit()
        return jsonify({"message": "Success"})
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return jsonify({"message": "Failed"}), 500
"""

@app.route('/SaveSymbolStats', methods=['POST'])
def saveSymbolStats():
    try:
        stats = request.get_json()
        for symbol, anzahl in stats.items():
            cursor.execute("INSERT INTO SymbolStatistik (symbol, anzahl) VALUES (?, ?) ON CONFLICT(symbol) DO UPDATE SET anzahl = anzahl + ?", (symbol, anzahl, anzahl))
        connection.commit()
        return jsonify({"message": "Symbolstatistiken erfolgreich gespeichert"})
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return jsonify({"message": "Failed"}), 500


@app.route('/DataGame', methods=['GET'])
def getStats():
    cursor.execute("SELECT * FROM SymbolStatistik")
    stats = cursor.fetchall()
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)
