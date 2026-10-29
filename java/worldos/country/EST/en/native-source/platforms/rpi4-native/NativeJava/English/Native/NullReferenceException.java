// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** NullReferenceException: an exception that can be declared, thrown and caught through the English API. */
public class NullReferenceException extends java.lang.NullPointerException {
    public NullReferenceException() { super(); }
    public NullReferenceException(String description) { super(description); }
    public String description() { return getMessage(); }
}
