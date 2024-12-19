package org.fluinnovators.FluInnovatorsBackend.external;

import java.util.concurrent.Future;

public interface RestAdapter<T> {
    String requestUrl();
    Future<T> completeRequest();
}
