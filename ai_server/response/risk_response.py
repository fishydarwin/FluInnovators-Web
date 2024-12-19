from flask import Blueprint, Response, request
from database import risk_database
from response import status
from ai import ai_model
from threading import Thread

risk_blueprint = Blueprint("risk", __name__);

risk_database.init()

# TODO: this should be moved to significant_response.py, with its own end-point,
#       as outlined in the theoretical document
expected_parameters = {
    'd_geo_mean': 22.314323,
    'geo_mean': 7.974775,
    'CD85j+CD4+_T_cells': 4.016304,
    'CD161+CD45RA+_Tregs': 2.182465,
    'L50_IFNB': 1.890115,
    'L50_ICAM1': 1.813595,
    'CD27+CD8+_T_cells': 1.568877,
    'L50_HGF': 1.506532,
    'HLADR-CD38+CD4+_T_cells': 1.475321,
    'B_cells': 1.459686,
    'total_vaccines_received': 1.422971,
    'L50_RANTES': 1.378472,
    'L50_PDGFBB': 1.236744,
    'Tregs': 1.208230,
    'L50_IL17F': 1.168467,
    'monocytes': 1.139914,
    'RANTES': 1.081454,
    'L50_CD40L': 1.069806,
    'Unstim_CD8+:_pSTAT3': 0.971132,
    'vaccine_type_2yr_prior': 0.960934
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
        
        thread = Thread(target=ai_model.compute_risk, args=(id,))
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
        return Response('{"complete":' + str(result[1]) + ', "at_risk":' + str(result[0]) + '}', 
                        status=status.ok, mimetype='application/json')

    return Response('{"complete": false, "at_risk": false}', status=status.ok, mimetype='application/json')
