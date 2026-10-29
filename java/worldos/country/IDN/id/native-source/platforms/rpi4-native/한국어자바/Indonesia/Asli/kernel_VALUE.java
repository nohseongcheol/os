// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** Asli JVM이 연결하는 고정 ABI. JNI 또는 임의의 native metode_VALUE 로더가 아니다. */
public final class kernel_VALUE {
    private kernel_VALUE() {}
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int persegi(int 가로, int Vertikal_posisi, int 폭, int 높이, int 색);
}
