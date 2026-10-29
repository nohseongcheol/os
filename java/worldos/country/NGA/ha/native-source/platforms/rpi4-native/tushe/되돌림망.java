// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 Tsarkiya_Daraja: 단일 Kwara_Daraja 안의 IPv4/UDP 루프백 Gusar_da_Daraja.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * Ƙarshe_maki 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] fot_Daraja = new int[8];
    static int[] imel = new int[8];
    static int[] kyamarar_gaba_Daraja = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] Tsawo_Daraja = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] Tarin_bayani = new int[32 * 512];
    static int[] Ingiza_Daraja = new int[512];
    static int 다음창구 = 49152;
    static int Tabbatar_da(int Indes) { return Indes >= 32 && Indes < 40 && 사용[Indes - 32] != 0 ? Indes - 32 : -1; }
    static boolean 겹침(int Indes) {
        for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 8; rami_Mashigar_bayanai++) if (사용[rami_Mashigar_bayanai] != 0 && fot_Daraja[rami_Mashigar_bayanai] == Indes) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = 다음창구++;
            if (다음창구 > 65535) 다음창구 = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int ƙirƙíra_Mashigar_bayanai(int 영역, int 종류, int Kes_Daraja) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (Kes_Daraja != 0 && Kes_Daraja != 17)) return -93;
        for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 8; rami_Mashigar_bayanai++) if (사용[rami_Mashigar_bayanai] == 0) {
            사용[rami_Mashigar_bayanai] = 1; fot_Daraja[rami_Mashigar_bayanai] = 0; imel[rami_Mashigar_bayanai] = 0; kyamarar_gaba_Daraja[rami_Mashigar_bayanai] = 0; 개수[rami_Mashigar_bayanai] = 0; 받은창구[rami_Mashigar_bayanai] = 0;
            return rami_Mashigar_bayanai + 32;
        }
        return -24;
    }
    public static int 묶기(int Indes, int Hanyar_sadarwa_imel_df3458bb, int 창구번호) {
        int rami_Mashigar_bayanai = Tabbatar_da(Indes);
        if (rami_Mashigar_bayanai < 0) return -9;
        if (Hanyar_sadarwa_imel_df3458bb != 0 && Hanyar_sadarwa_imel_df3458bb != 0x7f000001) return -99;
        if (fot_Daraja[rami_Mashigar_bayanai] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        fot_Daraja[rami_Mashigar_bayanai] = 창구번호; imel[rami_Mashigar_bayanai] = Hanyar_sadarwa_imel_df3458bb; return 0;
    }
    public static int 자료넣기(int Indes, int Daraja) {
        if (Indes < 0 || Indes >= 512) return -22;
        Ingiza_Daraja[Indes] = Daraja & 255; return 0;
    }
    public static int 자료읽기(int Indes) { return Indes >= 0 && Indes < 512 ? Ingiza_Daraja[Indes] : -22; }
    public static int Aika(int Indes, int Hanyar_sadarwa_imel_df3458bb, int 창구번호, int Girma) {
        int rami_Mashigar_bayanai = Tabbatar_da(Indes);
        if (rami_Mashigar_bayanai < 0) return -9;
        if (Hanyar_sadarwa_imel_df3458bb != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Girma < 0 || Girma > 512) return -90;
        if (fot_Daraja[rami_Mashigar_bayanai] == 0) {
            int 결과 = 묶기(Indes, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int Zangon_ƙarshe_Daraja = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && fot_Daraja[후보] == 창구번호) Zangon_ƙarshe_Daraja = 후보;
        if (Zangon_ƙarshe_Daraja < 0) return -111;
        if (개수[Zangon_ƙarshe_Daraja] == 4) return -11;
        int 자리 = Zangon_ƙarshe_Daraja * 4 + (kyamarar_gaba_Daraja[Zangon_ƙarshe_Daraja] + 개수[Zangon_ƙarshe_Daraja]) % 4;
        for (int bayit_Daraja = 0; bayit_Daraja < Girma; bayit_Daraja++) Tarin_bayani[자리 * 512 + bayit_Daraja] = Ingiza_Daraja[bayit_Daraja];
        Tsawo_Daraja[자리] = Girma; 보낸창구[자리] = fot_Daraja[rami_Mashigar_bayanai]; 개수[Zangon_ƙarshe_Daraja]++;
        return Girma;
    }
    public static int 받기(int Indes, int 용량) {
        int rami_Mashigar_bayanai = Tabbatar_da(Indes);
        if (rami_Mashigar_bayanai < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[rami_Mashigar_bayanai] == 0) return -11;
        int 자리 = rami_Mashigar_bayanai * 4 + kyamarar_gaba_Daraja[rami_Mashigar_bayanai];
        int Girma = Tsawo_Daraja[자리] < 용량 ? Tsawo_Daraja[자리] : 용량;
        for (int bayit_Daraja = 0; bayit_Daraja < Girma; bayit_Daraja++) Ingiza_Daraja[bayit_Daraja] = Tarin_bayani[자리 * 512 + bayit_Daraja];
        받은창구[rami_Mashigar_bayanai] = 보낸창구[자리]; kyamarar_gaba_Daraja[rami_Mashigar_bayanai] = (kyamarar_gaba_Daraja[rami_Mashigar_bayanai] + 1) % 4; 개수[rami_Mashigar_bayanai]--;
        return Girma;
    }
    public static int 창구읽기(int Indes) { int rami_Mashigar_bayanai = Tabbatar_da(Indes); return rami_Mashigar_bayanai < 0 ? -9 : fot_Daraja[rami_Mashigar_bayanai]; }
    public static int 주소읽기(int Indes) { int rami_Mashigar_bayanai = Tabbatar_da(Indes); return rami_Mashigar_bayanai < 0 ? -9 : imel[rami_Mashigar_bayanai]; }
    public static int 보낸곳(int Indes) { int rami_Mashigar_bayanai = Tabbatar_da(Indes); return rami_Mashigar_bayanai < 0 ? -9 : 받은창구[rami_Mashigar_bayanai]; }
    public static int Rufe(int Indes) {
        int rami_Mashigar_bayanai = Tabbatar_da(Indes); if (rami_Mashigar_bayanai < 0) return -9;
        사용[rami_Mashigar_bayanai] = 0; 개수[rami_Mashigar_bayanai] = 0; fot_Daraja[rami_Mashigar_bayanai] = 0; return 0;
    }
}
