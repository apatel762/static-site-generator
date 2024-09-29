package com.aspatel.ssg.books.repository;

import com.aspatel.ssg.books.configuration.BookProperties;
import com.aspatel.ssg.books.model.Book;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Path;
import java.util.Collections;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

@Repository
@RequiredArgsConstructor
public class JsonBookRepository implements BookRepository {

  private final BookProperties bookProperties;
  private final ObjectMapper objectMapper;

  @Override
  public List<Book> selectAll() {
    return bookProperties.inputFile().map(this::loadJson).orElse(Collections.emptyList());
  }

  private List<Book> loadJson(final Path path) {
    try {
      return objectMapper.readValue(path.toFile(), new TypeReference<>() {});

    } catch (final FileNotFoundException e) {
      System.out.println("Skipping processing of book data...");
      System.out.println("\\. Not found -> " + path);
      return Collections.emptyList();

    } catch (final IOException e) {
      throw new UncheckedIOException("Problem reading " + path, e);
    }
  }
}
