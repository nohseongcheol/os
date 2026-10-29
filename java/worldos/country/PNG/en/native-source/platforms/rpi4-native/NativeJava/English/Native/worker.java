// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Execution flow managed by the built-in JVM scheduler, without wrapping a standard Thread. */
public final class worker {
    public worker(RunnableTask TaskAction) {
        throw new StateException("The native JVM must support creating English API threads.");
    }
    public native void startTask() throws ThreadStateException;
    public native void await() throws WaitInterruptedException;
    public native boolean isAlive();
    public static native void yieldTask();
}
