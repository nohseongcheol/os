// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] invoer_gegevens = new int[16384], uitvoer_gegevens = new int[16384];
    static int invoer_tijdsduur, invoer_functie, uitvoer_tijdsduur, invoerbestand = -1, uitvoerbestand = -1;
    static boolean doorsluizen_invoer, doorsluizen_uitvoer;
    static int fout_WAARDE;
    static boolean Toestaan_interactief = true;
    public static int informatie_interactief() { return Toestaan_interactief && invoerbestand < 3 && uitvoerbestand < 3 && !doorsluizen_invoer && !doorsluizen_uitvoer ? 1 : 0; }
    public static int tekstuitvoer(int Kanaal_WAARDE, int WAARDE) {
        if (Kanaal_WAARDE != 1) return 0;
        if (uitvoerbestand >= 3) { int 처리값 = GeheugenBestanden.Schrijven(uitvoerbestand, WAARDE); if (처리값 < 0) fout_WAARDE = 처리값; return 1; }
        if (!doorsluizen_uitvoer) return 0;
        if (uitvoer_tijdsduur == uitvoer_gegevens.length) fout_WAARDE = -28;
        else uitvoer_gegevens[uitvoer_tijdsduur++] = WAARDE;
        return 1;
    }
    public static int invoer_WAARDE() {
        if (invoerbestand >= 3) { int 처리값 = GeheugenBestanden.Lezen(invoerbestand); return 처리값 == 256 ? -2 : 처리값; }
        if (doorsluizen_invoer) return invoer_functie < invoer_tijdsduur ? invoer_gegevens[invoer_functie++] : -2;
        return -3; // UART로 Vooruit_WAARDE
    }
    static void starten(boolean interlinie_doorsluizen, boolean navolgend_doorsluizen) {
        doorsluizen_invoer = interlinie_doorsluizen; doorsluizen_uitvoer = navolgend_doorsluizen;
        invoer_functie = 0; uitvoer_tijdsduur = 0; invoerbestand = -1; uitvoerbestand = -1; fout_WAARDE = 0;
    }
    static void 끝() {
        Bord.입출력전환(0);
        if (invoerbestand >= 3) GeheugenBestanden.Sluiten(invoerbestand);
        if (uitvoerbestand >= 3) GeheugenBestanden.Sluiten(uitvoerbestand);
        if (doorsluizen_uitvoer) { invoer_tijdsduur = uitvoer_tijdsduur; for (int lus_INDEX = 0; lus_INDEX < uitvoer_tijdsduur; lus_INDEX++) invoer_gegevens[lus_INDEX] = uitvoer_gegevens[lus_INDEX]; }
        invoerbestand = -1; uitvoerbestand = -1; doorsluizen_invoer = false; doorsluizen_uitvoer = false;
    }
}
