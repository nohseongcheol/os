// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] vstup_data = new int[16384], výstup_data = new int[16384];
    static int vstup_délka, vstup_pozice, výstup_délka, vstupní_soubor = -1, výstupní_soubor = -1;
    static boolean kanál_vstup, kanál_výstup;
    static int selhání_HODNOTA;
    static boolean Povolit_interaktivní = true;
    public static int informační_systémy_interaktivní() { return Povolit_interaktivní && vstupní_soubor < 3 && výstupní_soubor < 3 && !kanál_vstup && !kanál_výstup ? 1 : 0; }
    public static int výstupní_pozice(int Kanál_HODNOTA, int HODNOTA) {
        if (Kanál_HODNOTA != 1) return 0;
        if (výstupní_soubor >= 3) { int 처리값 = Paměť_Files.Zápis(výstupní_soubor, HODNOTA); if (처리값 < 0) selhání_HODNOTA = 처리값; return 1; }
        if (!kanál_výstup) return 0;
        if (výstup_délka == výstup_data.length) selhání_HODNOTA = -28;
        else výstup_data[výstup_délka++] = HODNOTA;
        return 1;
    }
    public static int vstup_HODNOTA() {
        if (vstupní_soubor >= 3) { int 처리값 = Paměť_Files.Čtení(vstupní_soubor); return 처리값 == 256 ? -2 : 처리값; }
        if (kanál_vstup) return vstup_pozice < vstup_délka ? vstup_data[vstup_pozice++] : -2;
        return -3; // UART로 Vpřed_HODNOTA
    }
    static void Spustit_2(boolean řádkování_kanál, boolean 뒤파이프) {
        kanál_vstup = řádkování_kanál; kanál_výstup = 뒤파이프;
        vstup_pozice = 0; výstup_délka = 0; vstupní_soubor = -1; výstupní_soubor = -1; selhání_HODNOTA = 0;
    }
    static void 끝() {
        Panel.입출력전환(0);
        if (vstupní_soubor >= 3) Paměť_Files.Zavřené(vstupní_soubor);
        if (výstupní_soubor >= 3) Paměť_Files.Zavřené(výstupní_soubor);
        if (kanál_výstup) { vstup_délka = výstup_délka; for (int Loop_INDEX = 0; Loop_INDEX < výstup_délka; Loop_INDEX++) vstup_data[Loop_INDEX] = výstup_data[Loop_INDEX]; }
        vstupní_soubor = -1; výstupní_soubor = -1; kanál_vstup = false; kanál_výstup = false;
    }
}
