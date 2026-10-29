// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 kerros_ARVO_e65604ef: 단일 ydin_ARVO 안의 IPv4/UDP 루프백 Siirrä_ARVO.
 * ulkoinen_ARVO IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * lopettaa_puhelu_piste 8개, 끝점당 datagrammi 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class silmukka_verkko {
    static int[] käyttö_ARVO = new int[8];
    static int[] portti_ARVO = new int[8];
    static int[] OSOITE = new int[8];
    static int[] etukamera_ARVO = new int[8];
    static int[] kohde_LASKE = new int[8];
    static int[] SAATU_HINTA_portti = new int[8];
    static int[] kesto_ARVO = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] siirrä_ARVO_24592b8a = new int[512];
    static int Seuraava_päätepiste = 49152;
    static int tarkistaa(int INDEKSI) { return INDEKSI >= 32 && INDEKSI < 40 && käyttö_ARVO[INDEKSI - 32] != 0 ? INDEKSI - 32 : -1; }
    static boolean 겹침(int INDEKSI) {
        for (int paikka_merkintä = 0; paikka_merkintä < 8; paikka_merkintä++) if (käyttö_ARVO[paikka_merkintä] != 0 && portti_ARVO[paikka_merkintä] == INDEKSI) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Seuraava_päätepiste++;
            if (Seuraava_päätepiste > 65535) Seuraava_päätepiste = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Luo_merkintä(int alue_ARVO_0e9a97ab, int 종류, int sopimuksen_arvo) {
        if (alue_ARVO_0e9a97ab != 2) return -97;
        if (종류 != 2 || (sopimuksen_arvo != 0 && sopimuksen_arvo != 17)) return -93;
        for (int paikka_merkintä = 0; paikka_merkintä < 8; paikka_merkintä++) if (käyttö_ARVO[paikka_merkintä] == 0) {
            käyttö_ARVO[paikka_merkintä] = 1; portti_ARVO[paikka_merkintä] = 0; OSOITE[paikka_merkintä] = 0; etukamera_ARVO[paikka_merkintä] = 0; kohde_LASKE[paikka_merkintä] = 0; SAATU_HINTA_portti[paikka_merkintä] = 0;
            return paikka_merkintä + 32;
        }
        return -24;
    }
    public static int BIND_päätepiste(int INDEKSI, int verkkotunnus, int päätepiste_portin_numero) {
        int paikka_merkintä = tarkistaa(INDEKSI);
        if (paikka_merkintä < 0) return -9;
        if (verkkotunnus != 0 && verkkotunnus != 0x7f000001) return -99;
        if (portti_ARVO[paikka_merkintä] != 0 || päätepiste_portin_numero < 0 || päätepiste_portin_numero > 65535) return -22;
        if (päätepiste_portin_numero == 0) päätepiste_portin_numero = 임시창구();
        if (päätepiste_portin_numero < 0) return päätepiste_portin_numero;
        if (겹침(päätepiste_portin_numero)) return -98;
        portti_ARVO[paikka_merkintä] = päätepiste_portin_numero; OSOITE[paikka_merkintä] = verkkotunnus; return 0;
    }
    public static int 자료넣기(int INDEKSI, int ARVO) {
        if (INDEKSI < 0 || INDEKSI >= 512) return -22;
        siirrä_ARVO_24592b8a[INDEKSI] = ARVO & 255; return 0;
    }
    public static int lukea_data(int INDEKSI) { return INDEKSI >= 0 && INDEKSI < 512 ? siirrä_ARVO_24592b8a[INDEKSI] : -22; }
    public static int lähettää(int INDEKSI, int verkkotunnus, int päätepiste_portin_numero, int Koko) {
        int paikka_merkintä = tarkistaa(INDEKSI);
        if (paikka_merkintä < 0) return -9;
        if (verkkotunnus != 0x7f000001) return -101;
        if (päätepiste_portin_numero < 1 || päätepiste_portin_numero > 65535) return -22;
        if (Koko < 0 || Koko > 512) return -90;
        if (portti_ARVO[paikka_merkintä] == 0) {
            int TULOS = BIND_päätepiste(INDEKSI, 0x7f000001, 0);
            if (TULOS < 0) return TULOS;
        }
        int kohde_ARVO = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (käyttö_ARVO[후보] != 0 && portti_ARVO[후보] == päätepiste_portin_numero) kohde_ARVO = 후보;
        if (kohde_ARVO < 0) return -111;
        if (kohde_LASKE[kohde_ARVO] == 4) return -11;
        int sijainti = kohde_ARVO * 4 + (etukamera_ARVO[kohde_ARVO] + kohde_LASKE[kohde_ARVO]) % 4;
        for (int tavu_ARVO = 0; tavu_ARVO < Koko; tavu_ARVO++) data[sijainti * 512 + tavu_ARVO] = siirrä_ARVO_24592b8a[tavu_ARVO];
        kesto_ARVO[sijainti] = Koko; 보낸창구[sijainti] = portti_ARVO[paikka_merkintä]; kohde_LASKE[kohde_ARVO]++;
        return Koko;
    }
    public static int saada(int INDEKSI, int kapasiteetti_ARVO) {
        int paikka_merkintä = tarkistaa(INDEKSI);
        if (paikka_merkintä < 0) return -9;
        if (kapasiteetti_ARVO < 0 || kapasiteetti_ARVO > 512) return -22;
        if (kohde_LASKE[paikka_merkintä] == 0) return -11;
        int sijainti = paikka_merkintä * 4 + etukamera_ARVO[paikka_merkintä];
        int Koko = kesto_ARVO[sijainti] < kapasiteetti_ARVO ? kesto_ARVO[sijainti] : kapasiteetti_ARVO;
        for (int tavu_ARVO = 0; tavu_ARVO < Koko; tavu_ARVO++) siirrä_ARVO_24592b8a[tavu_ARVO] = data[sijainti * 512 + tavu_ARVO];
        SAATU_HINTA_portti[paikka_merkintä] = 보낸창구[sijainti]; etukamera_ARVO[paikka_merkintä] = (etukamera_ARVO[paikka_merkintä] + 1) % 4; kohde_LASKE[paikka_merkintä]--;
        return Koko;
    }
    public static int lukea_päätepiste_portti(int INDEKSI) { int paikka_merkintä = tarkistaa(INDEKSI); return paikka_merkintä < 0 ? -9 : portti_ARVO[paikka_merkintä]; }
    public static int lukea_OSOITE(int INDEKSI) { int paikka_merkintä = tarkistaa(INDEKSI); return paikka_merkintä < 0 ? -9 : OSOITE[paikka_merkintä]; }
    public static int lähettäjä_päätepiste(int INDEKSI) { int paikka_merkintä = tarkistaa(INDEKSI); return paikka_merkintä < 0 ? -9 : SAATU_HINTA_portti[paikka_merkintä]; }
    public static int Sulje(int INDEKSI) {
        int paikka_merkintä = tarkistaa(INDEKSI); if (paikka_merkintä < 0) return -9;
        käyttö_ARVO[paikka_merkintä] = 0; kohde_LASKE[paikka_merkintä] = 0; portti_ARVO[paikka_merkintä] = 0; return 0;
    }
}
