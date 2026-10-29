// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;

/** Indicates interruption of an operation waiting for a thread, rather than termination of the task itself. */
public class WaitInterruptedException extends java.lang.InterruptedException {
    public WaitInterruptedException() { super(); }
    public WaitInterruptedException(String description) { super(description); }
    public String description() { return getMessage(); }
}
