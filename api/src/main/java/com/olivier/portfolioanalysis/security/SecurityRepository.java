package com.olivier.portfolioanalysis.security;

import org.springframework.data.repository.CrudRepository;
import java.util.List;

public interface SecurityRepository extends CrudRepository<Security, String> {
    List<Security> findBySymbolStartingWithIgnoreCaseOrderBySymbol(String symbol);
}
