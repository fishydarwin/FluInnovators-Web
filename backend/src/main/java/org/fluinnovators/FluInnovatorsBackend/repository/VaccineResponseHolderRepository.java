package org.fluinnovators.FluInnovatorsBackend.repository;

import org.fluinnovators.FluInnovatorsBackend.domain.VaccineResponse;
import org.springframework.data.jpa.repository.JpaRepository;

public interface VaccineResponseHolderRepository
        extends JpaRepository<VaccineResponse.VaccineResponseHolder, Integer> {
}
