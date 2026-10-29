// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 machine boundary. Never truncate a pointer to a Java int. */
public final class Board {
    public static native int readDisplayPixel(int horizontalPosition, int verticalPosition);
    public static native void writeDisplayPixel(int horizontalPosition, int verticalPosition, int colourValue);
    public static native int remoteControl(int kindValue, int action);
    public static native void endRemoteCommand(int stateValue);
    public static native void remoteWait(int stateValue);
    public static native void writeSerial(int value);
    public static native int readSerial();
    public static native int milliseconds();
    public static native int cpuPrivilegeLevel();
    public static native int prepareScreen();
    public static native int screenWidth();
    public static native int screenHeight();
    public static native void putScreenPixel(int horizontalPosition, int verticalPosition, int colourValue);
    public static native void yieldProcessor();
    public static native int createTask(int index);
    public static native int taskState(int index);
    public static native void stop(int stateValue);
    public static native int testCpp();
    public static native int runUserProgram(int index);
    public static native int checkUserProgram();
    public static native int prepareArguments(int itemCount);
    public static native int executeUserFile();
    public static native int executeLinuxFile();
    public static native int argumentByte(int index, int position, int value);
    public static native int terminal(int action);
    public static native int controlUserProgram(int action);
    public static native void switchIo(int action);
    public static native int fileTransferService(int action);
    public static native int networkStatus(int entryValue, int index);
    public static native int networkSettings(int action, int address, int maskValue, int gatewayValue);
    public static native int sendResponse(int address, int orderValue);
    public static native int readResponse(int entryValue);
    public static native int querySystem(int entryValue, int index);
    public static native void powerOff();
}
