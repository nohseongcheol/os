// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Window connected directly to the built-in JVM and the kernel window manager. */
public final class window extends ScreenElement {
    public window(String windowTitle, int widthSpan, int heightValue) {
        throw new StateException("The native JVM must support creating English API windows.");
    }
    public native void addElement(ScreenElement elementValue);
    public native void showWindow();
    public native void close();
    public native boolean isVisible();
}
