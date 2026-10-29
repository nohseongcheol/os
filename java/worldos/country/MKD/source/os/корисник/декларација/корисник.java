// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros корисник ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class корисник {
    public static native int 파일서술자열기(int[] датотека_внес_име, int отвори_Параметри);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int бајт_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Име, int[] податоци);
    public static native int запиши_знак_VALUE(int 문자);
    public static native int запиши_датотека(int[] Име, int[] податоци, int должина_VALUE);
    public static native int Запиши(String Содржина_VALUE);
    public static native int 인수개수();
    public static native String Аргументи(int INDEX);
    public static native int 실행권한();
    public static native int отвори_Мрежа(int локален_порта);
    public static native int испрати_податоци(int рачка_VALUE, int адреса, int одредиште_порта, int[] податоци, int должина_VALUE);
    public static native int 자료받기(int рачка_VALUE, int[] податоци, int 제한밀리초);
    public static native int затвори_Мрежа(int рачка_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int рачка_VALUE);
    public static native int 보낸창구(int рачка_VALUE);
}
