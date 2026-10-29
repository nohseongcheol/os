// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 lag_VALUE: 단일 kjarni_VALUE 안의 IPv4/UDP 루프백 flytja_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * ljúka_P 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] gátt_VALUE = new int[8];
    static int[] slóð = new int[8];
    static int[] myndavél_að_framan_VALUE = new int[8];
    static int[] vara_COUNT = new int[8];
    static int[] RECEIVED_gátt = new int[8];
    static int[] lengd_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] gögn = new int[32 * 512];
    static int[] Áfram_VALUE = new int[512];
    static int Áfram_endastöð = 49152;
    static int sannprófa(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int rauf_færsla = 0; rauf_færsla < 8; rauf_færsla++) if (사용[rauf_færsla] != 0 && gátt_VALUE[rauf_færsla] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Áfram_endastöð++;
            if (Áfram_endastöð > 65535) Áfram_endastöð = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int stofna_færsla(int 영역, int 종류, int samningsvirði) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (samningsvirði != 0 && samningsvirði != 17)) return -93;
        for (int rauf_færsla = 0; rauf_færsla < 8; rauf_færsla++) if (사용[rauf_færsla] == 0) {
            사용[rauf_færsla] = 1; gátt_VALUE[rauf_færsla] = 0; slóð[rauf_færsla] = 0; myndavél_að_framan_VALUE[rauf_færsla] = 0; vara_COUNT[rauf_færsla] = 0; RECEIVED_gátt[rauf_færsla] = 0;
            return rauf_færsla + 32;
        }
        return -24;
    }
    public static int BIND_endastöð(int INDEX, int Net_slóð, int endastöð_tengisnúmer) {
        int rauf_færsla = sannprófa(INDEX);
        if (rauf_færsla < 0) return -9;
        if (Net_slóð != 0 && Net_slóð != 0x7f000001) return -99;
        if (gátt_VALUE[rauf_færsla] != 0 || endastöð_tengisnúmer < 0 || endastöð_tengisnúmer > 65535) return -22;
        if (endastöð_tengisnúmer == 0) endastöð_tengisnúmer = 임시창구();
        if (endastöð_tengisnúmer < 0) return endastöð_tengisnúmer;
        if (겹침(endastöð_tengisnúmer)) return -98;
        gátt_VALUE[rauf_færsla] = endastöð_tengisnúmer; slóð[rauf_færsla] = Net_slóð; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Áfram_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Áfram_VALUE[INDEX] : -22; }
    public static int senda(int INDEX, int Net_slóð, int endastöð_tengisnúmer, int Stærð) {
        int rauf_færsla = sannprófa(INDEX);
        if (rauf_færsla < 0) return -9;
        if (Net_slóð != 0x7f000001) return -101;
        if (endastöð_tengisnúmer < 1 || endastöð_tengisnúmer > 65535) return -22;
        if (Stærð < 0 || Stærð > 512) return -90;
        if (gátt_VALUE[rauf_færsla] == 0) {
            int NIÐURSTAÐA = BIND_endastöð(INDEX, 0x7f000001, 0);
            if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        }
        int endastaður_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && gátt_VALUE[후보] == endastöð_tengisnúmer) endastaður_VALUE = 후보;
        if (endastaður_VALUE < 0) return -111;
        if (vara_COUNT[endastaður_VALUE] == 4) return -11;
        int staða_INDEX = endastaður_VALUE * 4 + (myndavél_að_framan_VALUE[endastaður_VALUE] + vara_COUNT[endastaður_VALUE]) % 4;
        for (int bæti_VALUE = 0; bæti_VALUE < Stærð; bæti_VALUE++) gögn[staða_INDEX * 512 + bæti_VALUE] = Áfram_VALUE[bæti_VALUE];
        lengd_VALUE[staða_INDEX] = Stærð; 보낸창구[staða_INDEX] = gátt_VALUE[rauf_færsla]; vara_COUNT[endastaður_VALUE]++;
        return Stærð;
    }
    public static int 받기(int INDEX, int afkastageta_VALUE) {
        int rauf_færsla = sannprófa(INDEX);
        if (rauf_færsla < 0) return -9;
        if (afkastageta_VALUE < 0 || afkastageta_VALUE > 512) return -22;
        if (vara_COUNT[rauf_færsla] == 0) return -11;
        int staða_INDEX = rauf_færsla * 4 + myndavél_að_framan_VALUE[rauf_færsla];
        int Stærð = lengd_VALUE[staða_INDEX] < afkastageta_VALUE ? lengd_VALUE[staða_INDEX] : afkastageta_VALUE;
        for (int bæti_VALUE = 0; bæti_VALUE < Stærð; bæti_VALUE++) Áfram_VALUE[bæti_VALUE] = gögn[staða_INDEX * 512 + bæti_VALUE];
        RECEIVED_gátt[rauf_færsla] = 보낸창구[staða_INDEX]; myndavél_að_framan_VALUE[rauf_færsla] = (myndavél_að_framan_VALUE[rauf_færsla] + 1) % 4; vara_COUNT[rauf_færsla]--;
        return Stærð;
    }
    public static int 창구읽기(int INDEX) { int rauf_færsla = sannprófa(INDEX); return rauf_færsla < 0 ? -9 : gátt_VALUE[rauf_færsla]; }
    public static int 주소읽기(int INDEX) { int rauf_færsla = sannprófa(INDEX); return rauf_færsla < 0 ? -9 : slóð[rauf_færsla]; }
    public static int sendandi_endastöð(int INDEX) { int rauf_færsla = sannprófa(INDEX); return rauf_færsla < 0 ? -9 : RECEIVED_gátt[rauf_færsla]; }
    public static int Loka(int INDEX) {
        int rauf_færsla = sannprófa(INDEX); if (rauf_færsla < 0) return -9;
        사용[rauf_færsla] = 0; vara_COUNT[rauf_færsla] = 0; gátt_VALUE[rauf_færsla] = 0; return 0;
    }
}
