package com.aspatel.ssg.books.service;

import com.aspatel.ssg.books.configuration.BookProperties;
import com.aspatel.ssg.books.model.Book;
import com.aspatel.ssg.books.repository.BookRepository;
import com.github.mustachejava.Mustache;
import com.github.mustachejava.MustacheFactory;
import java.io.*;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class BookService {

  private final BookRepository bookRepository;
  private final BookProperties bookProperties;
  private final MustacheFactory mustacheFactory;

  public void listAll() {
    final List<Book> books = bookRepository.selectAll();
    if (books.isEmpty()) {
      return;
    }

    bookProperties
        .outputDir()
        .ifPresentOrElse(
            outputDir -> generateBookFiles(outputDir, books),
            () -> System.out.println("\\. Must provide outputDir property to render book files"));
  }

  private void generateBookFiles(final Path outputDir, final List<Book> books) {
    final Mustache mustache = mustacheFactory.compile("book.html");
    final Map<String, Object> context = new HashMap<>();

    for (final Book book : books) {

      context.put("title", book.name());
      context.put("header", book.name());
      context.put("authors", String.join(", ", book.authors()));
      context.put("state", book.state());
      book.series()
          .ifPresent(
              series -> context.put("series", series.name() + ", book " + series.installment()));
      book.rating().ifPresent(rating -> context.put("rating", rating.name()));
      book.review().ifPresent(review -> context.put("review", review));

      try (final StringWriter sw = new StringWriter()) {

        mustache.execute(sw, context);
        final String html = sw.toString();

        final Path outputFile = Path.of(outputDir.toString(), "book_" + book.name() + ".html");
        try (final BufferedWriter fileWriter =
            new BufferedWriter(new FileWriter(outputFile.toString()))) {
          System.out.println("Writing " + outputFile);
          fileWriter.write(html);
        }

        context.clear();

      } catch (final IOException e) {
        throw new UncheckedIOException("Problem rendering " + book, e);
      }
    }
  }
}
