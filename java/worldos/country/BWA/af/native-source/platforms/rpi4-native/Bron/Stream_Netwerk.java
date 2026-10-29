// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kern_VALUE 안의 연결형 greep_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket laag_VALUE. */
public final class Stream_Netwerk {
    static int[] stand_VALUE = new int[16], ombou_VALUE = new int[16], 짝 = new int[16], portuur_ombou = new int[16], wag_VALUE = new int[16], 묶임 = new int[16];
    static int[] voor_VALUE = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int Volgende_item = 50000;
    static int verifieer(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && stand_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (stand_VALUE[lus_INDEX] != 0 && 묶임[lus_INDEX] != 0 && ombou_VALUE[lus_INDEX] == 접속번호) return true; return false; }
    public static int Skep_inskrywing() {
        for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) if (stand_VALUE[lus_INDEX] == 0) { stand_VALUE[lus_INDEX] = 1; portuur_ombou[lus_INDEX] = ombou_VALUE[lus_INDEX] = voor_VALUE[lus_INDEX] = 수[lus_INDEX] = wag_VALUE[lus_INDEX] = 묶임[lus_INDEX] = 0; 짝[lus_INDEX] = -1; return lus_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int lus_INDEX = verifieer(열린파일번호); if (lus_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (stand_VALUE[lus_INDEX] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = Volgende_item++; if (Volgende_item > 65535) Volgende_item = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; ombou_VALUE[lus_INDEX] = 접속번호; 묶임[lus_INDEX] = 1; stand_VALUE[lus_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int lus_INDEX = verifieer(열린파일번호); if (lus_INDEX < 0) return -9; if (stand_VALUE[lus_INDEX] != 2 || 연결대기한도 < 1) return -22; stand_VALUE[lus_INDEX] = 3; return 0; }
    public static int Koppel(int 열린파일번호, int 통신주소, int 접속번호) {
        int lus_INDEX = verifieer(열린파일번호); if (lus_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || stand_VALUE[lus_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int binnebind_plaas = 0; binnebind_plaas < 16; binnebind_plaas++) if (stand_VALUE[binnebind_plaas] == 3 && ombou_VALUE[binnebind_plaas] == 접속번호) 수신쪽 = binnebind_plaas;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int binnebind_plaas = 0; binnebind_plaas < 16; binnebind_plaas++) if (wag_VALUE[binnebind_plaas] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (stand_VALUE[lus_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Skep_inskrywing(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        stand_VALUE[lus_INDEX] = stand_VALUE[다른번호] = 4; 짝[lus_INDEX] = 다른번호; 짝[다른번호] = lus_INDEX; ombou_VALUE[다른번호] = 접속번호; portuur_ombou[lus_INDEX] = 접속번호; portuur_ombou[다른번호] = ombou_VALUE[lus_INDEX]; wag_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int aanvaar_verbinding(int 열린파일번호) { int lus_INDEX = verifieer(열린파일번호); if (lus_INDEX < 0) return -9; if (stand_VALUE[lus_INDEX] != 3) return -22; for (int binnebind_plaas = 0; binnebind_plaas < 16; binnebind_plaas++) if (stand_VALUE[binnebind_plaas] != 0 && wag_VALUE[binnebind_plaas] == lus_INDEX + 1) { wag_VALUE[binnebind_plaas] = 0; return binnebind_plaas + 40; } return -11; }
    public static int Skryf(int 열린파일번호, int inskrywing_COUNT) {
        int lus_INDEX = verifieer(열린파일번호); if (lus_INDEX < 0) return -9; if (stand_VALUE[lus_INDEX] != 4) return -107;
        if (inskrywing_COUNT < 0 || inskrywing_COUNT > 512) return -22; if (inskrywing_COUNT == 0) return 0;
        int binnebind_plaas = 짝[lus_INDEX]; if (binnebind_plaas < 0) return -32; int 총수 = 1024 - 수[binnebind_plaas]; if (총수 == 0) return -11; if (총수 > inskrywing_COUNT) 총수 = inskrywing_COUNT;
        for (int Vergelyking_plaas = 0; Vergelyking_plaas < 총수; Vergelyking_plaas++) data[binnebind_plaas * 1024 + (voor_VALUE[binnebind_plaas] + 수[binnebind_plaas] + Vergelyking_plaas) % 1024] = 되돌림망.aanstuur_VALUE_24592b8a[Vergelyking_plaas]; 수[binnebind_plaas] += 총수; return 총수;
    }
    public static int Lees(int 열린파일번호, int inskrywing_COUNT) {
        int lus_INDEX = verifieer(열린파일번호); if (lus_INDEX < 0) return -9; if (stand_VALUE[lus_INDEX] != 4) return -107; if (inskrywing_COUNT < 0 || inskrywing_COUNT > 512) return -22;
        if (inskrywing_COUNT == 0) return 0; if (수[lus_INDEX] == 0) return 짝[lus_INDEX] < 0 ? 0 : -11; if (inskrywing_COUNT > 수[lus_INDEX]) inskrywing_COUNT = 수[lus_INDEX];
        for (int Vergelyking_plaas = 0; Vergelyking_plaas < inskrywing_COUNT; Vergelyking_plaas++) 되돌림망.aanstuur_VALUE_24592b8a[Vergelyking_plaas] = data[lus_INDEX * 1024 + (voor_VALUE[lus_INDEX] + Vergelyking_plaas) % 1024]; voor_VALUE[lus_INDEX] = (voor_VALUE[lus_INDEX] + inskrywing_COUNT) % 1024; 수[lus_INDEX] -= inskrywing_COUNT; return inskrywing_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int lus_INDEX = verifieer(열린파일번호); return lus_INDEX < 0 ? -9 : ombou_VALUE[lus_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int lus_INDEX = verifieer(열린파일번호); return lus_INDEX < 0 ? -9 : portuur_ombou[lus_INDEX]; }
    public static int Sluit(int 열린파일번호) {
        int lus_INDEX = verifieer(열린파일번호); if (lus_INDEX < 0) return -9;
        if (stand_VALUE[lus_INDEX] == 3) for (int binnebind_plaas = 0; binnebind_plaas < 16; binnebind_plaas++) if (wag_VALUE[binnebind_plaas] == lus_INDEX + 1) { if (짝[binnebind_plaas] >= 0) 짝[짝[binnebind_plaas]] = -1; stand_VALUE[binnebind_plaas] = wag_VALUE[binnebind_plaas] = 묶임[binnebind_plaas] = 0; }
        if (짝[lus_INDEX] >= 0) 짝[짝[lus_INDEX]] = -1; stand_VALUE[lus_INDEX] = 묶임[lus_INDEX] = 수[lus_INDEX] = wag_VALUE[lus_INDEX] = 0; return 0;
    }
}
