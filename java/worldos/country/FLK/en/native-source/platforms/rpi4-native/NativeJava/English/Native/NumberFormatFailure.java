// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** NumberFormatFailure: an exception that can be declared, thrown and caught through the English API. */
public class NumberFormatFailure extends InvalidArgumentException {
    public NumberFormatFailure() { super(); }
    public NumberFormatFailure(String description) { super(description); }
    public String description() { return getMessage(); }
}
