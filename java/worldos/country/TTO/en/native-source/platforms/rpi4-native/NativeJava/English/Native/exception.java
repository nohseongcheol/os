// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** exception: an exception that can be declared, thrown and caught through the English API. */
public class exception extends java.lang.Exception {
    public exception() { super(); }
    public exception(String description) { super(description); }
    public String description() { return getMessage(); }
}
