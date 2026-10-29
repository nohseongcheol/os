// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kākano_uara_0611a8a8 안의 연결형 paita_uara roma_uara. Ethernet/TCP 패킷 스택이 아닌 루프백 socket apa_uara. */
public final class roma_whatunga {
    static int[] tūnga_uara = new int[16], kawe_uara = new int[16], 짝 = new int[16], hoa_kawe = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], raraunga = new int[16 * 1024];
    static int Panuku_tuemi = 50000;
    static int manatoko(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && tūnga_uara[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (tūnga_uara[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && kawe_uara[Loop_INDEX] == 접속번호) return true; return false; }
    public static int Waihanga_tāurunga() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (tūnga_uara[Loop_INDEX] == 0) { tūnga_uara[Loop_INDEX] = 1; hoa_kawe[Loop_INDEX] = kawe_uara[Loop_INDEX] = 앞[Loop_INDEX] = 수[Loop_INDEX] = 대기[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = manatoko(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (tūnga_uara[Loop_INDEX] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = Panuku_tuemi++; if (Panuku_tuemi > 65535) Panuku_tuemi = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; kawe_uara[Loop_INDEX] = 접속번호; 묶임[Loop_INDEX] = 1; tūnga_uara[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = manatoko(열린파일번호); if (Loop_INDEX < 0) return -9; if (tūnga_uara[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; tūnga_uara[Loop_INDEX] = 3; return 0; }
    public static int TŪHONO(int 열린파일번호, int 통신주소, int 접속번호) {
        int Loop_INDEX = manatoko(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || tūnga_uara[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int hono_roto_tūranga = 0; hono_roto_tūranga < 16; hono_roto_tūranga++) if (tūnga_uara[hono_roto_tūranga] == 3 && kawe_uara[hono_roto_tūranga] == 접속번호) 수신쪽 = hono_roto_tūranga;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int hono_roto_tūranga = 0; hono_roto_tūranga < 16; hono_roto_tūranga++) if (대기[hono_roto_tūranga] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (tūnga_uara[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Waihanga_tāurunga(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        tūnga_uara[Loop_INDEX] = tūnga_uara[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; kawe_uara[다른번호] = 접속번호; hoa_kawe[Loop_INDEX] = 접속번호; hoa_kawe[다른번호] = kawe_uara[Loop_INDEX]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int whakaae_hononga(int 열린파일번호) { int Loop_INDEX = manatoko(열린파일번호); if (Loop_INDEX < 0) return -9; if (tūnga_uara[Loop_INDEX] != 3) return -22; for (int hono_roto_tūranga = 0; hono_roto_tūranga < 16; hono_roto_tūranga++) if (tūnga_uara[hono_roto_tūranga] != 0 && 대기[hono_roto_tūranga] == Loop_INDEX + 1) { 대기[hono_roto_tūranga] = 0; return hono_roto_tūranga + 40; } return -11; }
    public static int Tuhia(int 열린파일번호, int tāurunga_COUNT) {
        int Loop_INDEX = manatoko(열린파일번호); if (Loop_INDEX < 0) return -9; if (tūnga_uara[Loop_INDEX] != 4) return -107;
        if (tāurunga_COUNT < 0 || tāurunga_COUNT > 512) return -22; if (tāurunga_COUNT == 0) return 0;
        int hono_roto_tūranga = 짝[Loop_INDEX]; if (hono_roto_tūranga < 0) return -32; int 총수 = 1024 - 수[hono_roto_tūranga]; if (총수 == 0) return -11; if (총수 > tāurunga_COUNT) 총수 = tāurunga_COUNT;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) raraunga[hono_roto_tūranga * 1024 + (앞[hono_roto_tūranga] + 수[hono_roto_tūranga] + 비교자리) % 1024] = 되돌림망.Whakamua_uara[비교자리]; 수[hono_roto_tūranga] += 총수; return 총수;
    }
    public static int Pānuitia(int 열린파일번호, int tāurunga_COUNT) {
        int Loop_INDEX = manatoko(열린파일번호); if (Loop_INDEX < 0) return -9; if (tūnga_uara[Loop_INDEX] != 4) return -107; if (tāurunga_COUNT < 0 || tāurunga_COUNT > 512) return -22;
        if (tāurunga_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (tāurunga_COUNT > 수[Loop_INDEX]) tāurunga_COUNT = 수[Loop_INDEX];
        for (int 비교자리 = 0; 비교자리 < tāurunga_COUNT; 비교자리++) 되돌림망.Whakamua_uara[비교자리] = raraunga[Loop_INDEX * 1024 + (앞[Loop_INDEX] + 비교자리) % 1024]; 앞[Loop_INDEX] = (앞[Loop_INDEX] + tāurunga_COUNT) % 1024; 수[Loop_INDEX] -= tāurunga_COUNT; return tāurunga_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = manatoko(열린파일번호); return Loop_INDEX < 0 ? -9 : kawe_uara[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = manatoko(열린파일번호); return Loop_INDEX < 0 ? -9 : hoa_kawe[Loop_INDEX]; }
    public static int Kati(int 열린파일번호) {
        int Loop_INDEX = manatoko(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (tūnga_uara[Loop_INDEX] == 3) for (int hono_roto_tūranga = 0; hono_roto_tūranga < 16; hono_roto_tūranga++) if (대기[hono_roto_tūranga] == Loop_INDEX + 1) { if (짝[hono_roto_tūranga] >= 0) 짝[짝[hono_roto_tūranga]] = -1; tūnga_uara[hono_roto_tūranga] = 대기[hono_roto_tūranga] = 묶임[hono_roto_tūranga] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; tūnga_uara[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = 대기[Loop_INDEX] = 0; return 0;
    }
}
