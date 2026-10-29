// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Nástroje 전용 SVC Pripojiť. 기존 x86 Nástroje 원문을 함께 빌드한다. */
public final class používateľ {
    public static native int 파일서술자열기(int[] Názov, int Nastavenia);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Názov, int[] údaje);
    public static native int zapísať_Súbor(int[] Názov, int[] údaje, int dĺžka_VALUE);
    public static native int Zápis(String Spracovanie_textu);
    public static native int zapísať_znak_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Argumenty(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Akcia, int INDEX, int 가, int SECOND_operand, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Spracovanie_textu, int dĺžka_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_riadenie(int Akcia, int 서술자, int VALUE);
    public static native int spojiť_Stream(int 서술자, int adresa, int port_VALUE);
    public static native int otvoriť_sieť(int port_VALUE);
    public static native int odoslať_sieť(int 서술자, int adresa, int port_VALUE, int[] údaje, int dĺžka_VALUE);
    public static native int dostať_sieť(int 서술자, int[] údaje, int dĺžka_VALUE);
    public static native int sieť_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int obdĺžnik(int 가로, int vertikála_pozícia, int 폭, int výška_VALUE, int 색);
}
