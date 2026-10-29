// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class NativeBridge {
    private static native long processIdentifier();
    public static void main(String[] arguments) {
        System.loadLibrary("worldos_jni");
        if (processIdentifier()!=ProcessHandle.current().pid()) throw new AssertionError("JNI getpid mismatch");
        System.out.println("PASS jni-native-library-getpid");
    }
}
