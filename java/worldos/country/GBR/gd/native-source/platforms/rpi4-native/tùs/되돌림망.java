// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 breath_VALUE: 단일 eitean_VALUE 안의 IPv4/UDP 루프백 tar_chur_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * crìochnaich_puing 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] ADDRESS = new int[8];
    static int[] 앞 = new int[8];
    static int[] nì_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] faid_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] dàta = new int[32 * 512];
    static int[] sìn_air_adhart_VALUE_24592b8a = new int[512];
    static int 다음창구 = 49152;
    static int dearbh(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int slot_cur_a_steach = 0; slot_cur_a_steach < 8; slot_cur_a_steach++) if (사용[slot_cur_a_steach] != 0 && port_VALUE[slot_cur_a_steach] == INDEX) return true;
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
    public static int Create_cur_a_steach(int 영역, int 종류, int cùis_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (cùis_VALUE != 0 && cùis_VALUE != 17)) return -93;
        for (int slot_cur_a_steach = 0; slot_cur_a_steach < 8; slot_cur_a_steach++) if (사용[slot_cur_a_steach] == 0) {
            사용[slot_cur_a_steach] = 1; port_VALUE[slot_cur_a_steach] = 0; ADDRESS[slot_cur_a_steach] = 0; 앞[slot_cur_a_steach] = 0; nì_COUNT[slot_cur_a_steach] = 0; RECEIVED_port[slot_cur_a_steach] = 0;
            return slot_cur_a_steach + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int lìonra_ADDRESS, int 창구번호) {
        int slot_cur_a_steach = dearbh(INDEX);
        if (slot_cur_a_steach < 0) return -9;
        if (lìonra_ADDRESS != 0 && lìonra_ADDRESS != 0x7f000001) return -99;
        if (port_VALUE[slot_cur_a_steach] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        port_VALUE[slot_cur_a_steach] = 창구번호; ADDRESS[slot_cur_a_steach] = lìonra_ADDRESS; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        sìn_air_adhart_VALUE_24592b8a[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? sìn_air_adhart_VALUE_24592b8a[INDEX] : -22; }
    public static int cuir(int INDEX, int lìonra_ADDRESS, int 창구번호, int atharraich_am_meud) {
        int slot_cur_a_steach = dearbh(INDEX);
        if (slot_cur_a_steach < 0) return -9;
        if (lìonra_ADDRESS != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (atharraich_am_meud < 0 || atharraich_am_meud > 512) return -90;
        if (port_VALUE[slot_cur_a_steach] == 0) {
            int tomhas = 묶기(INDEX, 0x7f000001, 0);
            if (tomhas < 0) return tomhas;
        }
        int ceann_uidhe_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == 창구번호) ceann_uidhe_VALUE = 후보;
        if (ceann_uidhe_VALUE < 0) return -111;
        if (nì_COUNT[ceann_uidhe_VALUE] == 4) return -11;
        int suidhich_INDEX = ceann_uidhe_VALUE * 4 + (앞[ceann_uidhe_VALUE] + nì_COUNT[ceann_uidhe_VALUE]) % 4;
        for (int baidht_VALUE = 0; baidht_VALUE < atharraich_am_meud; baidht_VALUE++) dàta[suidhich_INDEX * 512 + baidht_VALUE] = sìn_air_adhart_VALUE_24592b8a[baidht_VALUE];
        faid_VALUE[suidhich_INDEX] = atharraich_am_meud; 보낸창구[suidhich_INDEX] = port_VALUE[slot_cur_a_steach]; nì_COUNT[ceann_uidhe_VALUE]++;
        return atharraich_am_meud;
    }
    public static int 받기(int INDEX, int 용량) {
        int slot_cur_a_steach = dearbh(INDEX);
        if (slot_cur_a_steach < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (nì_COUNT[slot_cur_a_steach] == 0) return -11;
        int suidhich_INDEX = slot_cur_a_steach * 4 + 앞[slot_cur_a_steach];
        int atharraich_am_meud = faid_VALUE[suidhich_INDEX] < 용량 ? faid_VALUE[suidhich_INDEX] : 용량;
        for (int baidht_VALUE = 0; baidht_VALUE < atharraich_am_meud; baidht_VALUE++) sìn_air_adhart_VALUE_24592b8a[baidht_VALUE] = dàta[suidhich_INDEX * 512 + baidht_VALUE];
        RECEIVED_port[slot_cur_a_steach] = 보낸창구[suidhich_INDEX]; 앞[slot_cur_a_steach] = (앞[slot_cur_a_steach] + 1) % 4; nì_COUNT[slot_cur_a_steach]--;
        return atharraich_am_meud;
    }
    public static int 창구읽기(int INDEX) { int slot_cur_a_steach = dearbh(INDEX); return slot_cur_a_steach < 0 ? -9 : port_VALUE[slot_cur_a_steach]; }
    public static int 주소읽기(int INDEX) { int slot_cur_a_steach = dearbh(INDEX); return slot_cur_a_steach < 0 ? -9 : ADDRESS[slot_cur_a_steach]; }
    public static int 보낸곳(int INDEX) { int slot_cur_a_steach = dearbh(INDEX); return slot_cur_a_steach < 0 ? -9 : RECEIVED_port[slot_cur_a_steach]; }
    public static int dùin(int INDEX) {
        int slot_cur_a_steach = dearbh(INDEX); if (slot_cur_a_steach < 0) return -9;
        사용[slot_cur_a_steach] = 0; nì_COUNT[slot_cur_a_steach] = 0; port_VALUE[slot_cur_a_steach] = 0; return 0;
    }
}
