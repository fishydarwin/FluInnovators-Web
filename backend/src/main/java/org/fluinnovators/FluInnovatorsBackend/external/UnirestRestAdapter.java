package org.fluinnovators.FluInnovatorsBackend.external;

import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.request.HttpRequest;
import org.json.JSONObject;

import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public abstract class UnirestRestAdapter<T> implements RestAdapter<T> {

    protected final String requestUrl;
    public UnirestRestAdapter(String requestUrl) {
        this.requestUrl = requestUrl;
    }

    private static final ExecutorService unirestThreadPool =
            Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());

    protected abstract Map<String, Object> queryParams();
    protected abstract T adaptJsonToEntity(JSONObject json);

    @Override
    public String requestUrl() {
        return requestUrl;
    }

    @Override
    public Future<T> completeRequest() {
        return unirestThreadPool.submit(() -> {
            HttpRequest request = Unirest.get(requestUrl)
                    .header("accept", "application/json")
                    .queryString(queryParams());
            return adaptJsonToEntity(request.asJson().getBody().getObject());
        });
    }
}
