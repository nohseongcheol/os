// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** cnewyllyn_VALUE 안의 연결형 beit_VALUE ffrwd_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket haen_VALUE. */
public final class ffrwd_Rhwydwaith {
    static int[] cyflwr_VALUE = new int[16], porth_VALUE = new int[16], 짝 = new int[16], cymar_porth = new int[16], aros_VALUE = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int Nesaf_eitem = 50000;
    static int dilysu(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && cyflwr_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int rhif_porth) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (cyflwr_VALUE[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && porth_VALUE[Loop_INDEX] == rhif_porth) return true; return false; }
    public static int Creu_cofnod() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (cyflwr_VALUE[Loop_INDEX] == 0) { cyflwr_VALUE[Loop_INDEX] = 1; cymar_porth[Loop_INDEX] = porth_VALUE[Loop_INDEX] = 앞[Loop_INDEX] = 수[Loop_INDEX] = aros_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int rhif_porth) {
        int Loop_INDEX = dilysu(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (cyflwr_VALUE[Loop_INDEX] != 1 || rhif_porth < 0 || rhif_porth > 65535) return -22;
        if (rhif_porth == 0) { do { rhif_porth = Nesaf_eitem++; if (Nesaf_eitem > 65535) Nesaf_eitem = 50000; } while (사용중(rhif_porth)); }
        if (사용중(rhif_porth)) return -98; porth_VALUE[Loop_INDEX] = rhif_porth; 묶임[Loop_INDEX] = 1; cyflwr_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = dilysu(열린파일번호); if (Loop_INDEX < 0) return -9; if (cyflwr_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; cyflwr_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Cysylltu(int 열린파일번호, int 통신주소, int rhif_porth) {
        int Loop_INDEX = dilysu(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (rhif_porth < 1 || rhif_porth > 65535 || cyflwr_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int uno_mewnol_safle = 0; uno_mewnol_safle < 16; uno_mewnol_safle++) if (cyflwr_VALUE[uno_mewnol_safle] == 3 && porth_VALUE[uno_mewnol_safle] == rhif_porth) 수신쪽 = uno_mewnol_safle;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int uno_mewnol_safle = 0; uno_mewnol_safle < 16; uno_mewnol_safle++) if (aros_VALUE[uno_mewnol_safle] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (cyflwr_VALUE[Loop_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Creu_cofnod(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        cyflwr_VALUE[Loop_INDEX] = cyflwr_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; porth_VALUE[다른번호] = rhif_porth; cymar_porth[Loop_INDEX] = rhif_porth; cymar_porth[다른번호] = porth_VALUE[Loop_INDEX]; aros_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int derbyn_cyswllt(int 열린파일번호) { int Loop_INDEX = dilysu(열린파일번호); if (Loop_INDEX < 0) return -9; if (cyflwr_VALUE[Loop_INDEX] != 3) return -22; for (int uno_mewnol_safle = 0; uno_mewnol_safle < 16; uno_mewnol_safle++) if (cyflwr_VALUE[uno_mewnol_safle] != 0 && aros_VALUE[uno_mewnol_safle] == Loop_INDEX + 1) { aros_VALUE[uno_mewnol_safle] = 0; return uno_mewnol_safle + 40; } return -11; }
    public static int Ysgrifennu(int 열린파일번호, int cofnod_COUNT) {
        int Loop_INDEX = dilysu(열린파일번호); if (Loop_INDEX < 0) return -9; if (cyflwr_VALUE[Loop_INDEX] != 4) return -107;
        if (cofnod_COUNT < 0 || cofnod_COUNT > 512) return -22; if (cofnod_COUNT == 0) return 0;
        int uno_mewnol_safle = 짝[Loop_INDEX]; if (uno_mewnol_safle < 0) return -32; int 총수 = 1024 - 수[uno_mewnol_safle]; if (총수 == 0) return -11; if (총수 > cofnod_COUNT) 총수 = cofnod_COUNT;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) data[uno_mewnol_safle * 1024 + (앞[uno_mewnol_safle] + 수[uno_mewnol_safle] + 비교자리) % 1024] = 되돌림망.Ymlaen_VALUE[비교자리]; 수[uno_mewnol_safle] += 총수; return 총수;
    }
    public static int Darllen(int 열린파일번호, int cofnod_COUNT) {
        int Loop_INDEX = dilysu(열린파일번호); if (Loop_INDEX < 0) return -9; if (cyflwr_VALUE[Loop_INDEX] != 4) return -107; if (cofnod_COUNT < 0 || cofnod_COUNT > 512) return -22;
        if (cofnod_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (cofnod_COUNT > 수[Loop_INDEX]) cofnod_COUNT = 수[Loop_INDEX];
        for (int 비교자리 = 0; 비교자리 < cofnod_COUNT; 비교자리++) 되돌림망.Ymlaen_VALUE[비교자리] = data[Loop_INDEX * 1024 + (앞[Loop_INDEX] + 비교자리) % 1024]; 앞[Loop_INDEX] = (앞[Loop_INDEX] + cofnod_COUNT) % 1024; 수[Loop_INDEX] -= cofnod_COUNT; return cofnod_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = dilysu(열린파일번호); return Loop_INDEX < 0 ? -9 : porth_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = dilysu(열린파일번호); return Loop_INDEX < 0 ? -9 : cymar_porth[Loop_INDEX]; }
    public static int Cau(int 열린파일번호) {
        int Loop_INDEX = dilysu(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (cyflwr_VALUE[Loop_INDEX] == 3) for (int uno_mewnol_safle = 0; uno_mewnol_safle < 16; uno_mewnol_safle++) if (aros_VALUE[uno_mewnol_safle] == Loop_INDEX + 1) { if (짝[uno_mewnol_safle] >= 0) 짝[짝[uno_mewnol_safle]] = -1; cyflwr_VALUE[uno_mewnol_safle] = aros_VALUE[uno_mewnol_safle] = 묶임[uno_mewnol_safle] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; cyflwr_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 수[Loop_INDEX] = aros_VALUE[Loop_INDEX] = 0; return 0;
    }
}
