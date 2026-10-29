// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 ugqinsi_inani: 단일 ikhenela_inani 안의 IPv4/UDP 루프백 dlulisa_inani_630ba093.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * yekisa_iphoyinti 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] intuba_inani = new int[8];
    static int[] ikheli = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] ubude_inani = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] imininingwane = new int[32 * 512];
    static int[] dlulisela_phambili_inani = new int[512];
    static int 다음창구 = 49152;
    static int qiniseka(int thola_inkomba) { return thola_inkomba >= 32 && thola_inkomba < 40 && 사용[thola_inkomba - 32] != 0 ? thola_inkomba - 32 : -1; }
    static boolean 겹침(int thola_inkomba) {
        for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 8; isikhala_okufakwayo++) if (사용[isikhala_okufakwayo] != 0 && intuba_inani[isikhala_okufakwayo] == thola_inkomba) return true;
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
    public static int yakha_okufakwayo(int 영역, int 종류, int udaba_inani) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (udaba_inani != 0 && udaba_inani != 17)) return -93;
        for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 8; isikhala_okufakwayo++) if (사용[isikhala_okufakwayo] == 0) {
            사용[isikhala_okufakwayo] = 1; intuba_inani[isikhala_okufakwayo] = 0; ikheli[isikhala_okufakwayo] = 0; 앞[isikhala_okufakwayo] = 0; 개수[isikhala_okufakwayo] = 0; 받은창구[isikhala_okufakwayo] = 0;
            return isikhala_okufakwayo + 32;
        }
        return -24;
    }
    public static int 묶기(int thola_inkomba, int iNethiwekhi_ikheli, int 창구번호) {
        int isikhala_okufakwayo = qiniseka(thola_inkomba);
        if (isikhala_okufakwayo < 0) return -9;
        if (iNethiwekhi_ikheli != 0 && iNethiwekhi_ikheli != 0x7f000001) return -99;
        if (intuba_inani[isikhala_okufakwayo] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        intuba_inani[isikhala_okufakwayo] = 창구번호; ikheli[isikhala_okufakwayo] = iNethiwekhi_ikheli; return 0;
    }
    public static int 자료넣기(int thola_inkomba, int inani) {
        if (thola_inkomba < 0 || thola_inkomba >= 512) return -22;
        dlulisela_phambili_inani[thola_inkomba] = inani & 255; return 0;
    }
    public static int 자료읽기(int thola_inkomba) { return thola_inkomba >= 0 && thola_inkomba < 512 ? dlulisela_phambili_inani[thola_inkomba] : -22; }
    public static int Thumela(int thola_inkomba, int iNethiwekhi_ikheli, int 창구번호, int Ubungako) {
        int isikhala_okufakwayo = qiniseka(thola_inkomba);
        if (isikhala_okufakwayo < 0) return -9;
        if (iNethiwekhi_ikheli != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Ubungako < 0 || Ubungako > 512) return -90;
        if (intuba_inani[isikhala_okufakwayo] == 0) {
            int 결과 = 묶기(thola_inkomba, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int isikhumulo_inani = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && intuba_inani[후보] == 창구번호) isikhumulo_inani = 후보;
        if (isikhumulo_inani < 0) return -111;
        if (개수[isikhumulo_inani] == 4) return -11;
        int 자리 = isikhumulo_inani * 4 + (앞[isikhumulo_inani] + 개수[isikhumulo_inani]) % 4;
        for (int ibhayithi_inani = 0; ibhayithi_inani < Ubungako; ibhayithi_inani++) imininingwane[자리 * 512 + ibhayithi_inani] = dlulisela_phambili_inani[ibhayithi_inani];
        ubude_inani[자리] = Ubungako; 보낸창구[자리] = intuba_inani[isikhala_okufakwayo]; 개수[isikhumulo_inani]++;
        return Ubungako;
    }
    public static int 받기(int thola_inkomba, int 용량) {
        int isikhala_okufakwayo = qiniseka(thola_inkomba);
        if (isikhala_okufakwayo < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[isikhala_okufakwayo] == 0) return -11;
        int 자리 = isikhala_okufakwayo * 4 + 앞[isikhala_okufakwayo];
        int Ubungako = ubude_inani[자리] < 용량 ? ubude_inani[자리] : 용량;
        for (int ibhayithi_inani = 0; ibhayithi_inani < Ubungako; ibhayithi_inani++) dlulisela_phambili_inani[ibhayithi_inani] = imininingwane[자리 * 512 + ibhayithi_inani];
        받은창구[isikhala_okufakwayo] = 보낸창구[자리]; 앞[isikhala_okufakwayo] = (앞[isikhala_okufakwayo] + 1) % 4; 개수[isikhala_okufakwayo]--;
        return Ubungako;
    }
    public static int 창구읽기(int thola_inkomba) { int isikhala_okufakwayo = qiniseka(thola_inkomba); return isikhala_okufakwayo < 0 ? -9 : intuba_inani[isikhala_okufakwayo]; }
    public static int 주소읽기(int thola_inkomba) { int isikhala_okufakwayo = qiniseka(thola_inkomba); return isikhala_okufakwayo < 0 ? -9 : ikheli[isikhala_okufakwayo]; }
    public static int 보낸곳(int thola_inkomba) { int isikhala_okufakwayo = qiniseka(thola_inkomba); return isikhala_okufakwayo < 0 ? -9 : 받은창구[isikhala_okufakwayo]; }
    public static int Vala(int thola_inkomba) {
        int isikhala_okufakwayo = qiniseka(thola_inkomba); if (isikhala_okufakwayo < 0) return -9;
        사용[isikhala_okufakwayo] = 0; 개수[isikhala_okufakwayo] = 0; intuba_inani[isikhala_okufakwayo] = 0; return 0;
    }
}
