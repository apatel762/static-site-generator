package com.aspatel.ssg.books.configuration;

import jakarta.annotation.Nullable;
import java.nio.file.Path;
import java.util.Optional;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.bind.ConstructorBinding;
import org.springframework.validation.annotation.Validated;

@Validated
@ConfigurationProperties(prefix = "ssg.books")
public record BookProperties(Optional<Path> inputFile, Optional<Path> outputDir) {

  @ConstructorBinding
  public BookProperties(@Nullable final Path inputFile, @Nullable final Path outputDir) {
    this(Optional.ofNullable(inputFile), Optional.ofNullable(outputDir));
  }
}
