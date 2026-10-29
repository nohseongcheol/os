// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros кулланучы ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class кулланучы {
    public static native int 파일서술자열기(int[] файл_кертү_исем, int ачу_Параметрлар);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int байт_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] исем, int[] мәгълүмат);
    public static native int язу_символ_VALUE(int 문자);
    public static native int язу_файл(int[] исем, int[] мәгълүмат, int озынлык_VALUE);
    public static native int язу(String Эчтәлек_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int ачу_Челтәр(int локаль_порт);
    public static native int җибәрү_мәгълүмат(int дескриптор_VALUE, int адрес, int күчерү_урыны_порт, int[] мәгълүмат, int озынлык_VALUE);
    public static native int 자료받기(int дескриптор_VALUE, int[] мәгълүмат, int 제한밀리초);
    public static native int чик_Челтәр(int дескриптор_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int дескриптор_VALUE);
    public static native int 보낸창구(int дескриптор_VALUE);
}
