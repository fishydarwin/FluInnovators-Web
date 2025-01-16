package org.fluinnovators.FluInnovatorsBackend.util;

import com.fasterxml.jackson.databind.JsonNode;
import org.json.JSONObject;

public class JSONUtils {

    public static JSONObject jacksonToJSON(JsonNode jsonNode) {
        return new JSONObject(jsonNode.toString());
    }

}
