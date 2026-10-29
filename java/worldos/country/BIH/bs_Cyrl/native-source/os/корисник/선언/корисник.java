// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros корисник ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class корисник {
    public static native int 파일서술자열기(int[] фајл_унос_назив, int отворити_Подешавања);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int бајт_вриједност);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] назив, int[] подаци);
    public static native int писати_знак_вриједност(int 문자);
    public static native int писати_фајл(int[] назив, int[] подаци, int дужина_вриједност);
    public static native int писати(String Садржај_вриједност);
    public static native int 인수개수();
    public static native String 인수(int индекс);
    public static native int 실행권한();
    public static native int отворити_Мрежа(int локални_порт);
    public static native int послати_подаци(int хватиште_вриједност, int адреса, int одредиште_порт, int[] подаци, int дужина_вриједност);
    public static native int 자료받기(int хватиште_вриједност, int[] подаци, int 제한밀리초);
    public static native int затворити_Мрежа(int хватиште_вриједност);
    public static native int 내주소();
    public static native int 보낸주소(int хватиште_вриједност);
    public static native int 보낸창구(int хватиште_вриједност);
}
