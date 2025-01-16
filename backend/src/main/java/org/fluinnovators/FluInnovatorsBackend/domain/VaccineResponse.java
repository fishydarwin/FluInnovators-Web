package org.fluinnovators.FluInnovatorsBackend.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.Builder;
import lombok.Data;
import lombok.Getter;

public record VaccineResponse(long id, boolean complete, boolean atRisk) {

    public static VaccineResponse of(long id, boolean complete, boolean atRisk) {
        return new VaccineResponse(id, complete, atRisk);
    }

    public static VaccineResponse empty() {
        return new VaccineResponse(-1, false, false);
    }

    public record VaccineResponseComputeStatus(boolean complete) {

        public static VaccineResponseComputeStatus of(boolean complete) {
            return new VaccineResponseComputeStatus(complete);
        }

        public static VaccineResponseComputeStatus empty() {
            return new VaccineResponseComputeStatus(false);
        }
    }

    @Entity
    @Builder
    public static class VaccineResponseHolder {
        @Id
        private int id;
        private int patientId;
    }
}
