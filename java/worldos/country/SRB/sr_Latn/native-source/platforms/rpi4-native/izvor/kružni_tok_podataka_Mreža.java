// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 sloj_VALUE: 단일 jezgro_VALUE 안의 IPv4/UDP 루프백 prenos_VALUE.
 * spoljni_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * završiti_razgovor_p 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class kružni_tok_podataka_Mreža {
    static int[] koristiti_VALUE = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] adresa = new int[8];
    static int[] čeona_kamera_VALUE = new int[8];
    static int[] stavka_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] 길이 = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] podaci = new int[32 * 512];
    static int[] Napred_VALUE = new int[512];
    static int Dalje_učesnik = 49152;
    static int verifikovati(int INDEX) { return INDEX >= 32 && INDEX < 40 && koristiti_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (koristiti_VALUE[칸] != 0 && port_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Dalje_učesnik++;
            if (Dalje_učesnik > 65535) Dalje_učesnik = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Create_stavka(int oblast_VALUE_0e9a97ab, int 종류, int ugovor_VALUE) {
        if (oblast_VALUE_0e9a97ab != 2) return -97;
        if (종류 != 2 || (ugovor_VALUE != 0 && ugovor_VALUE != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (koristiti_VALUE[칸] == 0) {
            koristiti_VALUE[칸] = 1; port_VALUE[칸] = 0; adresa[칸] = 0; čeona_kamera_VALUE[칸] = 0; stavka_COUNT[칸] = 0; RECEIVED_port[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int povezati_učesnik(int INDEX, int ID_mreže, int učesnik_broj_porta) {
        int 칸 = verifikovati(INDEX);
        if (칸 < 0) return -9;
        if (ID_mreže != 0 && ID_mreže != 0x7f000001) return -99;
        if (port_VALUE[칸] != 0 || učesnik_broj_porta < 0 || učesnik_broj_porta > 65535) return -22;
        if (učesnik_broj_porta == 0) učesnik_broj_porta = 임시창구();
        if (učesnik_broj_porta < 0) return učesnik_broj_porta;
        if (겹침(učesnik_broj_porta)) return -98;
        port_VALUE[칸] = učesnik_broj_porta; adresa[칸] = ID_mreže; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Napred_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Napred_VALUE[INDEX] : -22; }
    public static int poslati(int INDEX, int ID_mreže, int učesnik_broj_porta, int promeniti_veličinu) {
        int 칸 = verifikovati(INDEX);
        if (칸 < 0) return -9;
        if (ID_mreže != 0x7f000001) return -101;
        if (učesnik_broj_porta < 1 || učesnik_broj_porta > 65535) return -22;
        if (promeniti_veličinu < 0 || promeniti_veličinu > 512) return -90;
        if (port_VALUE[칸] == 0) {
            int KR = povezati_učesnik(INDEX, 0x7f000001, 0);
            if (KR < 0) return KR;
        }
        int odredište_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (koristiti_VALUE[후보] != 0 && port_VALUE[후보] == učesnik_broj_porta) odredište_VALUE = 후보;
        if (odredište_VALUE < 0) return -111;
        if (stavka_COUNT[odredište_VALUE] == 4) return -11;
        int indeks_pozicije = odredište_VALUE * 4 + (čeona_kamera_VALUE[odredište_VALUE] + stavka_COUNT[odredište_VALUE]) % 4;
        for (int bajt_VALUE = 0; bajt_VALUE < promeniti_veličinu; bajt_VALUE++) podaci[indeks_pozicije * 512 + bajt_VALUE] = Napred_VALUE[bajt_VALUE];
        길이[indeks_pozicije] = promeniti_veličinu; 보낸창구[indeks_pozicije] = port_VALUE[칸]; stavka_COUNT[odredište_VALUE]++;
        return promeniti_veličinu;
    }
    public static int primiti(int INDEX, int kapacitet_VALUE) {
        int 칸 = verifikovati(INDEX);
        if (칸 < 0) return -9;
        if (kapacitet_VALUE < 0 || kapacitet_VALUE > 512) return -22;
        if (stavka_COUNT[칸] == 0) return -11;
        int indeks_pozicije = 칸 * 4 + čeona_kamera_VALUE[칸];
        int promeniti_veličinu = 길이[indeks_pozicije] < kapacitet_VALUE ? 길이[indeks_pozicije] : kapacitet_VALUE;
        for (int bajt_VALUE = 0; bajt_VALUE < promeniti_veličinu; bajt_VALUE++) Napred_VALUE[bajt_VALUE] = podaci[indeks_pozicije * 512 + bajt_VALUE];
        RECEIVED_port[칸] = 보낸창구[indeks_pozicije]; čeona_kamera_VALUE[칸] = (čeona_kamera_VALUE[칸] + 1) % 4; stavka_COUNT[칸]--;
        return promeniti_veličinu;
    }
    public static int 창구읽기(int INDEX) { int 칸 = verifikovati(INDEX); return 칸 < 0 ? -9 : port_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = verifikovati(INDEX); return 칸 < 0 ? -9 : adresa[칸]; }
    public static int pošiljalac_učesnik(int INDEX) { int 칸 = verifikovati(INDEX); return 칸 < 0 ? -9 : RECEIVED_port[칸]; }
    public static int Zatvori(int INDEX) {
        int 칸 = verifikovati(INDEX); if (칸 < 0) return -9;
        koristiti_VALUE[칸] = 0; stavka_COUNT[칸] = 0; port_VALUE[칸] = 0; return 0;
    }
}
