package org.fluinnovators.FluInnovatorsBackend.controller;

import org.fluinnovators.FluInnovatorsBackend.domain.VaccineResponse;
import org.fluinnovators.FluInnovatorsBackend.external.aimodel.VaccineResponseRestAdapter;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.Future;

@RestController
public class VaccineResponseController {


    @GetMapping("/vaccine-response/result/{id}")
    @CrossOrigin(origins = "http://localhost:3000")
    public ResponseEntity<VaccineResponse> getResult(@PathVariable long id) {
        try {
            var adapter = new VaccineResponseRestAdapter(id);
            Future<VaccineResponse> result = adapter.completeRequest();
            return new ResponseEntity<>(result.get(), HttpStatus.OK);
        } catch (Exception exception) {
            return new ResponseEntity<>(VaccineResponse.empty(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}
