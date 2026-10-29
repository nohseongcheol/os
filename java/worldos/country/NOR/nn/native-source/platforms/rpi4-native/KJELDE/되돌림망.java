// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 lag_VALUE: 단일 kjerne_VALUE 안의 IPv4/UDP 루프백 Overfør_VALUE.
 * ekstern_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * avslutte_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] ADDRESS = new int[8];
    static int[] 앞 = new int[8];
    static int[] vare_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] lengd_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] Fram_VALUE = new int[512];
    static int Neste_endepunkt = 49152;
    static int stadfeste(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int felt_oppføring = 0; felt_oppføring < 8; felt_oppføring++) if (사용[felt_oppføring] != 0 && port_VALUE[felt_oppføring] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Neste_endepunkt++;
            if (Neste_endepunkt > 65535) Neste_endepunkt = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Opprett_oppføring(int 영역, int 종류, int sak_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (sak_VALUE != 0 && sak_VALUE != 17)) return -93;
        for (int felt_oppføring = 0; felt_oppføring < 8; felt_oppføring++) if (사용[felt_oppføring] == 0) {
            사용[felt_oppføring] = 1; port_VALUE[felt_oppføring] = 0; ADDRESS[felt_oppføring] = 0; 앞[felt_oppføring] = 0; vare_COUNT[felt_oppføring] = 0; RECEIVED_port[felt_oppføring] = 0;
            return felt_oppføring + 32;
        }
        return -24;
    }
    public static int BIND_endepunkt(int INDEX, int Nettverk_ADDRESS, int endepunkt_portnummer) {
        int felt_oppføring = stadfeste(INDEX);
        if (felt_oppføring < 0) return -9;
        if (Nettverk_ADDRESS != 0 && Nettverk_ADDRESS != 0x7f000001) return -99;
        if (port_VALUE[felt_oppføring] != 0 || endepunkt_portnummer < 0 || endepunkt_portnummer > 65535) return -22;
        if (endepunkt_portnummer == 0) endepunkt_portnummer = 임시창구();
        if (endepunkt_portnummer < 0) return endepunkt_portnummer;
        if (겹침(endepunkt_portnummer)) return -98;
        port_VALUE[felt_oppføring] = endepunkt_portnummer; ADDRESS[felt_oppføring] = Nettverk_ADDRESS; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Fram_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Fram_VALUE[INDEX] : -22; }
    public static int sende(int INDEX, int Nettverk_ADDRESS, int endepunkt_portnummer, int Storleik) {
        int felt_oppføring = stadfeste(INDEX);
        if (felt_oppføring < 0) return -9;
        if (Nettverk_ADDRESS != 0x7f000001) return -101;
        if (endepunkt_portnummer < 1 || endepunkt_portnummer > 65535) return -22;
        if (Storleik < 0 || Storleik > 512) return -90;
        if (port_VALUE[felt_oppføring] == 0) {
            int forretningsmål = BIND_endepunkt(INDEX, 0x7f000001, 0);
            if (forretningsmål < 0) return forretningsmål;
        }
        int mål_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == endepunkt_portnummer) mål_VALUE = 후보;
        if (mål_VALUE < 0) return -111;
        if (vare_COUNT[mål_VALUE] == 4) return -11;
        int plassere_INDEX = mål_VALUE * 4 + (앞[mål_VALUE] + vare_COUNT[mål_VALUE]) % 4;
        for (int byte_VALUE = 0; byte_VALUE < Storleik; byte_VALUE++) data[plassere_INDEX * 512 + byte_VALUE] = Fram_VALUE[byte_VALUE];
        lengd_VALUE[plassere_INDEX] = Storleik; 보낸창구[plassere_INDEX] = port_VALUE[felt_oppføring]; vare_COUNT[mål_VALUE]++;
        return Storleik;
    }
    public static int 받기(int INDEX, int 용량) {
        int felt_oppføring = stadfeste(INDEX);
        if (felt_oppføring < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (vare_COUNT[felt_oppføring] == 0) return -11;
        int plassere_INDEX = felt_oppføring * 4 + 앞[felt_oppføring];
        int Storleik = lengd_VALUE[plassere_INDEX] < 용량 ? lengd_VALUE[plassere_INDEX] : 용량;
        for (int byte_VALUE = 0; byte_VALUE < Storleik; byte_VALUE++) Fram_VALUE[byte_VALUE] = data[plassere_INDEX * 512 + byte_VALUE];
        RECEIVED_port[felt_oppføring] = 보낸창구[plassere_INDEX]; 앞[felt_oppføring] = (앞[felt_oppføring] + 1) % 4; vare_COUNT[felt_oppføring]--;
        return Storleik;
    }
    public static int 창구읽기(int INDEX) { int felt_oppføring = stadfeste(INDEX); return felt_oppføring < 0 ? -9 : port_VALUE[felt_oppføring]; }
    public static int 주소읽기(int INDEX) { int felt_oppføring = stadfeste(INDEX); return felt_oppføring < 0 ? -9 : ADDRESS[felt_oppføring]; }
    public static int avsendar_endepunkt(int INDEX) { int felt_oppføring = stadfeste(INDEX); return felt_oppføring < 0 ? -9 : RECEIVED_port[felt_oppføring]; }
    public static int Lukk(int INDEX) {
        int felt_oppføring = stadfeste(INDEX); if (felt_oppføring < 0) return -9;
        사용[felt_oppføring] = 0; vare_COUNT[felt_oppføring] = 0; port_VALUE[felt_oppføring] = 0; return 0;
    }
}
