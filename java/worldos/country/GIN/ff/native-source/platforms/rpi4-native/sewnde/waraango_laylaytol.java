// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** aaluude_njaru 안의 연결형 oktee_njaru waraango_njaru. Ethernet/TCP 패킷 스택이 아닌 루프백 socket tekkeendi_njaru. */
public final class waraango_laylaytol {
    static int[] ngonka_njaru = new int[16], poor_njaru = new int[16], 짝 = new int[16], giƴiraaɗo_poor = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], keɓe = new int[16 * 1024];
    static int 다음 = 50000;
    static int ƴeewtaade(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && ngonka_njaru[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int kowal_joopirdu = 0; kowal_joopirdu < 16; kowal_joopirdu++) if (ngonka_njaru[kowal_joopirdu] != 0 && 묶임[kowal_joopirdu] != 0 && poor_njaru[kowal_joopirdu] == 접속번호) return true; return false; }
    public static int 만들기() {
        for (int kowal_joopirdu = 0; kowal_joopirdu < 16; kowal_joopirdu++) if (ngonka_njaru[kowal_joopirdu] == 0) { ngonka_njaru[kowal_joopirdu] = 1; giƴiraaɗo_poor[kowal_joopirdu] = poor_njaru[kowal_joopirdu] = 앞[kowal_joopirdu] = 수[kowal_joopirdu] = 대기[kowal_joopirdu] = 묶임[kowal_joopirdu] = 0; 짝[kowal_joopirdu] = -1; return kowal_joopirdu + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int kowal_joopirdu = ƴeewtaade(열린파일번호); if (kowal_joopirdu < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (ngonka_njaru[kowal_joopirdu] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; poor_njaru[kowal_joopirdu] = 접속번호; 묶임[kowal_joopirdu] = 1; ngonka_njaru[kowal_joopirdu] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int kowal_joopirdu = ƴeewtaade(열린파일번호); if (kowal_joopirdu < 0) return -9; if (ngonka_njaru[kowal_joopirdu] != 2 || 연결대기한도 < 1) return -22; ngonka_njaru[kowal_joopirdu] = 3; return 0; }
    public static int seŋaade(int 열린파일번호, int 통신주소, int 접속번호) {
        int kowal_joopirdu = ƴeewtaade(열린파일번호); if (kowal_joopirdu < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || ngonka_njaru[kowal_joopirdu] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (ngonka_njaru[안쪽자리] == 3 && poor_njaru[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (ngonka_njaru[kowal_joopirdu] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = 만들기(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        ngonka_njaru[kowal_joopirdu] = ngonka_njaru[다른번호] = 4; 짝[kowal_joopirdu] = 다른번호; 짝[다른번호] = kowal_joopirdu; poor_njaru[다른번호] = 접속번호; giƴiraaɗo_poor[kowal_joopirdu] = 접속번호; giƴiraaɗo_poor[다른번호] = poor_njaru[kowal_joopirdu]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int 받음(int 열린파일번호) { int kowal_joopirdu = ƴeewtaade(열린파일번호); if (kowal_joopirdu < 0) return -9; if (ngonka_njaru[kowal_joopirdu] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (ngonka_njaru[안쪽자리] != 0 && 대기[안쪽자리] == kowal_joopirdu + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int winndude(int 열린파일번호, int 항목수) {
        int kowal_joopirdu = ƴeewtaade(열린파일번호); if (kowal_joopirdu < 0) return -9; if (ngonka_njaru[kowal_joopirdu] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[kowal_joopirdu]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) keɓe[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.yawtinde_njaru[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int 항목수) {
        int kowal_joopirdu = ƴeewtaade(열린파일번호); if (kowal_joopirdu < 0) return -9; if (ngonka_njaru[kowal_joopirdu] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[kowal_joopirdu] == 0) return 짝[kowal_joopirdu] < 0 ? 0 : -11; if (항목수 > 수[kowal_joopirdu]) 항목수 = 수[kowal_joopirdu];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.yawtinde_njaru[비교자리] = keɓe[kowal_joopirdu * 1024 + (앞[kowal_joopirdu] + 비교자리) % 1024]; 앞[kowal_joopirdu] = (앞[kowal_joopirdu] + 항목수) % 1024; 수[kowal_joopirdu] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int kowal_joopirdu = ƴeewtaade(열린파일번호); return kowal_joopirdu < 0 ? -9 : poor_njaru[kowal_joopirdu]; }
    public static int 상대창구읽기(int 열린파일번호) { int kowal_joopirdu = ƴeewtaade(열린파일번호); return kowal_joopirdu < 0 ? -9 : giƴiraaɗo_poor[kowal_joopirdu]; }
    public static int uddude(int 열린파일번호) {
        int kowal_joopirdu = ƴeewtaade(열린파일번호); if (kowal_joopirdu < 0) return -9;
        if (ngonka_njaru[kowal_joopirdu] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == kowal_joopirdu + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; ngonka_njaru[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[kowal_joopirdu] >= 0) 짝[짝[kowal_joopirdu]] = -1; ngonka_njaru[kowal_joopirdu] = 묶임[kowal_joopirdu] = 수[kowal_joopirdu] = 대기[kowal_joopirdu] = 0; return 0;
    }
}
