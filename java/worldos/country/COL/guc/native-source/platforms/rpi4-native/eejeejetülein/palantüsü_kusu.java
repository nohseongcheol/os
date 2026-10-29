// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** keetnerü_ajutuu 안의 연결형 waai_ajutuu palantüsü_ajutuu. Ethernet/TCP 패킷 스택이 아닌 루프백 socket ayaleriaa_ajutuu. */
public final class palantüsü_kusu {
    static int[] jamakua_iparülein_ajutuu = new int[16], outtülee_ajutuu = new int[16], 짝 = new int[16], wanaawasü_outtülee = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], atijaaya = new int[16 * 1024];
    static int 다음 = 50000;
    static int 확인(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && jamakua_iparülein_ajutuu[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] != 0 && 묶임[eitawaakualü_ee_iyatialujuna] != 0 && outtülee_ajutuu[eitawaakualü_ee_iyatialujuna] == 접속번호) return true; return false; }
    public static int 만들기() {
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] == 0) { jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] = 1; wanaawasü_outtülee[eitawaakualü_ee_iyatialujuna] = outtülee_ajutuu[eitawaakualü_ee_iyatialujuna] = 앞[eitawaakualü_ee_iyatialujuna] = 수[eitawaakualü_ee_iyatialujuna] = 대기[eitawaakualü_ee_iyatialujuna] = 묶임[eitawaakualü_ee_iyatialujuna] = 0; 짝[eitawaakualü_ee_iyatialujuna] = -1; return eitawaakualü_ee_iyatialujuna + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); if (eitawaakualü_ee_iyatialujuna < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; outtülee_ajutuu[eitawaakualü_ee_iyatialujuna] = 접속번호; 묶임[eitawaakualü_ee_iyatialujuna] = 1; jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); if (eitawaakualü_ee_iyatialujuna < 0) return -9; if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] != 2 || 연결대기한도 < 1) return -22; jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] = 3; return 0; }
    public static int a_ataa(int 열린파일번호, int 통신주소, int 접속번호) {
        int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); if (eitawaakualü_ee_iyatialujuna < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (jamakua_iparülein_ajutuu[안쪽자리] == 3 && outtülee_ajutuu[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = 만들기(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] = jamakua_iparülein_ajutuu[다른번호] = 4; 짝[eitawaakualü_ee_iyatialujuna] = 다른번호; 짝[다른번호] = eitawaakualü_ee_iyatialujuna; outtülee_ajutuu[다른번호] = 접속번호; wanaawasü_outtülee[eitawaakualü_ee_iyatialujuna] = 접속번호; wanaawasü_outtülee[다른번호] = outtülee_ajutuu[eitawaakualü_ee_iyatialujuna]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int 받음(int 열린파일번호) { int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); if (eitawaakualü_ee_iyatialujuna < 0) return -9; if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (jamakua_iparülein_ajutuu[안쪽자리] != 0 && 대기[안쪽자리] == eitawaakualü_ee_iyatialujuna + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int ashajaa(int 열린파일번호, int 항목수) {
        int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); if (eitawaakualü_ee_iyatialujuna < 0) return -9; if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[eitawaakualü_ee_iyatialujuna]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) atijaaya[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.전달[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int 항목수) {
        int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); if (eitawaakualü_ee_iyatialujuna < 0) return -9; if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[eitawaakualü_ee_iyatialujuna] == 0) return 짝[eitawaakualü_ee_iyatialujuna] < 0 ? 0 : -11; if (항목수 > 수[eitawaakualü_ee_iyatialujuna]) 항목수 = 수[eitawaakualü_ee_iyatialujuna];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.전달[비교자리] = atijaaya[eitawaakualü_ee_iyatialujuna * 1024 + (앞[eitawaakualü_ee_iyatialujuna] + 비교자리) % 1024]; 앞[eitawaakualü_ee_iyatialujuna] = (앞[eitawaakualü_ee_iyatialujuna] + 항목수) % 1024; 수[eitawaakualü_ee_iyatialujuna] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); return eitawaakualü_ee_iyatialujuna < 0 ? -9 : outtülee_ajutuu[eitawaakualü_ee_iyatialujuna]; }
    public static int 상대창구읽기(int 열린파일번호) { int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); return eitawaakualü_ee_iyatialujuna < 0 ? -9 : wanaawasü_outtülee[eitawaakualü_ee_iyatialujuna]; }
    public static int asürülaa(int 열린파일번호) {
        int eitawaakualü_ee_iyatialujuna = 확인(열린파일번호); if (eitawaakualü_ee_iyatialujuna < 0) return -9;
        if (jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == eitawaakualü_ee_iyatialujuna + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; jamakua_iparülein_ajutuu[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[eitawaakualü_ee_iyatialujuna] >= 0) 짝[짝[eitawaakualü_ee_iyatialujuna]] = -1; jamakua_iparülein_ajutuu[eitawaakualü_ee_iyatialujuna] = 묶임[eitawaakualü_ee_iyatialujuna] = 수[eitawaakualü_ee_iyatialujuna] = 대기[eitawaakualü_ee_iyatialujuna] = 0; return 0;
    }
}
