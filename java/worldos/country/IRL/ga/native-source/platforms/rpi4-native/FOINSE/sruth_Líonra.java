// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** eithne_VALUE 안의 연결형 beart_VALUE sruth_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket sraith_VALUE. */
public final class sruth_Líonra {
    static int[] staid_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], piara_port = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], sonraí = new int[16 * 1024];
    static int Ar_aghaidh_mír = 50000;
    static int fíoraigh(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && staid_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int uimhir_phoirt) { for (int lúb_INDEX = 0; lúb_INDEX < 16; lúb_INDEX++) if (staid_VALUE[lúb_INDEX] != 0 && 묶임[lúb_INDEX] != 0 && port_VALUE[lúb_INDEX] == uimhir_phoirt) return true; return false; }
    public static int Create_iontráil() {
        for (int lúb_INDEX = 0; lúb_INDEX < 16; lúb_INDEX++) if (staid_VALUE[lúb_INDEX] == 0) { staid_VALUE[lúb_INDEX] = 1; piara_port[lúb_INDEX] = port_VALUE[lúb_INDEX] = 앞[lúb_INDEX] = 수[lúb_INDEX] = 대기[lúb_INDEX] = 묶임[lúb_INDEX] = 0; 짝[lúb_INDEX] = -1; return lúb_INDEX + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int uimhir_phoirt) {
        int lúb_INDEX = fíoraigh(열린파일번호); if (lúb_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (staid_VALUE[lúb_INDEX] != 1 || uimhir_phoirt < 0 || uimhir_phoirt > 65535) return -22;
        if (uimhir_phoirt == 0) { do { uimhir_phoirt = Ar_aghaidh_mír++; if (Ar_aghaidh_mír > 65535) Ar_aghaidh_mír = 50000; } while (사용중(uimhir_phoirt)); }
        if (사용중(uimhir_phoirt)) return -98; port_VALUE[lúb_INDEX] = uimhir_phoirt; 묶임[lúb_INDEX] = 1; staid_VALUE[lúb_INDEX] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int lúb_INDEX = fíoraigh(열린파일번호); if (lúb_INDEX < 0) return -9; if (staid_VALUE[lúb_INDEX] != 2 || 연결대기한도 < 1) return -22; staid_VALUE[lúb_INDEX] = 3; return 0; }
    public static int Nasc(int 열린파일번호, int 통신주소, int uimhir_phoirt) {
        int lúb_INDEX = fíoraigh(열린파일번호); if (lúb_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (uimhir_phoirt < 1 || uimhir_phoirt > 65535 || staid_VALUE[lúb_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 16; comhcheangal_istigh_suíomh++) if (staid_VALUE[comhcheangal_istigh_suíomh] == 3 && port_VALUE[comhcheangal_istigh_suíomh] == uimhir_phoirt) 수신쪽 = comhcheangal_istigh_suíomh;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 16; comhcheangal_istigh_suíomh++) if (대기[comhcheangal_istigh_suíomh] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (staid_VALUE[lúb_INDEX] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Create_iontráil(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        staid_VALUE[lúb_INDEX] = staid_VALUE[다른번호] = 4; 짝[lúb_INDEX] = 다른번호; 짝[다른번호] = lúb_INDEX; port_VALUE[다른번호] = uimhir_phoirt; piara_port[lúb_INDEX] = uimhir_phoirt; piara_port[다른번호] = port_VALUE[lúb_INDEX]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int glac_le_nasc(int 열린파일번호) { int lúb_INDEX = fíoraigh(열린파일번호); if (lúb_INDEX < 0) return -9; if (staid_VALUE[lúb_INDEX] != 3) return -22; for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 16; comhcheangal_istigh_suíomh++) if (staid_VALUE[comhcheangal_istigh_suíomh] != 0 && 대기[comhcheangal_istigh_suíomh] == lúb_INDEX + 1) { 대기[comhcheangal_istigh_suíomh] = 0; return comhcheangal_istigh_suíomh + 40; } return -11; }
    public static int Scríobh(int 열린파일번호, int iontráil_COUNT) {
        int lúb_INDEX = fíoraigh(열린파일번호); if (lúb_INDEX < 0) return -9; if (staid_VALUE[lúb_INDEX] != 4) return -107;
        if (iontráil_COUNT < 0 || iontráil_COUNT > 512) return -22; if (iontráil_COUNT == 0) return 0;
        int comhcheangal_istigh_suíomh = 짝[lúb_INDEX]; if (comhcheangal_istigh_suíomh < 0) return -32; int 총수 = 1024 - 수[comhcheangal_istigh_suíomh]; if (총수 == 0) return -11; if (총수 > iontráil_COUNT) 총수 = iontráil_COUNT;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) sonraí[comhcheangal_istigh_suíomh * 1024 + (앞[comhcheangal_istigh_suíomh] + 수[comhcheangal_istigh_suíomh] + 비교자리) % 1024] = 되돌림망.Ar_aghaidh_VALUE[비교자리]; 수[comhcheangal_istigh_suíomh] += 총수; return 총수;
    }
    public static int Léigh(int 열린파일번호, int iontráil_COUNT) {
        int lúb_INDEX = fíoraigh(열린파일번호); if (lúb_INDEX < 0) return -9; if (staid_VALUE[lúb_INDEX] != 4) return -107; if (iontráil_COUNT < 0 || iontráil_COUNT > 512) return -22;
        if (iontráil_COUNT == 0) return 0; if (수[lúb_INDEX] == 0) return 짝[lúb_INDEX] < 0 ? 0 : -11; if (iontráil_COUNT > 수[lúb_INDEX]) iontráil_COUNT = 수[lúb_INDEX];
        for (int 비교자리 = 0; 비교자리 < iontráil_COUNT; 비교자리++) 되돌림망.Ar_aghaidh_VALUE[비교자리] = sonraí[lúb_INDEX * 1024 + (앞[lúb_INDEX] + 비교자리) % 1024]; 앞[lúb_INDEX] = (앞[lúb_INDEX] + iontráil_COUNT) % 1024; 수[lúb_INDEX] -= iontráil_COUNT; return iontráil_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int lúb_INDEX = fíoraigh(열린파일번호); return lúb_INDEX < 0 ? -9 : port_VALUE[lúb_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int lúb_INDEX = fíoraigh(열린파일번호); return lúb_INDEX < 0 ? -9 : piara_port[lúb_INDEX]; }
    public static int Dún(int 열린파일번호) {
        int lúb_INDEX = fíoraigh(열린파일번호); if (lúb_INDEX < 0) return -9;
        if (staid_VALUE[lúb_INDEX] == 3) for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 16; comhcheangal_istigh_suíomh++) if (대기[comhcheangal_istigh_suíomh] == lúb_INDEX + 1) { if (짝[comhcheangal_istigh_suíomh] >= 0) 짝[짝[comhcheangal_istigh_suíomh]] = -1; staid_VALUE[comhcheangal_istigh_suíomh] = 대기[comhcheangal_istigh_suíomh] = 묶임[comhcheangal_istigh_suíomh] = 0; }
        if (짝[lúb_INDEX] >= 0) 짝[짝[lúb_INDEX]] = -1; staid_VALUE[lúb_INDEX] = 묶임[lúb_INDEX] = 수[lúb_INDEX] = 대기[lúb_INDEX] = 0; return 0;
    }
}
