// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** Eigen JVM이 연결하는 고정 ABI. JNI 또는 임의의 native methode_WAARDE 로더가 아니다. */
public final class kernel_WAARDE {
    private kernel_WAARDE() {}
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 화면너비();
    public static native int scherm_hoogte();
    public static native int rechthoek(int 가로, int Verticaal_functie, int 폭, int hoogte_WAARDE, int 색);
}
