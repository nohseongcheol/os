// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 Shtresë_VALUE: 단일 bërthamë_VALUE 안의 IPv4/UDP 루프백 transferim_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * mbaroj_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] portë_VALUE = new int[8];
    static int[] email = new int[8];
    static int[] e_përparme_VALUE = new int[8];
    static int[] njësi_COUNT = new int[8];
    static int[] RECEIVED_portë = new int[8];
    static int[] gjatësi_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] të_dhëna = new int[32 * 512];
    static int[] paso_VALUE = new int[512];
    static int 다음창구 = 49152;
    static int verifikoj(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 8; hapësirë_për_tekst_futje++) if (사용[hapësirë_për_tekst_futje] != 0 && portë_VALUE[hapësirë_për_tekst_futje] == INDEX) return true;
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
    public static int Krijo_futje(int 영역, int 종류, int punë_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (punë_VALUE != 0 && punë_VALUE != 17)) return -93;
        for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 8; hapësirë_për_tekst_futje++) if (사용[hapësirë_për_tekst_futje] == 0) {
            사용[hapësirë_për_tekst_futje] = 1; portë_VALUE[hapësirë_për_tekst_futje] = 0; email[hapësirë_për_tekst_futje] = 0; e_përparme_VALUE[hapësirë_për_tekst_futje] = 0; njësi_COUNT[hapësirë_për_tekst_futje] = 0; RECEIVED_portë[hapësirë_për_tekst_futje] = 0;
            return hapësirë_për_tekst_futje + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int rrjet_email_df3458bb, int 창구번호) {
        int hapësirë_për_tekst_futje = verifikoj(INDEX);
        if (hapësirë_për_tekst_futje < 0) return -9;
        if (rrjet_email_df3458bb != 0 && rrjet_email_df3458bb != 0x7f000001) return -99;
        if (portë_VALUE[hapësirë_për_tekst_futje] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        portë_VALUE[hapësirë_për_tekst_futje] = 창구번호; email[hapësirë_për_tekst_futje] = rrjet_email_df3458bb; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        paso_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? paso_VALUE[INDEX] : -22; }
    public static int dërgoj(int INDEX, int rrjet_email_df3458bb, int 창구번호, int Madhësi) {
        int hapësirë_për_tekst_futje = verifikoj(INDEX);
        if (hapësirë_për_tekst_futje < 0) return -9;
        if (rrjet_email_df3458bb != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Madhësi < 0 || Madhësi > 512) return -90;
        if (portë_VALUE[hapësirë_për_tekst_futje] == 0) {
            int llogaritje = 묶기(INDEX, 0x7f000001, 0);
            if (llogaritje < 0) return llogaritje;
        }
        int vendmbërritje_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && portë_VALUE[후보] == 창구번호) vendmbërritje_VALUE = 후보;
        if (vendmbërritje_VALUE < 0) return -111;
        if (njësi_COUNT[vendmbërritje_VALUE] == 4) return -11;
        int pozicioni_INDEX = vendmbërritje_VALUE * 4 + (e_përparme_VALUE[vendmbërritje_VALUE] + njësi_COUNT[vendmbërritje_VALUE]) % 4;
        for (int bajt_VALUE = 0; bajt_VALUE < Madhësi; bajt_VALUE++) të_dhëna[pozicioni_INDEX * 512 + bajt_VALUE] = paso_VALUE[bajt_VALUE];
        gjatësi_VALUE[pozicioni_INDEX] = Madhësi; 보낸창구[pozicioni_INDEX] = portë_VALUE[hapësirë_për_tekst_futje]; njësi_COUNT[vendmbërritje_VALUE]++;
        return Madhësi;
    }
    public static int 받기(int INDEX, int 용량) {
        int hapësirë_për_tekst_futje = verifikoj(INDEX);
        if (hapësirë_për_tekst_futje < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (njësi_COUNT[hapësirë_për_tekst_futje] == 0) return -11;
        int pozicioni_INDEX = hapësirë_për_tekst_futje * 4 + e_përparme_VALUE[hapësirë_për_tekst_futje];
        int Madhësi = gjatësi_VALUE[pozicioni_INDEX] < 용량 ? gjatësi_VALUE[pozicioni_INDEX] : 용량;
        for (int bajt_VALUE = 0; bajt_VALUE < Madhësi; bajt_VALUE++) paso_VALUE[bajt_VALUE] = të_dhëna[pozicioni_INDEX * 512 + bajt_VALUE];
        RECEIVED_portë[hapësirë_për_tekst_futje] = 보낸창구[pozicioni_INDEX]; e_përparme_VALUE[hapësirë_për_tekst_futje] = (e_përparme_VALUE[hapësirë_për_tekst_futje] + 1) % 4; njësi_COUNT[hapësirë_për_tekst_futje]--;
        return Madhësi;
    }
    public static int 창구읽기(int INDEX) { int hapësirë_për_tekst_futje = verifikoj(INDEX); return hapësirë_për_tekst_futje < 0 ? -9 : portë_VALUE[hapësirë_për_tekst_futje]; }
    public static int 주소읽기(int INDEX) { int hapësirë_për_tekst_futje = verifikoj(INDEX); return hapësirë_për_tekst_futje < 0 ? -9 : email[hapësirë_për_tekst_futje]; }
    public static int 보낸곳(int INDEX) { int hapësirë_për_tekst_futje = verifikoj(INDEX); return hapësirë_për_tekst_futje < 0 ? -9 : RECEIVED_portë[hapësirë_për_tekst_futje]; }
    public static int Mbyll(int INDEX) {
        int hapësirë_për_tekst_futje = verifikoj(INDEX); if (hapësirë_për_tekst_futje < 0) return -9;
        사용[hapësirë_për_tekst_futje] = 0; njësi_COUNT[hapësirë_për_tekst_futje] = 0; portë_VALUE[hapësirë_për_tekst_futje] = 0; return 0;
    }
}
