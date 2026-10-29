// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_VALUE 안의 연결형 byte_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket saff_VALUE. */
public final class Stream_netwerk {
    static int[] stat_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], peer_port = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int Li_Jmiss_element = 50000;
    static int vverifika(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && stat_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (stat_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == 접속번호) return true; return false; }
    public static int ħalaq_entrata() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (stat_VALUE[Loop_INDEX] == 0) { stat_VALUE[Loop_INDEX] = 1; peer_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = 앞[Loop_INDEX] = 수[Loop_INDEX] = 대기[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = vverifika(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (stat_VALUE[Loop_INDEX] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = Li_Jmiss_element++; if (Li_Jmiss_element > 65535) Li_Jmiss_element = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; port_VALUE[Loop_INDEX] = 접속번호; 묶임[Loop_INDEX] = 1; stat_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = vverifika(열린파일번호); if (Loop_INDEX < 0) return -9; if (stat_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; stat_VALUE[Loop_INDEX] = 3; return 0; }
    public static int AQBAD(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = vverifika(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || stat_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 16; inner_join_pożizzjoni++) if (stat_VALUE[inner_join_pożizzjoni] == 3 && port_VALUE[inner_join_pożizzjoni] == 접속번호) 수신쪽 = inner_join_pożizzjoni;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 16; inner_join_pożizzjoni++) if (대기[inner_join_pożizzjoni] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (stat_VALUE[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = ħalaq_entrata(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        stat_VALUE[Loop_INDEX] = stat_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALUE[다른번호] = 접속번호; peer_port[Loop_INDEX] = 접속번호; peer_port[다른번호] = port_VALUE[Loop_INDEX]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int aċċetta_konnessjoni(int 열린파일번호) { int Loop_INDEX = vverifika(열린파일번호); if (Loop_INDEX < 0) return -9; if (stat_VALUE[Loop_INDEX] != 3) return -22; for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 16; inner_join_pożizzjoni++) if (stat_VALUE[inner_join_pożizzjoni] != 0 && 대기[inner_join_pożizzjoni] == Loop_INDEX + 1) { 대기[inner_join_pożizzjoni] = 0; return inner_join_pożizzjoni + 40; } return -11; }
    public static int kiteb(int 열린파일번호, int entrata_COUNT) {
        int Loop_INDEX = vverifika(열린파일번호); if (Loop_INDEX < 0) return -9; if (stat_VALUE[Loop_INDEX] != 4) return -107;
        if (entrata_COUNT < 0 || entrata_COUNT > 512) return -22; if (entrata_COUNT == 0) return 0;
        int inner_join_pożizzjoni = 짝[Loop_INDEX]; if (inner_join_pożizzjoni < 0) return -32; int 총수 = 1024 - 수[inner_join_pożizzjoni]; if (총수 == 0) return -11; if (총수 > entrata_COUNT) 총수 = entrata_COUNT;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) data[inner_join_pożizzjoni * 1024 + (앞[inner_join_pożizzjoni] + 수[inner_join_pożizzjoni] + 비교자리) % 1024] = 되돌림망.għadda_VALUE_24592b8a[비교자리]; 수[inner_join_pożizzjoni] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int entrata_COUNT) {
        int Loop_INDEX = vverifika(열린파일번호); if (Loop_INDEX < 0) return -9; if (stat_VALUE[Loop_INDEX] != 4) return -107; if (entrata_COUNT < 0 || entrata_COUNT > 512) return -22;
        if (entrata_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (entrata_COUNT > 수[Loop_INDEX]) entrata_COUNT = 수[Loop_INDEX];
        for (int 비교자리 = 0; 비교자리 < entrata_COUNT; 비교자리++) 되돌림망.għadda_VALUE_24592b8a[비교자리] = data[Loop_INDEX * 1024 + (앞[Loop_INDEX] + 비교자리) % 1024]; 앞[Loop_INDEX] = (앞[Loop_INDEX] + entrata_COUNT) % 1024; 수[Loop_INDEX] -= entrata_COUNT; return entrata_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = vverifika(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = vverifika(열린파일번호); return Loop_INDEX < 0 ? -9 : peer_port[Loop_INDEX]; }
    public static int agħlaq(int 열린파일번호) {
        int Loop_INDEX = vverifika(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (stat_VALUE[Loop_INDEX] == 3) for (int inner_join_pożizzjoni = 0; inner_join_pożizzjoni < 16; inner_join_pożizzjoni++) if (대기[inner_join_pożizzjoni] == Loop_INDEX + 1) { if (짝[inner_join_pożizzjoni] >= 0) 짝[짝[inner_join_pożizzjoni]] = -1; stat_VALUE[inner_join_pożizzjoni] = 대기[inner_join_pożizzjoni] = 묶임[inner_join_pożizzjoni] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; stat_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = 대기[Loop_INDEX] = 0; return 0;
    }
}
