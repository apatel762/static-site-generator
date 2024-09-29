package com.aspatel.ssg.books.model;

import java.util.List;
import java.util.Optional;

public record Book(
    String name,
    List<String> authors,
    Optional<Series> series,
    State state,
    Optional<Rating> rating,
    Optional<String> review) {}
