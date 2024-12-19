from database import risk_database

def compute_risk(id: int) -> bool:
    # TODO: compute with AI

    at_risk = False # TODO: replace with AI result here!
    risk_database.end(id, at_risk)

    return at_risk
