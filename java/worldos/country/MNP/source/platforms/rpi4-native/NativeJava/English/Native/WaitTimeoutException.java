// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** WaitTimeoutException: an exception that can be declared, thrown and caught through the English API. */
public class WaitTimeoutException extends InputOutputException {
    public WaitTimeoutException() { super(); }
    public WaitTimeoutException(String description) { super(description); }
    public String description() { return getMessage(); }
}
