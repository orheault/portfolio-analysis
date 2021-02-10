package com.olivier.portfolioanalysis.company;

import javax.persistence.Entity;

@Entity
public class Security {
    private String symbol;
    private String description;

    public Security() {
    }

    public Security(String symbol, String description) {
        this.symbol = symbol;
        this.description = description;
    }

    @javax.persistence.Id
    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
