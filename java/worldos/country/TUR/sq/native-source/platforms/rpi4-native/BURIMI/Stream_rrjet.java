// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** bërthamë_VALUE 안의 연결형 bajt_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket Shtresë_VALUE. */
public final class Stream_rrjet {
    static int[] status_VALUE = new int[16], portë_VALUE = new int[16], 짝 = new int[16], homolog_portë = new int[16], Prit_VALUE = new int[16], 묶임 = new int[16];
    static int[] e_përparme_VALUE = new int[16], 수 = new int[16], të_dhëna = new int[16 * 1024];
    static int Tjetër_njësi = 50000;
    static int verifikoj(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && status_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int numri_i_portës) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (status_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && portë_VALUE[Loop_INDEX] == numri_i_portës) return true; return false; }
    public static int Krijo_futje() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (status_VALUE[Loop_INDEX] == 0) { status_VALUE[Loop_INDEX] = 1; homolog_portë[Loop_INDEX] = portë_VALUE[Loop_INDEX] = e_përparme_VALUE[Loop_INDEX] = 수[Loop_INDEX] = Prit_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int numri_i_portës) {
        int Loop_INDEX = verifikoj(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (status_VALUE[Loop_INDEX] != 1 || numri_i_portës < 0 || numri_i_portës > 65535) return -22;
        if (numri_i_portës == 0) { do { numri_i_portës = Tjetër_njësi++; if (Tjetër_njësi > 65535) Tjetër_njësi = 50000; } while (사용중(numri_i_portës)); }
        if (사용중(numri_i_portës)) return -98; portë_VALUE[Loop_INDEX] = numri_i_portës; 묶임[Loop_INDEX] = 1; status_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = verifikoj(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; status_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Lidhu(int 열린파일번호, int 통신주소, int numri_i_portës) {
        int Loop_INDEX = verifikoj(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (numri_i_portës < 1 || numri_i_portës > 65535 || status_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 16; bashkim_i_brendshëm_pozicioni++) if (status_VALUE[bashkim_i_brendshëm_pozicioni] == 3 && portë_VALUE[bashkim_i_brendshëm_pozicioni] == numri_i_portës) 수신쪽 = bashkim_i_brendshëm_pozicioni;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 16; bashkim_i_brendshëm_pozicioni++) if (Prit_VALUE[bashkim_i_brendshëm_pozicioni] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (status_VALUE[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Krijo_futje(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        status_VALUE[Loop_INDEX] = status_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; portë_VALUE[다른번호] = numri_i_portës; homolog_portë[Loop_INDEX] = numri_i_portës; homolog_portë[다른번호] = portë_VALUE[Loop_INDEX]; Prit_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int prano_lidhje(int 열린파일번호) { int Loop_INDEX = verifikoj(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 3) return -22; for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 16; bashkim_i_brendshëm_pozicioni++) if (status_VALUE[bashkim_i_brendshëm_pozicioni] != 0 && Prit_VALUE[bashkim_i_brendshëm_pozicioni] == Loop_INDEX + 1) { Prit_VALUE[bashkim_i_brendshëm_pozicioni] = 0; return bashkim_i_brendshëm_pozicioni + 40; } return -11; }
    public static int Shkrimi(int 열린파일번호, int futje_COUNT) {
        int Loop_INDEX = verifikoj(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 4) return -107;
        if (futje_COUNT < 0 || futje_COUNT > 512) return -22; if (futje_COUNT == 0) return 0;
        int bashkim_i_brendshëm_pozicioni = 짝[Loop_INDEX]; if (bashkim_i_brendshëm_pozicioni < 0) return -32; int 총수 = 1024 - 수[bashkim_i_brendshëm_pozicioni]; if (총수 == 0) return -11; if (총수 > futje_COUNT) 총수 = futje_COUNT;
        for (int Krahasim_pozicioni = 0; Krahasim_pozicioni < 총수; Krahasim_pozicioni++) të_dhëna[bashkim_i_brendshëm_pozicioni * 1024 + (e_përparme_VALUE[bashkim_i_brendshëm_pozicioni] + 수[bashkim_i_brendshëm_pozicioni] + Krahasim_pozicioni) % 1024] = 되돌림망.paso_VALUE[Krahasim_pozicioni]; 수[bashkim_i_brendshëm_pozicioni] += 총수; return 총수;
    }
    public static int Leximi(int 열린파일번호, int futje_COUNT) {
        int Loop_INDEX = verifikoj(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 4) return -107; if (futje_COUNT < 0 || futje_COUNT > 512) return -22;
        if (futje_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (futje_COUNT > 수[Loop_INDEX]) futje_COUNT = 수[Loop_INDEX];
        for (int Krahasim_pozicioni = 0; Krahasim_pozicioni < futje_COUNT; Krahasim_pozicioni++) 되돌림망.paso_VALUE[Krahasim_pozicioni] = të_dhëna[Loop_INDEX * 1024 + (e_përparme_VALUE[Loop_INDEX] + Krahasim_pozicioni) % 1024]; e_përparme_VALUE[Loop_INDEX] = (e_përparme_VALUE[Loop_INDEX] + futje_COUNT) % 1024; 수[Loop_INDEX] -= futje_COUNT; return futje_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = verifikoj(열린파일번호); return Loop_INDEX < 0 ? -9 : portë_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = verifikoj(열린파일번호); return Loop_INDEX < 0 ? -9 : homolog_portë[Loop_INDEX]; }
    public static int Mbyll(int 열린파일번호) {
        int Loop_INDEX = verifikoj(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (status_VALUE[Loop_INDEX] == 3) for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 16; bashkim_i_brendshëm_pozicioni++) if (Prit_VALUE[bashkim_i_brendshëm_pozicioni] == Loop_INDEX + 1) { if (짝[bashkim_i_brendshëm_pozicioni] >= 0) 짝[짝[bashkim_i_brendshëm_pozicioni]] = -1; status_VALUE[bashkim_i_brendshëm_pozicioni] = Prit_VALUE[bashkim_i_brendshëm_pozicioni] = 묶임[bashkim_i_brendshëm_pozicioni] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; status_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = Prit_VALUE[Loop_INDEX] = 0; return 0;
    }
}
