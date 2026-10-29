// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** ExecutionException: an exception that can be declared, thrown and caught through the English API. */
public class ExecutionException extends java.lang.RuntimeException {
    public ExecutionException() { super(); }
    public ExecutionException(String description) { super(description); }
    public String description() { return getMessage(); }
}
