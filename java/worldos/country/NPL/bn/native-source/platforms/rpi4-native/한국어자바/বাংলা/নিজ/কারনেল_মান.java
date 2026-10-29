// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
/** নিজ JVM이 연결하는 고정 ABI. JNI 또는 임의의 native পদ্ধতি_মান 로더가 아니다. */
public final class কারনেল_মান {
    private কারনেল_মান() {}
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int 사각형(int 가로, int উল্লম্ব_পদ, int 폭, int 높이, int 색);
}
