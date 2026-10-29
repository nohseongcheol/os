// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** branduolys_VALUE 안의 연결형 baitas_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket sluoksnis_VALUE. */
public final class Stream_tinklas {
    static int[] Būsena_VALUE = new int[16], jungtis_VALUE = new int[16], 짝 = new int[16], lygiavertis_mazgas_jungtis = new int[16], Palauk_VALUE = new int[16], informacinės_technologijos_riba = new int[16];
    static int[] priekinis_VALUE = new int[16], numeris = new int[16], duomenys = new int[16 * 1024];
    static int toliau_prekė = 50000;
    static int patvirtinti(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Būsena_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int prievado_numeris) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Būsena_VALUE[Loop_INDEX] != 0 && informacinės_technologijos_riba[Loop_INDEX] != 0 && jungtis_VALUE[Loop_INDEX] == prievado_numeris) return true; return false; }
    public static int kurti_įrašas() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Būsena_VALUE[Loop_INDEX] == 0) { Būsena_VALUE[Loop_INDEX] = 1; lygiavertis_mazgas_jungtis[Loop_INDEX] = jungtis_VALUE[Loop_INDEX] = priekinis_VALUE[Loop_INDEX] = numeris[Loop_INDEX] = Palauk_VALUE[Loop_INDEX] = informacinės_technologijos_riba[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_dalyvis(int 열린파일번호, int 통신주소, int prievado_numeris) {
        int Loop_INDEX = patvirtinti(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Būsena_VALUE[Loop_INDEX] != 1 || prievado_numeris < 0 || prievado_numeris > 65535) return -22;
        if (prievado_numeris == 0) { do { prievado_numeris = toliau_prekė++; if (toliau_prekė > 65535) toliau_prekė = 50000; } while (사용중(prievado_numeris)); }
        if (사용중(prievado_numeris)) return -98; jungtis_VALUE[Loop_INDEX] = prievado_numeris; informacinės_technologijos_riba[Loop_INDEX] = 1; Būsena_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int laukti_dalyvis(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = patvirtinti(열린파일번호); if (Loop_INDEX < 0) return -9; if (Būsena_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Būsena_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Prisijungti(int 열린파일번호, int 통신주소, int prievado_numeris) {
        int Loop_INDEX = patvirtinti(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (prievado_numeris < 1 || prievado_numeris > 65535 || Būsena_VALUE[Loop_INDEX] > 2) return -22;
        int gauti_puslapis = -1; for (int vidinis_padėtis = 0; vidinis_padėtis < 16; vidinis_padėtis++) if (Būsena_VALUE[vidinis_padėtis] == 3 && jungtis_VALUE[vidinis_padėtis] == prievado_numeris) gauti_puslapis = vidinis_padėtis;
        if (gauti_puslapis < 0) return -111;
        int 대기여부 = 0; for (int vidinis_padėtis = 0; vidinis_padėtis < 16; vidinis_padėtis++) if (Palauk_VALUE[vidinis_padėtis] == gauti_puslapis + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Būsena_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_dalyvis(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Kita = kurti_įrašas(); if (Kita < 0) return Kita; Kita -= 40;
        Būsena_VALUE[Loop_INDEX] = Būsena_VALUE[Kita] = 4; 짝[Loop_INDEX] = Kita; 짝[Kita] = Loop_INDEX; jungtis_VALUE[Kita] = prievado_numeris; lygiavertis_mazgas_jungtis[Loop_INDEX] = prievado_numeris; lygiavertis_mazgas_jungtis[Kita] = jungtis_VALUE[Loop_INDEX]; Palauk_VALUE[Kita] = gauti_puslapis + 1; return 0;
    }
    public static int priimti_ryšys(int 열린파일번호) { int Loop_INDEX = patvirtinti(열린파일번호); if (Loop_INDEX < 0) return -9; if (Būsena_VALUE[Loop_INDEX] != 3) return -22; for (int vidinis_padėtis = 0; vidinis_padėtis < 16; vidinis_padėtis++) if (Būsena_VALUE[vidinis_padėtis] != 0 && Palauk_VALUE[vidinis_padėtis] == Loop_INDEX + 1) { Palauk_VALUE[vidinis_padėtis] = 0; return vidinis_padėtis + 40; } return -11; }
    public static int Rašymas(int 열린파일번호, int įrašas_COUNT) {
        int Loop_INDEX = patvirtinti(열린파일번호); if (Loop_INDEX < 0) return -9; if (Būsena_VALUE[Loop_INDEX] != 4) return -107;
        if (įrašas_COUNT < 0 || įrašas_COUNT > 512) return -22; if (įrašas_COUNT == 0) return 0;
        int vidinis_padėtis = 짝[Loop_INDEX]; if (vidinis_padėtis < 0) return -32; int bendras_COUNT = 1024 - numeris[vidinis_padėtis]; if (bendras_COUNT == 0) return -11; if (bendras_COUNT > įrašas_COUNT) bendras_COUNT = įrašas_COUNT;
        for (int Palyginimas_padėtis = 0; Palyginimas_padėtis < bendras_COUNT; Palyginimas_padėtis++) duomenys[vidinis_padėtis * 1024 + (priekinis_VALUE[vidinis_padėtis] + numeris[vidinis_padėtis] + Palyginimas_padėtis) % 1024] = ciklinis_testas_tinklas.Pirmyn_VALUE[Palyginimas_padėtis]; numeris[vidinis_padėtis] += bendras_COUNT; return bendras_COUNT;
    }
    public static int Skaitymas(int 열린파일번호, int įrašas_COUNT) {
        int Loop_INDEX = patvirtinti(열린파일번호); if (Loop_INDEX < 0) return -9; if (Būsena_VALUE[Loop_INDEX] != 4) return -107; if (įrašas_COUNT < 0 || įrašas_COUNT > 512) return -22;
        if (įrašas_COUNT == 0) return 0; if (numeris[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (įrašas_COUNT > numeris[Loop_INDEX]) įrašas_COUNT = numeris[Loop_INDEX];
        for (int Palyginimas_padėtis = 0; Palyginimas_padėtis < įrašas_COUNT; Palyginimas_padėtis++) ciklinis_testas_tinklas.Pirmyn_VALUE[Palyginimas_padėtis] = duomenys[Loop_INDEX * 1024 + (priekinis_VALUE[Loop_INDEX] + Palyginimas_padėtis) % 1024]; priekinis_VALUE[Loop_INDEX] = (priekinis_VALUE[Loop_INDEX] + įrašas_COUNT) % 1024; numeris[Loop_INDEX] -= įrašas_COUNT; return įrašas_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = patvirtinti(열린파일번호); return Loop_INDEX < 0 ? -9 : jungtis_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = patvirtinti(열린파일번호); return Loop_INDEX < 0 ? -9 : lygiavertis_mazgas_jungtis[Loop_INDEX]; }
    public static int Užverti(int 열린파일번호) {
        int Loop_INDEX = patvirtinti(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Būsena_VALUE[Loop_INDEX] == 3) for (int vidinis_padėtis = 0; vidinis_padėtis < 16; vidinis_padėtis++) if (Palauk_VALUE[vidinis_padėtis] == Loop_INDEX + 1) { if (짝[vidinis_padėtis] >= 0) 짝[짝[vidinis_padėtis]] = -1; Būsena_VALUE[vidinis_padėtis] = Palauk_VALUE[vidinis_padėtis] = informacinės_technologijos_riba[vidinis_padėtis] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Būsena_VALUE[Loop_INDEX] = informacinės_technologijos_riba[Loop_INDEX] = numeris[Loop_INDEX] = Palauk_VALUE[Loop_INDEX] = 0; return 0;
    }
}
