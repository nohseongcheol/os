// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kjarni_VALUE 안의 연결형 bæti_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket lag_VALUE. */
public final class Stream_Net {
    static int[] staða_VALUE_e10195a1 = new int[16], gátt_VALUE = new int[16], 짝 = new int[16], jafningi_gátt = new int[16], Bíddu_VALUE = new int[16], 묶임 = new int[16];
    static int[] myndavél_að_framan_VALUE = new int[16], númer = new int[16], gögn = new int[16 * 1024];
    static int Áfram_vara = 50000;
    static int sannprófa(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && staða_VALUE_e10195a1[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int tengisnúmer) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (staða_VALUE_e10195a1[Loop_INDEX] != 0 && 묶임[Loop_INDEX] != 0 && gátt_VALUE[Loop_INDEX] == tengisnúmer) return true; return false; }
    public static int stofna_færsla() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (staða_VALUE_e10195a1[Loop_INDEX] == 0) { staða_VALUE_e10195a1[Loop_INDEX] = 1; jafningi_gátt[Loop_INDEX] = gátt_VALUE[Loop_INDEX] = myndavél_að_framan_VALUE[Loop_INDEX] = númer[Loop_INDEX] = Bíddu_VALUE[Loop_INDEX] = 묶임[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_endastöð(int 열린파일번호, int 통신주소, int tengisnúmer) {
        int Loop_INDEX = sannprófa(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (staða_VALUE_e10195a1[Loop_INDEX] != 1 || tengisnúmer < 0 || tengisnúmer > 65535) return -22;
        if (tengisnúmer == 0) { do { tengisnúmer = Áfram_vara++; if (Áfram_vara > 65535) Áfram_vara = 50000; } while (사용중(tengisnúmer)); }
        if (사용중(tengisnúmer)) return -98; gátt_VALUE[Loop_INDEX] = tengisnúmer; 묶임[Loop_INDEX] = 1; staða_VALUE_e10195a1[Loop_INDEX] = 2; return 0;
    }
    public static int hlusta_endastöð(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = sannprófa(열린파일번호); if (Loop_INDEX < 0) return -9; if (staða_VALUE_e10195a1[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; staða_VALUE_e10195a1[Loop_INDEX] = 3; return 0; }
    public static int Tengjast(int 열린파일번호, int 통신주소, int tengisnúmer) {
        int Loop_INDEX = sannprófa(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (tengisnúmer < 1 || tengisnúmer > 65535 || staða_VALUE_e10195a1[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int innri_samtenging_staða = 0; innri_samtenging_staða < 16; innri_samtenging_staða++) if (staða_VALUE_e10195a1[innri_samtenging_staða] == 3 && gátt_VALUE[innri_samtenging_staða] == tengisnúmer) 수신쪽 = innri_samtenging_staða;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int innri_samtenging_staða = 0; innri_samtenging_staða < 16; innri_samtenging_staða++) if (Bíddu_VALUE[innri_samtenging_staða] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (staða_VALUE_e10195a1[Loop_INDEX] == 1) { int 처리값 = BIND_endastöð(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = stofna_færsla(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        staða_VALUE_e10195a1[Loop_INDEX] = staða_VALUE_e10195a1[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; gátt_VALUE[다른번호] = tengisnúmer; jafningi_gátt[Loop_INDEX] = tengisnúmer; jafningi_gátt[다른번호] = gátt_VALUE[Loop_INDEX]; Bíddu_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int samþykkja_tenging(int 열린파일번호) { int Loop_INDEX = sannprófa(열린파일번호); if (Loop_INDEX < 0) return -9; if (staða_VALUE_e10195a1[Loop_INDEX] != 3) return -22; for (int innri_samtenging_staða = 0; innri_samtenging_staða < 16; innri_samtenging_staða++) if (staða_VALUE_e10195a1[innri_samtenging_staða] != 0 && Bíddu_VALUE[innri_samtenging_staða] == Loop_INDEX + 1) { Bíddu_VALUE[innri_samtenging_staða] = 0; return innri_samtenging_staða + 40; } return -11; }
    public static int Skrift(int 열린파일번호, int færsla_COUNT) {
        int Loop_INDEX = sannprófa(열린파일번호); if (Loop_INDEX < 0) return -9; if (staða_VALUE_e10195a1[Loop_INDEX] != 4) return -107;
        if (færsla_COUNT < 0 || færsla_COUNT > 512) return -22; if (færsla_COUNT == 0) return 0;
        int innri_samtenging_staða = 짝[Loop_INDEX]; if (innri_samtenging_staða < 0) return -32; int samtala_COUNT = 1024 - númer[innri_samtenging_staða]; if (samtala_COUNT == 0) return -11; if (samtala_COUNT > færsla_COUNT) samtala_COUNT = færsla_COUNT;
        for (int Samanburður_staða = 0; Samanburður_staða < samtala_COUNT; Samanburður_staða++) gögn[innri_samtenging_staða * 1024 + (myndavél_að_framan_VALUE[innri_samtenging_staða] + númer[innri_samtenging_staða] + Samanburður_staða) % 1024] = 되돌림망.Áfram_VALUE[Samanburður_staða]; númer[innri_samtenging_staða] += samtala_COUNT; return samtala_COUNT;
    }
    public static int Lestur(int 열린파일번호, int færsla_COUNT) {
        int Loop_INDEX = sannprófa(열린파일번호); if (Loop_INDEX < 0) return -9; if (staða_VALUE_e10195a1[Loop_INDEX] != 4) return -107; if (færsla_COUNT < 0 || færsla_COUNT > 512) return -22;
        if (færsla_COUNT == 0) return 0; if (númer[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (færsla_COUNT > númer[Loop_INDEX]) færsla_COUNT = númer[Loop_INDEX];
        for (int Samanburður_staða = 0; Samanburður_staða < færsla_COUNT; Samanburður_staða++) 되돌림망.Áfram_VALUE[Samanburður_staða] = gögn[Loop_INDEX * 1024 + (myndavél_að_framan_VALUE[Loop_INDEX] + Samanburður_staða) % 1024]; myndavél_að_framan_VALUE[Loop_INDEX] = (myndavél_að_framan_VALUE[Loop_INDEX] + færsla_COUNT) % 1024; númer[Loop_INDEX] -= færsla_COUNT; return færsla_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = sannprófa(열린파일번호); return Loop_INDEX < 0 ? -9 : gátt_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = sannprófa(열린파일번호); return Loop_INDEX < 0 ? -9 : jafningi_gátt[Loop_INDEX]; }
    public static int Loka(int 열린파일번호) {
        int Loop_INDEX = sannprófa(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (staða_VALUE_e10195a1[Loop_INDEX] == 3) for (int innri_samtenging_staða = 0; innri_samtenging_staða < 16; innri_samtenging_staða++) if (Bíddu_VALUE[innri_samtenging_staða] == Loop_INDEX + 1) { if (짝[innri_samtenging_staða] >= 0) 짝[짝[innri_samtenging_staða]] = -1; staða_VALUE_e10195a1[innri_samtenging_staða] = Bíddu_VALUE[innri_samtenging_staða] = 묶임[innri_samtenging_staða] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; staða_VALUE_e10195a1[Loop_INDEX] = 묶임[Loop_INDEX] = númer[Loop_INDEX] = Bíddu_VALUE[Loop_INDEX] = 0; return 0;
    }
}
