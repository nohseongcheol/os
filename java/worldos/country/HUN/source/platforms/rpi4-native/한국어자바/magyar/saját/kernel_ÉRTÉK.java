// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** saját JVM이 연결하는 고정 ABI. JNI 또는 임의의 native metódus_ÉRTÉK 로더가 아니다. */
public final class kernel_ÉRTÉK {
    private kernel_ÉRTÉK() {}
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int téglalap(int 가로, int szektor_pozíció, int 폭, int 높이, int 색);
}
