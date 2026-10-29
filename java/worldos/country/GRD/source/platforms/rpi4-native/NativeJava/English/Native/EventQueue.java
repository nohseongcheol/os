// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Submits a task to the built-in display event queue. */
public final class EventQueue {
    private EventQueue() {}
    public static native void invokeLater(RunnableTask TaskAction);
    public static native boolean isEventDispatching();
}
