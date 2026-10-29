// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jádro_HODNOTA 안의 연결형 bajt_HODNOTA tok_HODNOTA. Ethernet/TCP 패킷 스택이 아닌 루프백 socket vrstva_HODNOTA. */
public final class tok_síť {
    static int[] Stav_HODNOTA = new int[16], port_HODNOTA = new int[16], 짝 = new int[16], partner_port = new int[16], počkej_HODNOTA = new int[16], informační_systémy_mez = new int[16];
    static int[] přední_fotoaparát_HODNOTA = new int[16], číslo = new int[16], data = new int[16 * 1024];
    static int Další_zboží = 50000;
    static int ověřit(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Stav_HODNOTA[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int číslo_portu) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Stav_HODNOTA[Loop_INDEX] != 0 && informační_systémy_mez[Loop_INDEX] != 0 && port_HODNOTA[Loop_INDEX] == číslo_portu) return true; return false; }
    public static int Create_položka() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Stav_HODNOTA[Loop_INDEX] == 0) { Stav_HODNOTA[Loop_INDEX] = 1; partner_port[Loop_INDEX] = port_HODNOTA[Loop_INDEX] = přední_fotoaparát_HODNOTA[Loop_INDEX] = číslo[Loop_INDEX] = počkej_HODNOTA[Loop_INDEX] = informační_systémy_mez[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int vázat_účastník(int 열린파일번호, int soket_ODKAZ, int číslo_portu) {
        int Loop_INDEX = ověřit(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (soket_ODKAZ != 0 && soket_ODKAZ != 0x7f000001) return -99;
        if (Stav_HODNOTA[Loop_INDEX] != 1 || číslo_portu < 0 || číslo_portu > 65535) return -22;
        if (číslo_portu == 0) { do { číslo_portu = Další_zboží++; if (Další_zboží > 65535) Další_zboží = 50000; } while (사용중(číslo_portu)); }
        if (사용중(číslo_portu)) return -98; port_HODNOTA[Loop_INDEX] = číslo_portu; informační_systémy_mez[Loop_INDEX] = 1; Stav_HODNOTA[Loop_INDEX] = 2; return 0;
    }
    public static int naslouchat_účastník(int 열린파일번호, int backlog) { int Loop_INDEX = ověřit(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stav_HODNOTA[Loop_INDEX] != 2 || backlog < 1) return -22; Stav_HODNOTA[Loop_INDEX] = 3; return 0; }
    public static int Připojit(int 열린파일번호, int soket_ODKAZ, int číslo_portu) {
        int Loop_INDEX = ověřit(열린파일번호); if (Loop_INDEX < 0) return -9; if (soket_ODKAZ != 0x7f000001) return -101;
        if (číslo_portu < 1 || číslo_portu > 65535 || Stav_HODNOTA[Loop_INDEX] > 2) return -22;
        int dostat_stránka = -1; for (int vnitřní_pozice = 0; vnitřní_pozice < 16; vnitřní_pozice++) if (Stav_HODNOTA[vnitřní_pozice] == 3 && port_HODNOTA[vnitřní_pozice] == číslo_portu) dostat_stránka = vnitřní_pozice;
        if (dostat_stránka < 0) return -111;
        int 대기여부 = 0; for (int vnitřní_pozice = 0; vnitřní_pozice < 16; vnitřní_pozice++) if (počkej_HODNOTA[vnitřní_pozice] == dostat_stránka + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Stav_HODNOTA[Loop_INDEX] == 1) { int 처리값 = vázat_účastník(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Jiný = Create_položka(); if (Jiný < 0) return Jiný; Jiný -= 40;
        Stav_HODNOTA[Loop_INDEX] = Stav_HODNOTA[Jiný] = 4; 짝[Loop_INDEX] = Jiný; 짝[Jiný] = Loop_INDEX; port_HODNOTA[Jiný] = číslo_portu; partner_port[Loop_INDEX] = číslo_portu; partner_port[Jiný] = port_HODNOTA[Loop_INDEX]; počkej_HODNOTA[Jiný] = dostat_stránka + 1; return 0;
    }
    public static int přijmout_kontakt(int 열린파일번호) { int Loop_INDEX = ověřit(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stav_HODNOTA[Loop_INDEX] != 3) return -22; for (int vnitřní_pozice = 0; vnitřní_pozice < 16; vnitřní_pozice++) if (Stav_HODNOTA[vnitřní_pozice] != 0 && počkej_HODNOTA[vnitřní_pozice] == Loop_INDEX + 1) { počkej_HODNOTA[vnitřní_pozice] = 0; return vnitřní_pozice + 40; } return -11; }
    public static int Zápis(int 열린파일번호, int položka_POČET) {
        int Loop_INDEX = ověřit(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stav_HODNOTA[Loop_INDEX] != 4) return -107;
        if (položka_POČET < 0 || položka_POČET > 512) return -22; if (položka_POČET == 0) return 0;
        int vnitřní_pozice = 짝[Loop_INDEX]; if (vnitřní_pozice < 0) return -32; int celkem_POČET = 1024 - číslo[vnitřní_pozice]; if (celkem_POČET == 0) return -11; if (celkem_POČET > položka_POČET) celkem_POČET = položka_POČET;
        for (int Porovnání_pozice = 0; Porovnání_pozice < celkem_POČET; Porovnání_pozice++) data[vnitřní_pozice * 1024 + (přední_fotoaparát_HODNOTA[vnitřní_pozice] + číslo[vnitřní_pozice] + Porovnání_pozice) % 1024] = zpětná_smyčka_síť.Vpřed_HODNOTA[Porovnání_pozice]; číslo[vnitřní_pozice] += celkem_POČET; return celkem_POČET;
    }
    public static int Čtení(int 열린파일번호, int položka_POČET) {
        int Loop_INDEX = ověřit(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stav_HODNOTA[Loop_INDEX] != 4) return -107; if (položka_POČET < 0 || položka_POČET > 512) return -22;
        if (položka_POČET == 0) return 0; if (číslo[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (položka_POČET > číslo[Loop_INDEX]) položka_POČET = číslo[Loop_INDEX];
        for (int Porovnání_pozice = 0; Porovnání_pozice < položka_POČET; Porovnání_pozice++) zpětná_smyčka_síť.Vpřed_HODNOTA[Porovnání_pozice] = data[Loop_INDEX * 1024 + (přední_fotoaparát_HODNOTA[Loop_INDEX] + Porovnání_pozice) % 1024]; přední_fotoaparát_HODNOTA[Loop_INDEX] = (přední_fotoaparát_HODNOTA[Loop_INDEX] + položka_POČET) % 1024; číslo[Loop_INDEX] -= položka_POČET; return položka_POČET;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = ověřit(열린파일번호); return Loop_INDEX < 0 ? -9 : port_HODNOTA[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = ověřit(열린파일번호); return Loop_INDEX < 0 ? -9 : partner_port[Loop_INDEX]; }
    public static int Zavřené(int 열린파일번호) {
        int Loop_INDEX = ověřit(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Stav_HODNOTA[Loop_INDEX] == 3) for (int vnitřní_pozice = 0; vnitřní_pozice < 16; vnitřní_pozice++) if (počkej_HODNOTA[vnitřní_pozice] == Loop_INDEX + 1) { if (짝[vnitřní_pozice] >= 0) 짝[짝[vnitřní_pozice]] = -1; Stav_HODNOTA[vnitřní_pozice] = počkej_HODNOTA[vnitřní_pozice] = informační_systémy_mez[vnitřní_pozice] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Stav_HODNOTA[Loop_INDEX] = informační_systémy_mez[Loop_INDEX] = číslo[Loop_INDEX] = počkej_HODNOTA[Loop_INDEX] = 0; return 0;
    }
}
