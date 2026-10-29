// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ikhenela_inani 안의 연결형 ibhayithi_inani Stream_inani. Ethernet/TCP 패킷 스택이 아닌 루프백 socket ugqinsi_inani. */
public final class Stream_iNethiwekhi {
    static int[] isimo_inani = new int[16], intuba_inani = new int[16], 짝 = new int[16], untanga_intuba = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], imininingwane = new int[16 * 1024];
    static int 다음 = 50000;
    static int qiniseka(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && isimo_inani[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) if (isimo_inani[iluphu_thola_inkomba] != 0 && 묶임[iluphu_thola_inkomba] != 0 && intuba_inani[iluphu_thola_inkomba] == 접속번호) return true; return false; }
    public static int yakha_okufakwayo() {
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) if (isimo_inani[iluphu_thola_inkomba] == 0) { isimo_inani[iluphu_thola_inkomba] = 1; untanga_intuba[iluphu_thola_inkomba] = intuba_inani[iluphu_thola_inkomba] = 앞[iluphu_thola_inkomba] = 수[iluphu_thola_inkomba] = 대기[iluphu_thola_inkomba] = 묶임[iluphu_thola_inkomba] = 0; 짝[iluphu_thola_inkomba] = -1; return iluphu_thola_inkomba + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int iluphu_thola_inkomba = qiniseka(열린파일번호); if (iluphu_thola_inkomba < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (isimo_inani[iluphu_thola_inkomba] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; intuba_inani[iluphu_thola_inkomba] = 접속번호; 묶임[iluphu_thola_inkomba] = 1; isimo_inani[iluphu_thola_inkomba] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int iluphu_thola_inkomba = qiniseka(열린파일번호); if (iluphu_thola_inkomba < 0) return -9; if (isimo_inani[iluphu_thola_inkomba] != 2 || 연결대기한도 < 1) return -22; isimo_inani[iluphu_thola_inkomba] = 3; return 0; }
    public static int Xhumanisa(int 열린파일번호, int 통신주소, int 접속번호) {
        int iluphu_thola_inkomba = qiniseka(열린파일번호); if (iluphu_thola_inkomba < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || isimo_inani[iluphu_thola_inkomba] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (isimo_inani[안쪽자리] == 3 && intuba_inani[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (isimo_inani[iluphu_thola_inkomba] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = yakha_okufakwayo(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        isimo_inani[iluphu_thola_inkomba] = isimo_inani[다른번호] = 4; 짝[iluphu_thola_inkomba] = 다른번호; 짝[다른번호] = iluphu_thola_inkomba; intuba_inani[다른번호] = 접속번호; untanga_intuba[iluphu_thola_inkomba] = 접속번호; untanga_intuba[다른번호] = intuba_inani[iluphu_thola_inkomba]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int yamukela_uxhumano(int 열린파일번호) { int iluphu_thola_inkomba = qiniseka(열린파일번호); if (iluphu_thola_inkomba < 0) return -9; if (isimo_inani[iluphu_thola_inkomba] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (isimo_inani[안쪽자리] != 0 && 대기[안쪽자리] == iluphu_thola_inkomba + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int Bhala(int 열린파일번호, int 항목수) {
        int iluphu_thola_inkomba = qiniseka(열린파일번호); if (iluphu_thola_inkomba < 0) return -9; if (isimo_inani[iluphu_thola_inkomba] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[iluphu_thola_inkomba]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) imininingwane[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.dlulisela_phambili_inani[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int Funda(int 열린파일번호, int 항목수) {
        int iluphu_thola_inkomba = qiniseka(열린파일번호); if (iluphu_thola_inkomba < 0) return -9; if (isimo_inani[iluphu_thola_inkomba] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[iluphu_thola_inkomba] == 0) return 짝[iluphu_thola_inkomba] < 0 ? 0 : -11; if (항목수 > 수[iluphu_thola_inkomba]) 항목수 = 수[iluphu_thola_inkomba];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.dlulisela_phambili_inani[비교자리] = imininingwane[iluphu_thola_inkomba * 1024 + (앞[iluphu_thola_inkomba] + 비교자리) % 1024]; 앞[iluphu_thola_inkomba] = (앞[iluphu_thola_inkomba] + 항목수) % 1024; 수[iluphu_thola_inkomba] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int iluphu_thola_inkomba = qiniseka(열린파일번호); return iluphu_thola_inkomba < 0 ? -9 : intuba_inani[iluphu_thola_inkomba]; }
    public static int 상대창구읽기(int 열린파일번호) { int iluphu_thola_inkomba = qiniseka(열린파일번호); return iluphu_thola_inkomba < 0 ? -9 : untanga_intuba[iluphu_thola_inkomba]; }
    public static int Vala(int 열린파일번호) {
        int iluphu_thola_inkomba = qiniseka(열린파일번호); if (iluphu_thola_inkomba < 0) return -9;
        if (isimo_inani[iluphu_thola_inkomba] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == iluphu_thola_inkomba + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; isimo_inani[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[iluphu_thola_inkomba] >= 0) 짝[짝[iluphu_thola_inkomba]] = -1; isimo_inani[iluphu_thola_inkomba] = 묶임[iluphu_thola_inkomba] = 수[iluphu_thola_inkomba] = 대기[iluphu_thola_inkomba] = 0; return 0;
    }
}
