from flask import jsonify, request, Response
from distance_model import Distance
from init_config import app, check_db_connection
from help_funcs import get_or_create_distance, get_clean_name, create_distance_if_not_exist


# API 1: HELLO
@app.route('/hello', methods=['GET'])
def hello():
    return Response(status=200)


# API 2: get the distance in KM between a source and destination
@app.route('/distance', methods=['GET'])
def get_distance():
    source = request.args.get('source', '')
    destination = request.args.get('destination', '')
    # Error checking (empty fields)
    if not source:
        return "Source is empty", 400
    if not destination:
        return "Destination is empty", 400
    # Changing source and destination to lower case
    source = get_clean_name(source)
    destination = get_clean_name(destination)
    dis = get_or_create_distance(source, destination)
    if dis == -1:
        return "Source is not found", 400
    if dis == -2:
        return "Destination is not found", 400
    # return KM between source and destination
    return jsonify({"distance": dis})


# API 3:  The health API is responsible for determining the status of the connection to the DB
@app.route('/health', methods=['GET'])
def health():
    if check_db_connection():
        return Response(status=200)
    return "ERROR: DB is not OK", 500


# API 4: get the most popular search and number of hits for that search
@app.route('/popularsearch', methods=['GET'])
def popularsearch():
    most_popular = Distance.objects().order_by("-hits").limit(-1).first()
    if not most_popular:
        return "Data base is empty", 500
    return jsonify(most_popular.get_with_hits_as_json())


# API 5: allow ingesting a pair
@app.route('/distance', methods=['POST'])
def add_distance():
    json_data = request.json
    if not json_data:
        return 'Bad data', 400
    source = json_data.get('source', '')
    destination = json_data.get('destination', '')
    dist = json_data.get('distance', '')
    try:
        dist = float(dist)
    except Exception:
        return "Distance must be a number", 400
    if dist < 0:
        return 'Distance must be positive', 400
    # Error checking (empty fields)
    if not source or not destination or not dist:
        return 'Empty field', 400
    source = get_clean_name(source)
    destination = get_clean_name(destination)
    dis = create_distance_if_not_exist(source, destination, dist)
    return jsonify(dis.get_with_hits_as_json()), 201


# Main
if __name__ == "__main__":
    app.run(host="localhost", port=8080)