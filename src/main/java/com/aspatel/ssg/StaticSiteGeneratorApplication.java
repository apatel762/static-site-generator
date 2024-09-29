package com.aspatel.ssg;

import com.aspatel.ssg.books.service.BookService;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.springframework.modulith.Modulith;

@Modulith(systemName = "Static Site Generator", sharedModules = "common")
@RequiredArgsConstructor
@ConfigurationPropertiesScan
public class StaticSiteGeneratorApplication implements CommandLineRunner {

  private final BookService bookService;

  public static void main(String[] args) {

    try (final var applicationContext =
        SpringApplication.run(StaticSiteGeneratorApplication.class, args)) {

      /* Using a try-with-resources block here so that the application
         context automatically closes when the command-line runner has
         completed its work.
      */
    }
  }

  @Override
  public void run(final String... args) throws Exception {
    bookService.listAll();
  }
}
