// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** StateException: an exception that can be declared, thrown and caught through the English API. */
public class StateException extends java.lang.IllegalStateException {
    public StateException() { super(); }
    public StateException(String description) { super(description); }
    public String description() { return getMessage(); }
}
