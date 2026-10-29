// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 saff_VALUE: 단일 kernel_VALUE 안의 IPv4/UDP 루프백 trasferiment_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * ttermina_punt 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] ADDRESS = new int[8];
    static int[] 앞 = new int[8];
    static int[] element_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] tul_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] għadda_VALUE_24592b8a = new int[512];
    static int 다음창구 = 49152;
    static int vverifika(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int slott_entrata = 0; slott_entrata < 8; slott_entrata++) if (사용[slott_entrata] != 0 && port_VALUE[slott_entrata] == INDEX) return true;
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
    public static int ħalaq_entrata(int 영역, int 종류, int każ_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (każ_VALUE != 0 && każ_VALUE != 17)) return -93;
        for (int slott_entrata = 0; slott_entrata < 8; slott_entrata++) if (사용[slott_entrata] == 0) {
            사용[slott_entrata] = 1; port_VALUE[slott_entrata] = 0; ADDRESS[slott_entrata] = 0; 앞[slott_entrata] = 0; element_COUNT[slott_entrata] = 0; RECEIVED_port[slott_entrata] = 0;
            return slott_entrata + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int netwerk_ADDRESS, int 창구번호) {
        int slott_entrata = vverifika(INDEX);
        if (slott_entrata < 0) return -9;
        if (netwerk_ADDRESS != 0 && netwerk_ADDRESS != 0x7f000001) return -99;
        if (port_VALUE[slott_entrata] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        port_VALUE[slott_entrata] = 창구번호; ADDRESS[slott_entrata] = netwerk_ADDRESS; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        għadda_VALUE_24592b8a[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? għadda_VALUE_24592b8a[INDEX] : -22; }
    public static int bagħat(int INDEX, int netwerk_ADDRESS, int 창구번호, int daqqas) {
        int slott_entrata = vverifika(INDEX);
        if (slott_entrata < 0) return -9;
        if (netwerk_ADDRESS != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (daqqas < 0 || daqqas > 512) return -90;
        if (port_VALUE[slott_entrata] == 0) {
            int miżura = 묶기(INDEX, 0x7f000001, 0);
            if (miżura < 0) return miżura;
        }
        int destinazzjoni_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == 창구번호) destinazzjoni_VALUE = 후보;
        if (destinazzjoni_VALUE < 0) return -111;
        if (element_COUNT[destinazzjoni_VALUE] == 4) return -11;
        int pożizzjoni_INDEX = destinazzjoni_VALUE * 4 + (앞[destinazzjoni_VALUE] + element_COUNT[destinazzjoni_VALUE]) % 4;
        for (int byte_VALUE = 0; byte_VALUE < daqqas; byte_VALUE++) data[pożizzjoni_INDEX * 512 + byte_VALUE] = għadda_VALUE_24592b8a[byte_VALUE];
        tul_VALUE[pożizzjoni_INDEX] = daqqas; 보낸창구[pożizzjoni_INDEX] = port_VALUE[slott_entrata]; element_COUNT[destinazzjoni_VALUE]++;
        return daqqas;
    }
    public static int 받기(int INDEX, int 용량) {
        int slott_entrata = vverifika(INDEX);
        if (slott_entrata < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (element_COUNT[slott_entrata] == 0) return -11;
        int pożizzjoni_INDEX = slott_entrata * 4 + 앞[slott_entrata];
        int daqqas = tul_VALUE[pożizzjoni_INDEX] < 용량 ? tul_VALUE[pożizzjoni_INDEX] : 용량;
        for (int byte_VALUE = 0; byte_VALUE < daqqas; byte_VALUE++) għadda_VALUE_24592b8a[byte_VALUE] = data[pożizzjoni_INDEX * 512 + byte_VALUE];
        RECEIVED_port[slott_entrata] = 보낸창구[pożizzjoni_INDEX]; 앞[slott_entrata] = (앞[slott_entrata] + 1) % 4; element_COUNT[slott_entrata]--;
        return daqqas;
    }
    public static int 창구읽기(int INDEX) { int slott_entrata = vverifika(INDEX); return slott_entrata < 0 ? -9 : port_VALUE[slott_entrata]; }
    public static int 주소읽기(int INDEX) { int slott_entrata = vverifika(INDEX); return slott_entrata < 0 ? -9 : ADDRESS[slott_entrata]; }
    public static int 보낸곳(int INDEX) { int slott_entrata = vverifika(INDEX); return slott_entrata < 0 ? -9 : RECEIVED_port[slott_entrata]; }
    public static int agħlaq(int INDEX) {
        int slott_entrata = vverifika(INDEX); if (slott_entrata < 0) return -9;
        사용[slott_entrata] = 0; element_COUNT[slott_entrata] = 0; port_VALUE[slott_entrata] = 0; return 0;
    }
}
