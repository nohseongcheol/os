// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_ÉRTÉK 안의 연결형 bájt_ÉRTÉK Stream_ÉRTÉK. Ethernet/TCP 패킷 스택이 아닌 루프백 socket réteg_ÉRTÉK. */
public final class Stream_hálózat {
    static int[] Állapot_ÉRTÉK = new int[16], port_ÉRTÉK = new int[16], 짝 = new int[16], társ_port = new int[16], várj_ÉRTÉK = new int[16], informatikai_részleg_határ = new int[16];
    static int[] elülső_kamera_ÉRTÉK = new int[16], szám = new int[16], adat = new int[16 * 1024];
    static int Tovább_cikk = 50000;
    static int igazol(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Állapot_ÉRTÉK[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int portszám) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Állapot_ÉRTÉK[Loop_INDEX] != 0 && informatikai_részleg_határ[Loop_INDEX] != 0 && port_ÉRTÉK[Loop_INDEX] == portszám) return true; return false; }
    public static int készít_bejegyzés() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Állapot_ÉRTÉK[Loop_INDEX] == 0) { Állapot_ÉRTÉK[Loop_INDEX] = 1; társ_port[Loop_INDEX] = port_ÉRTÉK[Loop_INDEX] = elülső_kamera_ÉRTÉK[Loop_INDEX] = szám[Loop_INDEX] = várj_ÉRTÉK[Loop_INDEX] = informatikai_részleg_határ[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_végpont(int 열린파일번호, int szoftvercsatorna_CÍM, int portszám) {
        int Loop_INDEX = igazol(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (szoftvercsatorna_CÍM != 0 && szoftvercsatorna_CÍM != 0x7f000001) return -99;
        if (Állapot_ÉRTÉK[Loop_INDEX] != 1 || portszám < 0 || portszám > 65535) return -22;
        if (portszám == 0) { do { portszám = Tovább_cikk++; if (Tovább_cikk > 65535) Tovább_cikk = 50000; } while (사용중(portszám)); }
        if (사용중(portszám)) return -98; port_ÉRTÉK[Loop_INDEX] = portszám; informatikai_részleg_határ[Loop_INDEX] = 1; Állapot_ÉRTÉK[Loop_INDEX] = 2; return 0;
    }
    public static int figyelés_végpont(int 열린파일번호, int hátralék) { int Loop_INDEX = igazol(열린파일번호); if (Loop_INDEX < 0) return -9; if (Állapot_ÉRTÉK[Loop_INDEX] != 2 || hátralék < 1) return -22; Állapot_ÉRTÉK[Loop_INDEX] = 3; return 0; }
    public static int Kapcsolódás(int 열린파일번호, int szoftvercsatorna_CÍM, int portszám) {
        int Loop_INDEX = igazol(열린파일번호); if (Loop_INDEX < 0) return -9; if (szoftvercsatorna_CÍM != 0x7f000001) return -101;
        if (portszám < 1 || portszám > 65535 || Állapot_ÉRTÉK[Loop_INDEX] > 2) return -22;
        int fogad_lap = -1; for (int belső_pozíció = 0; belső_pozíció < 16; belső_pozíció++) if (Állapot_ÉRTÉK[belső_pozíció] == 3 && port_ÉRTÉK[belső_pozíció] == portszám) fogad_lap = belső_pozíció;
        if (fogad_lap < 0) return -111;
        int 대기여부 = 0; for (int belső_pozíció = 0; belső_pozíció < 16; belső_pozíció++) if (várj_ÉRTÉK[belső_pozíció] == fogad_lap + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Állapot_ÉRTÉK[Loop_INDEX] == 1) { int 처리값 = BIND_végpont(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Egyéb = készít_bejegyzés(); if (Egyéb < 0) return Egyéb; Egyéb -= 40;
        Állapot_ÉRTÉK[Loop_INDEX] = Állapot_ÉRTÉK[Egyéb] = 4; 짝[Loop_INDEX] = Egyéb; 짝[Egyéb] = Loop_INDEX; port_ÉRTÉK[Egyéb] = portszám; társ_port[Loop_INDEX] = portszám; társ_port[Egyéb] = port_ÉRTÉK[Loop_INDEX]; várj_ÉRTÉK[Egyéb] = fogad_lap + 1; return 0;
    }
    public static int elfogad_ismerős(int 열린파일번호) { int Loop_INDEX = igazol(열린파일번호); if (Loop_INDEX < 0) return -9; if (Állapot_ÉRTÉK[Loop_INDEX] != 3) return -22; for (int belső_pozíció = 0; belső_pozíció < 16; belső_pozíció++) if (Állapot_ÉRTÉK[belső_pozíció] != 0 && várj_ÉRTÉK[belső_pozíció] == Loop_INDEX + 1) { várj_ÉRTÉK[belső_pozíció] = 0; return belső_pozíció + 40; } return -11; }
    public static int Írás(int 열린파일번호, int bejegyzés_DARAB) {
        int Loop_INDEX = igazol(열린파일번호); if (Loop_INDEX < 0) return -9; if (Állapot_ÉRTÉK[Loop_INDEX] != 4) return -107;
        if (bejegyzés_DARAB < 0 || bejegyzés_DARAB > 512) return -22; if (bejegyzés_DARAB == 0) return 0;
        int belső_pozíció = 짝[Loop_INDEX]; if (belső_pozíció < 0) return -32; int összesen_DARAB = 1024 - szám[belső_pozíció]; if (összesen_DARAB == 0) return -11; if (összesen_DARAB > bejegyzés_DARAB) összesen_DARAB = bejegyzés_DARAB;
        for (int Összehasonlítás_pozíció = 0; Összehasonlítás_pozíció < összesen_DARAB; Összehasonlítás_pozíció++) adat[belső_pozíció * 1024 + (elülső_kamera_ÉRTÉK[belső_pozíció] + szám[belső_pozíció] + Összehasonlítás_pozíció) % 1024] = visszacsatolt_hálózat.Előre_ÉRTÉK[Összehasonlítás_pozíció]; szám[belső_pozíció] += összesen_DARAB; return összesen_DARAB;
    }
    public static int Olvasás(int 열린파일번호, int bejegyzés_DARAB) {
        int Loop_INDEX = igazol(열린파일번호); if (Loop_INDEX < 0) return -9; if (Állapot_ÉRTÉK[Loop_INDEX] != 4) return -107; if (bejegyzés_DARAB < 0 || bejegyzés_DARAB > 512) return -22;
        if (bejegyzés_DARAB == 0) return 0; if (szám[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (bejegyzés_DARAB > szám[Loop_INDEX]) bejegyzés_DARAB = szám[Loop_INDEX];
        for (int Összehasonlítás_pozíció = 0; Összehasonlítás_pozíció < bejegyzés_DARAB; Összehasonlítás_pozíció++) visszacsatolt_hálózat.Előre_ÉRTÉK[Összehasonlítás_pozíció] = adat[Loop_INDEX * 1024 + (elülső_kamera_ÉRTÉK[Loop_INDEX] + Összehasonlítás_pozíció) % 1024]; elülső_kamera_ÉRTÉK[Loop_INDEX] = (elülső_kamera_ÉRTÉK[Loop_INDEX] + bejegyzés_DARAB) % 1024; szám[Loop_INDEX] -= bejegyzés_DARAB; return bejegyzés_DARAB;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = igazol(열린파일번호); return Loop_INDEX < 0 ? -9 : port_ÉRTÉK[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = igazol(열린파일번호); return Loop_INDEX < 0 ? -9 : társ_port[Loop_INDEX]; }
    public static int Bezárás(int 열린파일번호) {
        int Loop_INDEX = igazol(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Állapot_ÉRTÉK[Loop_INDEX] == 3) for (int belső_pozíció = 0; belső_pozíció < 16; belső_pozíció++) if (várj_ÉRTÉK[belső_pozíció] == Loop_INDEX + 1) { if (짝[belső_pozíció] >= 0) 짝[짝[belső_pozíció]] = -1; Állapot_ÉRTÉK[belső_pozíció] = várj_ÉRTÉK[belső_pozíció] = informatikai_részleg_határ[belső_pozíció] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Állapot_ÉRTÉK[Loop_INDEX] = informatikai_részleg_határ[Loop_INDEX] = szám[Loop_INDEX] = várj_ÉRTÉK[Loop_INDEX] = 0; return 0;
    }
}
