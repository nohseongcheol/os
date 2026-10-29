// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kodols_VALUE 안의 연결형 byte_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket slānis_VALUE. */
public final class Stream_tīkls {
    static int[] Statuss_VALUE = new int[16], ports_VALUE = new int[16], 짝 = new int[16], vienranga_ports = new int[16], pagaidi_VALUE = new int[16], informācijas_tehnoloģija_robeža = new int[16];
    static int[] priekšējā_VALUE = new int[16], numurs = new int[16], dati = new int[16 * 1024];
    static int Tālāk_krājums = 50000;
    static int verificēt(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Statuss_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int porta_numurs) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Statuss_VALUE[Loop_INDEX] != 0 && informācijas_tehnoloģija_robeža[Loop_INDEX] != 0 && ports_VALUE[Loop_INDEX] == porta_numurs) return true; return false; }
    public static int atvērt_ievade() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Statuss_VALUE[Loop_INDEX] == 0) { Statuss_VALUE[Loop_INDEX] = 1; vienranga_ports[Loop_INDEX] = ports_VALUE[Loop_INDEX] = priekšējā_VALUE[Loop_INDEX] = numurs[Loop_INDEX] = pagaidi_VALUE[Loop_INDEX] = informācijas_tehnoloģija_robeža[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_dalībnieks(int 열린파일번호, int 통신주소, int porta_numurs) {
        int Loop_INDEX = verificēt(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Statuss_VALUE[Loop_INDEX] != 1 || porta_numurs < 0 || porta_numurs > 65535) return -22;
        if (porta_numurs == 0) { do { porta_numurs = Tālāk_krājums++; if (Tālāk_krājums > 65535) Tālāk_krājums = 50000; } while (사용중(porta_numurs)); }
        if (사용중(porta_numurs)) return -98; ports_VALUE[Loop_INDEX] = porta_numurs; informācijas_tehnoloģija_robeža[Loop_INDEX] = 1; Statuss_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int klausīties_dalībnieks(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = verificēt(열린파일번호); if (Loop_INDEX < 0) return -9; if (Statuss_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Statuss_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Savienoties(int 열린파일번호, int 통신주소, int porta_numurs) {
        int Loop_INDEX = verificēt(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (porta_numurs < 1 || porta_numurs > 65535 || Statuss_VALUE[Loop_INDEX] > 2) return -22;
        int saņemt_lapa = -1; for (int iekšējais_amats = 0; iekšējais_amats < 16; iekšējais_amats++) if (Statuss_VALUE[iekšējais_amats] == 3 && ports_VALUE[iekšējais_amats] == porta_numurs) saņemt_lapa = iekšējais_amats;
        if (saņemt_lapa < 0) return -111;
        int 대기여부 = 0; for (int iekšējais_amats = 0; iekšējais_amats < 16; iekšējais_amats++) if (pagaidi_VALUE[iekšējais_amats] == saņemt_lapa + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Statuss_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_dalībnieks(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Citi = atvērt_ievade(); if (Citi < 0) return Citi; Citi -= 40;
        Statuss_VALUE[Loop_INDEX] = Statuss_VALUE[Citi] = 4; 짝[Loop_INDEX] = Citi; 짝[Citi] = Loop_INDEX; ports_VALUE[Citi] = porta_numurs; vienranga_ports[Loop_INDEX] = porta_numurs; vienranga_ports[Citi] = ports_VALUE[Loop_INDEX]; pagaidi_VALUE[Citi] = saņemt_lapa + 1; return 0;
    }
    public static int akceptēt_paziņa(int 열린파일번호) { int Loop_INDEX = verificēt(열린파일번호); if (Loop_INDEX < 0) return -9; if (Statuss_VALUE[Loop_INDEX] != 3) return -22; for (int iekšējais_amats = 0; iekšējais_amats < 16; iekšējais_amats++) if (Statuss_VALUE[iekšējais_amats] != 0 && pagaidi_VALUE[iekšējais_amats] == Loop_INDEX + 1) { pagaidi_VALUE[iekšējais_amats] = 0; return iekšējais_amats + 40; } return -11; }
    public static int Rakstīt(int 열린파일번호, int ievade_COUNT) {
        int Loop_INDEX = verificēt(열린파일번호); if (Loop_INDEX < 0) return -9; if (Statuss_VALUE[Loop_INDEX] != 4) return -107;
        if (ievade_COUNT < 0 || ievade_COUNT > 512) return -22; if (ievade_COUNT == 0) return 0;
        int iekšējais_amats = 짝[Loop_INDEX]; if (iekšējais_amats < 0) return -32; int kopsumma_COUNT = 1024 - numurs[iekšējais_amats]; if (kopsumma_COUNT == 0) return -11; if (kopsumma_COUNT > ievade_COUNT) kopsumma_COUNT = ievade_COUNT;
        for (int Salīdzinājums_amats = 0; Salīdzinājums_amats < kopsumma_COUNT; Salīdzinājums_amats++) dati[iekšējais_amats * 1024 + (priekšējā_VALUE[iekšējais_amats] + numurs[iekšējais_amats] + Salīdzinājums_amats) % 1024] = atgriezeniskā_cilpa_tīkls.pārsūtīt_VALUE[Salīdzinājums_amats]; numurs[iekšējais_amats] += kopsumma_COUNT; return kopsumma_COUNT;
    }
    public static int Lasīt(int 열린파일번호, int ievade_COUNT) {
        int Loop_INDEX = verificēt(열린파일번호); if (Loop_INDEX < 0) return -9; if (Statuss_VALUE[Loop_INDEX] != 4) return -107; if (ievade_COUNT < 0 || ievade_COUNT > 512) return -22;
        if (ievade_COUNT == 0) return 0; if (numurs[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (ievade_COUNT > numurs[Loop_INDEX]) ievade_COUNT = numurs[Loop_INDEX];
        for (int Salīdzinājums_amats = 0; Salīdzinājums_amats < ievade_COUNT; Salīdzinājums_amats++) atgriezeniskā_cilpa_tīkls.pārsūtīt_VALUE[Salīdzinājums_amats] = dati[Loop_INDEX * 1024 + (priekšējā_VALUE[Loop_INDEX] + Salīdzinājums_amats) % 1024]; priekšējā_VALUE[Loop_INDEX] = (priekšējā_VALUE[Loop_INDEX] + ievade_COUNT) % 1024; numurs[Loop_INDEX] -= ievade_COUNT; return ievade_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = verificēt(열린파일번호); return Loop_INDEX < 0 ? -9 : ports_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = verificēt(열린파일번호); return Loop_INDEX < 0 ? -9 : vienranga_ports[Loop_INDEX]; }
    public static int Aizvērt(int 열린파일번호) {
        int Loop_INDEX = verificēt(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Statuss_VALUE[Loop_INDEX] == 3) for (int iekšējais_amats = 0; iekšējais_amats < 16; iekšējais_amats++) if (pagaidi_VALUE[iekšējais_amats] == Loop_INDEX + 1) { if (짝[iekšējais_amats] >= 0) 짝[짝[iekšējais_amats]] = -1; Statuss_VALUE[iekšējais_amats] = pagaidi_VALUE[iekšējais_amats] = informācijas_tehnoloģija_robeža[iekšējais_amats] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Statuss_VALUE[Loop_INDEX] = informācijas_tehnoloģija_robeža[Loop_INDEX] = numurs[Loop_INDEX] = pagaidi_VALUE[Loop_INDEX] = 0; return 0;
    }
}
