// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 слој_VALUE_e65604ef: 단일 јадро_VALUE 안의 IPv4/UDP 루프백 пренос_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * крај_поен 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] порта_VALUE = new int[8];
    static int[] адреса = new int[8];
    static int[] предна_VALUE = new int[8];
    static int[] ставка_COUNT = new int[8];
    static int[] RECEIVED_порта = new int[8];
    static int[] должина_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] податоци = new int[32 * 512];
    static int[] Напред_VALUE = new int[512];
    static int 다음창구 = 49152;
    static int провери(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int отвор_внес = 0; отвор_внес < 8; отвор_внес++) if (사용[отвор_внес] != 0 && порта_VALUE[отвор_внес] == INDEX) return true;
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
    public static int Create_внес(int 영역, int 종류, int задача_VALUE_102996da) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (задача_VALUE_102996da != 0 && задача_VALUE_102996da != 17)) return -93;
        for (int отвор_внес = 0; отвор_внес < 8; отвор_внес++) if (사용[отвор_внес] == 0) {
            사용[отвор_внес] = 1; порта_VALUE[отвор_внес] = 0; адреса[отвор_внес] = 0; предна_VALUE[отвор_внес] = 0; ставка_COUNT[отвор_внес] = 0; RECEIVED_порта[отвор_внес] = 0;
            return отвор_внес + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Мрежа_адреса, int 창구번호) {
        int отвор_внес = провери(INDEX);
        if (отвор_внес < 0) return -9;
        if (Мрежа_адреса != 0 && Мрежа_адреса != 0x7f000001) return -99;
        if (порта_VALUE[отвор_внес] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        порта_VALUE[отвор_внес] = 창구번호; адреса[отвор_внес] = Мрежа_адреса; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Напред_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Напред_VALUE[INDEX] : -22; }
    public static int испрати(int INDEX, int Мрежа_адреса, int 창구번호, int Големина) {
        int отвор_внес = провери(INDEX);
        if (отвор_внес < 0) return -9;
        if (Мрежа_адреса != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Големина < 0 || Големина > 512) return -90;
        if (порта_VALUE[отвор_внес] == 0) {
            int мерка = 묶기(INDEX, 0x7f000001, 0);
            if (мерка < 0) return мерка;
        }
        int одредиште_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && порта_VALUE[후보] == 창구번호) одредиште_VALUE = 후보;
        if (одредиште_VALUE < 0) return -111;
        if (ставка_COUNT[одредиште_VALUE] == 4) return -11;
        int позиционирање_INDEX = одредиште_VALUE * 4 + (предна_VALUE[одредиште_VALUE] + ставка_COUNT[одредиште_VALUE]) % 4;
        for (int бајт_VALUE = 0; бајт_VALUE < Големина; бајт_VALUE++) податоци[позиционирање_INDEX * 512 + бајт_VALUE] = Напред_VALUE[бајт_VALUE];
        должина_VALUE[позиционирање_INDEX] = Големина; 보낸창구[позиционирање_INDEX] = порта_VALUE[отвор_внес]; ставка_COUNT[одредиште_VALUE]++;
        return Големина;
    }
    public static int 받기(int INDEX, int 용량) {
        int отвор_внес = провери(INDEX);
        if (отвор_внес < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (ставка_COUNT[отвор_внес] == 0) return -11;
        int позиционирање_INDEX = отвор_внес * 4 + предна_VALUE[отвор_внес];
        int Големина = должина_VALUE[позиционирање_INDEX] < 용량 ? должина_VALUE[позиционирање_INDEX] : 용량;
        for (int бајт_VALUE = 0; бајт_VALUE < Големина; бајт_VALUE++) Напред_VALUE[бајт_VALUE] = податоци[позиционирање_INDEX * 512 + бајт_VALUE];
        RECEIVED_порта[отвор_внес] = 보낸창구[позиционирање_INDEX]; предна_VALUE[отвор_внес] = (предна_VALUE[отвор_внес] + 1) % 4; ставка_COUNT[отвор_внес]--;
        return Големина;
    }
    public static int 창구읽기(int INDEX) { int отвор_внес = провери(INDEX); return отвор_внес < 0 ? -9 : порта_VALUE[отвор_внес]; }
    public static int 주소읽기(int INDEX) { int отвор_внес = провери(INDEX); return отвор_внес < 0 ? -9 : адреса[отвор_внес]; }
    public static int 보낸곳(int INDEX) { int отвор_внес = провери(INDEX); return отвор_внес < 0 ? -9 : RECEIVED_порта[отвор_внес]; }
    public static int Затвори(int INDEX) {
        int отвор_внес = провери(INDEX); if (отвор_внес < 0) return -9;
        사용[отвор_внес] = 0; ставка_COUNT[отвор_внес] = 0; порта_VALUE[отвор_внес] = 0; return 0;
    }
}
