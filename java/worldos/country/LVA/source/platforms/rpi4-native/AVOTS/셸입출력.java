// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], ražojums_dati = new int[16384];
    static int 입력길이, 입력위치, 출력길이, ievades_fails = -1, izvades_fails = -1;
    static boolean 파이프입력, vertikālā_josla_ražojums;
    static int kļūme_VALUE;
    static boolean 대화허용 = true;
    public static int 대화가능() { return 대화허용 && ievades_fails < 3 && izvades_fails < 3 && !파이프입력 && !vertikālā_josla_ražojums ? 1 : 0; }
    public static int Izvade(int Kanāls_VALUE, int VALUE) {
        if (Kanāls_VALUE != 1) return 0;
        if (izvades_fails >= 3) { int 처리값 = atmiņa_Faili.Rakstīt(izvades_fails, VALUE); if (처리값 < 0) kļūme_VALUE = 처리값; return 1; }
        if (!vertikālā_josla_ražojums) return 0;
        if (출력길이 == ražojums_dati.length) kļūme_VALUE = -28;
        else ražojums_dati[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (ievades_fails >= 3) { int 처리값 = atmiņa_Faili.Lasīt(ievades_fails); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 pārsūtīt_VALUE
    }
    static void Palaist(boolean rindstarpa_vertikālā_josla, boolean 뒤파이프) {
        파이프입력 = rindstarpa_vertikālā_josla; vertikālā_josla_ražojums = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; ievades_fails = -1; izvades_fails = -1; kļūme_VALUE = 0;
    }
    static void 끝() {
        Panelis.입출력전환(0);
        if (ievades_fails >= 3) atmiņa_Faili.Aizvērt(ievades_fails);
        if (izvades_fails >= 3) atmiņa_Faili.Aizvērt(izvades_fails);
        if (vertikālā_josla_ražojums) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = ražojums_dati[Loop_INDEX]; }
        ievades_fails = -1; izvades_fails = -1; 파이프입력 = false; vertikālā_josla_ražojums = false;
    }
}
