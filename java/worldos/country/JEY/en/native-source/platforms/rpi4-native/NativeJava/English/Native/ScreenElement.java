// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Common contract for built-in JVM display objects; does not retain standard Swing objects. */
public abstract class ScreenElement {
    public native String readText();
    public native void writeText(String text);
    public native void setBounds(int horizontalPosition, int verticalPosition, int widthSpan, int heightValue);
}
