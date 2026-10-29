// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 kiht_VALUE: 단일 tuum_VALUE 안의 IPv4/UDP 루프백 Edasta_VALUE.
 * väline_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * lõpeta_kõne_p 8개, 끝점당 datagramm 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class tagastusliides_võrk {
    static int[] kasutus_VALUE = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] ADDRESS = new int[8];
    static int[] esikaamera_VALUE = new int[8];
    static int[] kaup_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] 길이 = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] andmed = new int[32 * 512];
    static int[] Edasi_VALUE = new int[512];
    static int Edasi_osaleja = 49152;
    static int kinnitama(int INDEX) { return INDEX >= 32 && INDEX < 40 && kasutus_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (kasutus_VALUE[칸] != 0 && port_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Edasi_osaleja++;
            if (Edasi_osaleja > 65535) Edasi_osaleja = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int avama_kirje(int regioon_VALUE, int 종류, int lepingu_väärtus) {
        if (regioon_VALUE != 2) return -97;
        if (종류 != 2 || (lepingu_väärtus != 0 && lepingu_väärtus != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (kasutus_VALUE[칸] == 0) {
            kasutus_VALUE[칸] = 1; port_VALUE[칸] = 0; ADDRESS[칸] = 0; esikaamera_VALUE[칸] = 0; kaup_COUNT[칸] = 0; RECEIVED_port[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int BIND_osaleja(int INDEX, int võrgu_ID, int osaleja_pordinumber) {
        int 칸 = kinnitama(INDEX);
        if (칸 < 0) return -9;
        if (võrgu_ID != 0 && võrgu_ID != 0x7f000001) return -99;
        if (port_VALUE[칸] != 0 || osaleja_pordinumber < 0 || osaleja_pordinumber > 65535) return -22;
        if (osaleja_pordinumber == 0) osaleja_pordinumber = 임시창구();
        if (osaleja_pordinumber < 0) return osaleja_pordinumber;
        if (겹침(osaleja_pordinumber)) return -98;
        port_VALUE[칸] = osaleja_pordinumber; ADDRESS[칸] = võrgu_ID; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Edasi_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Edasi_VALUE[INDEX] : -22; }
    public static int saatma(int INDEX, int võrgu_ID, int osaleja_pordinumber, int Suurus) {
        int 칸 = kinnitama(INDEX);
        if (칸 < 0) return -9;
        if (võrgu_ID != 0x7f000001) return -101;
        if (osaleja_pordinumber < 1 || osaleja_pordinumber > 65535) return -22;
        if (Suurus < 0 || Suurus > 512) return -90;
        if (port_VALUE[칸] == 0) {
            int TULEMUS = BIND_osaleja(INDEX, 0x7f000001, 0);
            if (TULEMUS < 0) return TULEMUS;
        }
        int sihtkoht_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (kasutus_VALUE[후보] != 0 && port_VALUE[후보] == osaleja_pordinumber) sihtkoht_VALUE = 후보;
        if (sihtkoht_VALUE < 0) return -111;
        if (kaup_COUNT[sihtkoht_VALUE] == 4) return -11;
        int asukohaindeks = sihtkoht_VALUE * 4 + (esikaamera_VALUE[sihtkoht_VALUE] + kaup_COUNT[sihtkoht_VALUE]) % 4;
        for (int bait_VALUE = 0; bait_VALUE < Suurus; bait_VALUE++) andmed[asukohaindeks * 512 + bait_VALUE] = Edasi_VALUE[bait_VALUE];
        길이[asukohaindeks] = Suurus; 보낸창구[asukohaindeks] = port_VALUE[칸]; kaup_COUNT[sihtkoht_VALUE]++;
        return Suurus;
    }
    public static int saama(int INDEX, int võimsus_VALUE) {
        int 칸 = kinnitama(INDEX);
        if (칸 < 0) return -9;
        if (võimsus_VALUE < 0 || võimsus_VALUE > 512) return -22;
        if (kaup_COUNT[칸] == 0) return -11;
        int asukohaindeks = 칸 * 4 + esikaamera_VALUE[칸];
        int Suurus = 길이[asukohaindeks] < võimsus_VALUE ? 길이[asukohaindeks] : võimsus_VALUE;
        for (int bait_VALUE = 0; bait_VALUE < Suurus; bait_VALUE++) Edasi_VALUE[bait_VALUE] = andmed[asukohaindeks * 512 + bait_VALUE];
        RECEIVED_port[칸] = 보낸창구[asukohaindeks]; esikaamera_VALUE[칸] = (esikaamera_VALUE[칸] + 1) % 4; kaup_COUNT[칸]--;
        return Suurus;
    }
    public static int 창구읽기(int INDEX) { int 칸 = kinnitama(INDEX); return 칸 < 0 ? -9 : port_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = kinnitama(INDEX); return 칸 < 0 ? -9 : ADDRESS[칸]; }
    public static int saatja_osaleja(int INDEX) { int 칸 = kinnitama(INDEX); return 칸 < 0 ? -9 : RECEIVED_port[칸]; }
    public static int Suletud(int INDEX) {
        int 칸 = kinnitama(INDEX); if (칸 < 0) return -9;
        kasutus_VALUE[칸] = 0; kaup_COUNT[칸] = 0; port_VALUE[칸] = 0; return 0;
    }
}
