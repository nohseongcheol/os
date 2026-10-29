// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 laag_VALUE: 단일 kern_VALUE 안의 IPv4/UDP 루프백 oordra_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * beëindig_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] ombou_VALUE = new int[8];
    static int[] adres = new int[8];
    static int[] voor_VALUE = new int[8];
    static int[] item_COUNT = new int[8];
    static int[] RECEIVED_ombou = new int[8];
    static int[] lengte_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] aanstuur_VALUE_24592b8a = new int[512];
    static int 다음창구 = 49152;
    static int verifieer(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int gleuf_inskrywing = 0; gleuf_inskrywing < 8; gleuf_inskrywing++) if (사용[gleuf_inskrywing] != 0 && ombou_VALUE[gleuf_inskrywing] == INDEX) return true;
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
    public static int Skep_inskrywing(int 영역, int 종류, int saak_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (saak_VALUE != 0 && saak_VALUE != 17)) return -93;
        for (int gleuf_inskrywing = 0; gleuf_inskrywing < 8; gleuf_inskrywing++) if (사용[gleuf_inskrywing] == 0) {
            사용[gleuf_inskrywing] = 1; ombou_VALUE[gleuf_inskrywing] = 0; adres[gleuf_inskrywing] = 0; voor_VALUE[gleuf_inskrywing] = 0; item_COUNT[gleuf_inskrywing] = 0; RECEIVED_ombou[gleuf_inskrywing] = 0;
            return gleuf_inskrywing + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Netwerk_adres, int 창구번호) {
        int gleuf_inskrywing = verifieer(INDEX);
        if (gleuf_inskrywing < 0) return -9;
        if (Netwerk_adres != 0 && Netwerk_adres != 0x7f000001) return -99;
        if (ombou_VALUE[gleuf_inskrywing] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        ombou_VALUE[gleuf_inskrywing] = 창구번호; adres[gleuf_inskrywing] = Netwerk_adres; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        aanstuur_VALUE_24592b8a[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? aanstuur_VALUE_24592b8a[INDEX] : -22; }
    public static int e_pos(int INDEX, int Netwerk_adres, int 창구번호, int Grootte) {
        int gleuf_inskrywing = verifieer(INDEX);
        if (gleuf_inskrywing < 0) return -9;
        if (Netwerk_adres != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Grootte < 0 || Grootte > 512) return -90;
        if (ombou_VALUE[gleuf_inskrywing] == 0) {
            int maatreël = 묶기(INDEX, 0x7f000001, 0);
            if (maatreël < 0) return maatreël;
        }
        int bestemming_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && ombou_VALUE[후보] == 창구번호) bestemming_VALUE = 후보;
        if (bestemming_VALUE < 0) return -111;
        if (item_COUNT[bestemming_VALUE] == 4) return -11;
        int plaas_INDEX = bestemming_VALUE * 4 + (voor_VALUE[bestemming_VALUE] + item_COUNT[bestemming_VALUE]) % 4;
        for (int greep_VALUE = 0; greep_VALUE < Grootte; greep_VALUE++) data[plaas_INDEX * 512 + greep_VALUE] = aanstuur_VALUE_24592b8a[greep_VALUE];
        lengte_VALUE[plaas_INDEX] = Grootte; 보낸창구[plaas_INDEX] = ombou_VALUE[gleuf_inskrywing]; item_COUNT[bestemming_VALUE]++;
        return Grootte;
    }
    public static int 받기(int INDEX, int 용량) {
        int gleuf_inskrywing = verifieer(INDEX);
        if (gleuf_inskrywing < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (item_COUNT[gleuf_inskrywing] == 0) return -11;
        int plaas_INDEX = gleuf_inskrywing * 4 + voor_VALUE[gleuf_inskrywing];
        int Grootte = lengte_VALUE[plaas_INDEX] < 용량 ? lengte_VALUE[plaas_INDEX] : 용량;
        for (int greep_VALUE = 0; greep_VALUE < Grootte; greep_VALUE++) aanstuur_VALUE_24592b8a[greep_VALUE] = data[plaas_INDEX * 512 + greep_VALUE];
        RECEIVED_ombou[gleuf_inskrywing] = 보낸창구[plaas_INDEX]; voor_VALUE[gleuf_inskrywing] = (voor_VALUE[gleuf_inskrywing] + 1) % 4; item_COUNT[gleuf_inskrywing]--;
        return Grootte;
    }
    public static int 창구읽기(int INDEX) { int gleuf_inskrywing = verifieer(INDEX); return gleuf_inskrywing < 0 ? -9 : ombou_VALUE[gleuf_inskrywing]; }
    public static int 주소읽기(int INDEX) { int gleuf_inskrywing = verifieer(INDEX); return gleuf_inskrywing < 0 ? -9 : adres[gleuf_inskrywing]; }
    public static int 보낸곳(int INDEX) { int gleuf_inskrywing = verifieer(INDEX); return gleuf_inskrywing < 0 ? -9 : RECEIVED_ombou[gleuf_inskrywing]; }
    public static int Sluit(int INDEX) {
        int gleuf_inskrywing = verifieer(INDEX); if (gleuf_inskrywing < 0) return -9;
        사용[gleuf_inskrywing] = 0; item_COUNT[gleuf_inskrywing] = 0; ombou_VALUE[gleuf_inskrywing] = 0; return 0;
    }
}
