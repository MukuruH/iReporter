"""
Endpoints

Author: Abraham Arishian
"""
from flask import Flask, request, jsonify, Response
from models import convert_to_dict, Incident
from werkzeug.exceptions import HTTPException, HTTP_STATUS_CODES

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

red_flags = []

# Counter to generate unique ids
count = 0


@app.route('/api/v1/red-flags', methods=['POST'])
def add_red_flag():
    """ Create a red-flag record. """
    global count

    try:
        # Get unique id
        count += 1

        # Access form data transmitted in the POST method
        red_flag = Incident(count, request.form['createdOn'], request.form['createdBy'],
                            request.form['type'], request.form['location'], request.form['status'], [], [], request.form['comment'])

        # Update red_flags list
        red_flags.append(convert_to_dict(red_flag))

        return jsonify(status=201, data=[{"id": count, "message": "Created red-flag record"}])
    except HTTPException as e:
        # Get status code
        status_code = int(str(e)[:3])
        # Get message corresponding to status code above
        message = HTTP_STATUS_CODES[int(str(e)[:3])]

        return jsonify(status=status_code, message=message)


@app.route('/api/v1/red-flags', methods=['GET'])
def get_red_flags():
    """ Return all red-flag records. """

    return jsonify(status=200, data=red_flags)


@app.route('/api/v1/red-flags/<int:red_flag_id>', methods=['GET'])
def get_red_flag(red_flag_id):
    """ Return a specific red-flag record """

    # red-flags list is empty
    if red_flags == []:
        return jsonify(status=404, message="The resource does not exist")
    else:
        for position in range(len(red_flags)):
            if red_flags[position]['id'] == red_flag_id:
                return jsonify(status=200, data=red_flags[position])

            # The elif block will be executed if and only if
            # the red_flags list has been exhausted/searched completely
            # so that it doesn't terminate the loop prematurely.
            elif position == (len(red_flags) - 1):
                return jsonify(status=404, message="The resource does not exist")


@app.route('/api/v1/red-flags/<int:red_flag_id>/<string:key>', methods=['PATCH'])
def update_red_flag(red_flag_id, key):
    """ Edit a specific red-flag record. """

    # red-flags list is empty
    if red_flags == []:
        return jsonify(status=204, message="No content")
    else:
        for position in range(len(red_flags)):
            # Firstly, check if red_flag_id exists
            if red_flags[position]['id'] == red_flag_id:
                # Secondly, check if the key specified exists
                try:
                    if red_flags[position][key]:
                        # Update red_flag resource identified by the key
                        red_flags[position][key] = request.get_json()[key]
                        return jsonify(status=200, data=[{"id": red_flags[position]['id'], "message": "Updated red-flag record's {}".format(key)}]), 200
                except KeyError:
                    # Key doesn't exist
                    return jsonify(status=404, message="The resource does not exist")

            # The elif block will be executed if and only if
            # the red_flags list has been exhausted/searched completely
            # so that it doesn't terminate the loop prematurely.
            elif position == (len(red_flags) - 1):
                return jsonify(status=404, message="The resource does not exist")


@app.route('/api/v1/red-flags/<int:red_flag_id>', methods=['DELETE'])
def delete_red_flag(red_flag_id):
    """ Delete a specific red-flag record """

    # red-flags list is empty
    if red_flags == []:
        return jsonify(status=404, message="The resource does not exist")
    else:
        for position in range(len(red_flags)):
            if red_flags[position]['id'] == red_flag_id:
                # Update red_flags list
                red_flags.remove(red_flags[position])
                return jsonify(status=200, data=[{"id": (red_flags[position]['id'] - 1), "message": "red-flag record has been deleted"}]), 200

            # The elif block will be executed if and only if
            # the red_flags list has been exhausted/searched completely
            # so that it doesn't terminate the loop prematurely.
            elif position == (len(red_flags) - 1):
                return jsonify(status=404, message="The resource does not exist")


if __name__ == "__main__":
    app.run(debug=True)
