package com.aspatel.ssg.common;

import com.github.mustachejava.MustacheFactory;
import com.github.mustachejava.SafeMustacheFactory;
import java.util.Set;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class TemplatingConfiguration {

  @Bean
  public MustacheFactory mustacheFactory() {
    return new SafeMustacheFactory(Set.of("book.html"), "templates");
  }
}
