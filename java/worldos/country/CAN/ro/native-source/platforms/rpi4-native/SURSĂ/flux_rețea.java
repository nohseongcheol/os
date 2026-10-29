// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** nucleu_VALUE 안의 연결형 byte_VALUE flux_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket strat_VALUE. */
public final class flux_rețea {
    static int[] Stare_VALUE = new int[16], muta_VALUE = new int[16], 짝 = new int[16], pereche_muta = new int[16], 대기 = new int[16], sisteme_de_informații_limită = new int[16];
    static int[] frontală_VALUE = new int[16], 수 = new int[16], date = new int[16 * 1024];
    static int Următorul_element = 50000;
    static int verifica(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Stare_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int număr_port) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Stare_VALUE[Loop_INDEX] != 0 && sisteme_de_informații_limită[Loop_INDEX] != 0 && muta_VALUE[Loop_INDEX] == număr_port) return true; return false; }
    public static int crea_intrare() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Stare_VALUE[Loop_INDEX] == 0) { Stare_VALUE[Loop_INDEX] = 1; pereche_muta[Loop_INDEX] = muta_VALUE[Loop_INDEX] = frontală_VALUE[Loop_INDEX] = 수[Loop_INDEX] = 대기[Loop_INDEX] = sisteme_de_informații_limită[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_participant(int 열린파일번호, int 통신주소, int număr_port) {
        int Loop_INDEX = verifica(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Stare_VALUE[Loop_INDEX] != 1 || număr_port < 0 || număr_port > 65535) return -22;
        if (număr_port == 0) { do { număr_port = Următorul_element++; if (Următorul_element > 65535) Următorul_element = 50000; } while (사용중(număr_port)); }
        if (사용중(număr_port)) return -98; muta_VALUE[Loop_INDEX] = număr_port; sisteme_de_informații_limită[Loop_INDEX] = 1; Stare_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int asculta_participant(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = verifica(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stare_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Stare_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Conectează(int 열린파일번호, int 통신주소, int număr_port) {
        int Loop_INDEX = verifica(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (număr_port < 1 || număr_port > 65535 || Stare_VALUE[Loop_INDEX] > 2) return -22;
        int primi_pagina = -1; for (int internă_poziție = 0; internă_poziție < 16; internă_poziție++) if (Stare_VALUE[internă_poziție] == 3 && muta_VALUE[internă_poziție] == număr_port) primi_pagina = internă_poziție;
        if (primi_pagina < 0) return -111;
        int 대기여부 = 0; for (int internă_poziție = 0; internă_poziție < 16; internă_poziție++) if (대기[internă_poziție] == primi_pagina + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Stare_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_participant(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Altele = crea_intrare(); if (Altele < 0) return Altele; Altele -= 40;
        Stare_VALUE[Loop_INDEX] = Stare_VALUE[Altele] = 4; 짝[Loop_INDEX] = Altele; 짝[Altele] = Loop_INDEX; muta_VALUE[Altele] = număr_port; pereche_muta[Loop_INDEX] = număr_port; pereche_muta[Altele] = muta_VALUE[Loop_INDEX]; 대기[Altele] = primi_pagina + 1; return 0;
    }
    public static int accepta_conexiune(int 열린파일번호) { int Loop_INDEX = verifica(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stare_VALUE[Loop_INDEX] != 3) return -22; for (int internă_poziție = 0; internă_poziție < 16; internă_poziție++) if (Stare_VALUE[internă_poziție] != 0 && 대기[internă_poziție] == Loop_INDEX + 1) { 대기[internă_poziție] = 0; return internă_poziție + 40; } return -11; }
    public static int Scriere(int 열린파일번호, int intrare_COUNT) {
        int Loop_INDEX = verifica(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stare_VALUE[Loop_INDEX] != 4) return -107;
        if (intrare_COUNT < 0 || intrare_COUNT > 512) return -22; if (intrare_COUNT == 0) return 0;
        int internă_poziție = 짝[Loop_INDEX]; if (internă_poziție < 0) return -32; int total_COUNT = 1024 - 수[internă_poziție]; if (total_COUNT == 0) return -11; if (total_COUNT > intrare_COUNT) total_COUNT = intrare_COUNT;
        for (int Comparație_poziție = 0; Comparație_poziție < total_COUNT; Comparație_poziție++) date[internă_poziție * 1024 + (frontală_VALUE[internă_poziție] + 수[internă_poziție] + Comparație_poziție) % 1024] = cu_reacție_în_buclă_rețea.Înainte_VALUE[Comparație_poziție]; 수[internă_poziție] += total_COUNT; return total_COUNT;
    }
    public static int Citire(int 열린파일번호, int intrare_COUNT) {
        int Loop_INDEX = verifica(열린파일번호); if (Loop_INDEX < 0) return -9; if (Stare_VALUE[Loop_INDEX] != 4) return -107; if (intrare_COUNT < 0 || intrare_COUNT > 512) return -22;
        if (intrare_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (intrare_COUNT > 수[Loop_INDEX]) intrare_COUNT = 수[Loop_INDEX];
        for (int Comparație_poziție = 0; Comparație_poziție < intrare_COUNT; Comparație_poziție++) cu_reacție_în_buclă_rețea.Înainte_VALUE[Comparație_poziție] = date[Loop_INDEX * 1024 + (frontală_VALUE[Loop_INDEX] + Comparație_poziție) % 1024]; frontală_VALUE[Loop_INDEX] = (frontală_VALUE[Loop_INDEX] + intrare_COUNT) % 1024; 수[Loop_INDEX] -= intrare_COUNT; return intrare_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = verifica(열린파일번호); return Loop_INDEX < 0 ? -9 : muta_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = verifica(열린파일번호); return Loop_INDEX < 0 ? -9 : pereche_muta[Loop_INDEX]; }
    public static int Închide(int 열린파일번호) {
        int Loop_INDEX = verifica(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Stare_VALUE[Loop_INDEX] == 3) for (int internă_poziție = 0; internă_poziție < 16; internă_poziție++) if (대기[internă_poziție] == Loop_INDEX + 1) { if (짝[internă_poziție] >= 0) 짝[짝[internă_poziție]] = -1; Stare_VALUE[internă_poziție] = 대기[internă_poziție] = sisteme_de_informații_limită[internă_poziție] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Stare_VALUE[Loop_INDEX] = sisteme_de_informații_limită[Loop_INDEX] = 수[Loop_INDEX] = 대기[Loop_INDEX] = 0; return 0;
    }
}
