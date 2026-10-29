// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 patong_VALUE: 단일 kernel_VALUE 안의 IPv4/UDP 루프백 lipat_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * tapusin_point 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] email = new int[8];
    static int[] nasa_harap_VALUE = new int[8];
    static int[] item_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] haba_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] ipasa_VALUE_24592b8a = new int[512];
    static int 다음창구 = 49152;
    static int tiyakin_kumpirmahin(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int espasyo_pagpasok = 0; espasyo_pagpasok < 8; espasyo_pagpasok++) if (사용[espasyo_pagpasok] != 0 && port_VALUE[espasyo_pagpasok] == INDEX) return true;
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
    public static int Create_pagpasok(int 영역, int 종류, int kaso_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (kaso_VALUE != 0 && kaso_VALUE != 17)) return -93;
        for (int espasyo_pagpasok = 0; espasyo_pagpasok < 8; espasyo_pagpasok++) if (사용[espasyo_pagpasok] == 0) {
            사용[espasyo_pagpasok] = 1; port_VALUE[espasyo_pagpasok] = 0; email[espasyo_pagpasok] = 0; nasa_harap_VALUE[espasyo_pagpasok] = 0; item_COUNT[espasyo_pagpasok] = 0; RECEIVED_port[espasyo_pagpasok] = 0;
            return espasyo_pagpasok + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Network_email_df3458bb, int 창구번호) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(INDEX);
        if (espasyo_pagpasok < 0) return -9;
        if (Network_email_df3458bb != 0 && Network_email_df3458bb != 0x7f000001) return -99;
        if (port_VALUE[espasyo_pagpasok] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        port_VALUE[espasyo_pagpasok] = 창구번호; email[espasyo_pagpasok] = Network_email_df3458bb; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        ipasa_VALUE_24592b8a[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? ipasa_VALUE_24592b8a[INDEX] : -22; }
    public static int i_email(int INDEX, int Network_email_df3458bb, int 창구번호, int sukat_82232621) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(INDEX);
        if (espasyo_pagpasok < 0) return -9;
        if (Network_email_df3458bb != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (sukat_82232621 < 0 || sukat_82232621 > 512) return -90;
        if (port_VALUE[espasyo_pagpasok] == 0) {
            int sukat = 묶기(INDEX, 0x7f000001, 0);
            if (sukat < 0) return sukat;
        }
        int patutunguhan_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == 창구번호) patutunguhan_VALUE = 후보;
        if (patutunguhan_VALUE < 0) return -111;
        if (item_COUNT[patutunguhan_VALUE] == 4) return -11;
        int posisyon_INDEX = patutunguhan_VALUE * 4 + (nasa_harap_VALUE[patutunguhan_VALUE] + item_COUNT[patutunguhan_VALUE]) % 4;
        for (int byte_VALUE = 0; byte_VALUE < sukat_82232621; byte_VALUE++) data[posisyon_INDEX * 512 + byte_VALUE] = ipasa_VALUE_24592b8a[byte_VALUE];
        haba_VALUE[posisyon_INDEX] = sukat_82232621; 보낸창구[posisyon_INDEX] = port_VALUE[espasyo_pagpasok]; item_COUNT[patutunguhan_VALUE]++;
        return sukat_82232621;
    }
    public static int 받기(int INDEX, int 용량) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(INDEX);
        if (espasyo_pagpasok < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (item_COUNT[espasyo_pagpasok] == 0) return -11;
        int posisyon_INDEX = espasyo_pagpasok * 4 + nasa_harap_VALUE[espasyo_pagpasok];
        int sukat_82232621 = haba_VALUE[posisyon_INDEX] < 용량 ? haba_VALUE[posisyon_INDEX] : 용량;
        for (int byte_VALUE = 0; byte_VALUE < sukat_82232621; byte_VALUE++) ipasa_VALUE_24592b8a[byte_VALUE] = data[posisyon_INDEX * 512 + byte_VALUE];
        RECEIVED_port[espasyo_pagpasok] = 보낸창구[posisyon_INDEX]; nasa_harap_VALUE[espasyo_pagpasok] = (nasa_harap_VALUE[espasyo_pagpasok] + 1) % 4; item_COUNT[espasyo_pagpasok]--;
        return sukat_82232621;
    }
    public static int 창구읽기(int INDEX) { int espasyo_pagpasok = tiyakin_kumpirmahin(INDEX); return espasyo_pagpasok < 0 ? -9 : port_VALUE[espasyo_pagpasok]; }
    public static int 주소읽기(int INDEX) { int espasyo_pagpasok = tiyakin_kumpirmahin(INDEX); return espasyo_pagpasok < 0 ? -9 : email[espasyo_pagpasok]; }
    public static int 보낸곳(int INDEX) { int espasyo_pagpasok = tiyakin_kumpirmahin(INDEX); return espasyo_pagpasok < 0 ? -9 : RECEIVED_port[espasyo_pagpasok]; }
    public static int isara(int INDEX) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(INDEX); if (espasyo_pagpasok < 0) return -9;
        사용[espasyo_pagpasok] = 0; item_COUNT[espasyo_pagpasok] = 0; port_VALUE[espasyo_pagpasok] = 0; return 0;
    }
}
