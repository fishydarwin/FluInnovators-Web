package org.fluinnovators.FluInnovatorsBackend.domain;

public record VaccineResponse(long id, boolean complete, boolean atRisk) {

    public static VaccineResponse of(long id, boolean complete, boolean atRisk) {
        return new VaccineResponse(id, complete, atRisk);
    }

    public static VaccineResponse empty() {
        return new VaccineResponse(-1, false, false);
    }
}
