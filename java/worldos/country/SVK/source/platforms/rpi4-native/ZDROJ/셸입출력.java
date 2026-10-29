// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] vstup_údaje = new int[16384], 출력자료 = new int[16384];
    static int vstup_dĺžka, vstup_pozícia, 출력길이, vstupný_súbor = -1, výstupný_súbor = -1;
    static boolean 파이프입력, 파이프출력;
    static int zlyhanie_VALUE;
    static boolean Povoliť_interaktívny = true;
    public static int Informačné_systémy_interaktívny() { return Povoliť_interaktívny && vstupný_súbor < 3 && výstupný_súbor < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int Výstup(int Kanál_VALUE, int VALUE) {
        if (Kanál_VALUE != 1) return 0;
        if (výstupný_súbor >= 3) { int 처리값 = Pamäť_Súbory.Zápis(výstupný_súbor, VALUE); if (처리값 < 0) zlyhanie_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) zlyhanie_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int vstup_VALUE() {
        if (vstupný_súbor >= 3) { int 처리값 = Pamäť_Súbory.Čítanie(vstupný_súbor); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return vstup_pozícia < vstup_dĺžka ? vstup_údaje[vstup_pozícia++] : -2;
        return -3; // UART로 Dopredu_VALUE
    }
    static void Spustiť_2(boolean 앞파이프, boolean 뒤파이프) {
        파이프입력 = 앞파이프; 파이프출력 = 뒤파이프;
        vstup_pozícia = 0; 출력길이 = 0; vstupný_súbor = -1; výstupný_súbor = -1; zlyhanie_VALUE = 0;
    }
    static void 끝() {
        Panel.입출력전환(0);
        if (vstupný_súbor >= 3) Pamäť_Súbory.Zatvoriť(vstupný_súbor);
        if (výstupný_súbor >= 3) Pamäť_Súbory.Zatvoriť(výstupný_súbor);
        if (파이프출력) { vstup_dĺžka = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) vstup_údaje[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        vstupný_súbor = -1; výstupný_súbor = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
