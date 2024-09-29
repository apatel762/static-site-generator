package com.aspatel.ssg.books.repository;

import com.aspatel.ssg.books.model.Book;
import java.util.List;

public interface BookRepository {

  List<Book> selectAll();
}
