// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** oma JVM이 연결하는 고정 ABI. JNI 또는 임의의 native menetelmä_ARVO 로더가 아니다. */
public final class ydin_ARVO {
    private ydin_ARVO() {}
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int suorakulmio(int 가로, int toimiala_toimi, int 폭, int 높이, int 색);
}
