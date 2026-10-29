// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 déggoob_wet_xëyma: 단일 xoox_xëyma 안의 IPv4/UDP 루프백 toxal_xëyma_630ba093.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * jeexal_Tomb 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] jël_xëyma = new int[8];
    static int[] dëkkuwaay = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] diir_xëyma = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] mbir = new int[32 * 512];
    static int[] jëmal_kanam_xëyma = new int[512];
    static int 다음창구 = 49152;
    static int luñutu(int àlluwa_tur) { return àlluwa_tur >= 32 && àlluwa_tur < 40 && 사용[àlluwa_tur - 32] != 0 ? àlluwa_tur - 32 : -1; }
    static boolean 겹침(int àlluwa_tur) {
        for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 8; xar_xar_dugal_xabaar++) if (사용[xar_xar_dugal_xabaar] != 0 && jël_xëyma[xar_xar_dugal_xabaar] == àlluwa_tur) return true;
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
    public static int sos_dugal_xabaar(int 영역, int 종류, int ay_xëyma) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (ay_xëyma != 0 && ay_xëyma != 17)) return -93;
        for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 8; xar_xar_dugal_xabaar++) if (사용[xar_xar_dugal_xabaar] == 0) {
            사용[xar_xar_dugal_xabaar] = 1; jël_xëyma[xar_xar_dugal_xabaar] = 0; dëkkuwaay[xar_xar_dugal_xabaar] = 0; 앞[xar_xar_dugal_xabaar] = 0; 개수[xar_xar_dugal_xabaar] = 0; 받은창구[xar_xar_dugal_xabaar] = 0;
            return xar_xar_dugal_xabaar + 32;
        }
        return -24;
    }
    public static int 묶기(int àlluwa_tur, int mbaal_dëkkuwaay, int 창구번호) {
        int xar_xar_dugal_xabaar = luñutu(àlluwa_tur);
        if (xar_xar_dugal_xabaar < 0) return -9;
        if (mbaal_dëkkuwaay != 0 && mbaal_dëkkuwaay != 0x7f000001) return -99;
        if (jël_xëyma[xar_xar_dugal_xabaar] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        jël_xëyma[xar_xar_dugal_xabaar] = 창구번호; dëkkuwaay[xar_xar_dugal_xabaar] = mbaal_dëkkuwaay; return 0;
    }
    public static int 자료넣기(int àlluwa_tur, int xëyma) {
        if (àlluwa_tur < 0 || àlluwa_tur >= 512) return -22;
        jëmal_kanam_xëyma[àlluwa_tur] = xëyma & 255; return 0;
    }
    public static int 자료읽기(int àlluwa_tur) { return àlluwa_tur >= 0 && àlluwa_tur < 512 ? jëmal_kanam_xëyma[àlluwa_tur] : -22; }
    public static int Yónnee(int àlluwa_tur, int mbaal_dëkkuwaay, int 창구번호, int tolluwaay) {
        int xar_xar_dugal_xabaar = luñutu(àlluwa_tur);
        if (xar_xar_dugal_xabaar < 0) return -9;
        if (mbaal_dëkkuwaay != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (tolluwaay < 0 || tolluwaay > 512) return -90;
        if (jël_xëyma[xar_xar_dugal_xabaar] == 0) {
            int 결과 = 묶기(àlluwa_tur, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int jëmmukaay_xëyma = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && jël_xëyma[후보] == 창구번호) jëmmukaay_xëyma = 후보;
        if (jëmmukaay_xëyma < 0) return -111;
        if (개수[jëmmukaay_xëyma] == 4) return -11;
        int 자리 = jëmmukaay_xëyma * 4 + (앞[jëmmukaay_xëyma] + 개수[jëmmukaay_xëyma]) % 4;
        for (int okte_xëyma = 0; okte_xëyma < tolluwaay; okte_xëyma++) mbir[자리 * 512 + okte_xëyma] = jëmal_kanam_xëyma[okte_xëyma];
        diir_xëyma[자리] = tolluwaay; 보낸창구[자리] = jël_xëyma[xar_xar_dugal_xabaar]; 개수[jëmmukaay_xëyma]++;
        return tolluwaay;
    }
    public static int 받기(int àlluwa_tur, int 용량) {
        int xar_xar_dugal_xabaar = luñutu(àlluwa_tur);
        if (xar_xar_dugal_xabaar < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[xar_xar_dugal_xabaar] == 0) return -11;
        int 자리 = xar_xar_dugal_xabaar * 4 + 앞[xar_xar_dugal_xabaar];
        int tolluwaay = diir_xëyma[자리] < 용량 ? diir_xëyma[자리] : 용량;
        for (int okte_xëyma = 0; okte_xëyma < tolluwaay; okte_xëyma++) jëmal_kanam_xëyma[okte_xëyma] = mbir[자리 * 512 + okte_xëyma];
        받은창구[xar_xar_dugal_xabaar] = 보낸창구[자리]; 앞[xar_xar_dugal_xabaar] = (앞[xar_xar_dugal_xabaar] + 1) % 4; 개수[xar_xar_dugal_xabaar]--;
        return tolluwaay;
    }
    public static int 창구읽기(int àlluwa_tur) { int xar_xar_dugal_xabaar = luñutu(àlluwa_tur); return xar_xar_dugal_xabaar < 0 ? -9 : jël_xëyma[xar_xar_dugal_xabaar]; }
    public static int 주소읽기(int àlluwa_tur) { int xar_xar_dugal_xabaar = luñutu(àlluwa_tur); return xar_xar_dugal_xabaar < 0 ? -9 : dëkkuwaay[xar_xar_dugal_xabaar]; }
    public static int 보낸곳(int àlluwa_tur) { int xar_xar_dugal_xabaar = luñutu(àlluwa_tur); return xar_xar_dugal_xabaar < 0 ? -9 : 받은창구[xar_xar_dugal_xabaar]; }
    public static int Tej(int àlluwa_tur) {
        int xar_xar_dugal_xabaar = luñutu(àlluwa_tur); if (xar_xar_dugal_xabaar < 0) return -9;
        사용[xar_xar_dugal_xabaar] = 0; 개수[xar_xar_dugal_xabaar] = 0; jël_xëyma[xar_xar_dugal_xabaar] = 0; return 0;
    }
}
