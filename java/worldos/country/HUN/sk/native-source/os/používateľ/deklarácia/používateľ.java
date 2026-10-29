// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros používateľ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class používateľ {
    public static native int 파일서술자열기(int[] Súbor_položka_názov, int otvoriť_Nastavenia);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int Byte_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int potvrdenie_ukladací_priestor_súborov(int 파일서술자);
    public static native int 파일읽기(int[] Názov, int[] údaje);
    public static native int zapísať_znak_VALUE(int 문자);
    public static native int zapísať_Súbor(int[] Názov, int[] údaje, int dĺžka_VALUE);
    public static native int Zápis(String obsah_VALUE);
    public static native int 인수개수();
    public static native String Argumenty(int INDEX);
    public static native int 실행권한();
    public static native int otvoriť_sieť(int miestny_port);
    public static native int odoslať_údaje(int rukoväť_VALUE, int adresa, int cieľ_port, int[] údaje, int dĺžka_VALUE);
    public static native int dostať_údaje(int rukoväť_VALUE, int[] údaje, int 제한밀리초);
    public static native int Zavrieť_sieť(int rukoväť_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int rukoväť_VALUE);
    public static native int 보낸창구(int rukoväť_VALUE);
}
