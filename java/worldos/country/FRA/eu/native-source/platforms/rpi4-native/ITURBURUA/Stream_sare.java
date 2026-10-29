// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** nukleo_balio 안의 연결형 byte_balio Stream_balio. Ethernet/TCP 패킷 스택이 아닌 루프백 socket maila_balio. */
public final class Stream_sare {
    static int[] Egoera_balio = new int[16], ataka_balio = new int[16], 짝 = new int[16], pareko_ataka = new int[16], itxaron_balio = new int[16], 묶임 = new int[16];
    static int[] aurrekoa_balio = new int[16], 수 = new int[16], datuak = new int[16 * 1024];
    static int Hurrengoa_elementu = 50000;
    static int egiaztatu(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Egoera_balio[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int ataka_zenbaki) { for (int Loop_INDIZE = 0; Loop_INDIZE < 16; Loop_INDIZE++) if (Egoera_balio[Loop_INDIZE] != 0 && 묶임[Loop_INDIZE] != 0 && ataka_balio[Loop_INDIZE] == ataka_zenbaki) return true; return false; }
    public static int sortu_sarrera() {
        for (int Loop_INDIZE = 0; Loop_INDIZE < 16; Loop_INDIZE++) if (Egoera_balio[Loop_INDIZE] == 0) { Egoera_balio[Loop_INDIZE] = 1; pareko_ataka[Loop_INDIZE] = ataka_balio[Loop_INDIZE] = aurrekoa_balio[Loop_INDIZE] = 수[Loop_INDIZE] = itxaron_balio[Loop_INDIZE] = 묶임[Loop_INDIZE] = 0; 짝[Loop_INDIZE] = -1; return Loop_INDIZE + 40; }
        return -24;
    }
    public static int lotu_amaiera_puntu(int 열린파일번호, int 통신주소, int ataka_zenbaki) {
        int Loop_INDIZE = egiaztatu(열린파일번호); if (Loop_INDIZE < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Egoera_balio[Loop_INDIZE] != 1 || ataka_zenbaki < 0 || ataka_zenbaki > 65535) return -22;
        if (ataka_zenbaki == 0) { do { ataka_zenbaki = Hurrengoa_elementu++; if (Hurrengoa_elementu > 65535) Hurrengoa_elementu = 50000; } while (사용중(ataka_zenbaki)); }
        if (사용중(ataka_zenbaki)) return -98; ataka_balio[Loop_INDIZE] = ataka_zenbaki; 묶임[Loop_INDIZE] = 1; Egoera_balio[Loop_INDIZE] = 2; return 0;
    }
    public static int entzun_amaiera_puntu(int 열린파일번호, int 연결대기한도) { int Loop_INDIZE = egiaztatu(열린파일번호); if (Loop_INDIZE < 0) return -9; if (Egoera_balio[Loop_INDIZE] != 2 || 연결대기한도 < 1) return -22; Egoera_balio[Loop_INDIZE] = 3; return 0; }
    public static int Konektatu(int 열린파일번호, int 통신주소, int ataka_zenbaki) {
        int Loop_INDIZE = egiaztatu(열린파일번호); if (Loop_INDIZE < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (ataka_zenbaki < 1 || ataka_zenbaki > 65535 || Egoera_balio[Loop_INDIZE] > 2) return -22;
        int 수신쪽 = -1; for (int barnekoa_kargu = 0; barnekoa_kargu < 16; barnekoa_kargu++) if (Egoera_balio[barnekoa_kargu] == 3 && ataka_balio[barnekoa_kargu] == ataka_zenbaki) 수신쪽 = barnekoa_kargu;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int barnekoa_kargu = 0; barnekoa_kargu < 16; barnekoa_kargu++) if (itxaron_balio[barnekoa_kargu] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Egoera_balio[Loop_INDIZE] == 1) { int 처리값 = lotu_amaiera_puntu(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = sortu_sarrera(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        Egoera_balio[Loop_INDIZE] = Egoera_balio[다른번호] = 4; 짝[Loop_INDIZE] = 다른번호; 짝[다른번호] = Loop_INDIZE; ataka_balio[다른번호] = ataka_zenbaki; pareko_ataka[Loop_INDIZE] = ataka_zenbaki; pareko_ataka[다른번호] = ataka_balio[Loop_INDIZE]; itxaron_balio[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int onartu_konexio(int 열린파일번호) { int Loop_INDIZE = egiaztatu(열린파일번호); if (Loop_INDIZE < 0) return -9; if (Egoera_balio[Loop_INDIZE] != 3) return -22; for (int barnekoa_kargu = 0; barnekoa_kargu < 16; barnekoa_kargu++) if (Egoera_balio[barnekoa_kargu] != 0 && itxaron_balio[barnekoa_kargu] == Loop_INDIZE + 1) { itxaron_balio[barnekoa_kargu] = 0; return barnekoa_kargu + 40; } return -11; }
    public static int Idatzi(int 열린파일번호, int sarrera_ZENBATU) {
        int Loop_INDIZE = egiaztatu(열린파일번호); if (Loop_INDIZE < 0) return -9; if (Egoera_balio[Loop_INDIZE] != 4) return -107;
        if (sarrera_ZENBATU < 0 || sarrera_ZENBATU > 512) return -22; if (sarrera_ZENBATU == 0) return 0;
        int barnekoa_kargu = 짝[Loop_INDIZE]; if (barnekoa_kargu < 0) return -32; int 총수 = 1024 - 수[barnekoa_kargu]; if (총수 == 0) return -11; if (총수 > sarrera_ZENBATU) 총수 = sarrera_ZENBATU;
        for (int Konparazioa_kargu = 0; Konparazioa_kargu < 총수; Konparazioa_kargu++) datuak[barnekoa_kargu * 1024 + (aurrekoa_balio[barnekoa_kargu] + 수[barnekoa_kargu] + Konparazioa_kargu) % 1024] = 되돌림망.Aurrera_balio[Konparazioa_kargu]; 수[barnekoa_kargu] += 총수; return 총수;
    }
    public static int Irakurri(int 열린파일번호, int sarrera_ZENBATU) {
        int Loop_INDIZE = egiaztatu(열린파일번호); if (Loop_INDIZE < 0) return -9; if (Egoera_balio[Loop_INDIZE] != 4) return -107; if (sarrera_ZENBATU < 0 || sarrera_ZENBATU > 512) return -22;
        if (sarrera_ZENBATU == 0) return 0; if (수[Loop_INDIZE] == 0) return 짝[Loop_INDIZE] < 0 ? 0 : -11; if (sarrera_ZENBATU > 수[Loop_INDIZE]) sarrera_ZENBATU = 수[Loop_INDIZE];
        for (int Konparazioa_kargu = 0; Konparazioa_kargu < sarrera_ZENBATU; Konparazioa_kargu++) 되돌림망.Aurrera_balio[Konparazioa_kargu] = datuak[Loop_INDIZE * 1024 + (aurrekoa_balio[Loop_INDIZE] + Konparazioa_kargu) % 1024]; aurrekoa_balio[Loop_INDIZE] = (aurrekoa_balio[Loop_INDIZE] + sarrera_ZENBATU) % 1024; 수[Loop_INDIZE] -= sarrera_ZENBATU; return sarrera_ZENBATU;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDIZE = egiaztatu(열린파일번호); return Loop_INDIZE < 0 ? -9 : ataka_balio[Loop_INDIZE]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDIZE = egiaztatu(열린파일번호); return Loop_INDIZE < 0 ? -9 : pareko_ataka[Loop_INDIZE]; }
    public static int Itxi(int 열린파일번호) {
        int Loop_INDIZE = egiaztatu(열린파일번호); if (Loop_INDIZE < 0) return -9;
        if (Egoera_balio[Loop_INDIZE] == 3) for (int barnekoa_kargu = 0; barnekoa_kargu < 16; barnekoa_kargu++) if (itxaron_balio[barnekoa_kargu] == Loop_INDIZE + 1) { if (짝[barnekoa_kargu] >= 0) 짝[짝[barnekoa_kargu]] = -1; Egoera_balio[barnekoa_kargu] = itxaron_balio[barnekoa_kargu] = 묶임[barnekoa_kargu] = 0; }
        if (짝[Loop_INDIZE] >= 0) 짝[짝[Loop_INDIZE]] = -1; Egoera_balio[Loop_INDIZE] = 묶임[Loop_INDIZE] = 수[Loop_INDIZE] = itxaron_balio[Loop_INDIZE] = 0; return 0;
    }
}
