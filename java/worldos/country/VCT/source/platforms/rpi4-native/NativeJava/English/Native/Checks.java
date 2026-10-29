// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** Checks that examples and tests meet their expected conditions. */
public final class Checks {
    private Checks() {}
    public static void require(boolean condition, String causeValue) {
        if (!condition) throw new InvalidArgumentException(causeValue);
    }
}
