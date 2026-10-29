// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** API for jkoros user ELF programs, not Linux/JVM JNI or java.net. */
public final class User {
    public static native int openFileDescriptor(int[] fileEntryName, int openSettings);
    public static native int readOneFileByte(int fileDescriptor);
    public static native int writeOneFileByte(int fileDescriptor, int byteValue);
    public static native int closeFileDescriptor(int fileDescriptor);
    public static native int commitFileStorage(int fileDescriptor);
    public static native int readFile(int[] name, int[] data);
    public static native int writeCharacterValue(int Characters);
    public static native int writeFile(int[] name, int[] data, int lengthValue);
    public static native int write(String contentValue);
    public static native int argumentsCount();
    public static native String arguments(int index);
    public static native int executionPermission();
    public static native int openNetwork(int localPort);
    public static native int sendData(int handleValue, int address, int destinationPort, int[] data, int lengthValue);
    public static native int receiveData(int handleValue, int[] data, int limitMilliseconds);
    public static native int closeNetwork(int handleValue);
    public static native int ownAddress();
    public static native int sentAddress(int handleValue);
    public static native int sentPort(int handleValue);
}
