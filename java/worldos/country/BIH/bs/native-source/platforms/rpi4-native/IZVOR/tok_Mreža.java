// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jezgro_VALUE 안의 연결형 bajt_VALUE tok_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket sloj_VALUE. */
public final class tok_Mreža {
    static int[] stanje_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], peer_port = new int[16], čekaj_VALUE = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], podaci = new int[16 * 1024];
    static int Dalje_stavka = 50000;
    static int potvrditi(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && stanje_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int broj_priključka) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (stanje_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == broj_priključka) return true; return false; }
    public static int Create_unos() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (stanje_VALUE[Loop_INDEX] == 0) { stanje_VALUE[Loop_INDEX] = 1; peer_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = 앞[Loop_INDEX] = 수[Loop_INDEX] = čekaj_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_završna_tačka(int 열린파일번호, int 통신주소, int broj_priključka) {
        int Loop_INDEX = potvrditi(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (stanje_VALUE[Loop_INDEX] != 1 || broj_priključka < 0 || broj_priključka > 65535) return -22;
        if (broj_priključka == 0) { do { broj_priključka = Dalje_stavka++; if (Dalje_stavka > 65535) Dalje_stavka = 50000; } while (사용중(broj_priključka)); }
        if (사용중(broj_priključka)) return -98; port_VALUE[Loop_INDEX] = broj_priključka; 묶임[Loop_INDEX] = 1; stanje_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int slušati_završna_tačka(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = potvrditi(열린파일번호); if (Loop_INDEX < 0) return -9; if (stanje_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; stanje_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Spoji_se(int 열린파일번호, int 통신주소, int broj_priključka) {
        int Loop_INDEX = potvrditi(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (broj_priključka < 1 || broj_priključka > 65535 || stanje_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 16; unutrašnje_spajanje_položaj++) if (stanje_VALUE[unutrašnje_spajanje_položaj] == 3 && port_VALUE[unutrašnje_spajanje_položaj] == broj_priključka) 수신쪽 = unutrašnje_spajanje_položaj;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 16; unutrašnje_spajanje_položaj++) if (čekaj_VALUE[unutrašnje_spajanje_položaj] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (stanje_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_završna_tačka(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Create_unos(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        stanje_VALUE[Loop_INDEX] = stanje_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALUE[다른번호] = broj_priključka; peer_port[Loop_INDEX] = broj_priključka; peer_port[다른번호] = port_VALUE[Loop_INDEX]; čekaj_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int prihvatiti_veza(int 열린파일번호) { int Loop_INDEX = potvrditi(열린파일번호); if (Loop_INDEX < 0) return -9; if (stanje_VALUE[Loop_INDEX] != 3) return -22; for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 16; unutrašnje_spajanje_položaj++) if (stanje_VALUE[unutrašnje_spajanje_položaj] != 0 && čekaj_VALUE[unutrašnje_spajanje_položaj] == Loop_INDEX + 1) { čekaj_VALUE[unutrašnje_spajanje_položaj] = 0; return unutrašnje_spajanje_položaj + 40; } return -11; }
    public static int Piši(int 열린파일번호, int unos_COUNT) {
        int Loop_INDEX = potvrditi(열린파일번호); if (Loop_INDEX < 0) return -9; if (stanje_VALUE[Loop_INDEX] != 4) return -107;
        if (unos_COUNT < 0 || unos_COUNT > 512) return -22; if (unos_COUNT == 0) return 0;
        int unutrašnje_spajanje_položaj = 짝[Loop_INDEX]; if (unutrašnje_spajanje_položaj < 0) return -32; int 총수 = 1024 - 수[unutrašnje_spajanje_položaj]; if (총수 == 0) return -11; if (총수 > unos_COUNT) 총수 = unos_COUNT;
        for (int Poređenje_položaj = 0; Poređenje_položaj < 총수; Poređenje_položaj++) podaci[unutrašnje_spajanje_položaj * 1024 + (앞[unutrašnje_spajanje_položaj] + 수[unutrašnje_spajanje_položaj] + Poređenje_položaj) % 1024] = 되돌림망.Naprijed_VALUE[Poređenje_položaj]; 수[unutrašnje_spajanje_položaj] += 총수; return 총수;
    }
    public static int Čitaj(int 열린파일번호, int unos_COUNT) {
        int Loop_INDEX = potvrditi(열린파일번호); if (Loop_INDEX < 0) return -9; if (stanje_VALUE[Loop_INDEX] != 4) return -107; if (unos_COUNT < 0 || unos_COUNT > 512) return -22;
        if (unos_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (unos_COUNT > 수[Loop_INDEX]) unos_COUNT = 수[Loop_INDEX];
        for (int Poređenje_položaj = 0; Poređenje_položaj < unos_COUNT; Poređenje_položaj++) 되돌림망.Naprijed_VALUE[Poređenje_položaj] = podaci[Loop_INDEX * 1024 + (앞[Loop_INDEX] + Poređenje_položaj) % 1024]; 앞[Loop_INDEX] = (앞[Loop_INDEX] + unos_COUNT) % 1024; 수[Loop_INDEX] -= unos_COUNT; return unos_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = potvrditi(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = potvrditi(열린파일번호); return Loop_INDEX < 0 ? -9 : peer_port[Loop_INDEX]; }
    public static int Zatvori(int 열린파일번호) {
        int Loop_INDEX = potvrditi(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (stanje_VALUE[Loop_INDEX] == 3) for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 16; unutrašnje_spajanje_položaj++) if (čekaj_VALUE[unutrašnje_spajanje_položaj] == Loop_INDEX + 1) { if (짝[unutrašnje_spajanje_položaj] >= 0) 짝[짝[unutrašnje_spajanje_položaj]] = -1; stanje_VALUE[unutrašnje_spajanje_položaj] = čekaj_VALUE[unutrašnje_spajanje_položaj] = 묶임[unutrašnje_spajanje_položaj] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; stanje_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = čekaj_VALUE[Loop_INDEX] = 0; return 0;
    }
}
