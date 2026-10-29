// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 boalo_Boleng: 단일 Khenele_Boleng 안의 IPv4/UDP 루프백 fudusa_Boleng.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * kgaola_ntlha 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] gorogisetsa_Boleng = new int[8];
    static int[] aterese = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] boleele_Boleng = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] tshedimosetso = new int[32 * 512];
    static int[] fetisa_Boleng_24592b8a = new int[512];
    static int 다음창구 = 49152;
    static int netefatsa(int tshupane) { return tshupane >= 32 && tshupane < 40 && 사용[tshupane - 32] != 0 ? tshupane - 32 : -1; }
    static boolean 겹침(int tshupane) {
        for (int sebaka_tsenyo = 0; sebaka_tsenyo < 8; sebaka_tsenyo++) if (사용[sebaka_tsenyo] != 0 && gorogisetsa_Boleng[sebaka_tsenyo] == tshupane) return true;
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
    public static int tlhama_tsenyo(int 영역, int 종류, int konteraka_Boleng) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (konteraka_Boleng != 0 && konteraka_Boleng != 17)) return -93;
        for (int sebaka_tsenyo = 0; sebaka_tsenyo < 8; sebaka_tsenyo++) if (사용[sebaka_tsenyo] == 0) {
            사용[sebaka_tsenyo] = 1; gorogisetsa_Boleng[sebaka_tsenyo] = 0; aterese[sebaka_tsenyo] = 0; 앞[sebaka_tsenyo] = 0; 개수[sebaka_tsenyo] = 0; 받은창구[sebaka_tsenyo] = 0;
            return sebaka_tsenyo + 32;
        }
        return -24;
    }
    public static int 묶기(int tshupane, int Neteweke_aterese, int 창구번호) {
        int sebaka_tsenyo = netefatsa(tshupane);
        if (sebaka_tsenyo < 0) return -9;
        if (Neteweke_aterese != 0 && Neteweke_aterese != 0x7f000001) return -99;
        if (gorogisetsa_Boleng[sebaka_tsenyo] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        gorogisetsa_Boleng[sebaka_tsenyo] = 창구번호; aterese[sebaka_tsenyo] = Neteweke_aterese; return 0;
    }
    public static int 자료넣기(int tshupane, int Boleng) {
        if (tshupane < 0 || tshupane >= 512) return -22;
        fetisa_Boleng_24592b8a[tshupane] = Boleng & 255; return 0;
    }
    public static int 자료읽기(int tshupane) { return tshupane >= 0 && tshupane < 512 ? fetisa_Boleng_24592b8a[tshupane] : -22; }
    public static int romela(int tshupane, int Neteweke_aterese, int 창구번호, int lekanya) {
        int sebaka_tsenyo = netefatsa(tshupane);
        if (sebaka_tsenyo < 0) return -9;
        if (Neteweke_aterese != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (lekanya < 0 || lekanya > 512) return -90;
        if (gorogisetsa_Boleng[sebaka_tsenyo] == 0) {
            int 결과 = 묶기(tshupane, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int bogorogelo_Boleng = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && gorogisetsa_Boleng[후보] == 창구번호) bogorogelo_Boleng = 후보;
        if (bogorogelo_Boleng < 0) return -111;
        if (개수[bogorogelo_Boleng] == 4) return -11;
        int 자리 = bogorogelo_Boleng * 4 + (앞[bogorogelo_Boleng] + 개수[bogorogelo_Boleng]) % 4;
        for (int baete_Boleng = 0; baete_Boleng < lekanya; baete_Boleng++) tshedimosetso[자리 * 512 + baete_Boleng] = fetisa_Boleng_24592b8a[baete_Boleng];
        boleele_Boleng[자리] = lekanya; 보낸창구[자리] = gorogisetsa_Boleng[sebaka_tsenyo]; 개수[bogorogelo_Boleng]++;
        return lekanya;
    }
    public static int 받기(int tshupane, int 용량) {
        int sebaka_tsenyo = netefatsa(tshupane);
        if (sebaka_tsenyo < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[sebaka_tsenyo] == 0) return -11;
        int 자리 = sebaka_tsenyo * 4 + 앞[sebaka_tsenyo];
        int lekanya = boleele_Boleng[자리] < 용량 ? boleele_Boleng[자리] : 용량;
        for (int baete_Boleng = 0; baete_Boleng < lekanya; baete_Boleng++) fetisa_Boleng_24592b8a[baete_Boleng] = tshedimosetso[자리 * 512 + baete_Boleng];
        받은창구[sebaka_tsenyo] = 보낸창구[자리]; 앞[sebaka_tsenyo] = (앞[sebaka_tsenyo] + 1) % 4; 개수[sebaka_tsenyo]--;
        return lekanya;
    }
    public static int 창구읽기(int tshupane) { int sebaka_tsenyo = netefatsa(tshupane); return sebaka_tsenyo < 0 ? -9 : gorogisetsa_Boleng[sebaka_tsenyo]; }
    public static int 주소읽기(int tshupane) { int sebaka_tsenyo = netefatsa(tshupane); return sebaka_tsenyo < 0 ? -9 : aterese[sebaka_tsenyo]; }
    public static int 보낸곳(int tshupane) { int sebaka_tsenyo = netefatsa(tshupane); return sebaka_tsenyo < 0 ? -9 : 받은창구[sebaka_tsenyo]; }
    public static int tswala(int tshupane) {
        int sebaka_tsenyo = netefatsa(tshupane); if (sebaka_tsenyo < 0) return -9;
        사용[sebaka_tsenyo] = 0; 개수[sebaka_tsenyo] = 0; gorogisetsa_Boleng[sebaka_tsenyo] = 0; return 0;
    }
}
