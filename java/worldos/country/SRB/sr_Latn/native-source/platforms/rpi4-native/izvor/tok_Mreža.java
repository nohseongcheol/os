// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jezgro_VALUE 안의 연결형 bajt_VALUE tok_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket sloj_VALUE. */
public final class tok_Mreža {
    static int[] Status_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], ravnopravni_uređaj_port = new int[16], čekaj_VALUE = new int[16], informatičko_odeljenje_ograničen = new int[16];
    static int[] čeona_kamera_VALUE = new int[16], 수 = new int[16], podaci = new int[16 * 1024];
    static int Dalje_stavka = 50000;
    static int verifikovati(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Status_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int broj_porta) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Status_VALUE[Loop_INDEX] != 0 && informatičko_odeljenje_ograničen[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == broj_porta) return true; return false; }
    public static int Create_stavka() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Status_VALUE[Loop_INDEX] == 0) { Status_VALUE[Loop_INDEX] = 1; ravnopravni_uređaj_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = čeona_kamera_VALUE[Loop_INDEX] = 수[Loop_INDEX] = čekaj_VALUE[Loop_INDEX] = informatičko_odeljenje_ograničen[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int povezati_učesnik(int 열린파일번호, int 통신주소, int broj_porta) {
        int Loop_INDEX = verifikovati(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Status_VALUE[Loop_INDEX] != 1 || broj_porta < 0 || broj_porta > 65535) return -22;
        if (broj_porta == 0) { do { broj_porta = Dalje_stavka++; if (Dalje_stavka > 65535) Dalje_stavka = 50000; } while (사용중(broj_porta)); }
        if (사용중(broj_porta)) return -98; port_VALUE[Loop_INDEX] = broj_porta; informatičko_odeljenje_ograničen[Loop_INDEX] = 1; Status_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int slušati_učesnik(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = verifikovati(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Status_VALUE[Loop_INDEX] = 3; return 0; }
    public static int veze(int 열린파일번호, int 통신주소, int broj_porta) {
        int Loop_INDEX = verifikovati(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (broj_porta < 1 || broj_porta > 65535 || Status_VALUE[Loop_INDEX] > 2) return -22;
        int primiti_stranica = -1; for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 16; unutrašnje_pozicija++) if (Status_VALUE[unutrašnje_pozicija] == 3 && port_VALUE[unutrašnje_pozicija] == broj_porta) primiti_stranica = unutrašnje_pozicija;
        if (primiti_stranica < 0) return -111;
        int 대기여부 = 0; for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 16; unutrašnje_pozicija++) if (čekaj_VALUE[unutrašnje_pozicija] == primiti_stranica + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Status_VALUE[Loop_INDEX] == 1) { int 처리값 = povezati_učesnik(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Ostalo = Create_stavka(); if (Ostalo < 0) return Ostalo; Ostalo -= 40;
        Status_VALUE[Loop_INDEX] = Status_VALUE[Ostalo] = 4; 짝[Loop_INDEX] = Ostalo; 짝[Ostalo] = Loop_INDEX; port_VALUE[Ostalo] = broj_porta; ravnopravni_uređaj_port[Loop_INDEX] = broj_porta; ravnopravni_uređaj_port[Ostalo] = port_VALUE[Loop_INDEX]; čekaj_VALUE[Ostalo] = primiti_stranica + 1; return 0;
    }
    public static int prihvatiti_veza(int 열린파일번호) { int Loop_INDEX = verifikovati(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 3) return -22; for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 16; unutrašnje_pozicija++) if (Status_VALUE[unutrašnje_pozicija] != 0 && čekaj_VALUE[unutrašnje_pozicija] == Loop_INDEX + 1) { čekaj_VALUE[unutrašnje_pozicija] = 0; return unutrašnje_pozicija + 40; } return -11; }
    public static int 쓰기(int 열린파일번호, int stavka_COUNT_8f7753a1) {
        int Loop_INDEX = verifikovati(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 4) return -107;
        if (stavka_COUNT_8f7753a1 < 0 || stavka_COUNT_8f7753a1 > 512) return -22; if (stavka_COUNT_8f7753a1 == 0) return 0;
        int unutrašnje_pozicija = 짝[Loop_INDEX]; if (unutrašnje_pozicija < 0) return -32; int ukupan_COUNT = 1024 - 수[unutrašnje_pozicija]; if (ukupan_COUNT == 0) return -11; if (ukupan_COUNT > stavka_COUNT_8f7753a1) ukupan_COUNT = stavka_COUNT_8f7753a1;
        for (int Poređenje_pozicija = 0; Poređenje_pozicija < ukupan_COUNT; Poređenje_pozicija++) podaci[unutrašnje_pozicija * 1024 + (čeona_kamera_VALUE[unutrašnje_pozicija] + 수[unutrašnje_pozicija] + Poređenje_pozicija) % 1024] = kružni_tok_podataka_Mreža.Napred_VALUE[Poređenje_pozicija]; 수[unutrašnje_pozicija] += ukupan_COUNT; return ukupan_COUNT;
    }
    public static int 읽기(int 열린파일번호, int stavka_COUNT_8f7753a1) {
        int Loop_INDEX = verifikovati(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 4) return -107; if (stavka_COUNT_8f7753a1 < 0 || stavka_COUNT_8f7753a1 > 512) return -22;
        if (stavka_COUNT_8f7753a1 == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (stavka_COUNT_8f7753a1 > 수[Loop_INDEX]) stavka_COUNT_8f7753a1 = 수[Loop_INDEX];
        for (int Poređenje_pozicija = 0; Poređenje_pozicija < stavka_COUNT_8f7753a1; Poređenje_pozicija++) kružni_tok_podataka_Mreža.Napred_VALUE[Poređenje_pozicija] = podaci[Loop_INDEX * 1024 + (čeona_kamera_VALUE[Loop_INDEX] + Poređenje_pozicija) % 1024]; čeona_kamera_VALUE[Loop_INDEX] = (čeona_kamera_VALUE[Loop_INDEX] + stavka_COUNT_8f7753a1) % 1024; 수[Loop_INDEX] -= stavka_COUNT_8f7753a1; return stavka_COUNT_8f7753a1;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = verifikovati(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = verifikovati(열린파일번호); return Loop_INDEX < 0 ? -9 : ravnopravni_uređaj_port[Loop_INDEX]; }
    public static int Zatvori(int 열린파일번호) {
        int Loop_INDEX = verifikovati(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Status_VALUE[Loop_INDEX] == 3) for (int unutrašnje_pozicija = 0; unutrašnje_pozicija < 16; unutrašnje_pozicija++) if (čekaj_VALUE[unutrašnje_pozicija] == Loop_INDEX + 1) { if (짝[unutrašnje_pozicija] >= 0) 짝[짝[unutrašnje_pozicija]] = -1; Status_VALUE[unutrašnje_pozicija] = čekaj_VALUE[unutrašnje_pozicija] = informatičko_odeljenje_ograničen[unutrašnje_pozicija] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Status_VALUE[Loop_INDEX] = informatičko_odeljenje_ograničen[Loop_INDEX] = 수[Loop_INDEX] = čekaj_VALUE[Loop_INDEX] = 0; return 0;
    }
}
