// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros uživatelský_prostor ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class uživatelský_prostor {
    public static native int otevřít_Soubor_popisovač(int[] Soubor_položka_název, int otevřít_Nastavení);
    public static native int 파일한바이트읽기(int Soubor_popisovač);
    public static native int 파일한바이트쓰기(int Soubor_popisovač, int bajt_HODNOTA);
    public static native int Zavřít_Soubor_popisovač(int Soubor_popisovač);
    public static native int zápis_Files(int Soubor_popisovač);
    public static native int 파일읽기(int[] Název, int[] data);
    public static native int zápis_znak_HODNOTA(int 문자);
    public static native int zápis_Soubor(int[] Název, int[] data, int délka_HODNOTA);
    public static native int Zápis(String Obsah_HODNOTA);
    public static native int 인수개수();
    public static native String argumenty(int INDEX);
    public static native int spuštění_oprávnění();
    public static native int otevřít_síť(int místní_port);
    public static native int poslat_data(int úchyt_HODNOTA, int Adresa, int cíl_port, int[] data, int délka_HODNOTA);
    public static native int dostat_data(int úchyt_HODNOTA, int[] data, int 제한밀리초);
    public static native int Zavřít_síť(int úchyt_HODNOTA);
    public static native int 내주소();
    public static native int 보낸주소(int úchyt_HODNOTA);
    public static native int 보낸창구(int úchyt_HODNOTA);
}
