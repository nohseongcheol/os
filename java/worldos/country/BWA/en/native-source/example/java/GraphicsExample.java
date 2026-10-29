// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class GraphicsExample {
    public static void run() {
        // Draw red, green and blue rectangles on the right of the 640x480 display.
        English.Native.Screen.rectangle(600, 400, 28, 20, 0x0000ff);
        English.Native.Screen.rectangle(600, 425, 28, 20, 0x00ff00);
        English.Native.Screen.rectangle(600, 450, 28, 20, 0xff0000);
        English.Native.Output.writeLine("JAVA 그래픽: RGB");
        English.Native.Output.writeLine("Enter");
        English.Native.Screen.await();
    }
}
