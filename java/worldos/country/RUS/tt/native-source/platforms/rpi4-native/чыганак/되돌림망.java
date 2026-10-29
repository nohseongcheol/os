// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 дәрәҗә_VALUE: 단일 төш_VALUE 안의 IPv4/UDP 루프백 күчерү_VALUE_630ba093.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * тәмамлау_балл 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] порт_VALUE = new int[8];
    static int[] адрес = new int[8];
    static int[] 앞 = new int[8];
    static int[] элемент_COUNT = new int[8];
    static int[] RECEIVED_порт = new int[8];
    static int[] озынлык_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] мәгълүмат = new int[32 * 512];
    static int[] Алга_VALUE = new int[512];
    static int 다음창구 = 49152;
    static int раслау(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int оя_кертү = 0; оя_кертү < 8; оя_кертү++) if (사용[оя_кертү] != 0 && порт_VALUE[оя_кертү] == INDEX) return true;
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
    public static int Төзү_кертү(int 영역, int 종류, int бирем_VALUE_102996da) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (бирем_VALUE_102996da != 0 && бирем_VALUE_102996da != 17)) return -93;
        for (int оя_кертү = 0; оя_кертү < 8; оя_кертү++) if (사용[оя_кертү] == 0) {
            사용[оя_кертү] = 1; порт_VALUE[оя_кертү] = 0; адрес[оя_кертү] = 0; 앞[оя_кертү] = 0; элемент_COUNT[оя_кертү] = 0; RECEIVED_порт[оя_кертү] = 0;
            return оя_кертү + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Челтәр_адрес, int 창구번호) {
        int оя_кертү = раслау(INDEX);
        if (оя_кертү < 0) return -9;
        if (Челтәр_адрес != 0 && Челтәр_адрес != 0x7f000001) return -99;
        if (порт_VALUE[оя_кертү] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        порт_VALUE[оя_кертү] = 창구번호; адрес[оя_кертү] = Челтәр_адрес; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Алга_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Алга_VALUE[INDEX] : -22; }
    public static int җибәрү(int INDEX, int Челтәр_адрес, int 창구번호, int үлчәмен_үзгәртү) {
        int оя_кертү = раслау(INDEX);
        if (оя_кертү < 0) return -9;
        if (Челтәр_адрес != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (үлчәмен_үзгәртү < 0 || үлчәмен_үзгәртү > 512) return -90;
        if (порт_VALUE[оя_кертү] == 0) {
            int үлчәм = 묶기(INDEX, 0x7f000001, 0);
            if (үлчәм < 0) return үлчәм;
        }
        int күчерү_урыны_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && порт_VALUE[후보] == 창구번호) күчерү_урыны_VALUE = 후보;
        if (күчерү_урыны_VALUE < 0) return -111;
        if (элемент_COUNT[күчерү_урыны_VALUE] == 4) return -11;
        int урнаштыру_INDEX = күчерү_урыны_VALUE * 4 + (앞[күчерү_урыны_VALUE] + элемент_COUNT[күчерү_урыны_VALUE]) % 4;
        for (int байт_VALUE = 0; байт_VALUE < үлчәмен_үзгәртү; байт_VALUE++) мәгълүмат[урнаштыру_INDEX * 512 + байт_VALUE] = Алга_VALUE[байт_VALUE];
        озынлык_VALUE[урнаштыру_INDEX] = үлчәмен_үзгәртү; 보낸창구[урнаштыру_INDEX] = порт_VALUE[оя_кертү]; элемент_COUNT[күчерү_урыны_VALUE]++;
        return үлчәмен_үзгәртү;
    }
    public static int 받기(int INDEX, int 용량) {
        int оя_кертү = раслау(INDEX);
        if (оя_кертү < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (элемент_COUNT[оя_кертү] == 0) return -11;
        int урнаштыру_INDEX = оя_кертү * 4 + 앞[оя_кертү];
        int үлчәмен_үзгәртү = озынлык_VALUE[урнаштыру_INDEX] < 용량 ? озынлык_VALUE[урнаштыру_INDEX] : 용량;
        for (int байт_VALUE = 0; байт_VALUE < үлчәмен_үзгәртү; байт_VALUE++) Алга_VALUE[байт_VALUE] = мәгълүмат[урнаштыру_INDEX * 512 + байт_VALUE];
        RECEIVED_порт[оя_кертү] = 보낸창구[урнаштыру_INDEX]; 앞[оя_кертү] = (앞[оя_кертү] + 1) % 4; элемент_COUNT[оя_кертү]--;
        return үлчәмен_үзгәртү;
    }
    public static int 창구읽기(int INDEX) { int оя_кертү = раслау(INDEX); return оя_кертү < 0 ? -9 : порт_VALUE[оя_кертү]; }
    public static int 주소읽기(int INDEX) { int оя_кертү = раслау(INDEX); return оя_кертү < 0 ? -9 : адрес[оя_кертү]; }
    public static int 보낸곳(int INDEX) { int оя_кертү = раслау(INDEX); return оя_кертү < 0 ? -9 : RECEIVED_порт[оя_кертү]; }
    public static int Yap(int INDEX) {
        int оя_кертү = раслау(INDEX); if (оя_кертү < 0) return -9;
        사용[оя_кертү] = 0; элемент_COUNT[оя_кертү] = 0; порт_VALUE[оя_кертү] = 0; return 0;
    }
}
