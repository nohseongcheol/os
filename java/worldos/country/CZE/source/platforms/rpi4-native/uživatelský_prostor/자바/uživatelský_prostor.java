// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 nástroje 전용 SVC Připojit. 기존 x86 nástroje 원문을 함께 빌드한다. */
public final class uživatelský_prostor {
    public static native int otevřít_Soubor_popisovač(int[] Název, int Nastavení);
    public static native int 파일한바이트읽기(int popisovač_položka);
    public static native int 파일한바이트쓰기(int popisovač_položka, int HODNOTA);
    public static native int Zavřít_Soubor_popisovač(int popisovač_položka);
    public static native int 파일읽기(int[] Název, int[] data);
    public static native int zápis_Soubor(int[] Název, int[] data, int délka_HODNOTA);
    public static native int Zápis(String text);
    public static native int zápis_znak_HODNOTA(int HODNOTA);
    public static native int 인수개수();
    public static native String argumenty(int INDEX);
    public static native int nástroj_číslo();
    public static native int 화면연결(int Akce, int INDEX, int 가, int SEKUNDA_operand, int 다, int 라);
    public static native int 화면글(int INDEX, int[] text, int délka_HODNOTA);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int tok_řízení(int Akce, int popisovač_položka, int HODNOTA);
    public static native int spojit_tok(int popisovač_položka, int Adresa, int port_HODNOTA);
    public static native int otevřít_síť(int port_HODNOTA);
    public static native int poslat_síť(int popisovač_položka, int Adresa, int port_HODNOTA, int[] data, int délka_HODNOTA);
    public static native int dostat_síť(int popisovač_položka, int[] data, int délka_HODNOTA);
    public static native int síť_port(int popisovač_položka);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int obdélník(int 가로, int Svislá_pozice, int 폭, int výška_HODNOTA, int 색);
}
