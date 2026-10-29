// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros потребител ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class потребител {
    public static native int 파일서술자열기(int[] Файл_запис_препратка_към_клетка, int отварям_Настройки);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int байт_стойност);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int фиксиране_място_за_съхранение_на_файлове(int 파일서술자);
    public static native int 파일읽기(int[] Име, int[] данни);
    public static native int записване_знак_стойност(int 문자);
    public static native int записване_Файл(int[] Име, int[] данни, int 길이);
    public static native int Писане(String Съдържание_стойност);
    public static native int 인수개수();
    public static native String Параметри(int индекс);
    public static native int 실행권한();
    public static native int отварям_мрежа(int локален_порт);
    public static native int изпращам_данни(int манипулатор_стойност, int адрес, int местоназначение_порт, int[] данни, int 길이);
    public static native int получавам_данни(int манипулатор_стойност, int[] данни, int 제한밀리초);
    public static native int затварям_мрежа(int манипулатор_стойност);
    public static native int 내주소();
    public static native int 보낸주소(int манипулатор_стойност);
    public static native int 보낸창구(int манипулатор_стойност);
}
