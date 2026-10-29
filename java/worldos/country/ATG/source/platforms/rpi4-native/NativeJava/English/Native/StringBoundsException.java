// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** StringBoundsException: an exception that can be declared, thrown and caught through the English API. */
public class StringBoundsException extends BoundsException {
    public StringBoundsException() { super(); }
    public StringBoundsException(String description) { super(description); }
    public String description() { return getMessage(); }
}
