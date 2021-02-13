package com.olivier.portfolioanalysis;

import com.olivier.portfolioanalysis.security.Security;
import com.olivier.portfolioanalysis.security.SecurityRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DatabaseLoader  implements CommandLineRunner {
    private  final SecurityRepository repository;

    @Autowired
    public DatabaseLoader(SecurityRepository repository) {
        this.repository = repository;
    }

    @Override
    public void run(String... strings) throws Exception {
        this.repository.save(new Security("T.TO", "Telus Corporation"));
    }
}
