package org.fluinnovators.FluInnovatorsBackend.controller;

import com.fasterxml.jackson.databind.JsonNode;
import org.fluinnovators.FluInnovatorsBackend.domain.VaccineResponse;
import org.fluinnovators.FluInnovatorsBackend.external.aimodel.VaccineResponseRestComputeAdapter;
import org.fluinnovators.FluInnovatorsBackend.external.aimodel.VaccineResponseRestResultAdapter;
import org.fluinnovators.FluInnovatorsBackend.repository.VaccineResponseHolderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.concurrent.Future;

@RestController
public class VaccineResponseController {

    @Autowired
    VaccineResponseHolderRepository repository;

    @PostMapping("/vaccine-response/add")
    @CrossOrigin(origins = "http://localhost:3000")
    public ResponseEntity<VaccineResponse.VaccineResponseHolder> add
            (@RequestParam(value="patientId") int patientId) {
        var newEntry = repository.save(
                VaccineResponse.VaccineResponseHolder.builder().patientId(patientId).build()
        );
        return new ResponseEntity<>(newEntry, HttpStatus.OK);
    }

    @GetMapping("/vaccine-response/result/{id}")
    @CrossOrigin(origins = "http://localhost:3000")
    public ResponseEntity<VaccineResponse> getResult(@PathVariable long id) {
        try {
            var adapter = new VaccineResponseRestResultAdapter(id);
            Future<VaccineResponse> result = adapter.completeRequest();
            return new ResponseEntity<>(result.get(), HttpStatus.OK);
        } catch (Exception exception) {
            return new ResponseEntity<>(VaccineResponse.empty(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @PostMapping("/vaccine-response/compute/{id}")
    @CrossOrigin(origins = "http://localhost:3000")
    public ResponseEntity<VaccineResponse.VaccineResponseComputeStatus>
        postCompute(@PathVariable long id, @RequestBody JsonNode requestBody) {
        try {

            var adapter = new VaccineResponseRestComputeAdapter(id, requestBody);
            var result = adapter.completeRequest();
            return new ResponseEntity<>(result.get(), HttpStatus.OK);

        } catch (Exception exception) {
            return new ResponseEntity<>(
                    VaccineResponse.VaccineResponseComputeStatus.empty(),
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

}
