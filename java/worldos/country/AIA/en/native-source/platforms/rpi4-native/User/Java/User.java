// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** SVC bridge for ARM64 EL0 Java tools. Built together with the existing x86 tool sources. */
public final class User {
    public static native int openFileDescriptor(int[] name, int settings);
    public static native int readOneFileByte(int descriptorEntry);
    public static native int writeOneFileByte(int descriptorEntry, int value);
    public static native int closeFileDescriptor(int descriptorEntry);
    public static native int readFile(int[] name, int[] data);
    public static native int writeFile(int[] name, int[] data, int lengthValue);
    public static native int write(String text);
    public static native int writeCharacterValue(int value);
    public static native int argumentsCount();
    public static native String arguments(int index);
    public static native int toolNumber();
    public static native int screenConnection(int action, int index, int firstOperand, int secondOperand, int thirdOperand, int fourthOperand);
    public static native int screenText(int index, int[] text, int lengthValue);
    public static native int screenWidth();
    public static native int screenHeight();
    public static native int streamControl(int action, int descriptorEntry, int value);
    public static native int connectStream(int descriptorEntry, int address, int portValue);
    public static native int openNetwork(int portValue);
    public static native int sendNetwork(int descriptorEntry, int address, int portValue, int[] data, int lengthValue);
    public static native int receiveNetwork(int descriptorEntry, int[] data, int lengthValue);
    public static native int networkPort(int descriptorEntry);
    public static native int milliseconds();
    public static native int waitForImage();
    public static native int rectangle(int horizontalPosition, int verticalPosition, int widthSpan, int heightValue, int colourValue);
}
