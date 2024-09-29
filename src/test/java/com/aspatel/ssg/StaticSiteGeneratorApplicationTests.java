package com.aspatel.ssg;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest
@ActiveProfiles("local")
class StaticSiteGeneratorApplicationTests {

  @Test
  @DisplayName("Ensure that the application context starts up")
  void contextLoads() {}
}
