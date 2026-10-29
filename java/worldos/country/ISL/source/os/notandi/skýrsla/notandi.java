// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros notandi ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class notandi {
    public static native int 파일서술자열기(int[] skrá_færsla_heiti, int opið_Stillingar);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bæti_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Heiti, int[] gögn);
    public static native int skrifa_stafur_VALUE(int 문자);
    public static native int skrifa_skrá(int[] Heiti, int[] gögn, int lengd_VALUE);
    public static native int Skrift(String Efni_VALUE);
    public static native int 인수개수();
    public static native String Viðföng(int INDEX);
    public static native int 실행권한();
    public static native int opið_Net(int staðbundið_gátt);
    public static native int senda_gögn(int hald_VALUE, int slóð, int endastaður_gátt, int[] gögn, int lengd_VALUE);
    public static native int 자료받기(int hald_VALUE, int[] gögn, int 제한밀리초);
    public static native int loka_Net(int hald_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int hald_VALUE);
    public static native int 보낸창구(int hald_VALUE);
}
