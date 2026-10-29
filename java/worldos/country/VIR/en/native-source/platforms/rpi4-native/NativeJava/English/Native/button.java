// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Button that sends action notifications in the built-in display. */
public final class button extends ScreenElement {
    public button(String text, int horizontalPosition, int verticalPosition, int widthSpan, int heightValue, ActionReceiver receiverValue) {
        throw new StateException("The native JVM must support creating English API buttons.");
    }
    public native void setActionReceiver(ActionReceiver receiverValue);
}
