// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 warstwa_WARTOŚĆ: 단일 jądro_WARTOŚĆ 안의 IPv4/UDP 루프백 transfer_WARTOŚĆ.
 * zewnętrzny_WARTOŚĆ IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * Koniec_punkt 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class sprzężenie_zwrotne_sieć {
    static int[] używać_WARTOŚĆ = new int[8];
    static int[] port_WARTOŚĆ = new int[8];
    static int[] Adres = new int[8];
    static int[] przód_WARTOŚĆ = new int[8];
    static int[] towar_ILE_LICZB = new int[8];
    static int[] KWOTA_WYKUP_port = new int[8];
    static int[] długość_WARTOŚĆ = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] dane = new int[32 * 512];
    static int[] Dalej_WARTOŚĆ = new int[512];
    static int Dalej_uczestnik = 49152;
    static int 확인(int INDEKS) { return INDEKS >= 32 && INDEKS < 40 && używać_WARTOŚĆ[INDEKS - 32] != 0 ? INDEKS - 32 : -1; }
    static boolean 겹침(int INDEKS) {
        for (int gniazdo_wpis = 0; gniazdo_wpis < 8; gniazdo_wpis++) if (używać_WARTOŚĆ[gniazdo_wpis] != 0 && port_WARTOŚĆ[gniazdo_wpis] == INDEKS) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int kandydat = Dalej_uczestnik++;
            if (Dalej_uczestnik > 65535) Dalej_uczestnik = 49152;
            if (!겹침(kandydat)) return kandydat;
        }
        return -98;
    }
    public static int Twórca_wpis(int region_WARTOŚĆ, int Rodzaj_WARTOŚĆ, int wartość_kontraktu) {
        if (region_WARTOŚĆ != 2) return -97;
        if (Rodzaj_WARTOŚĆ != 2 || (wartość_kontraktu != 0 && wartość_kontraktu != 17)) return -93;
        for (int gniazdo_wpis = 0; gniazdo_wpis < 8; gniazdo_wpis++) if (używać_WARTOŚĆ[gniazdo_wpis] == 0) {
            używać_WARTOŚĆ[gniazdo_wpis] = 1; port_WARTOŚĆ[gniazdo_wpis] = 0; Adres[gniazdo_wpis] = 0; przód_WARTOŚĆ[gniazdo_wpis] = 0; towar_ILE_LICZB[gniazdo_wpis] = 0; KWOTA_WYKUP_port[gniazdo_wpis] = 0;
            return gniazdo_wpis + 32;
        }
        return -24;
    }
    public static int BIND_uczestnik(int INDEKS, int identyfikator_sieciowy, int uczestnik_numer_portu) {
        int gniazdo_wpis = 확인(INDEKS);
        if (gniazdo_wpis < 0) return -9;
        if (identyfikator_sieciowy != 0 && identyfikator_sieciowy != 0x7f000001) return -99;
        if (port_WARTOŚĆ[gniazdo_wpis] != 0 || uczestnik_numer_portu < 0 || uczestnik_numer_portu > 65535) return -22;
        if (uczestnik_numer_portu == 0) uczestnik_numer_portu = 임시창구();
        if (uczestnik_numer_portu < 0) return uczestnik_numer_portu;
        if (겹침(uczestnik_numer_portu)) return -98;
        port_WARTOŚĆ[gniazdo_wpis] = uczestnik_numer_portu; Adres[gniazdo_wpis] = identyfikator_sieciowy; return 0;
    }
    public static int 자료넣기(int INDEKS, int WARTOŚĆ) {
        if (INDEKS < 0 || INDEKS >= 512) return -22;
        Dalej_WARTOŚĆ[INDEKS] = WARTOŚĆ & 255; return 0;
    }
    public static int 자료읽기(int INDEKS) { return INDEKS >= 0 && INDEKS < 512 ? Dalej_WARTOŚĆ[INDEKS] : -22; }
    public static int wysłać(int INDEKS, int identyfikator_sieciowy, int uczestnik_numer_portu, int Rozmiar) {
        int gniazdo_wpis = 확인(INDEKS);
        if (gniazdo_wpis < 0) return -9;
        if (identyfikator_sieciowy != 0x7f000001) return -101;
        if (uczestnik_numer_portu < 1 || uczestnik_numer_portu > 65535) return -22;
        if (Rozmiar < 0 || Rozmiar > 512) return -90;
        if (port_WARTOŚĆ[gniazdo_wpis] == 0) {
            int WYNIK = BIND_uczestnik(INDEKS, 0x7f000001, 0);
            if (WYNIK < 0) return WYNIK;
        }
        int cel_WARTOŚĆ = -1;
        for (int kandydat = 0; kandydat < 8; kandydat++) if (używać_WARTOŚĆ[kandydat] != 0 && port_WARTOŚĆ[kandydat] == uczestnik_numer_portu) cel_WARTOŚĆ = kandydat;
        if (cel_WARTOŚĆ < 0) return -111;
        if (towar_ILE_LICZB[cel_WARTOŚĆ] == 4) return -11;
        int indeks_pozycji = cel_WARTOŚĆ * 4 + (przód_WARTOŚĆ[cel_WARTOŚĆ] + towar_ILE_LICZB[cel_WARTOŚĆ]) % 4;
        for (int bajt_WARTOŚĆ = 0; bajt_WARTOŚĆ < Rozmiar; bajt_WARTOŚĆ++) dane[indeks_pozycji * 512 + bajt_WARTOŚĆ] = Dalej_WARTOŚĆ[bajt_WARTOŚĆ];
        długość_WARTOŚĆ[indeks_pozycji] = Rozmiar; 보낸창구[indeks_pozycji] = port_WARTOŚĆ[gniazdo_wpis]; towar_ILE_LICZB[cel_WARTOŚĆ]++;
        return Rozmiar;
    }
    public static int odbierać(int INDEKS, int pojemność_WARTOŚĆ) {
        int gniazdo_wpis = 확인(INDEKS);
        if (gniazdo_wpis < 0) return -9;
        if (pojemność_WARTOŚĆ < 0 || pojemność_WARTOŚĆ > 512) return -22;
        if (towar_ILE_LICZB[gniazdo_wpis] == 0) return -11;
        int indeks_pozycji = gniazdo_wpis * 4 + przód_WARTOŚĆ[gniazdo_wpis];
        int Rozmiar = długość_WARTOŚĆ[indeks_pozycji] < pojemność_WARTOŚĆ ? długość_WARTOŚĆ[indeks_pozycji] : pojemność_WARTOŚĆ;
        for (int bajt_WARTOŚĆ = 0; bajt_WARTOŚĆ < Rozmiar; bajt_WARTOŚĆ++) Dalej_WARTOŚĆ[bajt_WARTOŚĆ] = dane[indeks_pozycji * 512 + bajt_WARTOŚĆ];
        KWOTA_WYKUP_port[gniazdo_wpis] = 보낸창구[indeks_pozycji]; przód_WARTOŚĆ[gniazdo_wpis] = (przód_WARTOŚĆ[gniazdo_wpis] + 1) % 4; towar_ILE_LICZB[gniazdo_wpis]--;
        return Rozmiar;
    }
    public static int 창구읽기(int INDEKS) { int gniazdo_wpis = 확인(INDEKS); return gniazdo_wpis < 0 ? -9 : port_WARTOŚĆ[gniazdo_wpis]; }
    public static int 주소읽기(int INDEKS) { int gniazdo_wpis = 확인(INDEKS); return gniazdo_wpis < 0 ? -9 : Adres[gniazdo_wpis]; }
    public static int nadawca_uczestnik(int INDEKS) { int gniazdo_wpis = 확인(INDEKS); return gniazdo_wpis < 0 ? -9 : KWOTA_WYKUP_port[gniazdo_wpis]; }
    public static int Zamknięte(int INDEKS) {
        int gniazdo_wpis = 확인(INDEKS); if (gniazdo_wpis < 0) return -9;
        używać_WARTOŚĆ[gniazdo_wpis] = 0; towar_ILE_LICZB[gniazdo_wpis] = 0; port_WARTOŚĆ[gniazdo_wpis] = 0; return 0;
    }
}
