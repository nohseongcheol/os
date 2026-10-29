// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** InputOutputException: an exception that can be declared, thrown and caught through the English API. */
public class InputOutputException extends java.io.IOException {
    public InputOutputException() { super(); }
    public InputOutputException(String description) { super(description); }
    public String description() { return getMessage(); }
}
