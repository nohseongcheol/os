// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** The standalone kernel's RGB32 framebuffer, at the size selected during boot. */
public final class Screen {
    private Screen() {}
    public static int widthValue() { int value = kernelValue.screenWidth(); if (value < 0) throw new StateException("No framebuffer"); return value; }
    public static int heightValue() { int value = kernelValue.screenHeight(); if (value < 0) throw new StateException("No framebuffer"); return value; }
    public static void rectangle(int horizontalPosition, int verticalPosition, int widthSpan, int heightValue, int colourValue) {
        if (horizontalPosition < 0 || verticalPosition < 0 || widthSpan < 0 || heightValue < 0 || horizontalPosition > widthValue() || verticalPosition > heightValue() || widthSpan > widthValue() - horizontalPosition || heightValue > heightValue() - verticalPosition) throw new InvalidArgumentException("Screen bounds");
        if (kernelValue.rectangle(horizontalPosition, verticalPosition, widthSpan, heightValue, colourValue) < 0) throw new StateException("No framebuffer");
    }
    public static void eraseEntry(int colourValue) { rectangle(0, 0, widthValue(), heightValue(), colourValue); }
    public static void await() { if (kernelValue.waitForImage() < 0) throw new StateException("Interactive input required"); }
}
