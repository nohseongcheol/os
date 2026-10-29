// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Khenele_Boleng 안의 연결형 baete_Boleng moela_Boleng. Ethernet/TCP 패킷 스택이 아닌 루프백 socket boalo_Boleng. */
public final class moela_Neteweke {
    static int[] kemo_Boleng = new int[16], gorogisetsa_Boleng = new int[16], 짝 = new int[16], semphato_gorogisetsa = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], tshedimosetso = new int[16 * 1024];
    static int 다음 = 50000;
    static int netefatsa(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && kemo_Boleng[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int lupu_tshupane = 0; lupu_tshupane < 16; lupu_tshupane++) if (kemo_Boleng[lupu_tshupane] != 0 && 묶임[lupu_tshupane] != 0 && gorogisetsa_Boleng[lupu_tshupane] == 접속번호) return true; return false; }
    public static int tlhama_tsenyo() {
        for (int lupu_tshupane = 0; lupu_tshupane < 16; lupu_tshupane++) if (kemo_Boleng[lupu_tshupane] == 0) { kemo_Boleng[lupu_tshupane] = 1; semphato_gorogisetsa[lupu_tshupane] = gorogisetsa_Boleng[lupu_tshupane] = 앞[lupu_tshupane] = 수[lupu_tshupane] = 대기[lupu_tshupane] = 묶임[lupu_tshupane] = 0; 짝[lupu_tshupane] = -1; return lupu_tshupane + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int lupu_tshupane = netefatsa(열린파일번호); if (lupu_tshupane < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (kemo_Boleng[lupu_tshupane] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; gorogisetsa_Boleng[lupu_tshupane] = 접속번호; 묶임[lupu_tshupane] = 1; kemo_Boleng[lupu_tshupane] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int lupu_tshupane = netefatsa(열린파일번호); if (lupu_tshupane < 0) return -9; if (kemo_Boleng[lupu_tshupane] != 2 || 연결대기한도 < 1) return -22; kemo_Boleng[lupu_tshupane] = 3; return 0; }
    public static int Golaganya(int 열린파일번호, int 통신주소, int 접속번호) {
        int lupu_tshupane = netefatsa(열린파일번호); if (lupu_tshupane < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || kemo_Boleng[lupu_tshupane] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (kemo_Boleng[안쪽자리] == 3 && gorogisetsa_Boleng[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (kemo_Boleng[lupu_tshupane] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = tlhama_tsenyo(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        kemo_Boleng[lupu_tshupane] = kemo_Boleng[다른번호] = 4; 짝[lupu_tshupane] = 다른번호; 짝[다른번호] = lupu_tshupane; gorogisetsa_Boleng[다른번호] = 접속번호; semphato_gorogisetsa[lupu_tshupane] = 접속번호; semphato_gorogisetsa[다른번호] = gorogisetsa_Boleng[lupu_tshupane]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int amogela_Kgolagano(int 열린파일번호) { int lupu_tshupane = netefatsa(열린파일번호); if (lupu_tshupane < 0) return -9; if (kemo_Boleng[lupu_tshupane] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (kemo_Boleng[안쪽자리] != 0 && 대기[안쪽자리] == lupu_tshupane + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int kwala(int 열린파일번호, int 항목수) {
        int lupu_tshupane = netefatsa(열린파일번호); if (lupu_tshupane < 0) return -9; if (kemo_Boleng[lupu_tshupane] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[lupu_tshupane]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) tshedimosetso[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.fetisa_Boleng_24592b8a[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int 읽기(int 열린파일번호, int 항목수) {
        int lupu_tshupane = netefatsa(열린파일번호); if (lupu_tshupane < 0) return -9; if (kemo_Boleng[lupu_tshupane] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[lupu_tshupane] == 0) return 짝[lupu_tshupane] < 0 ? 0 : -11; if (항목수 > 수[lupu_tshupane]) 항목수 = 수[lupu_tshupane];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.fetisa_Boleng_24592b8a[비교자리] = tshedimosetso[lupu_tshupane * 1024 + (앞[lupu_tshupane] + 비교자리) % 1024]; 앞[lupu_tshupane] = (앞[lupu_tshupane] + 항목수) % 1024; 수[lupu_tshupane] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int lupu_tshupane = netefatsa(열린파일번호); return lupu_tshupane < 0 ? -9 : gorogisetsa_Boleng[lupu_tshupane]; }
    public static int 상대창구읽기(int 열린파일번호) { int lupu_tshupane = netefatsa(열린파일번호); return lupu_tshupane < 0 ? -9 : semphato_gorogisetsa[lupu_tshupane]; }
    public static int tswala(int 열린파일번호) {
        int lupu_tshupane = netefatsa(열린파일번호); if (lupu_tshupane < 0) return -9;
        if (kemo_Boleng[lupu_tshupane] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == lupu_tshupane + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; kemo_Boleng[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[lupu_tshupane] >= 0) 짝[짝[lupu_tshupane]] = -1; kemo_Boleng[lupu_tshupane] = 묶임[lupu_tshupane] = 수[lupu_tshupane] = 대기[lupu_tshupane] = 0; return 0;
    }
}
