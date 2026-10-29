// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** ArrayBoundsException: an exception that can be declared, thrown and caught through the English API. */
public class ArrayBoundsException extends BoundsException {
    public ArrayBoundsException() { super(); }
    public ArrayBoundsException(String description) { super(description); }
    public String description() { return getMessage(); }
}
