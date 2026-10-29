// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 도구 전용 SVC མཐུད. 기존 x86 도구 원문을 함께 빌드한다. */
public final class 사용자 {
    public static native int 파일서술자열기(int[] མིང, int གཞི_སྒྲིག_ཚུ);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int 값);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] མིང, int[] 자료);
    public static native int 파일쓰기(int[] མིང, int[] 자료, int 길이);
    public static native int བྲིས(String བརྟག_ཞིབ);
    public static native int 문자쓰기(int 값);
    public static native int 인수개수();
    public static native String 인수(int 번호);
    public static native int 도구번호();
    public static native int 화면연결(int བྱ_བ, int 번호, int 가, int 나, int 다, int 라);
    public static native int 화면글(int 번호, int[] བརྟག_ཞིབ, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int 흐름제어(int བྱ_བ, int 서술자, int 값);
    public static native int 흐름연결(int 서술자, int 주소, int 창구);
    public static native int 통신열기(int 창구);
    public static native int 통신보내기(int 서술자, int 주소, int 창구, int[] 자료, int 길이);
    public static native int 통신받기(int 서술자, int[] 자료, int 길이);
    public static native int 통신창구(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
