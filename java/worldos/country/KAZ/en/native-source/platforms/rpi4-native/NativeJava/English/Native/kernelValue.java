// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Fixed ABI connected by the built-in JVM, not JNI or a loader for arbitrary native methods. */
public final class kernelValue {
    private kernelValue() {}
    public static native int milliseconds();
    public static native int waitForImage();
    public static native int screenWidth();
    public static native int screenHeight();
    public static native int rectangle(int horizontalPosition, int verticalPosition, int widthSpan, int heightValue, int colourValue);
}
