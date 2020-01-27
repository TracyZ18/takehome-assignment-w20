from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/shows", methods=['GET'])
def get_all_shows():
    minEpisodes=request.args.get('minEpisodes')
    if minEpisodes is None : 
        return create_response({"shows": db.get('shows')})
    minEpisodes = int(minEpisodes)
    shows= {"shows": []}
    for i in db.get("shows"):
        if i["episodes_seen"] >= minEpisodes:
            shows["shows"].append(i)
    return create_response({"shows": shows["shows"]},status=200)

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!
@app.route("/shows/<id>", methods=['GET'])
def get_show(id):
    show = db.getById('shows', int(id))
    if show is None:
        return create_response(status=404, message="ID not found.")
    return create_response({"id": id, "name": show["name"],"episodes_seen": show["episodes_seen"]})

@app.route("/shows", methods=['POST'])
def post_show():
    name = request.args.get("name")
    episodes_seen = request.args.get("episodes_seen")
    if name is None or episodes_seen is None:
        return create_response({"name":name},status=422, message='Must provide "name" and "episodes_seen"')
    payload = {"id":-1, "name":name, "episodes_seen":episodes_seen}
    payload = db.create("shows",payload)
    #return create_response(payload,status=201)
    return create_response(payload,status=201)

@app.route("/shows/<id>", methods=['PUT'])
def put_show(id):
    id = int(id)
    update_values = db.getById("shows",id)
    # id not found
    if update_values is None:
        return create_response(status=404, message="ID not found.")
    name = request.args.get("name")
    episodes_seen = request.args.get("episodes_seen")
    # no changes provided
    if name is None and episodes_seen is None:
        return create_response({"name":name},status=422, message='Must provide "name" or "episodes_seen" or both')
    # make changes
    if name is not None:
        update_values["name"] = name
    if episodes_seen is not None:
        update_values["episodes_seen"] = episodes_seen
    update_values = db.updateById("shows",id,update_values)
    return create_response(update_values,status=201)


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
