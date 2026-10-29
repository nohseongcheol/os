// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** nüvə_VALUE 안의 연결형 bayt_VALUE axın_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket lay_VALUE. */
public final class axın_Şəbəkə {
    static int[] vəziyyət_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], eynisəviyyəli_port = new int[16], gözlə_VALUE = new int[16], 묶임 = new int[16];
    static int[] ön_VALUE = new int[16], 수 = new int[16], verilənlər = new int[16 * 1024];
    static int Sonrakı_element = 50000;
    static int yoxlamaq(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && vəziyyət_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (vəziyyət_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == 접속번호) return true; return false; }
    public static int yarat_daxiletmə() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (vəziyyət_VALUE[Loop_INDEX] == 0) { vəziyyət_VALUE[Loop_INDEX] = 1; eynisəviyyəli_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = ön_VALUE[Loop_INDEX] = 수[Loop_INDEX] = gözlə_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = yoxlamaq(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (vəziyyət_VALUE[Loop_INDEX] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = Sonrakı_element++; if (Sonrakı_element > 65535) Sonrakı_element = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; port_VALUE[Loop_INDEX] = 접속번호; 묶임[Loop_INDEX] = 1; vəziyyət_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = yoxlamaq(열린파일번호); if (Loop_INDEX < 0) return -9; if (vəziyyət_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; vəziyyət_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Bağlan(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = yoxlamaq(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || vəziyyət_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 16; daxili_qoşulma_yerinə_qoymaq++) if (vəziyyət_VALUE[daxili_qoşulma_yerinə_qoymaq] == 3 && port_VALUE[daxili_qoşulma_yerinə_qoymaq] == 접속번호) 수신쪽 = daxili_qoşulma_yerinə_qoymaq;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 16; daxili_qoşulma_yerinə_qoymaq++) if (gözlə_VALUE[daxili_qoşulma_yerinə_qoymaq] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (vəziyyət_VALUE[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = yarat_daxiletmə(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        vəziyyət_VALUE[Loop_INDEX] = vəziyyət_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALUE[다른번호] = 접속번호; eynisəviyyəli_port[Loop_INDEX] = 접속번호; eynisəviyyəli_port[다른번호] = port_VALUE[Loop_INDEX]; gözlə_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int qəbul_et_qoşulma(int 열린파일번호) { int Loop_INDEX = yoxlamaq(열린파일번호); if (Loop_INDEX < 0) return -9; if (vəziyyət_VALUE[Loop_INDEX] != 3) return -22; for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 16; daxili_qoşulma_yerinə_qoymaq++) if (vəziyyət_VALUE[daxili_qoşulma_yerinə_qoymaq] != 0 && gözlə_VALUE[daxili_qoşulma_yerinə_qoymaq] == Loop_INDEX + 1) { gözlə_VALUE[daxili_qoşulma_yerinə_qoymaq] = 0; return daxili_qoşulma_yerinə_qoymaq + 40; } return -11; }
    public static int Yazma(int 열린파일번호, int daxiletmə_COUNT) {
        int Loop_INDEX = yoxlamaq(열린파일번호); if (Loop_INDEX < 0) return -9; if (vəziyyət_VALUE[Loop_INDEX] != 4) return -107;
        if (daxiletmə_COUNT < 0 || daxiletmə_COUNT > 512) return -22; if (daxiletmə_COUNT == 0) return 0;
        int daxili_qoşulma_yerinə_qoymaq = 짝[Loop_INDEX]; if (daxili_qoşulma_yerinə_qoymaq < 0) return -32; int 총수 = 1024 - 수[daxili_qoşulma_yerinə_qoymaq]; if (총수 == 0) return -11; if (총수 > daxiletmə_COUNT) 총수 = daxiletmə_COUNT;
        for (int Müqayisə_yerinə_qoymaq = 0; Müqayisə_yerinə_qoymaq < 총수; Müqayisə_yerinə_qoymaq++) verilənlər[daxili_qoşulma_yerinə_qoymaq * 1024 + (ön_VALUE[daxili_qoşulma_yerinə_qoymaq] + 수[daxili_qoşulma_yerinə_qoymaq] + Müqayisə_yerinə_qoymaq) % 1024] = 되돌림망.irəli_VALUE[Müqayisə_yerinə_qoymaq]; 수[daxili_qoşulma_yerinə_qoymaq] += 총수; return 총수;
    }
    public static int Oxuma(int 열린파일번호, int daxiletmə_COUNT) {
        int Loop_INDEX = yoxlamaq(열린파일번호); if (Loop_INDEX < 0) return -9; if (vəziyyət_VALUE[Loop_INDEX] != 4) return -107; if (daxiletmə_COUNT < 0 || daxiletmə_COUNT > 512) return -22;
        if (daxiletmə_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (daxiletmə_COUNT > 수[Loop_INDEX]) daxiletmə_COUNT = 수[Loop_INDEX];
        for (int Müqayisə_yerinə_qoymaq = 0; Müqayisə_yerinə_qoymaq < daxiletmə_COUNT; Müqayisə_yerinə_qoymaq++) 되돌림망.irəli_VALUE[Müqayisə_yerinə_qoymaq] = verilənlər[Loop_INDEX * 1024 + (ön_VALUE[Loop_INDEX] + Müqayisə_yerinə_qoymaq) % 1024]; ön_VALUE[Loop_INDEX] = (ön_VALUE[Loop_INDEX] + daxiletmə_COUNT) % 1024; 수[Loop_INDEX] -= daxiletmə_COUNT; return daxiletmə_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = yoxlamaq(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = yoxlamaq(열린파일번호); return Loop_INDEX < 0 ? -9 : eynisəviyyəli_port[Loop_INDEX]; }
    public static int Bağla(int 열린파일번호) {
        int Loop_INDEX = yoxlamaq(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (vəziyyət_VALUE[Loop_INDEX] == 3) for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 16; daxili_qoşulma_yerinə_qoymaq++) if (gözlə_VALUE[daxili_qoşulma_yerinə_qoymaq] == Loop_INDEX + 1) { if (짝[daxili_qoşulma_yerinə_qoymaq] >= 0) 짝[짝[daxili_qoşulma_yerinə_qoymaq]] = -1; vəziyyət_VALUE[daxili_qoşulma_yerinə_qoymaq] = gözlə_VALUE[daxili_qoşulma_yerinə_qoymaq] = 묶임[daxili_qoşulma_yerinə_qoymaq] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; vəziyyət_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = gözlə_VALUE[Loop_INDEX] = 0; return 0;
    }
}
