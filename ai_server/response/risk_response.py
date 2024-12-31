from flask import Blueprint, Response, request
from database import risk_database
from response import status
from ai import ai_model
from threading import Thread

risk_blueprint = Blueprint("risk", __name__)

risk_database.init()

# TODO: this should be moved to significant_response.py, with its own end-point,
#       as outlined in the theoretical document
# TODO: Decide whether the request can be sent without all of the features being mandatory.
#       OR
#       The exact structure with all the features is mandatory for the request, but let
#       the Spring Boot backend handle missing features, setting them to NaN
# The model handles missing features, setting NaN to them
# This one is just an example, there are around 126 features
expected_parameters = {
    'd_geo_mean': 22.314323,
    'geo_mean': 7.974775,
    "basophils": 45.5,
    "BDNF": 30.1,
}

@risk_blueprint.route("/risk/compute")
def compute():
    args = request.args
    id = args.get('id')
    sample = args.get('sample')

    if None in (id, sample):
        return Response("Bad request. Missing all GET params: id, sample", status=status.bad_request)

    try:
        id = int(id)
        sample = sample.split(";")
        aux = {}
        for parameter in sample:
            param_split = parameter.split("==")
            aux[param_split[0].replace(" ", "_")] = param_split[1].replace(" ", "_")
        sample = aux
        if sample.keys() != expected_parameters.keys():
            return Response("Bad request. Sample parameters are invalid/missing.", status=status.bad_request)
    except:
        return Response("Bad request. Are your params correct?", status=status.bad_request)

    if risk_database.has(id):
        if risk_database.completed(id):
            return Response('{"complete": true}', status=status.ok, mimetype='application/json')
        return Response('{"complete": false}', status=status.processing, mimetype='application/json')
    else:

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
