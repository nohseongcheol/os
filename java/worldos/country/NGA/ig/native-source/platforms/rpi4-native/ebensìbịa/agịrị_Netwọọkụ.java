// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** mkpụrụobī_kọmpùta_valuu 안의 연결형 baịtị_valuu agịrị_valuu. Ethernet/TCP 패킷 스택이 아닌 루프백 socket òkpùkpù_valuu. */
public final class agịrị_Netwọọkụ {
    static int[] ọnọdụ_valuu = new int[16], pọọt_valuu = new int[16], 짝 = new int[16], ibè_pọọt = new int[16], 대기 = new int[16], 묶임 = new int[16];
    static int[] 앞 = new int[16], 수 = new int[16], datà = new int[16 * 1024];
    static int 다음 = 50000;
    static int nkwàdo_eziokwū(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && ọnọdụ_valuu[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int 접속번호) { for (int memmenwè_indèks = 0; memmenwè_indèks < 16; memmenwè_indèks++) if (ọnọdụ_valuu[memmenwè_indèks] != 0 && 묶임[memmenwè_indèks] != 0 && pọọt_valuu[memmenwè_indèks] == 접속번호) return true; return false; }
    public static int mepụta_ndebà() {
        for (int memmenwè_indèks = 0; memmenwè_indèks < 16; memmenwè_indèks++) if (ọnọdụ_valuu[memmenwè_indèks] == 0) { ọnọdụ_valuu[memmenwè_indèks] = 1; ibè_pọọt[memmenwè_indèks] = pọọt_valuu[memmenwè_indèks] = 앞[memmenwè_indèks] = 수[memmenwè_indèks] = 대기[memmenwè_indèks] = 묶임[memmenwè_indèks] = 0; 짝[memmenwè_indèks] = -1; return memmenwè_indèks + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int 접속번호) {
        int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); if (memmenwè_indèks < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (ọnọdụ_valuu[memmenwè_indèks] != 1 || 접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 == 0) { do { 접속번호 = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(접속번호)); }
        if (사용중(접속번호)) return -98; pọọt_valuu[memmenwè_indèks] = 접속번호; 묶임[memmenwè_indèks] = 1; ọnọdụ_valuu[memmenwè_indèks] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); if (memmenwè_indèks < 0) return -9; if (ọnọdụ_valuu[memmenwè_indèks] != 2 || 연결대기한도 < 1) return -22; ọnọdụ_valuu[memmenwè_indèks] = 3; return 0; }
    public static int Banye(int 열린파일번호, int 통신주소, int 접속번호) {
        int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); if (memmenwè_indèks < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (접속번호 < 1 || 접속번호 > 65535 || ọnọdụ_valuu[memmenwè_indèks] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (ọnọdụ_valuu[안쪽자리] == 3 && pọọt_valuu[안쪽자리] == 접속번호) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (ọnọdụ_valuu[memmenwè_indèks] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = mepụta_ndebà(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        ọnọdụ_valuu[memmenwè_indèks] = ọnọdụ_valuu[다른번호] = 4; 짝[memmenwè_indèks] = 다른번호; 짝[다른번호] = memmenwè_indèks; pọọt_valuu[다른번호] = 접속번호; ibè_pọọt[memmenwè_indèks] = 접속번호; ibè_pọọt[다른번호] = pọọt_valuu[memmenwè_indèks]; 대기[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int nabata_njikọ(int 열린파일번호) { int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); if (memmenwè_indèks < 0) return -9; if (ọnọdụ_valuu[memmenwè_indèks] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (ọnọdụ_valuu[안쪽자리] != 0 && 대기[안쪽자리] == memmenwè_indèks + 1) { 대기[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int Chekwaa_ozi(int 열린파일번호, int 항목수) {
        int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); if (memmenwè_indèks < 0) return -9; if (ọnọdụ_valuu[memmenwè_indèks] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[memmenwè_indèks]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) datà[안쪽자리 * 1024 + (앞[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.zìgaā_valuu[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int Wepụta_ọzi(int 열린파일번호, int 항목수) {
        int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); if (memmenwè_indèks < 0) return -9; if (ọnọdụ_valuu[memmenwè_indèks] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[memmenwè_indèks] == 0) return 짝[memmenwè_indèks] < 0 ? 0 : -11; if (항목수 > 수[memmenwè_indèks]) 항목수 = 수[memmenwè_indèks];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.zìgaā_valuu[비교자리] = datà[memmenwè_indèks * 1024 + (앞[memmenwè_indèks] + 비교자리) % 1024]; 앞[memmenwè_indèks] = (앞[memmenwè_indèks] + 항목수) % 1024; 수[memmenwè_indèks] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); return memmenwè_indèks < 0 ? -9 : pọọt_valuu[memmenwè_indèks]; }
    public static int 상대창구읽기(int 열린파일번호) { int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); return memmenwè_indèks < 0 ? -9 : ibè_pọọt[memmenwè_indèks]; }
    public static int Mechie(int 열린파일번호) {
        int memmenwè_indèks = nkwàdo_eziokwū(열린파일번호); if (memmenwè_indèks < 0) return -9;
        if (ọnọdụ_valuu[memmenwè_indèks] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (대기[안쪽자리] == memmenwè_indèks + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; ọnọdụ_valuu[안쪽자리] = 대기[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[memmenwè_indèks] >= 0) 짝[짝[memmenwè_indèks]] = -1; ọnọdụ_valuu[memmenwè_indèks] = 묶임[memmenwè_indèks] = 수[memmenwè_indèks] = 대기[memmenwè_indèks] = 0; return 0;
    }
}
