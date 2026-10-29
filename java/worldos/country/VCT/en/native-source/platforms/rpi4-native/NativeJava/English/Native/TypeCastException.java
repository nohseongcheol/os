// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** TypeCastException: an exception that can be declared, thrown and caught through the English API. */
public class TypeCastException extends java.lang.ClassCastException {
    public TypeCastException() { super(); }
    public TypeCastException(String description) { super(description); }
    public String description() { return getMessage(); }
}
