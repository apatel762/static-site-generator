package com.aspatel.ssg.common.converter;

import java.nio.file.Path;
import java.util.Optional;
import lombok.NonNull;
import org.springframework.boot.context.properties.ConfigurationPropertiesBinding;
import org.springframework.core.convert.converter.Converter;
import org.springframework.stereotype.Component;

@Component
@ConfigurationPropertiesBinding
public class PathConverter implements Converter<String, Optional<Path>> {

  @Override
  public Optional<Path> convert(@NonNull final String path) {
    return Optional.of(path).filter(p -> !p.isBlank()).map(Path::of);
  }
}
