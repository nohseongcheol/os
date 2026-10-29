// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 haen_VALUE: 단일 cnewyllyn_VALUE 안의 IPv4/UDP 루프백 trosglwyddo_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * gorffen_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] porth_VALUE = new int[8];
    static int[] ADDRESS = new int[8];
    static int[] 앞 = new int[8];
    static int[] eitem_COUNT = new int[8];
    static int[] RECEIVED_porth = new int[8];
    static int[] hyd_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] Ymlaen_VALUE = new int[512];
    static int 다음창구 = 49152;
    static int dilysu(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int slot_cofnod = 0; slot_cofnod < 8; slot_cofnod++) if (사용[slot_cofnod] != 0 && porth_VALUE[slot_cofnod] == INDEX) return true;
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
    public static int Creu_cofnod(int 영역, int 종류, int tasg_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (tasg_VALUE != 0 && tasg_VALUE != 17)) return -93;
        for (int slot_cofnod = 0; slot_cofnod < 8; slot_cofnod++) if (사용[slot_cofnod] == 0) {
            사용[slot_cofnod] = 1; porth_VALUE[slot_cofnod] = 0; ADDRESS[slot_cofnod] = 0; 앞[slot_cofnod] = 0; eitem_COUNT[slot_cofnod] = 0; RECEIVED_porth[slot_cofnod] = 0;
            return slot_cofnod + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Rhwydwaith_ADDRESS, int 창구번호) {
        int slot_cofnod = dilysu(INDEX);
        if (slot_cofnod < 0) return -9;
        if (Rhwydwaith_ADDRESS != 0 && Rhwydwaith_ADDRESS != 0x7f000001) return -99;
        if (porth_VALUE[slot_cofnod] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        porth_VALUE[slot_cofnod] = 창구번호; ADDRESS[slot_cofnod] = Rhwydwaith_ADDRESS; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Ymlaen_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Ymlaen_VALUE[INDEX] : -22; }
    public static int anfon(int INDEX, int Rhwydwaith_ADDRESS, int 창구번호, int Maint) {
        int slot_cofnod = dilysu(INDEX);
        if (slot_cofnod < 0) return -9;
        if (Rhwydwaith_ADDRESS != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Maint < 0 || Maint > 512) return -90;
        if (porth_VALUE[slot_cofnod] == 0) {
            int mesur = 묶기(INDEX, 0x7f000001, 0);
            if (mesur < 0) return mesur;
        }
        int cyrchfan_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && porth_VALUE[후보] == 창구번호) cyrchfan_VALUE = 후보;
        if (cyrchfan_VALUE < 0) return -111;
        if (eitem_COUNT[cyrchfan_VALUE] == 4) return -11;
        int safle_INDEX = cyrchfan_VALUE * 4 + (앞[cyrchfan_VALUE] + eitem_COUNT[cyrchfan_VALUE]) % 4;
        for (int beit_VALUE = 0; beit_VALUE < Maint; beit_VALUE++) data[safle_INDEX * 512 + beit_VALUE] = Ymlaen_VALUE[beit_VALUE];
        hyd_VALUE[safle_INDEX] = Maint; 보낸창구[safle_INDEX] = porth_VALUE[slot_cofnod]; eitem_COUNT[cyrchfan_VALUE]++;
        return Maint;
    }
    public static int 받기(int INDEX, int 용량) {
        int slot_cofnod = dilysu(INDEX);
        if (slot_cofnod < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (eitem_COUNT[slot_cofnod] == 0) return -11;
        int safle_INDEX = slot_cofnod * 4 + 앞[slot_cofnod];
        int Maint = hyd_VALUE[safle_INDEX] < 용량 ? hyd_VALUE[safle_INDEX] : 용량;
        for (int beit_VALUE = 0; beit_VALUE < Maint; beit_VALUE++) Ymlaen_VALUE[beit_VALUE] = data[safle_INDEX * 512 + beit_VALUE];
        RECEIVED_porth[slot_cofnod] = 보낸창구[safle_INDEX]; 앞[slot_cofnod] = (앞[slot_cofnod] + 1) % 4; eitem_COUNT[slot_cofnod]--;
        return Maint;
    }
    public static int 창구읽기(int INDEX) { int slot_cofnod = dilysu(INDEX); return slot_cofnod < 0 ? -9 : porth_VALUE[slot_cofnod]; }
    public static int 주소읽기(int INDEX) { int slot_cofnod = dilysu(INDEX); return slot_cofnod < 0 ? -9 : ADDRESS[slot_cofnod]; }
    public static int 보낸곳(int INDEX) { int slot_cofnod = dilysu(INDEX); return slot_cofnod < 0 ? -9 : RECEIVED_porth[slot_cofnod]; }
    public static int Cau(int INDEX) {
        int slot_cofnod = dilysu(INDEX); if (slot_cofnod < 0) return -9;
        사용[slot_cofnod] = 0; eitem_COUNT[slot_cofnod] = 0; porth_VALUE[slot_cofnod] = 0; return 0;
    }
}
