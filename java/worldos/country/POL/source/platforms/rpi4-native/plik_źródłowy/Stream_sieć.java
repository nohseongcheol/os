// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jądro_WARTOŚĆ 안의 연결형 bajt_WARTOŚĆ Stream_WARTOŚĆ. Ethernet/TCP 패킷 스택이 아닌 루프백 socket warstwa_WARTOŚĆ. */
public final class Stream_sieć {
    static int[] Stan_WARTOŚĆ = new int[16], port_WARTOŚĆ = new int[16], 짝 = new int[16], węzeł_równorzędny_port = new int[16], chwileczkę_WARTOŚĆ = new int[16], systemy_informacyjne_granica = new int[16];
    static int[] przód_WARTOŚĆ = new int[16], identyfikator = new int[16], dane = new int[16 * 1024];
    static int Dalej_towar = 50000;
    static int 확인(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Stan_WARTOŚĆ[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int numer_portu) { for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (Stan_WARTOŚĆ[Loop_INDEKS] != 0 && systemy_informacyjne_granica[Loop_INDEKS] != 0 && port_WARTOŚĆ[Loop_INDEKS] == numer_portu) return true; return false; }
    public static int Twórca_wpis() {
        for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) if (Stan_WARTOŚĆ[Loop_INDEKS] == 0) { Stan_WARTOŚĆ[Loop_INDEKS] = 1; węzeł_równorzędny_port[Loop_INDEKS] = port_WARTOŚĆ[Loop_INDEKS] = przód_WARTOŚĆ[Loop_INDEKS] = identyfikator[Loop_INDEKS] = chwileczkę_WARTOŚĆ[Loop_INDEKS] = systemy_informacyjne_granica[Loop_INDEKS] = 0; 짝[Loop_INDEKS] = -1; return Loop_INDEKS + 40; }
        return -24;
    }
    public static int BIND_uczestnik(int 열린파일번호, int gniazdo_ADRES, int numer_portu) {
        int Loop_INDEKS = 확인(열린파일번호); if (Loop_INDEKS < 0) return -9;
        if (gniazdo_ADRES != 0 && gniazdo_ADRES != 0x7f000001) return -99;
        if (Stan_WARTOŚĆ[Loop_INDEKS] != 1 || numer_portu < 0 || numer_portu > 65535) return -22;
        if (numer_portu == 0) { do { numer_portu = Dalej_towar++; if (Dalej_towar > 65535) Dalej_towar = 50000; } while (사용중(numer_portu)); }
        if (사용중(numer_portu)) return -98; port_WARTOŚĆ[Loop_INDEKS] = numer_portu; systemy_informacyjne_granica[Loop_INDEKS] = 1; Stan_WARTOŚĆ[Loop_INDEKS] = 2; return 0;
    }
    public static int nasłuchiwać_uczestnik(int 열린파일번호, int lista_prac) { int Loop_INDEKS = 확인(열린파일번호); if (Loop_INDEKS < 0) return -9; if (Stan_WARTOŚĆ[Loop_INDEKS] != 2 || lista_prac < 1) return -22; Stan_WARTOŚĆ[Loop_INDEKS] = 3; return 0; }
    public static int Połącz(int 열린파일번호, int gniazdo_ADRES, int numer_portu) {
        int Loop_INDEKS = 확인(열린파일번호); if (Loop_INDEKS < 0) return -9; if (gniazdo_ADRES != 0x7f000001) return -101;
        if (numer_portu < 1 || numer_portu > 65535 || Stan_WARTOŚĆ[Loop_INDEKS] > 2) return -22;
        int odbierać_strona = -1; for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < 16; wewnętrzne_stanowisko++) if (Stan_WARTOŚĆ[wewnętrzne_stanowisko] == 3 && port_WARTOŚĆ[wewnętrzne_stanowisko] == numer_portu) odbierać_strona = wewnętrzne_stanowisko;
        if (odbierać_strona < 0) return -111;
        int 대기여부 = 0; for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < 16; wewnętrzne_stanowisko++) if (chwileczkę_WARTOŚĆ[wewnętrzne_stanowisko] == odbierać_strona + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Stan_WARTOŚĆ[Loop_INDEKS] == 1) { int 처리값 = BIND_uczestnik(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Inne = Twórca_wpis(); if (Inne < 0) return Inne; Inne -= 40;
        Stan_WARTOŚĆ[Loop_INDEKS] = Stan_WARTOŚĆ[Inne] = 4; 짝[Loop_INDEKS] = Inne; 짝[Inne] = Loop_INDEKS; port_WARTOŚĆ[Inne] = numer_portu; węzeł_równorzędny_port[Loop_INDEKS] = numer_portu; węzeł_równorzędny_port[Inne] = port_WARTOŚĆ[Loop_INDEKS]; chwileczkę_WARTOŚĆ[Inne] = odbierać_strona + 1; return 0;
    }
    public static int akceptować_połączenie(int 열린파일번호) { int Loop_INDEKS = 확인(열린파일번호); if (Loop_INDEKS < 0) return -9; if (Stan_WARTOŚĆ[Loop_INDEKS] != 3) return -22; for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < 16; wewnętrzne_stanowisko++) if (Stan_WARTOŚĆ[wewnętrzne_stanowisko] != 0 && chwileczkę_WARTOŚĆ[wewnętrzne_stanowisko] == Loop_INDEKS + 1) { chwileczkę_WARTOŚĆ[wewnętrzne_stanowisko] = 0; return wewnętrzne_stanowisko + 40; } return -11; }
    public static int Zapis(int 열린파일번호, int wpis_ILE_LICZB) {
        int Loop_INDEKS = 확인(열린파일번호); if (Loop_INDEKS < 0) return -9; if (Stan_WARTOŚĆ[Loop_INDEKS] != 4) return -107;
        if (wpis_ILE_LICZB < 0 || wpis_ILE_LICZB > 512) return -22; if (wpis_ILE_LICZB == 0) return 0;
        int wewnętrzne_stanowisko = 짝[Loop_INDEKS]; if (wewnętrzne_stanowisko < 0) return -32; int suma_ILE_LICZB = 1024 - identyfikator[wewnętrzne_stanowisko]; if (suma_ILE_LICZB == 0) return -11; if (suma_ILE_LICZB > wpis_ILE_LICZB) suma_ILE_LICZB = wpis_ILE_LICZB;
        for (int Porównanie_stanowisko = 0; Porównanie_stanowisko < suma_ILE_LICZB; Porównanie_stanowisko++) dane[wewnętrzne_stanowisko * 1024 + (przód_WARTOŚĆ[wewnętrzne_stanowisko] + identyfikator[wewnętrzne_stanowisko] + Porównanie_stanowisko) % 1024] = sprzężenie_zwrotne_sieć.Dalej_WARTOŚĆ[Porównanie_stanowisko]; identyfikator[wewnętrzne_stanowisko] += suma_ILE_LICZB; return suma_ILE_LICZB;
    }
    public static int Odczyt(int 열린파일번호, int wpis_ILE_LICZB) {
        int Loop_INDEKS = 확인(열린파일번호); if (Loop_INDEKS < 0) return -9; if (Stan_WARTOŚĆ[Loop_INDEKS] != 4) return -107; if (wpis_ILE_LICZB < 0 || wpis_ILE_LICZB > 512) return -22;
        if (wpis_ILE_LICZB == 0) return 0; if (identyfikator[Loop_INDEKS] == 0) return 짝[Loop_INDEKS] < 0 ? 0 : -11; if (wpis_ILE_LICZB > identyfikator[Loop_INDEKS]) wpis_ILE_LICZB = identyfikator[Loop_INDEKS];
        for (int Porównanie_stanowisko = 0; Porównanie_stanowisko < wpis_ILE_LICZB; Porównanie_stanowisko++) sprzężenie_zwrotne_sieć.Dalej_WARTOŚĆ[Porównanie_stanowisko] = dane[Loop_INDEKS * 1024 + (przód_WARTOŚĆ[Loop_INDEKS] + Porównanie_stanowisko) % 1024]; przód_WARTOŚĆ[Loop_INDEKS] = (przód_WARTOŚĆ[Loop_INDEKS] + wpis_ILE_LICZB) % 1024; identyfikator[Loop_INDEKS] -= wpis_ILE_LICZB; return wpis_ILE_LICZB;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEKS = 확인(열린파일번호); return Loop_INDEKS < 0 ? -9 : port_WARTOŚĆ[Loop_INDEKS]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEKS = 확인(열린파일번호); return Loop_INDEKS < 0 ? -9 : węzeł_równorzędny_port[Loop_INDEKS]; }
    public static int Zamknięte(int 열린파일번호) {
        int Loop_INDEKS = 확인(열린파일번호); if (Loop_INDEKS < 0) return -9;
        if (Stan_WARTOŚĆ[Loop_INDEKS] == 3) for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < 16; wewnętrzne_stanowisko++) if (chwileczkę_WARTOŚĆ[wewnętrzne_stanowisko] == Loop_INDEKS + 1) { if (짝[wewnętrzne_stanowisko] >= 0) 짝[짝[wewnętrzne_stanowisko]] = -1; Stan_WARTOŚĆ[wewnętrzne_stanowisko] = chwileczkę_WARTOŚĆ[wewnętrzne_stanowisko] = systemy_informacyjne_granica[wewnętrzne_stanowisko] = 0; }
        if (짝[Loop_INDEKS] >= 0) 짝[짝[Loop_INDEKS]] = -1; Stan_WARTOŚĆ[Loop_INDEKS] = systemy_informacyjne_granica[Loop_INDEKS] = identyfikator[Loop_INDEKS] = chwileczkę_WARTOŚĆ[Loop_INDEKS] = 0; return 0;
    }
}
