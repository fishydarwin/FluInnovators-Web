from flask import Blueprint, Response, request
from database import risk_database
from response import status
from ai import ai_model
from threading import Thread

risk_blueprint = Blueprint("risk", __name__)

risk_database.init()

# TODO: this should be moved to significant_response.py, with its own end-point,
#       as outlined in the theoretical document
# TODO: Find a way to define all the possible features that can be sent without all of them being mandatory.
# The model handles missing features, setting NaN to them
# This one is just an example, there are around 250 features
expected_parameters = {
    'd_geo_mean': 22.314323,
    'geo_mean': 7.974775,
    "basophils": 45.5,
    "BDNF": 30.1,
}


# expected_parameters = {
#   "B cells": 45.5,
#   "BDNF": 30.1,
#   "CD16+ monocytes": 50.2,
#   "CD16+CD14+ monocytes": 20.0,
#   "CD16+CD14- monocytes": 10.0,
#   "CD16-CD56bright NK cells": 15.3,
#   "CD161+ NK cells": 12.0,
#   "CD161+ NKT cells": 5.2,
#   "CD161+CD4+ T cells": 25.4,
#   "CD161+CD45RA+ Tregs": 20.5,
#   "CD161+CD45RA- Tregs": 30.2,
#   "CD161+CD8+ T cells": 18.5,
#   "CD161-CD45RA+ Tregs": 10.1,
#   "CD27+CD8+ T cells": 25.0,
#   "CD28+CD8+ T cells": 20.4,
#   "CD4+ T cells": 45.3,
#   "CD4+CD27+ T cells": 18.6,
#   "CD4+CD28+ T cells": 22.1,
#   "CD40L": 35.7,
#   "CD57+ NK cells": 10.3,
#   "CD57+CD4+ T cells": 12.7,
#   "CD57+CD8+ T cells": 9.5,
#   "CD8+ T cells": 50.2,
#   "CD85j+CD4+ T cells": 22.4,
#   "CD85j+CD8+ T cells": 21.1,
#   "CD94+ NK cells": 6.5,
#   "CD94+CD4+ T cells": 8.2,
#   "CD94+CD8+ T cells": 7.3,
#   "EGF": 12.1,
#   "ENA78": 8.5,
#   "EOTAXIN": 10.7,
#   "FASL": 11.3,
#   "FGFB": 9.8,
#   "GCSF": 7.4,
#   "GMCSF": 6.2,
#   "GROA": 5.9,
#   "HGF": 4.1,
#   "HLADR+ NK cells": 13.5,
#   "HLADR+CD38+CD4+ T cells": 14.0,
#   "HLADR+CD38+CD8+ T cells": 13.2,
#   "HLADR+CD38-CD4+ T cells": 12.0,
#   "HLADR+CD38-CD8+ T cells": 11.4,
#   "HLADR-CD38+CD4+ T cells": 10.0,
#   "HLADR-CD38+CD8+ T cells": 9.0,
#   "ICAM1": 5.5,
#   "ICOS+CD4+ T cell": 9.3,
#   "ICOS+CD8+ T cell": 7.8,
#   "IFNA": 15.2,
#   "IFNB": 17.3,
#   "IFNG": 14.5,
#   "IFNa_B cell: pSTAT1": 11.2,
#   "IFNa_B cell: pSTAT3": 10.5,
#   "IFNa_B cell: pSTAT5": 12.1,
#   "IFNa_CD4+: pSTAT1": 13.3,
#   "IFNa_CD4+: pSTAT3": 12.0,
#   "IFNa_CD4+: pSTAT5": 11.0,
#   "IFNa_CD8+: pSTAT1": 9.4,
#   "IFNa_CD8+: pSTAT3": 8.2,
#   "IFNa_CD8+: pSTAT5": 7.5,
#   "IFNa_Mono: pSTAT1": 6.4,
#   "IFNa_Mono: pSTAT3": 6.1,
#   "IFNa_Mono: pSTAT5": 5.7,
#   "IL10": 3.0,
#   "IL12P40": 2.5,
#   "IL12P70": 4.0,
#   "IL13": 5.0,
#   "IL15": 3.3,
#   "IL17A": 2.8,
#   "IL17F": 3.6,
#   "IL18": 3.1,
#   "IL1A": 5.4,
#   "IL1B": 4.9,
#   "IL1RA": 6.0,
#   "IL2": 7.1,
#   "IL21": 4.8,
#   "IL22": 4.2,
#   "IL23": 3.7,
#   "IL27": 3.9,
#   "IL31": 5.1,
#   "IL4": 6.4,
#   "IL5": 7.2,
#   "IL6": 7.9,
#   "IL7": 5.5,
#   "IL8": 5.0,
#   "IL9": 6.0,
#   "IP10": 5.6,
#   "IgD+CD27+ B cells": 4.3,
#   "IgD+CD27- B cells": 3.8,
#   "IgD-CD27+ B cells": 2.7,
#   "IgD-CD27- B cells": 3.1,
#   "L50_CD40L": 1.2,
#   "L50_ENA78": 1.1,
#   "L50_EOTAXIN": 1.3,
#   "L50_FASL": 1.2,
#   "L50_FGFB": 1.0,
#   "L50_GCSF": 0.8,
#   "L50_GMCSF": 0.9,
#   "L50_GROA": 1.4,
#   "L50_HGF": 0.7,
#   "L50_ICAM1": 1.5,
#   "L50_IFNA": 1.6,
#   "L50_IFNB": 1.8,
#   "L50_IFNG": 1.7,
#   "L50_IL10": 1.2,
#   "L50_IL12P40": 1.3,
#   "L50_IL12P70": 1.4,
#   "L50_IL13": 1.5,
#   "L50_IL15": 1.0,
#   "L50_IL17": 1.0,
#   "L50_IL17F": 1.1,
#   "L50_IL1A": 0.9,
#   "L50_IL1B": 1.2,
#   "L50_IL1RA": 0.8,
#   "L50_IL2": 1.3,
#   "L50_IL4": 1.2,
#   "L50_IL5": 1.5,
#   "L50_IL6": 1.4,
#   "L50_IL7": 1.2,
#   "L50_IL8": 1.3,
#   "L50_IP10": 1.6,
#   "LEPTIN": 6.0,
#   "LIF": 5.7,
#   "MCP1": 5.2,
#   "MCP3": 4.9,
#   "MCSF": 5.1,
#   "MIG": 4.8,
#   "MIP1A": 4.3,
#   "MIP1B": 4.4,
#   "NGF": 5.3,
#   "NK cells": 15.2,
#   "NKT cells": 10.2,
#   "PAI1": 7.6,
#   "PD1+CD4+ T cells": 11.2,
#   "PD1+CD8+ T cells": 10.3,
#   "PDGFBB": 9.5,
#   "RANTES": 8.1,
#   "RESISTIN": 6.8,
#   "SCF": 4.7,
#   "SDF1A": 5.3,
#   "T cells": 20.1,
#   "TFH CD4+ T cells": 19.4,
#   "TFH CD8+ T cells": 18.2,
#   "TGFA": 5.0,
#   "TGFB": 4.3,
#   "TNFA": 6.1,
#   "TNFB": 5.5,
#   "TRAIL": 4.2,
#   "Th1 TFH CD4+ T cells": 3.8,
#   "Th1 TFH CD8+ T cells": 3.2,
#   "Th1 non-TFH CD4+ T cells": 4.0,
#   "Th1 non-TFH CD8+ T cells": 4.1,
#   "Th17 TFH CD4+ T cells": 3.9,
#   "Th17 TFH CD8+ T cells": 3.7,
#   "Th17 non-TFH CD4+ T cells": 4.5,
#   "Th17 non-TFH CD8+ T cells": 4.6,
#   "Th2 TFH CD4+ T cells": 4.3,
#   "Th2 TFH CD8+ T cells": 4.0,
#   "Th2 non-TFH CD4+ T cells": 4.1,
#   "Th2 non-TFH CD8+ T cells": 4.2,
#   "Tregs": 30.1,
#   "Unstim_B cell: pSTAT1": 3.4,
#   "Unstim_B cell: pSTAT3": 3.2,
#   "Unstim_B cell: pSTAT5": 3.1,
#   "Unstim_CD4+: pSTAT1": 2.9,
#   "Unstim_CD4+: pSTAT3": 2.7,
#   "Unstim_CD4+: pSTAT5": 2.5,
#   "Unstim_CD8+: pSTAT1": 2.3,
#   "Unstim_CD8+: pSTAT3": 2.1,
#   "Unstim_CD8+: pSTAT5": 2.0,
#   "Unstim_Mono: pSTAT1": 1.9,
#   "Unstim_Mono: pSTAT3": 1.8,
#   "Unstim_Mono: pSTAT5": 1.7,
#   "VCAM1": 5.6,
#   "VEGF": 6.1,
#   "VEGFD": 5.4,
#   "basophils": 2.4,
#   "central memory CD4+ T cells": 9.2,
#   "central memory CD8+ T cells": 8.3,
#   "effector CD4+ T cells": 7.2,
#   "effector CD8+ T cells": 6.9,
#   "effector memory CD4+ T cells": 6.8,
#   "effector memory CD8+ T cells": 6.6,
#   "gamma-delta T cells": 3.9,
#   "mDCs": 4.3,
#   "memory B cells": 5.2,
#   "monocytes": 5.0,
#   "naive B cells": 4.4,
#   "naive CD4+ T cells": 6.2,
#   "naive CD8+ T cells": 6.0,
#   "pDCs": 3.8,
#   "plasmablasts": 3.5,
#   "transitional B cells": 3.3,
#   "gender": "Female",
#   "race": "Caucasian",
#   "visit_age": 30,
#   "cmv_status": 0,
#   "ebv_status": 1,
#   "bmi": 23.5,
#   "vaccine": 1,
#   "geo_mean": 1.2,
#   "d_geo_mean": 0.9,
#   "flu_vaccination_history": 1,
#   "total_vaccines_received": 5,
#   "vaccinated_1yr_prior": 1,
#   #"vaccine_type_1yr_prior": 1,
#   "vaccinated_2yr_prior": 1,
#   #"vaccine_type_2yr_prior": 2,
#   "vaccinated_3yr_prior": 0,
#   #"vaccine_type_3yr_prior": 0,
#   "vaccinated_4yr_prior": 1,
#   #"vaccine_type_4yr_prior": 3,
#   "influenza_infection_history": 0,
#   "influenza_hospitalization": 0
# }

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
