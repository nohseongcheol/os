// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 sloj_VALUE: 단일 jezgra_sustava_VALUE 안의 IPv4/UDP 루프백 Prijenos_VALUE.
 * vanjski_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * završiti_razgovor_p 8개, 끝점당 datogram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class povratna_obrada_mreža {
    static int[] uporaba_VALUE = new int[8];
    static int[] prebaciti_VALUE = new int[8];
    static int[] adresa = new int[8];
    static int[] prednja_VALUE = new int[8];
    static int[] artikl_COUNT = new int[8];
    static int[] RECEIVED_prebaciti = new int[8];
    static int[] 길이 = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] podaci = new int[32 * 512];
    static int[] Naprijed_VALUE = new int[512];
    static int Dalje_sudionik = 49152;
    static int provjeriti(int INDEX) { return INDEX >= 32 && INDEX < 40 && uporaba_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (uporaba_VALUE[칸] != 0 && prebaciti_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Dalje_sudionik++;
            if (Dalje_sudionik > 65535) Dalje_sudionik = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Create_unos(int regije_VALUE, int 종류, int slučaj_VALUE) {
        if (regije_VALUE != 2) return -97;
        if (종류 != 2 || (slučaj_VALUE != 0 && slučaj_VALUE != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (uporaba_VALUE[칸] == 0) {
            uporaba_VALUE[칸] = 1; prebaciti_VALUE[칸] = 0; adresa[칸] = 0; prednja_VALUE[칸] = 0; artikl_COUNT[칸] = 0; RECEIVED_prebaciti[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int BIND_sudionik(int INDEX, int mrežni_ID, int sudionik_broj_priključka) {
        int 칸 = provjeriti(INDEX);
        if (칸 < 0) return -9;
        if (mrežni_ID != 0 && mrežni_ID != 0x7f000001) return -99;
        if (prebaciti_VALUE[칸] != 0 || sudionik_broj_priključka < 0 || sudionik_broj_priključka > 65535) return -22;
        if (sudionik_broj_priključka == 0) sudionik_broj_priključka = 임시창구();
        if (sudionik_broj_priključka < 0) return sudionik_broj_priključka;
        if (겹침(sudionik_broj_priključka)) return -98;
        prebaciti_VALUE[칸] = sudionik_broj_priključka; adresa[칸] = mrežni_ID; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Naprijed_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Naprijed_VALUE[INDEX] : -22; }
    public static int slati(int INDEX, int mrežni_ID, int sudionik_broj_priključka, int Veličina) {
        int 칸 = provjeriti(INDEX);
        if (칸 < 0) return -9;
        if (mrežni_ID != 0x7f000001) return -101;
        if (sudionik_broj_priključka < 1 || sudionik_broj_priključka > 65535) return -22;
        if (Veličina < 0 || Veličina > 512) return -90;
        if (prebaciti_VALUE[칸] == 0) {
            int REZULTAT = BIND_sudionik(INDEX, 0x7f000001, 0);
            if (REZULTAT < 0) return REZULTAT;
        }
        int odredište_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (uporaba_VALUE[후보] != 0 && prebaciti_VALUE[후보] == sudionik_broj_priključka) odredište_VALUE = 후보;
        if (odredište_VALUE < 0) return -111;
        if (artikl_COUNT[odredište_VALUE] == 4) return -11;
        int indeks_položaja = odredište_VALUE * 4 + (prednja_VALUE[odredište_VALUE] + artikl_COUNT[odredište_VALUE]) % 4;
        for (int bajt_VALUE = 0; bajt_VALUE < Veličina; bajt_VALUE++) podaci[indeks_položaja * 512 + bajt_VALUE] = Naprijed_VALUE[bajt_VALUE];
        길이[indeks_položaja] = Veličina; 보낸창구[indeks_položaja] = prebaciti_VALUE[칸]; artikl_COUNT[odredište_VALUE]++;
        return Veličina;
    }
    public static int primiti(int INDEX, int kapacitet_VALUE) {
        int 칸 = provjeriti(INDEX);
        if (칸 < 0) return -9;
        if (kapacitet_VALUE < 0 || kapacitet_VALUE > 512) return -22;
        if (artikl_COUNT[칸] == 0) return -11;
        int indeks_položaja = 칸 * 4 + prednja_VALUE[칸];
        int Veličina = 길이[indeks_položaja] < kapacitet_VALUE ? 길이[indeks_položaja] : kapacitet_VALUE;
        for (int bajt_VALUE = 0; bajt_VALUE < Veličina; bajt_VALUE++) Naprijed_VALUE[bajt_VALUE] = podaci[indeks_položaja * 512 + bajt_VALUE];
        RECEIVED_prebaciti[칸] = 보낸창구[indeks_položaja]; prednja_VALUE[칸] = (prednja_VALUE[칸] + 1) % 4; artikl_COUNT[칸]--;
        return Veličina;
    }
    public static int 창구읽기(int INDEX) { int 칸 = provjeriti(INDEX); return 칸 < 0 ? -9 : prebaciti_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = provjeriti(INDEX); return 칸 < 0 ? -9 : adresa[칸]; }
    public static int pošiljatelj_sudionik(int INDEX) { int 칸 = provjeriti(INDEX); return 칸 < 0 ? -9 : RECEIVED_prebaciti[칸]; }
    public static int Zatvori(int INDEX) {
        int 칸 = provjeriti(INDEX); if (칸 < 0) return -9;
        uporaba_VALUE[칸] = 0; artikl_COUNT[칸] = 0; prebaciti_VALUE[칸] = 0; return 0;
    }
}
