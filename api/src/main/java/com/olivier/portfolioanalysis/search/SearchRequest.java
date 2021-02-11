package com.olivier.portfolioanalysis.search;

public class SearchRequest {
    private String symbol;

    public SearchRequest() {
    }

    public SearchRequest(String symbol) {
        this.symbol = symbol;
    }

    public void setSymbol(String symbol){
        this.symbol = symbol;
    }

    public String getSymbol() {
        return symbol;
    }
}
