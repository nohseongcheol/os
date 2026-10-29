// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** NegativeArraySizeFailure: an exception that can be declared, thrown and caught through the English API. */
public class NegativeArraySizeFailure extends java.lang.NegativeArraySizeException {
    public NegativeArraySizeFailure() { super(); }
    public NegativeArraySizeFailure(String description) { super(description); }
    public String description() { return getMessage(); }
}
