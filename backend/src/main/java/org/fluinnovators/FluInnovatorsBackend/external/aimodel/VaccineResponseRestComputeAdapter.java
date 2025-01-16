package org.fluinnovators.FluInnovatorsBackend.external.aimodel;

import com.fasterxml.jackson.databind.JsonNode;
import org.fluinnovators.FluInnovatorsBackend.config.ApplicationConfig;
import org.fluinnovators.FluInnovatorsBackend.domain.VaccineResponse;
import org.fluinnovators.FluInnovatorsBackend.external.UnirestRestPostAdapter;
import org.fluinnovators.FluInnovatorsBackend.util.JSONUtils;
import org.json.JSONObject;

import java.util.Map;

public class VaccineResponseRestComputeAdapter extends
        UnirestRestPostAdapter<VaccineResponse.VaccineResponseComputeStatus> {

    private final long id;
    private final JsonNode sampleDetails;
    public VaccineResponseRestComputeAdapter(long id, JsonNode sampleDetails) {
        super(ApplicationConfig.AI_MODEL_SERVER_URL + "/risk/compute");
        this.id = id;
        this.sampleDetails = sampleDetails;
    }

    @Override
    protected Map<String, Object> queryParams() {
        return Map.of("id", id);
    }

    @Override
    protected JSONObject body() {
        return JSONUtils.jacksonToJSON(sampleDetails);
    }

    @Override
    protected VaccineResponse.VaccineResponseComputeStatus adaptJsonToEntity(JSONObject json) {
        return VaccineResponse.VaccineResponseComputeStatus.of(json.getBoolean("complete"));
    }
}
