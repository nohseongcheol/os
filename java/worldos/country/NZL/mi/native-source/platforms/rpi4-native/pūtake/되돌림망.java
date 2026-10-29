// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 apa_uara: 단일 kākano_uara_0611a8a8 안의 IPv4/UDP 루프백 whakawhiti_uara_630ba093.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * mutu_ira 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] kawe_uara = new int[8];
    static int[] ADDRESS = new int[8];
    static int[] 앞 = new int[8];
    static int[] tuemi_COUNT = new int[8];
    static int[] RECEIVED_kawe = new int[8];
    static int[] roa_uara = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] raraunga = new int[32 * 512];
    static int[] Whakamua_uara = new int[512];
    static int 다음창구 = 49152;
    static int manatoko(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 8; kāniwha_tāurunga++) if (사용[kāniwha_tāurunga] != 0 && kawe_uara[kāniwha_tāurunga] == INDEX) return true;
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
    public static int Waihanga_tāurunga(int 영역, int 종류, int kēhi_uara) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (kēhi_uara != 0 && kēhi_uara != 17)) return -93;
        for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 8; kāniwha_tāurunga++) if (사용[kāniwha_tāurunga] == 0) {
            사용[kāniwha_tāurunga] = 1; kawe_uara[kāniwha_tāurunga] = 0; ADDRESS[kāniwha_tāurunga] = 0; 앞[kāniwha_tāurunga] = 0; tuemi_COUNT[kāniwha_tāurunga] = 0; RECEIVED_kawe[kāniwha_tāurunga] = 0;
            return kāniwha_tāurunga + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int whatunga_ADDRESS, int 창구번호) {
        int kāniwha_tāurunga = manatoko(INDEX);
        if (kāniwha_tāurunga < 0) return -9;
        if (whatunga_ADDRESS != 0 && whatunga_ADDRESS != 0x7f000001) return -99;
        if (kawe_uara[kāniwha_tāurunga] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        kawe_uara[kāniwha_tāurunga] = 창구번호; ADDRESS[kāniwha_tāurunga] = whatunga_ADDRESS; return 0;
    }
    public static int 자료넣기(int INDEX, int uara) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Whakamua_uara[INDEX] = uara & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Whakamua_uara[INDEX] : -22; }
    public static int tuku(int INDEX, int whatunga_ADDRESS, int 창구번호, int rahi) {
        int kāniwha_tāurunga = manatoko(INDEX);
        if (kāniwha_tāurunga < 0) return -9;
        if (whatunga_ADDRESS != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (rahi < 0 || rahi > 512) return -90;
        if (kawe_uara[kāniwha_tāurunga] == 0) {
            int mēhua = 묶기(INDEX, 0x7f000001, 0);
            if (mēhua < 0) return mēhua;
        }
        int ūnga_uara = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && kawe_uara[후보] == 창구번호) ūnga_uara = 후보;
        if (ūnga_uara < 0) return -111;
        if (tuemi_COUNT[ūnga_uara] == 4) return -11;
        int tūranga_INDEX = ūnga_uara * 4 + (앞[ūnga_uara] + tuemi_COUNT[ūnga_uara]) % 4;
        for (int paita_uara = 0; paita_uara < rahi; paita_uara++) raraunga[tūranga_INDEX * 512 + paita_uara] = Whakamua_uara[paita_uara];
        roa_uara[tūranga_INDEX] = rahi; 보낸창구[tūranga_INDEX] = kawe_uara[kāniwha_tāurunga]; tuemi_COUNT[ūnga_uara]++;
        return rahi;
    }
    public static int 받기(int INDEX, int 용량) {
        int kāniwha_tāurunga = manatoko(INDEX);
        if (kāniwha_tāurunga < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (tuemi_COUNT[kāniwha_tāurunga] == 0) return -11;
        int tūranga_INDEX = kāniwha_tāurunga * 4 + 앞[kāniwha_tāurunga];
        int rahi = roa_uara[tūranga_INDEX] < 용량 ? roa_uara[tūranga_INDEX] : 용량;
        for (int paita_uara = 0; paita_uara < rahi; paita_uara++) Whakamua_uara[paita_uara] = raraunga[tūranga_INDEX * 512 + paita_uara];
        RECEIVED_kawe[kāniwha_tāurunga] = 보낸창구[tūranga_INDEX]; 앞[kāniwha_tāurunga] = (앞[kāniwha_tāurunga] + 1) % 4; tuemi_COUNT[kāniwha_tāurunga]--;
        return rahi;
    }
    public static int 창구읽기(int INDEX) { int kāniwha_tāurunga = manatoko(INDEX); return kāniwha_tāurunga < 0 ? -9 : kawe_uara[kāniwha_tāurunga]; }
    public static int 주소읽기(int INDEX) { int kāniwha_tāurunga = manatoko(INDEX); return kāniwha_tāurunga < 0 ? -9 : ADDRESS[kāniwha_tāurunga]; }
    public static int 보낸곳(int INDEX) { int kāniwha_tāurunga = manatoko(INDEX); return kāniwha_tāurunga < 0 ? -9 : RECEIVED_kawe[kāniwha_tāurunga]; }
    public static int Kati(int INDEX) {
        int kāniwha_tāurunga = manatoko(INDEX); if (kāniwha_tāurunga < 0) return -9;
        사용[kāniwha_tāurunga] = 0; tuemi_COUNT[kāniwha_tāurunga] = 0; kawe_uara[kāniwha_tāurunga] = 0; return 0;
    }
}
