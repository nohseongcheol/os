// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kiini_thamani_0611a8a8 안의 연결형 baiti_thamani Stream_thamani. Ethernet/TCP 패킷 스택이 아닌 루프백 socket tabaka_thamani. */
public final class Stream_Mtandao {
    static int[] hali_thamani = new int[16], kituo_thamani = new int[16], 짝 = new int[16], kompyuta_rika_kituo = new int[16], subiri_thamani = new int[16], 묶임 = new int[16];
    static int[] mbele_thamani = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int 다음 = 50000;
    static int thibitisha(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && hali_thamani[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int namba_ya_kituo) { for (int kitanzi_kielezo = 0; kitanzi_kielezo < 16; kitanzi_kielezo++) if (hali_thamani[kitanzi_kielezo] != 0 && 묶임[kitanzi_kielezo] != 0 && kituo_thamani[kitanzi_kielezo] == namba_ya_kituo) return true; return false; }
    public static int unda_ingizo() {
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 16; kitanzi_kielezo++) if (hali_thamani[kitanzi_kielezo] == 0) { hali_thamani[kitanzi_kielezo] = 1; kompyuta_rika_kituo[kitanzi_kielezo] = kituo_thamani[kitanzi_kielezo] = mbele_thamani[kitanzi_kielezo] = 수[kitanzi_kielezo] = subiri_thamani[kitanzi_kielezo] = 묶임[kitanzi_kielezo] = 0; 짝[kitanzi_kielezo] = -1; return kitanzi_kielezo + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int namba_ya_kituo) {
        int kitanzi_kielezo = thibitisha(열린파일번호); if (kitanzi_kielezo < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (hali_thamani[kitanzi_kielezo] != 1 || namba_ya_kituo < 0 || namba_ya_kituo > 65535) return -22;
        if (namba_ya_kituo == 0) { do { namba_ya_kituo = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(namba_ya_kituo)); }
        if (사용중(namba_ya_kituo)) return -98; kituo_thamani[kitanzi_kielezo] = namba_ya_kituo; 묶임[kitanzi_kielezo] = 1; hali_thamani[kitanzi_kielezo] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int kitanzi_kielezo = thibitisha(열린파일번호); if (kitanzi_kielezo < 0) return -9; if (hali_thamani[kitanzi_kielezo] != 2 || 연결대기한도 < 1) return -22; hali_thamani[kitanzi_kielezo] = 3; return 0; }
    public static int UNGANISHA(int 열린파일번호, int 통신주소, int namba_ya_kituo) {
        int kitanzi_kielezo = thibitisha(열린파일번호); if (kitanzi_kielezo < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (namba_ya_kituo < 1 || namba_ya_kituo > 65535 || hali_thamani[kitanzi_kielezo] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (hali_thamani[안쪽자리] == 3 && kituo_thamani[안쪽자리] == namba_ya_kituo) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (subiri_thamani[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (hali_thamani[kitanzi_kielezo] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = unda_ingizo(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        hali_thamani[kitanzi_kielezo] = hali_thamani[다른번호] = 4; 짝[kitanzi_kielezo] = 다른번호; 짝[다른번호] = kitanzi_kielezo; kituo_thamani[다른번호] = namba_ya_kituo; kompyuta_rika_kituo[kitanzi_kielezo] = namba_ya_kituo; kompyuta_rika_kituo[다른번호] = kituo_thamani[kitanzi_kielezo]; subiri_thamani[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int kubali_muunganisho(int 열린파일번호) { int kitanzi_kielezo = thibitisha(열린파일번호); if (kitanzi_kielezo < 0) return -9; if (hali_thamani[kitanzi_kielezo] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (hali_thamani[안쪽자리] != 0 && subiri_thamani[안쪽자리] == kitanzi_kielezo + 1) { subiri_thamani[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int andika(int 열린파일번호, int 항목수) {
        int kitanzi_kielezo = thibitisha(열린파일번호); if (kitanzi_kielezo < 0) return -9; if (hali_thamani[kitanzi_kielezo] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[kitanzi_kielezo]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) data[안쪽자리 * 1024 + (mbele_thamani[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.tuma_mbele_thamani[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int 항목수) {
        int kitanzi_kielezo = thibitisha(열린파일번호); if (kitanzi_kielezo < 0) return -9; if (hali_thamani[kitanzi_kielezo] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[kitanzi_kielezo] == 0) return 짝[kitanzi_kielezo] < 0 ? 0 : -11; if (항목수 > 수[kitanzi_kielezo]) 항목수 = 수[kitanzi_kielezo];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.tuma_mbele_thamani[비교자리] = data[kitanzi_kielezo * 1024 + (mbele_thamani[kitanzi_kielezo] + 비교자리) % 1024]; mbele_thamani[kitanzi_kielezo] = (mbele_thamani[kitanzi_kielezo] + 항목수) % 1024; 수[kitanzi_kielezo] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int kitanzi_kielezo = thibitisha(열린파일번호); return kitanzi_kielezo < 0 ? -9 : kituo_thamani[kitanzi_kielezo]; }
    public static int 상대창구읽기(int 열린파일번호) { int kitanzi_kielezo = thibitisha(열린파일번호); return kitanzi_kielezo < 0 ? -9 : kompyuta_rika_kituo[kitanzi_kielezo]; }
    public static int funga(int 열린파일번호) {
        int kitanzi_kielezo = thibitisha(열린파일번호); if (kitanzi_kielezo < 0) return -9;
        if (hali_thamani[kitanzi_kielezo] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (subiri_thamani[안쪽자리] == kitanzi_kielezo + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; hali_thamani[안쪽자리] = subiri_thamani[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[kitanzi_kielezo] >= 0) 짝[짝[kitanzi_kielezo]] = -1; hali_thamani[kitanzi_kielezo] = 묶임[kitanzi_kielezo] = 수[kitanzi_kielezo] = subiri_thamani[kitanzi_kielezo] = 0; return 0;
    }
}
