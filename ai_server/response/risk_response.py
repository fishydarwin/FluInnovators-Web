from flask import Blueprint, Response, request
from database import risk_database
from response import status
from ai import ai_model
from threading import Thread

risk_blueprint = Blueprint("risk", __name__)

risk_database.init()

# POST request required for arbitrary content length
@risk_blueprint.route("/risk/compute", methods=['POST'])
def compute():
    args = request.args
    id = args.get('id')

    if id is None:
        return Response("Bad request. Missing all POST params: id", status=status.bad_request)

    if risk_database.has(id):
        if risk_database.completed(id):
            return Response('{"complete": true}', status=status.ok, mimetype='application/json')
        return Response('{"complete": false}', status=status.processing, mimetype='application/json')
    else:
            
        sample_json = None
        try:
            sample_json = request.json['params']
        except:
            return Response("Bad request. Could not parse JSON body containing sample data.", 
                            status=status.bad_request)

        sample = {}
        try:
            id = int(id)
            for index in range(len(sample_json)):
                parameter_json_obj = sample_json[index]
                parameter_name = next(iter(parameter_json_obj))
                parameter_value = str(parameter_json_obj[parameter_name]).replace(" ", "_")
                try:
                    parameter_value = float(parameter_value)
                except:
                    pass
                sample[parameter_name.replace(" ", "_")] = parameter_value
        except:
            return Response("Bad request. Is your JSON body correct?", status=status.bad_request)

        thread = Thread(target=ai_model.compute_risk, args=(id, sample))
        thread.start()
        risk_database.start(id)

        return Response('{"complete": false}', status=status.accepted, mimetype='application/json')


@risk_blueprint.route("/risk/result")
def result():
    args = request.args
    id = args.get('id')

    try:
        id = int(id)
    except:
        return Response("Bad request. Are your params correct?", status=status.bad_request)

    if risk_database.has(id):
        result = risk_database.at_risk(id)
        return Response(
            '{"complete":' + str(result[1] == 1).lower() + ', "at_risk":' + str(result[0] == 1).lower() + '}',
            status=status.ok, mimetype='application/json')

    return Response('{"complete": false, "at_risk": false}', status=status.ok, mimetype='application/json')
