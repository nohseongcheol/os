// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 työkalut 전용 SVC Yhdistä. 기존 x86 työkalut 원문을 함께 빌드한다. */
public final class käyttäjätila {
    public static native int 파일서술자열기(int[] Nimi, int Asetukset);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ARVO);
    public static native int 파일서술자닫기(int 서술자);
    public static native int lukea_Tiedosto(int[] Nimi, int[] data);
    public static native int kirjoitus_Tiedosto(int[] Nimi, int[] data, int kesto_ARVO);
    public static native int Kirjoitus(String teksti);
    public static native int kirjoitus_merkki_ARVO(int ARVO);
    public static native int 인수개수();
    public static native String argumentit(int INDEKSI);
    public static native int työkalu_numero();
    public static native int 화면연결(int Toiminto, int INDEKSI, int 가, int SEKUNNIT_operandi, int 다, int 라);
    public static native int 화면글(int INDEKSI, int[] teksti, int kesto_ARVO);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int virta_ohjain(int Toiminto, int 서술자, int ARVO);
    public static native int YHDISTÄ_virta(int 서술자, int OSOITE, int portti_ARVO);
    public static native int avata_verkko(int portti_ARVO);
    public static native int lähettää_verkko(int 서술자, int OSOITE, int portti_ARVO, int[] data, int kesto_ARVO);
    public static native int saada_verkko(int 서술자, int[] data, int kesto_ARVO);
    public static native int verkko_portti(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int suorakulmio(int 가로, int toimiala_toimi, int 폭, int 높이, int 색);
}
