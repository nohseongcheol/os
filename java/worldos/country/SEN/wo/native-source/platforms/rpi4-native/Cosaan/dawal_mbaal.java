// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** xoox_xëyma 안의 연결형 okte_xëyma dawal_xëyma. Ethernet/TCP 패킷 스택이 아닌 루프백 socket déggoob_wet_xëyma. */
public final class dawal_mbaal {
    static int[] nekkin_xëyma = new int[16], jël_xëyma = new int[16], 짝 = new int[16], Nàttangoo_jël = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], mbir = new int[16 * 1024];
    static int 다음 = 50000;
    static int luñutu(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && nekkin_xëyma[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) if (nekkin_xëyma[wërngël_àlluwa_tur] != 0 && 묶임[wërngël_àlluwa_tur] != 0 && jël_xëyma[wërngël_àlluwa_tur] == 접속번호) return true; return false; }
    public static int sos_dugal_xabaar() {
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) if (nekkin_xëyma[wërngël_àlluwa_tur] == 0) { nekkin_xëyma[wërngël_àlluwa_tur] = 1; Nàttangoo_jël[wërngël_àlluwa_tur] = jël_xëyma[wërngël_àlluwa_tur] = 앞[wërngël_àlluwa_tur] = 수[wërngël_àlluwa_tur] = 대기[wërngël_àlluwa_tur] = 묶임[wërngël_àlluwa_tur] = 0; 짝[wërngël_àlluwa_tur] = -1; return wërngël_àlluwa_tur + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int wërngël_àlluwa_tur = luñutu(열린파일번호); if (wërngël_àlluwa_tur < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (nekkin_xëyma[wërngël_àlluwa_tur] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; jël_xëyma[wërngël_àlluwa_tur] = 접속번호; 묶임[wërngël_àlluwa_tur] = 1; nekkin_xëyma[wërngël_àlluwa_tur] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int wërngël_àlluwa_tur = luñutu(열린파일번호); if (wërngël_àlluwa_tur < 0) return -9; if (nekkin_xëyma[wërngël_àlluwa_tur] != 2 || 연결대기한도 < 1) return -22; nekkin_xëyma[wërngël_àlluwa_tur] = 3; return 0; }
    public static int JOKKOO(int 열린파일번호, int 통신주소, int 접속번호) {
        int wërngël_àlluwa_tur = luñutu(열린파일번호); if (wërngël_àlluwa_tur < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || nekkin_xëyma[wërngël_àlluwa_tur] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (nekkin_xëyma[안쪽자리] == 3 && jël_xëyma[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (nekkin_xëyma[wërngël_àlluwa_tur] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = sos_dugal_xabaar(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        nekkin_xëyma[wërngël_àlluwa_tur] = nekkin_xëyma[다른번호] = 4; 짝[wërngël_àlluwa_tur] = 다른번호; 짝[다른번호] = wërngël_àlluwa_tur; jël_xëyma[다른번호] = 접속번호; Nàttangoo_jël[wërngël_àlluwa_tur] = 접속번호; Nàttangoo_jël[다른번호] = jël_xëyma[wërngël_àlluwa_tur]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int nangu_jokkalóo(int 열린파일번호) { int wërngël_àlluwa_tur = luñutu(열린파일번호); if (wërngël_àlluwa_tur < 0) return -9; if (nekkin_xëyma[wërngël_àlluwa_tur] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (nekkin_xëyma[안쪽자리] != 0 && 대기[안쪽자리] == wërngël_àlluwa_tur + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int biir(int 열린파일번호, int 항목수) {
        int wërngël_àlluwa_tur = luñutu(열린파일번호); if (wërngël_àlluwa_tur < 0) return -9; if (nekkin_xëyma[wërngël_àlluwa_tur] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[wërngël_àlluwa_tur]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) mbir[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.jëmal_kanam_xëyma[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int 항목수) {
        int wërngël_àlluwa_tur = luñutu(열린파일번호); if (wërngël_àlluwa_tur < 0) return -9; if (nekkin_xëyma[wërngël_àlluwa_tur] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[wërngël_àlluwa_tur] == 0) return 짝[wërngël_àlluwa_tur] < 0 ? 0 : -11; if (항목수 > 수[wërngël_àlluwa_tur]) 항목수 = 수[wërngël_àlluwa_tur];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.jëmal_kanam_xëyma[비교자리] = mbir[wërngël_àlluwa_tur * 1024 + (앞[wërngël_àlluwa_tur] + 비교자리) % 1024]; 앞[wërngël_àlluwa_tur] = (앞[wërngël_àlluwa_tur] + 항목수) % 1024; 수[wërngël_àlluwa_tur] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int wërngël_àlluwa_tur = luñutu(열린파일번호); return wërngël_àlluwa_tur < 0 ? -9 : jël_xëyma[wërngël_àlluwa_tur]; }
    public static int 상대창구읽기(int 열린파일번호) { int wërngël_àlluwa_tur = luñutu(열린파일번호); return wërngël_àlluwa_tur < 0 ? -9 : Nàttangoo_jël[wërngël_àlluwa_tur]; }
    public static int Tej(int 열린파일번호) {
        int wërngël_àlluwa_tur = luñutu(열린파일번호); if (wërngël_àlluwa_tur < 0) return -9;
        if (nekkin_xëyma[wërngël_àlluwa_tur] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == wërngël_àlluwa_tur + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; nekkin_xëyma[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[wërngël_àlluwa_tur] >= 0) 짝[짝[wërngël_àlluwa_tur]] = -1; nekkin_xëyma[wërngël_àlluwa_tur] = 묶임[wërngël_àlluwa_tur] = 수[wërngël_àlluwa_tur] = 대기[wërngël_àlluwa_tur] = 0; return 0;
    }
}
