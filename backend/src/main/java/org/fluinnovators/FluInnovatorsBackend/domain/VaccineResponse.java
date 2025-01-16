package org.fluinnovators.FluInnovatorsBackend.domain;

import lombok.Getter;

public record VaccineResponse(long id, boolean complete, boolean atRisk) {

    public static VaccineResponse of(long id, boolean complete, boolean atRisk) {
        return new VaccineResponse(id, complete, atRisk);
    }

    public static VaccineResponse empty() {
        return new VaccineResponse(-1, false, false);
    }

    @Getter
    public static class VaccineResponseComputeStatus {
        private final boolean complete;

        public VaccineResponseComputeStatus(boolean complete) {
            this.complete = complete;
        }

        public static VaccineResponseComputeStatus of(boolean complete) {
            return new VaccineResponseComputeStatus(complete);
        }

        public static VaccineResponseComputeStatus empty() {
            return new VaccineResponseComputeStatus(false);
        }
    }
}
