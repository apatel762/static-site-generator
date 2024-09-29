package com.aspatel.ssg;

import com.aspatel.ssg.books.service.BookService;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.springframework.modulith.Modulith;

@Modulith
@RequiredArgsConstructor
@ConfigurationPropertiesScan
public class StaticSiteGeneratorApplication implements CommandLineRunner {

  private final BookService bookService;

  public static void main(String[] args) {
    SpringApplication.run(StaticSiteGeneratorApplication.class, args);
  }

  @Override
  public void run(final String... args) throws Exception {
    bookService.listAll();
    System.exit(0);
  }
}
