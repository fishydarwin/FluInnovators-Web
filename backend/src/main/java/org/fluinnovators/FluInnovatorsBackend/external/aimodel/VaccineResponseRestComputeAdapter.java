package org.fluinnovators.FluInnovatorsBackend.external.aimodel;

import org.fluinnovators.FluInnovatorsBackend.config.ApplicationConfig;
import org.fluinnovators.FluInnovatorsBackend.domain.VaccineResponse;
import org.fluinnovators.FluInnovatorsBackend.external.UnirestRestGetAdapter;
import org.json.JSONObject;

import java.util.Map;

public class VaccineResponseRestResultAdapter extends UnirestRestGetAdapter<VaccineResponse> {

    private final long id;
    public VaccineResponseRestResultAdapter(long id) {
        super(ApplicationConfig.AI_MODEL_SERVER_URL + "/risk/result");
        this.id = id;
    }

    @Override
    protected Map<String, Object> queryParams() {
        return Map.of("id", id);
    }

    @Override
    protected VaccineResponse adaptJsonToEntity(JSONObject json) {
        return VaccineResponse.of(id,
                json.getInt("complete") != 0,
                json.getInt("at_risk") != 0);
    }
}
