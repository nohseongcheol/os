// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 sloj_VALUE: 단일 jezgro_VALUE 안의 IPv4/UDP 루프백 prijenos_VALUE.
 * iz_eksternog_izvora_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * završiti_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] adresa = new int[8];
    static int[] 앞 = new int[8];
    static int[] stavka_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] dužina_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] podaci = new int[32 * 512];
    static int[] Naprijed_VALUE = new int[512];
    static int Dalje_završna_tačka = 49152;
    static int potvrditi(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 8; prostor_za_unos_unos++) if (사용[prostor_za_unos_unos] != 0 && port_VALUE[prostor_za_unos_unos] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Dalje_završna_tačka++;
            if (Dalje_završna_tačka > 65535) Dalje_završna_tačka = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Create_unos(int 영역, int 종류, int slučaj_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (slučaj_VALUE != 0 && slučaj_VALUE != 17)) return -93;
        for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 8; prostor_za_unos_unos++) if (사용[prostor_za_unos_unos] == 0) {
            사용[prostor_za_unos_unos] = 1; port_VALUE[prostor_za_unos_unos] = 0; adresa[prostor_za_unos_unos] = 0; 앞[prostor_za_unos_unos] = 0; stavka_COUNT[prostor_za_unos_unos] = 0; RECEIVED_port[prostor_za_unos_unos] = 0;
            return prostor_za_unos_unos + 32;
        }
        return -24;
    }
    public static int BIND_završna_tačka(int INDEX, int Mreža_adresa, int završna_tačka_broj_priključka) {
        int prostor_za_unos_unos = potvrditi(INDEX);
        if (prostor_za_unos_unos < 0) return -9;
        if (Mreža_adresa != 0 && Mreža_adresa != 0x7f000001) return -99;
        if (port_VALUE[prostor_za_unos_unos] != 0 || završna_tačka_broj_priključka < 0 || završna_tačka_broj_priključka > 65535) return -22;
        if (završna_tačka_broj_priključka == 0) završna_tačka_broj_priključka = 임시창구();
        if (završna_tačka_broj_priključka < 0) return završna_tačka_broj_priključka;
        if (겹침(završna_tačka_broj_priključka)) return -98;
        port_VALUE[prostor_za_unos_unos] = završna_tačka_broj_priključka; adresa[prostor_za_unos_unos] = Mreža_adresa; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Naprijed_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Naprijed_VALUE[INDEX] : -22; }
    public static int poslati(int INDEX, int Mreža_adresa, int završna_tačka_broj_priključka, int Veličina) {
        int prostor_za_unos_unos = potvrditi(INDEX);
        if (prostor_za_unos_unos < 0) return -9;
        if (Mreža_adresa != 0x7f000001) return -101;
        if (završna_tačka_broj_priključka < 1 || završna_tačka_broj_priključka > 65535) return -22;
        if (Veličina < 0 || Veličina > 512) return -90;
        if (port_VALUE[prostor_za_unos_unos] == 0) {
            int mjera = BIND_završna_tačka(INDEX, 0x7f000001, 0);
            if (mjera < 0) return mjera;
        }
        int odredište_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == završna_tačka_broj_priključka) odredište_VALUE = 후보;
        if (odredište_VALUE < 0) return -111;
        if (stavka_COUNT[odredište_VALUE] == 4) return -11;
        int položaj_INDEX = odredište_VALUE * 4 + (앞[odredište_VALUE] + stavka_COUNT[odredište_VALUE]) % 4;
        for (int bajt_VALUE = 0; bajt_VALUE < Veličina; bajt_VALUE++) podaci[položaj_INDEX * 512 + bajt_VALUE] = Naprijed_VALUE[bajt_VALUE];
        dužina_VALUE[položaj_INDEX] = Veličina; 보낸창구[položaj_INDEX] = port_VALUE[prostor_za_unos_unos]; stavka_COUNT[odredište_VALUE]++;
        return Veličina;
    }
    public static int 받기(int INDEX, int 용량) {
        int prostor_za_unos_unos = potvrditi(INDEX);
        if (prostor_za_unos_unos < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (stavka_COUNT[prostor_za_unos_unos] == 0) return -11;
        int položaj_INDEX = prostor_za_unos_unos * 4 + 앞[prostor_za_unos_unos];
        int Veličina = dužina_VALUE[položaj_INDEX] < 용량 ? dužina_VALUE[položaj_INDEX] : 용량;
        for (int bajt_VALUE = 0; bajt_VALUE < Veličina; bajt_VALUE++) Naprijed_VALUE[bajt_VALUE] = podaci[položaj_INDEX * 512 + bajt_VALUE];
        RECEIVED_port[prostor_za_unos_unos] = 보낸창구[položaj_INDEX]; 앞[prostor_za_unos_unos] = (앞[prostor_za_unos_unos] + 1) % 4; stavka_COUNT[prostor_za_unos_unos]--;
        return Veličina;
    }
    public static int 창구읽기(int INDEX) { int prostor_za_unos_unos = potvrditi(INDEX); return prostor_za_unos_unos < 0 ? -9 : port_VALUE[prostor_za_unos_unos]; }
    public static int 주소읽기(int INDEX) { int prostor_za_unos_unos = potvrditi(INDEX); return prostor_za_unos_unos < 0 ? -9 : adresa[prostor_za_unos_unos]; }
    public static int pošiljalac_završna_tačka(int INDEX) { int prostor_za_unos_unos = potvrditi(INDEX); return prostor_za_unos_unos < 0 ? -9 : RECEIVED_port[prostor_za_unos_unos]; }
    public static int Zatvori(int INDEX) {
        int prostor_za_unos_unos = potvrditi(INDEX); if (prostor_za_unos_unos < 0) return -9;
        사용[prostor_za_unos_unos] = 0; stavka_COUNT[prostor_za_unos_unos] = 0; port_VALUE[prostor_za_unos_unos] = 0; return 0;
    }
}
