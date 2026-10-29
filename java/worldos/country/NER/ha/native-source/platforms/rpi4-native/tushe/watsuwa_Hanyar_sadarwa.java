// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Kwara_Daraja 안의 연결형 bayit_Daraja watsuwa_Daraja. Ethernet/TCP 패킷 스택이 아닌 루프백 socket Tsarkiya_Daraja. */
public final class watsuwa_Hanyar_sadarwa {
    static int[] Matsayi_Daraja = new int[16], fot_Daraja = new int[16], 짝 = new int[16], Fiya_fot = new int[16], jira_Daraja = new int[16], 묶임 = new int[16];
    static int[] kyamarar_gaba_Daraja = new int[16], 수 = new int[16], Tarin_bayani = new int[16 * 1024];
    static int 다음 = 50000;
    static int Tabbatar_da(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Matsayi_Daraja[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int lambar_kafa) { for (int Warware_Indes = 0; Warware_Indes < 16; Warware_Indes++) if (Matsayi_Daraja[Warware_Indes] != 0 && 묶임[Warware_Indes] != 0 && fot_Daraja[Warware_Indes] == lambar_kafa) return true; return false; }
    public static int ƙirƙíra_Mashigar_bayanai() {
        for (int Warware_Indes = 0; Warware_Indes < 16; Warware_Indes++) if (Matsayi_Daraja[Warware_Indes] == 0) { Matsayi_Daraja[Warware_Indes] = 1; Fiya_fot[Warware_Indes] = fot_Daraja[Warware_Indes] = kyamarar_gaba_Daraja[Warware_Indes] = 수[Warware_Indes] = jira_Daraja[Warware_Indes] = 묶임[Warware_Indes] = 0; 짝[Warware_Indes] = -1; return Warware_Indes + 40; }
        return -24;
    }
    public static int 묶기(int 열린파일번호, int 통신주소, int lambar_kafa) {
        int Warware_Indes = Tabbatar_da(열린파일번호); if (Warware_Indes < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Matsayi_Daraja[Warware_Indes] != 1 || lambar_kafa < 0 || lambar_kafa > 65535) return -22;
        if (lambar_kafa == 0) { do { lambar_kafa = 다음++; if (다음 > 65535) 다음 = 50000; } while (사용중(lambar_kafa)); }
        if (사용중(lambar_kafa)) return -98; fot_Daraja[Warware_Indes] = lambar_kafa; 묶임[Warware_Indes] = 1; Matsayi_Daraja[Warware_Indes] = 2; return 0;
    }
    public static int 듣기(int 열린파일번호, int 연결대기한도) { int Warware_Indes = Tabbatar_da(열린파일번호); if (Warware_Indes < 0) return -9; if (Matsayi_Daraja[Warware_Indes] != 2 || 연결대기한도 < 1) return -22; Matsayi_Daraja[Warware_Indes] = 3; return 0; }
    public static int Haɗi(int 열린파일번호, int 통신주소, int lambar_kafa) {
        int Warware_Indes = Tabbatar_da(열린파일번호); if (Warware_Indes < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (lambar_kafa < 1 || lambar_kafa > 65535 || Matsayi_Daraja[Warware_Indes] > 2) return -22;
        int 수신쪽 = -1; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (Matsayi_Daraja[안쪽자리] == 3 && fot_Daraja[안쪽자리] == lambar_kafa) 수신쪽 = 안쪽자리;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (jira_Daraja[안쪽자리] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Matsayi_Daraja[Warware_Indes] == 1) { int 처리값 = 묶기(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = ƙirƙíra_Mashigar_bayanai(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        Matsayi_Daraja[Warware_Indes] = Matsayi_Daraja[다른번호] = 4; 짝[Warware_Indes] = 다른번호; 짝[다른번호] = Warware_Indes; fot_Daraja[다른번호] = lambar_kafa; Fiya_fot[Warware_Indes] = lambar_kafa; Fiya_fot[다른번호] = fot_Daraja[Warware_Indes]; jira_Daraja[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int 받음(int 열린파일번호) { int Warware_Indes = Tabbatar_da(열린파일번호); if (Warware_Indes < 0) return -9; if (Matsayi_Daraja[Warware_Indes] != 3) return -22; for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (Matsayi_Daraja[안쪽자리] != 0 && jira_Daraja[안쪽자리] == Warware_Indes + 1) { jira_Daraja[안쪽자리] = 0; return 안쪽자리 + 40; } return -11; }
    public static int Yi_Rubutu(int 열린파일번호, int 항목수) {
        int Warware_Indes = Tabbatar_da(열린파일번호); if (Warware_Indes < 0) return -9; if (Matsayi_Daraja[Warware_Indes] != 4) return -107;
        if (항목수 < 0 || 항목수 > 512) return -22; if (항목수 == 0) return 0;
        int 안쪽자리 = 짝[Warware_Indes]; if (안쪽자리 < 0) return -32; int 총수 = 1024 - 수[안쪽자리]; if (총수 == 0) return -11; if (총수 > 항목수) 총수 = 항목수;
        for (int 비교자리 = 0; 비교자리 < 총수; 비교자리++) Tarin_bayani[안쪽자리 * 1024 + (kyamarar_gaba_Daraja[안쪽자리] + 수[안쪽자리] + 비교자리) % 1024] = 되돌림망.Ingiza_Daraja[비교자리]; 수[안쪽자리] += 총수; return 총수;
    }
    public static int Yi_Karatu(int 열린파일번호, int 항목수) {
        int Warware_Indes = Tabbatar_da(열린파일번호); if (Warware_Indes < 0) return -9; if (Matsayi_Daraja[Warware_Indes] != 4) return -107; if (항목수 < 0 || 항목수 > 512) return -22;
        if (항목수 == 0) return 0; if (수[Warware_Indes] == 0) return 짝[Warware_Indes] < 0 ? 0 : -11; if (항목수 > 수[Warware_Indes]) 항목수 = 수[Warware_Indes];
        for (int 비교자리 = 0; 비교자리 < 항목수; 비교자리++) 되돌림망.Ingiza_Daraja[비교자리] = Tarin_bayani[Warware_Indes * 1024 + (kyamarar_gaba_Daraja[Warware_Indes] + 비교자리) % 1024]; kyamarar_gaba_Daraja[Warware_Indes] = (kyamarar_gaba_Daraja[Warware_Indes] + 항목수) % 1024; 수[Warware_Indes] -= 항목수; return 항목수;
    }
    public static int 창구읽기(int 열린파일번호) { int Warware_Indes = Tabbatar_da(열린파일번호); return Warware_Indes < 0 ? -9 : fot_Daraja[Warware_Indes]; }
    public static int 상대창구읽기(int 열린파일번호) { int Warware_Indes = Tabbatar_da(열린파일번호); return Warware_Indes < 0 ? -9 : Fiya_fot[Warware_Indes]; }
    public static int Rufe(int 열린파일번호) {
        int Warware_Indes = Tabbatar_da(열린파일번호); if (Warware_Indes < 0) return -9;
        if (Matsayi_Daraja[Warware_Indes] == 3) for (int 안쪽자리 = 0; 안쪽자리 < 16; 안쪽자리++) if (jira_Daraja[안쪽자리] == Warware_Indes + 1) { if (짝[안쪽자리] >= 0) 짝[짝[안쪽자리]] = -1; Matsayi_Daraja[안쪽자리] = jira_Daraja[안쪽자리] = 묶임[안쪽자리] = 0; }
        if (짝[Warware_Indes] >= 0) 짝[짝[Warware_Indes]] = -1; Matsayi_Daraja[Warware_Indes] = 묶임[Warware_Indes] = 수[Warware_Indes] = jira_Daraja[Warware_Indes] = 0; return 0;
    }
}
