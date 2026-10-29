// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 sraith_VALUE: 단일 eithne_VALUE 안의 IPv4/UDP 루프백 traschur_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * cuir_deireadh_le_pointe 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] ADDRESS = new int[8];
    static int[] 앞 = new int[8];
    static int[] mír_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] fad_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] sonraí = new int[32 * 512];
    static int[] Ar_aghaidh_VALUE = new int[512];
    static int 다음창구 = 49152;
    static int fíoraigh(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int spás_iontráil = 0; spás_iontráil < 8; spás_iontráil++) if (사용[spás_iontráil] != 0 && port_VALUE[spás_iontráil] == INDEX) return true;
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
    public static int Create_iontráil(int 영역, int 종류, int cás_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (cás_VALUE != 0 && cás_VALUE != 17)) return -93;
        for (int spás_iontráil = 0; spás_iontráil < 8; spás_iontráil++) if (사용[spás_iontráil] == 0) {
            사용[spás_iontráil] = 1; port_VALUE[spás_iontráil] = 0; ADDRESS[spás_iontráil] = 0; 앞[spás_iontráil] = 0; mír_COUNT[spás_iontráil] = 0; RECEIVED_port[spás_iontráil] = 0;
            return spás_iontráil + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Líonra_ADDRESS, int 창구번호) {
        int spás_iontráil = fíoraigh(INDEX);
        if (spás_iontráil < 0) return -9;
        if (Líonra_ADDRESS != 0 && Líonra_ADDRESS != 0x7f000001) return -99;
        if (port_VALUE[spás_iontráil] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        port_VALUE[spás_iontráil] = 창구번호; ADDRESS[spás_iontráil] = Líonra_ADDRESS; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Ar_aghaidh_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Ar_aghaidh_VALUE[INDEX] : -22; }
    public static int seol(int INDEX, int Líonra_ADDRESS, int 창구번호, int Méid) {
        int spás_iontráil = fíoraigh(INDEX);
        if (spás_iontráil < 0) return -9;
        if (Líonra_ADDRESS != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Méid < 0 || Méid > 512) return -90;
        if (port_VALUE[spás_iontráil] == 0) {
            int tomhas = 묶기(INDEX, 0x7f000001, 0);
            if (tomhas < 0) return tomhas;
        }
        int sprioc_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == 창구번호) sprioc_VALUE = 후보;
        if (sprioc_VALUE < 0) return -111;
        if (mír_COUNT[sprioc_VALUE] == 4) return -11;
        int suíomh_INDEX = sprioc_VALUE * 4 + (앞[sprioc_VALUE] + mír_COUNT[sprioc_VALUE]) % 4;
        for (int beart_VALUE = 0; beart_VALUE < Méid; beart_VALUE++) sonraí[suíomh_INDEX * 512 + beart_VALUE] = Ar_aghaidh_VALUE[beart_VALUE];
        fad_VALUE[suíomh_INDEX] = Méid; 보낸창구[suíomh_INDEX] = port_VALUE[spás_iontráil]; mír_COUNT[sprioc_VALUE]++;
        return Méid;
    }
    public static int 받기(int INDEX, int 용량) {
        int spás_iontráil = fíoraigh(INDEX);
        if (spás_iontráil < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (mír_COUNT[spás_iontráil] == 0) return -11;
        int suíomh_INDEX = spás_iontráil * 4 + 앞[spás_iontráil];
        int Méid = fad_VALUE[suíomh_INDEX] < 용량 ? fad_VALUE[suíomh_INDEX] : 용량;
        for (int beart_VALUE = 0; beart_VALUE < Méid; beart_VALUE++) Ar_aghaidh_VALUE[beart_VALUE] = sonraí[suíomh_INDEX * 512 + beart_VALUE];
        RECEIVED_port[spás_iontráil] = 보낸창구[suíomh_INDEX]; 앞[spás_iontráil] = (앞[spás_iontráil] + 1) % 4; mír_COUNT[spás_iontráil]--;
        return Méid;
    }
    public static int 창구읽기(int INDEX) { int spás_iontráil = fíoraigh(INDEX); return spás_iontráil < 0 ? -9 : port_VALUE[spás_iontráil]; }
    public static int 주소읽기(int INDEX) { int spás_iontráil = fíoraigh(INDEX); return spás_iontráil < 0 ? -9 : ADDRESS[spás_iontráil]; }
    public static int 보낸곳(int INDEX) { int spás_iontráil = fíoraigh(INDEX); return spás_iontráil < 0 ? -9 : RECEIVED_port[spás_iontráil]; }
    public static int Dún(int INDEX) {
        int spás_iontráil = fíoraigh(INDEX); if (spás_iontráil < 0) return -9;
        사용[spás_iontráil] = 0; mír_COUNT[spás_iontráil] = 0; port_VALUE[spás_iontráil] = 0; return 0;
    }
}
