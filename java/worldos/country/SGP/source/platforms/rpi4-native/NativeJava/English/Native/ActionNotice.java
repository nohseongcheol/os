// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Action notification created by the built-in JVM event handler. */
public final class ActionNotice {
    private ActionNotice() {}
    public native String commandText();
    public native ScreenElement eventSource();
    public native int index();
}
