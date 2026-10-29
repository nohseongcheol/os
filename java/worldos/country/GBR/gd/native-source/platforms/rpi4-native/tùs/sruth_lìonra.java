// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** eitean_VALUE 안의 연결형 baidht_VALUE sruth_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket breath_VALUE. */
public final class sruth_lìonra {
    static int[] cor_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], seise_port = new int[16], fuirich_VALUE = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], dàta = new int[16 * 1024];
    static int air_adhart_nì = 50000;
    static int dearbh(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && cor_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int lùb_INDEX = 0; lùb_INDEX < 16; lùb_INDEX++) if (cor_VALUE[lùb_INDEX] != 0 && 묶임[lùb_INDEX] != 0 && port_VALUE[lùb_INDEX] == 접속번호) return true; return false; }
    public static int Create_cur_a_steach() {
        for (int lùb_INDEX = 0; lùb_INDEX < 16; lùb_INDEX++) if (cor_VALUE[lùb_INDEX] == 0) { cor_VALUE[lùb_INDEX] = 1; seise_port[lùb_INDEX] = port_VALUE[lùb_INDEX] = 앞[lùb_INDEX] = 수[lùb_INDEX] = fuirich_VALUE[lùb_INDEX] = 묶임[lùb_INDEX] = 0; 짝[lùb_INDEX] = -1; return lùb_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int lùb_INDEX = dearbh(열린파일번호); if (lùb_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (cor_VALUE[lùb_INDEX] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = air_adhart_nì++; if (air_adhart_nì > 65535) air_adhart_nì = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; port_VALUE[lùb_INDEX] = 접속번호; 묶임[lùb_INDEX] = 1; cor_VALUE[lùb_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int lùb_INDEX = dearbh(열린파일번호); if (lùb_INDEX < 0) return -9; if (cor_VALUE[lùb_INDEX] != 2 || 연결대기한도 < 1) return -22; cor_VALUE[lùb_INDEX] = 3; return 0; }
    public static int CONNECT(int 열린파일번호, int 통신주소, int 접속번호) {
        int lùb_INDEX = dearbh(열린파일번호); if (lùb_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || cor_VALUE[lùb_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 16; Inner_Join_suidhich++) if (cor_VALUE[Inner_Join_suidhich] == 3 && port_VALUE[Inner_Join_suidhich] == 접속번호) 수신쪽 = Inner_Join_suidhich;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 16; Inner_Join_suidhich++) if (fuirich_VALUE[Inner_Join_suidhich] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (cor_VALUE[lùb_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Create_cur_a_steach(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        cor_VALUE[lùb_INDEX] = cor_VALUE[다른번호] = 4; 짝[lùb_INDEX] = 다른번호; 짝[다른번호] = lùb_INDEX; port_VALUE[다른번호] = 접속번호; seise_port[lùb_INDEX] = 접속번호; seise_port[다른번호] = port_VALUE[lùb_INDEX]; fuirich_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int gabh_ris_ceangal(int 열린파일번호) { int lùb_INDEX = dearbh(열린파일번호); if (lùb_INDEX < 0) return -9; if (cor_VALUE[lùb_INDEX] != 3) return -22; for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 16; Inner_Join_suidhich++) if (cor_VALUE[Inner_Join_suidhich] != 0 && fuirich_VALUE[Inner_Join_suidhich] == lùb_INDEX + 1) { fuirich_VALUE[Inner_Join_suidhich] = 0; return Inner_Join_suidhich + 40; } return -11; }
    public static int sgrìobh(int 열린파일번호, int cur_a_steach_COUNT) {
        int lùb_INDEX = dearbh(열린파일번호); if (lùb_INDEX < 0) return -9; if (cor_VALUE[lùb_INDEX] != 4) return -107;
        if (cur_a_steach_COUNT < 0 || cur_a_steach_COUNT > 512) return -22; if (cur_a_steach_COUNT == 0) return 0;
        int Inner_Join_suidhich = 짝[lùb_INDEX]; if (Inner_Join_suidhich < 0) return -32; int 총수 = 1024 - 수[Inner_Join_suidhich]; if (총수 == 0) return -11; if (총수 > cur_a_steach_COUNT) 총수 = cur_a_steach_COUNT;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) dàta[Inner_Join_suidhich * 1024 + (앞[Inner_Join_suidhich] + 수[Inner_Join_suidhich] + 비교자리) % 1024] = 되돌림망.sìn_air_adhart_VALUE_24592b8a[비교자리]; 수[Inner_Join_suidhich] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int cur_a_steach_COUNT) {
        int lùb_INDEX = dearbh(열린파일번호); if (lùb_INDEX < 0) return -9; if (cor_VALUE[lùb_INDEX] != 4) return -107; if (cur_a_steach_COUNT < 0 || cur_a_steach_COUNT > 512) return -22;
        if (cur_a_steach_COUNT == 0) return 0; if (수[lùb_INDEX] == 0) return 짝[lùb_INDEX] < 0 ? 0 : -11; if (cur_a_steach_COUNT > 수[lùb_INDEX]) cur_a_steach_COUNT = 수[lùb_INDEX];
        for (int 비교자리 = 0; 비교자리 < cur_a_steach_COUNT; 비교자리++) 되돌림망.sìn_air_adhart_VALUE_24592b8a[비교자리] = dàta[lùb_INDEX * 1024 + (앞[lùb_INDEX] + 비교자리) % 1024]; 앞[lùb_INDEX] = (앞[lùb_INDEX] + cur_a_steach_COUNT) % 1024; 수[lùb_INDEX] -= cur_a_steach_COUNT; return cur_a_steach_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int lùb_INDEX = dearbh(열린파일번호); return lùb_INDEX < 0 ? -9 : port_VALUE[lùb_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int lùb_INDEX = dearbh(열린파일번호); return lùb_INDEX < 0 ? -9 : seise_port[lùb_INDEX]; }
    public static int dùin(int 열린파일번호) {
        int lùb_INDEX = dearbh(열린파일번호); if (lùb_INDEX < 0) return -9;
        if (cor_VALUE[lùb_INDEX] == 3) for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 16; Inner_Join_suidhich++) if (fuirich_VALUE[Inner_Join_suidhich] == lùb_INDEX + 1) { if (짝[Inner_Join_suidhich] >= 0) 짝[짝[Inner_Join_suidhich]] = -1; cor_VALUE[Inner_Join_suidhich] = fuirich_VALUE[Inner_Join_suidhich] = 묶임[Inner_Join_suidhich] = 0; }
        if (짝[lùb_INDEX] >= 0) 짝[짝[lùb_INDEX]] = -1; cor_VALUE[lùb_INDEX] = 묶임[lùb_INDEX] = 수[lùb_INDEX] = fuirich_VALUE[lùb_INDEX] = 0; return 0;
    }
}
