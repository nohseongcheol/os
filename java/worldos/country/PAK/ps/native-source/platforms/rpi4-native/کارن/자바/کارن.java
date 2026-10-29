// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 도구 전용 SVC نښلېدل. 기존 x86 도구 원문을 함께 빌드한다. */
public final class کارن {
    public static native int 파일서술자열기(int[] نوم, int امستنې);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ارزښت);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] نوم, int[] اومتوک);
    public static native int ليکل_دوتنه(int[] نوم, int[] اومتوک, int اوږدوالى_ارزښت);
    public static native int لوستل_2(String ليکنه);
    public static native int ليکل_لوښه_ارزښت(int ارزښت);
    public static native int 인수개수();
    public static native String 인수(int لړیال);
    public static native int 도구번호();
    public static native int 화면연결(int چار, int لړیال, int 가, int 나, int 다, int 라);
    public static native int 화면글(int لړیال, int[] ليکنه, int اوږدوالى_ارزښت);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int بهنګ_مهار(int چار, int 서술자, int ارزښت);
    public static native int پيوستول_بهنګ(int 서술자, int پته, int درشل_ارزښت);
    public static native int 통신열기(int درشل_ارزښت);
    public static native int استول_جال(int 서술자, int پته, int درشل_ارزښت, int[] اومتوک, int اوږدوالى_ارزښت);
    public static native int 통신받기(int 서술자, int[] اومتوک, int اوږدوالى_ارزښت);
    public static native int جال_درشل(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
