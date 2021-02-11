package com.olivier.portfolioanalysis.search;

import com.olivier.portfolioanalysis.company.Security;
import com.olivier.portfolioanalysis.company.SecurityRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class SearchController {

    @Autowired
    SecurityRepository securityRepository;

    @PostMapping(value = "/search", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<Security>> search(@RequestBody SearchRequest request) {
        System.out.println("symbol " + request.getSymbol());
        var symbols = securityRepository.findBySymbolStartingWithIgnoreCaseOrderBySymbol(request.getSymbol());
        return new ResponseEntity<>(symbols, HttpStatus.OK);
    }



}
