package com.aspatel.ssg.books.repository;

import com.aspatel.ssg.books.model.Book;
import java.util.List;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Repository;

@Profile("local")
@Primary
@Repository
public class MockBookRepository implements BookRepository {

  @Override
  public List<Book> selectAll() {
    return List.of();
  }
}
