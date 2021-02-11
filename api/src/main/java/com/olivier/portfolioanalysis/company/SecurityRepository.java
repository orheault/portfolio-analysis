package com.olivier.portfolioanalysis.company;

import org.springframework.data.repository.CrudRepository;
import java.util.List;

public interface SecurityRepository extends CrudRepository<Security, String> {
    List<Security> findBySymbolStartingWithIgnoreCaseOrderBySymbol(String symbol);
}
