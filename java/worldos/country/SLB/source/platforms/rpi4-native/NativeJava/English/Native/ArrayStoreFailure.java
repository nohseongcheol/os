// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** ArrayStoreFailure: an exception that can be declared, thrown and caught through the English API. */
public class ArrayStoreFailure extends java.lang.ArrayStoreException {
    public ArrayStoreFailure() { super(); }
    public ArrayStoreFailure(String description) { super(description); }
    public String description() { return getMessage(); }
}
