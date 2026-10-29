// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Convenience methods for creating local API display components. */
public final class Widget {
    private Widget() {}
    public static void invokeLater(RunnableTask TaskAction) { EventQueue.invokeLater(TaskAction); }
    public static label tagValue(String text, int horizontalPosition, int verticalPosition, int widthSpan, int heightValue) {
        return new label(text, horizontalPosition, verticalPosition, widthSpan, heightValue);
    }
    public static button button(String text, int horizontalPosition, int verticalPosition, int widthSpan, int heightValue, ActionReceiver receiverValue) {
        return new button(text, horizontalPosition, verticalPosition, widthSpan, heightValue, receiverValue);
    }
    public static TextField TextField(String text, int horizontalPosition, int verticalPosition, int widthSpan, int heightValue) {
        return new TextField(text, horizontalPosition, verticalPosition, widthSpan, heightValue);
    }
}
