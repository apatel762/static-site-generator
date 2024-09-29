package com.aspatel.ssg;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;
import org.springframework.modulith.test.ApplicationModuleTest;
import org.springframework.test.context.ActiveProfiles;

@ApplicationModuleTest
@ActiveProfiles("local")
public class ModularityTests {

  private final ApplicationModules modules =
      ApplicationModules.of(StaticSiteGeneratorApplication.class);

  @Test
  @DisplayName("Verify the modularity of the application packages")
  void verifyModularity() {
    modules.verify();
  }
}
