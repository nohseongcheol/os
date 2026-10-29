// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros käyttäjätila ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class käyttäjätila {
    public static native int 파일서술자열기(int[] Tiedosto_merkintä_nimi, int avata_Asetukset);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int tavu_ARVO);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int vahvistaa_muutokset_Files(int 파일서술자);
    public static native int lukea_Tiedosto(int[] Nimi, int[] data);
    public static native int kirjoitus_merkki_ARVO(int 문자);
    public static native int kirjoitus_Tiedosto(int[] Nimi, int[] data, int kesto_ARVO);
    public static native int Kirjoitus(String Sisältö_ARVO);
    public static native int 인수개수();
    public static native String argumentit(int INDEKSI);
    public static native int suoritus_lupa();
    public static native int avata_verkko(int paikallinen_portti);
    public static native int lähettää_data_5b5410b2(int kahva_ARVO, int OSOITE, int kohde_portti, int[] data, int kesto_ARVO);
    public static native int saada_data(int kahva_ARVO, int[] data, int 제한밀리초);
    public static native int Sulje_verkko(int kahva_ARVO);
    public static native int 내주소();
    public static native int 보낸주소(int kahva_ARVO);
    public static native int 보낸창구(int kahva_ARVO);
}
