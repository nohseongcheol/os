// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros 사용자 ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class 사용자 {
    public static native int 파일서술자열기(int[] 파일이름, int 열기설정);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int 바이트);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] נאָמען, int[] 자료);
    public static native int 문자쓰기(int 문자);
    public static native int 파일쓰기(int[] נאָמען, int[] 자료, int 길이);
    public static native int 쓰기(String 내용);
    public static native int 인수개수();
    public static native String 인수(int 번호);
    public static native int 실행권한();
    public static native int 통신열기(int 지역창구);
    public static native int 자료보내기(int 손잡이, int 주소, int 목적창구, int[] 자료, int 길이);
    public static native int 자료받기(int 손잡이, int[] 자료, int 제한밀리초);
    public static native int 통신닫기(int 손잡이);
    public static native int 내주소();
    public static native int 보낸주소(int 손잡이);
    public static native int 보낸창구(int 손잡이);
}
