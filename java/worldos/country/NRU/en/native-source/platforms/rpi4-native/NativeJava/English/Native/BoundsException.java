// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** BoundsException: an exception that can be declared, thrown and caught through the English API. */
public class BoundsException extends java.lang.IndexOutOfBoundsException {
    public BoundsException() { super(); }
    public BoundsException(String description) { super(description); }
    public String description() { return getMessage(); }
}
