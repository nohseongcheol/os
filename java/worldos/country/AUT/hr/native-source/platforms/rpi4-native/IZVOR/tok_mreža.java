// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jezgra_sustava_VALUE 안의 연결형 bajt_VALUE tok_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket sloj_VALUE. */
public final class tok_mreža {
    static int[] Stanje_VALUE = new int[16], prebaciti_VALUE = new int[16], 짝 = new int[16], ravnopravan_član_prebaciti = new int[16], čekaj_VALUE = new int[16], odjel_informacijske_tehnologije_ograničen = new int[16];
    static int[] prednja_VALUE = new int[16], 수 = new int[16], podaci = new int[16 * 1024];
    static int Dalje_artikl = 50000;
    static int provjeriti(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Stanje_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int broj_priključka) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Stanje_VALUE[Loop_INDEX] != 0 && odjel_informacijske_tehnologije_ograničen[Loop_INDEX] != 0 && prebaciti_VALUE[Loop_INDEX] == broj_priključka) return true; return false; }
    public static int Create_unos() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Stanje_VALUE[Loop_INDEX] == 0) { Stanje_VALUE[Loop_INDEX] = 1; ravnopravan_član_prebaciti[Loop_INDEX] = prebaciti_VALUE[Loop_INDEX] = prednja_VALUE[Loop_INDEX] = 수[Loop_INDEX] = čekaj_VALUE[Loop_INDEX] = odjel_informacijske_tehnologije_ograničen[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_sudionik(int 열린파일번호, int 통신주소, int broj_priključka) {
        int Loop_INDEX = provjeriti(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Stanje_VALUE[Loop_INDEX] != 1 || broj_priključka < 0 || broj_priključka > 65535) return -22;
        if (broj_priključka == 0) { do { broj_priključka = Dalje_artikl++; if (Dalje_artikl > 65535) Dalje_artikl = 50000; } while (사용중(broj_priključka)); }
        if (사용중(broj_priključka)) return -98; prebaciti_VALUE[Loop_INDEX] = broj_priključka; odjel_informacijske_tehnologije_ograničen[Loop_INDEX] = 1; Stanje_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int osluškivati_sudionik(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = provjeriti(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stanje_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Stanje_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Spoji_se(int 열린파일번호, int 통신주소, int broj_priključka) {
        int Loop_INDEX = provjeriti(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (broj_priključka < 1 || broj_priključka > 65535 || Stanje_VALUE[Loop_INDEX] > 2) return -22;
        int primiti_dojaviti = -1; for (int unutarnji_položaj = 0; unutarnji_položaj < 16; unutarnji_položaj++) if (Stanje_VALUE[unutarnji_položaj] == 3 && prebaciti_VALUE[unutarnji_položaj] == broj_priključka) primiti_dojaviti = unutarnji_položaj;
        if (primiti_dojaviti < 0) return -111;
        int 대기여부 = 0; for (int unutarnji_položaj = 0; unutarnji_položaj < 16; unutarnji_položaj++) if (čekaj_VALUE[unutarnji_položaj] == primiti_dojaviti + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Stanje_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_sudionik(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Ostalo = Create_unos(); if (Ostalo < 0) return Ostalo; Ostalo -= 40;
        Stanje_VALUE[Loop_INDEX] = Stanje_VALUE[Ostalo] = 4; 짝[Loop_INDEX] = Ostalo; 짝[Ostalo] = Loop_INDEX; prebaciti_VALUE[Ostalo] = broj_priključka; ravnopravan_član_prebaciti[Loop_INDEX] = broj_priključka; ravnopravan_član_prebaciti[Ostalo] = prebaciti_VALUE[Loop_INDEX]; čekaj_VALUE[Ostalo] = primiti_dojaviti + 1; return 0;
    }
    public static int prihvatiti_veza(int 열린파일번호) { int Loop_INDEX = provjeriti(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stanje_VALUE[Loop_INDEX] != 3) return -22; for (int unutarnji_položaj = 0; unutarnji_položaj < 16; unutarnji_položaj++) if (Stanje_VALUE[unutarnji_položaj] != 0 && čekaj_VALUE[unutarnji_položaj] == Loop_INDEX + 1) { čekaj_VALUE[unutarnji_položaj] = 0; return unutarnji_položaj + 40; } return -11; }
    public static int Zapisuj(int 열린파일번호, int unos_COUNT) {
        int Loop_INDEX = provjeriti(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stanje_VALUE[Loop_INDEX] != 4) return -107;
        if (unos_COUNT < 0 || unos_COUNT > 512) return -22; if (unos_COUNT == 0) return 0;
        int unutarnji_položaj = 짝[Loop_INDEX]; if (unutarnji_položaj < 0) return -32; int ukupni_zbroj_COUNT = 1024 - 수[unutarnji_položaj]; if (ukupni_zbroj_COUNT == 0) return -11; if (ukupni_zbroj_COUNT > unos_COUNT) ukupni_zbroj_COUNT = unos_COUNT;
        for (int Usporedba_položaj = 0; Usporedba_položaj < ukupni_zbroj_COUNT; Usporedba_položaj++) podaci[unutarnji_položaj * 1024 + (prednja_VALUE[unutarnji_položaj] + 수[unutarnji_položaj] + Usporedba_položaj) % 1024] = povratna_obrada_mreža.Naprijed_VALUE[Usporedba_položaj]; 수[unutarnji_položaj] += ukupni_zbroj_COUNT; return ukupni_zbroj_COUNT;
    }
    public static int Čitaj(int 열린파일번호, int unos_COUNT) {
        int Loop_INDEX = provjeriti(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stanje_VALUE[Loop_INDEX] != 4) return -107; if (unos_COUNT < 0 || unos_COUNT > 512) return -22;
        if (unos_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (unos_COUNT > 수[Loop_INDEX]) unos_COUNT = 수[Loop_INDEX];
        for (int Usporedba_položaj = 0; Usporedba_položaj < unos_COUNT; Usporedba_položaj++) povratna_obrada_mreža.Naprijed_VALUE[Usporedba_položaj] = podaci[Loop_INDEX * 1024 + (prednja_VALUE[Loop_INDEX] + Usporedba_položaj) % 1024]; prednja_VALUE[Loop_INDEX] = (prednja_VALUE[Loop_INDEX] + unos_COUNT) % 1024; 수[Loop_INDEX] -= unos_COUNT; return unos_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = provjeriti(열린파일번호); return Loop_INDEX < 0 ? -9 : prebaciti_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = provjeriti(열린파일번호); return Loop_INDEX < 0 ? -9 : ravnopravan_član_prebaciti[Loop_INDEX]; }
    public static int Zatvori(int 열린파일번호) {
        int Loop_INDEX = provjeriti(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Stanje_VALUE[Loop_INDEX] == 3) for (int unutarnji_položaj = 0; unutarnji_položaj < 16; unutarnji_položaj++) if (čekaj_VALUE[unutarnji_položaj] == Loop_INDEX + 1) { if (짝[unutarnji_položaj] >= 0) 짝[짝[unutarnji_položaj]] = -1; Stanje_VALUE[unutarnji_položaj] = čekaj_VALUE[unutarnji_položaj] = odjel_informacijske_tehnologije_ograničen[unutarnji_položaj] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Stanje_VALUE[Loop_INDEX] = odjel_informacijske_tehnologije_ograničen[Loop_INDEX] = 수[Loop_INDEX] = čekaj_VALUE[Loop_INDEX] = 0; return 0;
    }
}
