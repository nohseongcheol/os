// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jadro_VALUE 안의 연결형 Byte_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket vrstva_VALUE. */
public final class Stream_sieť {
    static int[] Stav_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], partnerský_uzol_port = new int[16], počkaj_VALUE = new int[16], Informačné_systémy_hranica = new int[16];
    static int[] predný_VALUE = new int[16], 수 = new int[16], údaje = new int[16 * 1024];
    static int Ďalej_položka = 50000;
    static int overiť(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Stav_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int číslo_portu) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Stav_VALUE[Loop_INDEX] != 0 && Informačné_systémy_hranica[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == číslo_portu) return true; return false; }
    public static int Create_položka() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Stav_VALUE[Loop_INDEX] == 0) { Stav_VALUE[Loop_INDEX] = 1; partnerský_uzol_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = predný_VALUE[Loop_INDEX] = 수[Loop_INDEX] = počkaj_VALUE[Loop_INDEX] = Informačné_systémy_hranica[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_účastník(int 열린파일번호, int soket_adresa, int číslo_portu) {
        int Loop_INDEX = overiť(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (soket_adresa != 0 && soket_adresa != 0x7f000001) return -99;
        if (Stav_VALUE[Loop_INDEX] != 1 || číslo_portu < 0 || číslo_portu > 65535) return -22;
        if (číslo_portu == 0) { do { číslo_portu = Ďalej_položka++; if (Ďalej_položka > 65535) Ďalej_položka = 50000; } while (사용중(číslo_portu)); }
        if (사용중(číslo_portu)) return -98; port_VALUE[Loop_INDEX] = číslo_portu; Informačné_systémy_hranica[Loop_INDEX] = 1; Stav_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int načúvať_účastník(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = overiť(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stav_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Stav_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Pripojiť(int 열린파일번호, int soket_adresa, int číslo_portu) {
        int Loop_INDEX = overiť(열린파일번호); if (Loop_INDEX < 0) return -9; if (soket_adresa != 0x7f000001) return -101;
        if (číslo_portu < 1 || číslo_portu > 65535 || Stav_VALUE[Loop_INDEX] > 2) return -22;
        int dostať_strana = -1; for (int vnútorné_pozícia = 0; vnútorné_pozícia < 16; vnútorné_pozícia++) if (Stav_VALUE[vnútorné_pozícia] == 3 && port_VALUE[vnútorné_pozícia] == číslo_portu) dostať_strana = vnútorné_pozícia;
        if (dostať_strana < 0) return -111;
        int 대기여부 = 0; for (int vnútorné_pozícia = 0; vnútorné_pozícia < 16; vnútorné_pozícia++) if (počkaj_VALUE[vnútorné_pozícia] == dostať_strana + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Stav_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_účastník(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Iné = Create_položka(); if (Iné < 0) return Iné; Iné -= 40;
        Stav_VALUE[Loop_INDEX] = Stav_VALUE[Iné] = 4; 짝[Loop_INDEX] = Iné; 짝[Iné] = Loop_INDEX; port_VALUE[Iné] = číslo_portu; partnerský_uzol_port[Loop_INDEX] = číslo_portu; partnerský_uzol_port[Iné] = port_VALUE[Loop_INDEX]; počkaj_VALUE[Iné] = dostať_strana + 1; return 0;
    }
    public static int prijať_kontakt(int 열린파일번호) { int Loop_INDEX = overiť(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stav_VALUE[Loop_INDEX] != 3) return -22; for (int vnútorné_pozícia = 0; vnútorné_pozícia < 16; vnútorné_pozícia++) if (Stav_VALUE[vnútorné_pozícia] != 0 && počkaj_VALUE[vnútorné_pozícia] == Loop_INDEX + 1) { počkaj_VALUE[vnútorné_pozícia] = 0; return vnútorné_pozícia + 40; } return -11; }
    public static int Zápis(int 열린파일번호, int položka_COUNT_8f7753a1) {
        int Loop_INDEX = overiť(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stav_VALUE[Loop_INDEX] != 4) return -107;
        if (položka_COUNT_8f7753a1 < 0 || položka_COUNT_8f7753a1 > 512) return -22; if (položka_COUNT_8f7753a1 == 0) return 0;
        int vnútorné_pozícia = 짝[Loop_INDEX]; if (vnútorné_pozícia < 0) return -32; int celkovo_COUNT = 1024 - 수[vnútorné_pozícia]; if (celkovo_COUNT == 0) return -11; if (celkovo_COUNT > položka_COUNT_8f7753a1) celkovo_COUNT = položka_COUNT_8f7753a1;
        for (int Porovnanie_pozícia = 0; Porovnanie_pozícia < celkovo_COUNT; Porovnanie_pozícia++) údaje[vnútorné_pozícia * 1024 + (predný_VALUE[vnútorné_pozícia] + 수[vnútorné_pozícia] + Porovnanie_pozícia) % 1024] = spätná_slučka_sieť.Dopredu_VALUE[Porovnanie_pozícia]; 수[vnútorné_pozícia] += celkovo_COUNT; return celkovo_COUNT;
    }
    public static int Čítanie(int 열린파일번호, int položka_COUNT_8f7753a1) {
        int Loop_INDEX = overiť(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stav_VALUE[Loop_INDEX] != 4) return -107; if (položka_COUNT_8f7753a1 < 0 || položka_COUNT_8f7753a1 > 512) return -22;
        if (položka_COUNT_8f7753a1 == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (položka_COUNT_8f7753a1 > 수[Loop_INDEX]) položka_COUNT_8f7753a1 = 수[Loop_INDEX];
        for (int Porovnanie_pozícia = 0; Porovnanie_pozícia < položka_COUNT_8f7753a1; Porovnanie_pozícia++) spätná_slučka_sieť.Dopredu_VALUE[Porovnanie_pozícia] = údaje[Loop_INDEX * 1024 + (predný_VALUE[Loop_INDEX] + Porovnanie_pozícia) % 1024]; predný_VALUE[Loop_INDEX] = (predný_VALUE[Loop_INDEX] + položka_COUNT_8f7753a1) % 1024; 수[Loop_INDEX] -= položka_COUNT_8f7753a1; return položka_COUNT_8f7753a1;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = overiť(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = overiť(열린파일번호); return Loop_INDEX < 0 ? -9 : partnerský_uzol_port[Loop_INDEX]; }
    public static int Zatvoriť(int 열린파일번호) {
        int Loop_INDEX = overiť(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Stav_VALUE[Loop_INDEX] == 3) for (int vnútorné_pozícia = 0; vnútorné_pozícia < 16; vnútorné_pozícia++) if (počkaj_VALUE[vnútorné_pozícia] == Loop_INDEX + 1) { if (짝[vnútorné_pozícia] >= 0) 짝[짝[vnútorné_pozícia]] = -1; Stav_VALUE[vnútorné_pozícia] = počkaj_VALUE[vnútorné_pozícia] = Informačné_systémy_hranica[vnútorné_pozícia] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Stav_VALUE[Loop_INDEX] = Informačné_systémy_hranica[Loop_INDEX] = 수[Loop_INDEX] = počkaj_VALUE[Loop_INDEX] = 0; return 0;
    }
}
