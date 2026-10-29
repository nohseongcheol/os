// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** InvalidArgumentException: an exception that can be declared, thrown and caught through the English API. */
public class InvalidArgumentException extends java.lang.IllegalArgumentException {
    public InvalidArgumentException() { super(); }
    public InvalidArgumentException(String description) { super(description); }
    public String description() { return getMessage(); }
}
