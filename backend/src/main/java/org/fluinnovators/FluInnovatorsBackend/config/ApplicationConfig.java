package org.fluinnovators.FluInnovatorsBackend.config;

import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

@Component
public class ApplicationConfig {

    public static String AI_MODEL_SERVER_URL;

    public ApplicationConfig(Environment environment) {
        AI_MODEL_SERVER_URL = environment.getProperty("fluinnovators.ai.url", "http://127.0.0.1:5123");
    }

}
