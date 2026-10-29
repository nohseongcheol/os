// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 kone rajattu_alue_ARVO. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Taulu {
    public static native int lukea_näyttö_kuvapiste(int 가로, int toimiala_toimi);
    public static native void kirjoitus_näyttö_kuvapiste(int 가로, int toimiala_toimi, int 색);
    public static native int etähallinta(int 종류, int Toiminto);
    public static native void lopettaa_puhelu_etä_komento(int Tila_ARVO);
    public static native void etä_odottaa(int Tila_ARVO);
    public static native void 직렬쓰기(int ARVO);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int suoritin_oikeus_taso();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int toimiala_toimi, int 색);
    public static native void TUOTTO_suoritin();
    public static native int Luo_tehtävä(int INDEKSI);
    public static native int tehtävä_Tila(int INDEKSI);
    public static native void Pysäytä(int Tila_ARVO);
    public static native int 씨플러스시험();
    public static native int suorittaa_käyttäjä_ohjelma(int INDEKSI);
    public static native int sekki_käyttäjä_ohjelma();
    public static native int 인수준비(int kohde_LASKE);
    public static native int Suorita_käyttäjä_Tiedosto();
    public static native int 리눅스파일실행();
    public static native int argumentti_tavu(int INDEKSI, int paikka, int ARVO);
    public static native int komentotulkki(int Toiminto);
    public static native int ohjain_käyttäjä_ohjelma(int Toiminto);
    public static native void 입출력전환(int Toiminto);
    public static native int tiedostonsiirto_palvelu(int Toiminto);
    public static native int verkko_tila(int merkintä_ARVO_962f286b, int INDEKSI);
    public static native int verkko_Asetukset(int Toiminto, int OSOITE, int peite_ARVO, int yhdyskäytävä_ARVO);
    public static native int lähettää_vastaus(int OSOITE, int tilata_ARVO);
    public static native int lukea_vastaus(int merkintä_ARVO_962f286b);
    public static native int kysely_Järjestelmä(int merkintä_ARVO_962f286b, int INDEKSI);
    public static native void 전원끄기();
}
