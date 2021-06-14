import csv
import json
from flask import Flask, make_response
app = Flask(__name__)


@app.route('/flights/<int:id>')
def get_flight_info(id):
    try:
        with open('dataFiles/orginalFile.csv', encoding='utf-8-sig') as file:
            table = csv.reader(file)
            for row in table:
                if row[0][0:2] == "Id":
                    continue
                if int(row[0]) == id:
                    try:
                        return json.dumps({"Number": row[7], "DepartureTime": row[4], "ArrivalTime": row[6]})
                    except IndexError:
                        return make_response(json.dumps({"Error": f'Unexpected problems with file! It may use wrong '
                                                                  f'split signs (not ,), not have enough columns or '
                                                                  f'elements into them'}), 404)
            else:
                return make_response(json.dumps({"Error": f'Flight with id={id} can\'t be found!'}), 404)
    except UnicodeDecodeError:
        return make_response(json.dumps({"Error": f'That\'s not a SCV file or it uses different from'
                                                  f' \'utf-8\' codec'}), 404)


@app.route('/flights/<id>')
def not_correct_id(id):
    return make_response(json.dumps({"Error": f'The id you entered: {id} isn\'t integer or less than zero'}), 404)


if __name__ == "__main__":
    app.run()