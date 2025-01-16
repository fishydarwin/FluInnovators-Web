package org.fluinnovators.FluInnovatorsBackend.external.aimodel;

import org.fluinnovators.FluInnovatorsBackend.config.ApplicationConfig;
import org.fluinnovators.FluInnovatorsBackend.domain.VaccineResponse;
import org.fluinnovators.FluInnovatorsBackend.external.UnirestRestGetAdapter;
import org.fluinnovators.FluInnovatorsBackend.external.UnirestRestPostAdapter;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.Map;

public class VaccineResponseRestComputeAdapter extends
        UnirestRestPostAdapter<VaccineResponse.VaccineResponseComputeStatus> {

    private final long id;
    public VaccineResponseRestComputeAdapter(long id, Map<String, Object> sampleDetails) {
        super(ApplicationConfig.AI_MODEL_SERVER_URL + "/risk/compute");
        this.id = id;
    }

    @Override
    protected Map<String, Object> queryParams() {
        return Map.of("id", id);
    }

    @Override
    protected JSONObject body() {
        var body = new JSONObject();
        var list = new JSONArray();

        for ()

        body.put("params", list);
        return body;
    }

    @Override
    protected VaccineResponse.VaccineResponseComputeStatus adaptJsonToEntity(JSONObject json) {
        return VaccineResponse.VaccineResponseComputeStatus.of(json.getBoolean("complete"));
    }
}
