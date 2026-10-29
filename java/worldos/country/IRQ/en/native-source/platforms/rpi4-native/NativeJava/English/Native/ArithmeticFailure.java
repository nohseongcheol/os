// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** ArithmeticFailure: an exception that can be declared, thrown and caught through the English API. */
public class ArithmeticFailure extends java.lang.ArithmeticException {
    public ArithmeticFailure() { super(); }
    public ArithmeticFailure(String description) { super(description); }
    public String description() { return getMessage(); }
}
