package com.aspatel.ssg;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.test.ApplicationModuleTest;
import org.springframework.modulith.test.ApplicationModuleTest.BootstrapMode;
import org.springframework.test.context.ActiveProfiles;

@ActiveProfiles("local")
@ApplicationModuleTest(BootstrapMode.ALL_DEPENDENCIES)
public class ModularityTests {

  @Test
  @DisplayName("Verify the modularity of the application packages")
  void verifyModularity() {}
}
