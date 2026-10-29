// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Restricted compiler native boundary for x86 instructions and physical-address access only. */
public final class deviceValue {
    public static native int fileMemory();
    public static native int javaFileBundle();
    public static native int javaFileBundleSize();
    public static native int readIoByte(int index);
    public static native void writeIoByte(int index, int value);
    public static native int readMemory(int address);
    public static native void writeMemory(int address, int value);
    public static native int bootMarker();
    public static native int bootInformation();
    public static native int arrayUsage();
    public static native void yieldBriefly();
    public static native void haltExecution();
    public static native void finishTest(int value);
    public static native int readIoInteger(int index);
    public static native void writeIoInteger(int index, int value);
    public static native void writeIoShort(int index, int value);
    public static native int readIoShort(int index);
    public static native void prepareUserProgram();
    public static native void userClearContents();
    public static native int runUserProgram(int entryAddress, int operandStackAddress);
    public static native int milliseconds();
    public static native int userRemainingMilliseconds();
    public static native int ExecutableBundle();
    public static native int executableBundleSize();
    public static native int networkMemory();
}
