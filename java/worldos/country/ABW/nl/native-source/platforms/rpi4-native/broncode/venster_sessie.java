// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 Shell Status_WAARDE. bestand 저장소는 공유하고 pad/variabele_WAARDE/LOG_RECORD/입력은 분리한다. */
public final class venster_sessie {
    static int[] 보관 = new int[4 * 30000], Bereid_voor = new int[4];
    static int actueel_item, positie;
    static boolean 이어읽기;
    static void MATRIX_WAARDE(int[] gegevens, boolean Store_WAARDE) {
        for (int lus_INDEX = 0; lus_INDEX < gegevens.length; lus_INDEX++) { if (Store_WAARDE) 보관[positie++] = gegevens[lus_INDEX]; else gegevens[lus_INDEX] = 보관[positie++]; }
    }
    static int WAARDE(int gegevens_WAARDE, boolean 저장여부) { if (저장여부) { 보관[positie++] = gegevens_WAARDE; return gegevens_WAARDE; } return 보관[positie++]; }
    static void zoeken_functie(int 보관칸, boolean 저장여부) {
        positie = 보관칸 * 30000;
        MATRIX_WAARDE(GeheugenBestanden.actueel_item, 저장여부); GeheugenBestanden.actueel_tijdsduur = WAARDE(GeheugenBestanden.actueel_tijdsduur, 저장여부);
        MATRIX_WAARDE(Shell_syntaxis.variabele_naam, 저장여부); MATRIX_WAARDE(Shell_syntaxis.variabele_gegevens, 저장여부); MATRIX_WAARDE(Shell_syntaxis.이름길이, 저장여부); MATRIX_WAARDE(Shell_syntaxis.WAARDE_tijdsduur, 저장여부);
        Shell_syntaxis.Status_WAARDE = WAARDE(Shell_syntaxis.Status_WAARDE, 저장여부);
        MATRIX_WAARDE(regeleditor.LOG_RECORD, 저장여부); MATRIX_WAARDE(regeleditor.LOG_tijdsduur, 저장여부); MATRIX_WAARDE(regeleditor.Store_WAARDE, 저장여부); MATRIX_WAARDE(Opdrachtvertolker.invoerregel, 저장여부);
        regeleditor.LOG_AANTAL = WAARDE(regeleditor.LOG_AANTAL, 저장여부); regeleditor.LOG_RECORD_beëindigen = WAARDE(regeleditor.LOG_RECORD_beëindigen, 저장여부);
        regeleditor.Search_WAARDE = WAARDE(regeleditor.Search_WAARDE, 저장여부); regeleditor.저장길이 = WAARDE(regeleditor.저장길이, 저장여부);
        regeleditor.Grootte = WAARDE(regeleditor.Grootte, 저장여부); regeleditor.cursor_WAARDE = WAARDE(regeleditor.cursor_WAARDE, 저장여부); regeleditor.START_venster = WAARDE(regeleditor.START_venster, 저장여부);
        Bereid_voor[보관칸] = 1;
    }
    static void Proces_WAARDE_invoer() {
        int gebeurtenis_nummer = Bord.terminal(12); if (gebeurtenis_nummer == 0) return;
        zoeken_functie(actueel_item, true);
        for (int lus_INDEX = 0; lus_INDEX < 4; lus_INDEX++) {
            if ((gebeurtenis_nummer & (1 << (8 + lus_INDEX))) != 0) { Bord.controle_gebruiker_app(32 + lus_INDEX); Bereid_voor[lus_INDEX] = 0; }
            if ((gebeurtenis_nummer & (1 << (4 + lus_INDEX))) != 0 && lus_INDEX != actueel_item) Bereid_voor[lus_INDEX] = 0;
        }
        int Volgende_functie = (gebeurtenis_nummer & 15) - 1; if (Volgende_functie < 0) Volgende_functie = 0;
        if (Bereid_voor[Volgende_functie] == 0) for (int lus_INDEX = 0; lus_INDEX < 30000; lus_INDEX++) 보관[Volgende_functie * 30000 + lus_INDEX] = 0;
        actueel_item = Volgende_functie; zoeken_functie(actueel_item, false); Bord.terminal(100 + actueel_item); 이어읽기 = true;
        단말.Schrijven("\nTERMINAL FOCUS "); 단말.nummer(actueel_item + 1); 단말.문자(10);
    }
    static boolean cv_uitvoerbewerking() {
        if (Bord.controle_gebruiker_app(16 + actueel_item) == 0) return false;
        셸입출력.Toestaan_interactief = true; 셸입출력.starten(false, false); Bord.입출력전환(1);
        int 처리값 = Bord.controle_gebruiker_app(actueel_item); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; Shell_syntaxis.Status_WAARDE = 처리값 < 0 ? 126 : 처리값; 단말.Schrijven("exit "); 단말.nummer(처리값); 단말.문자(10); Bord.terminal(3); }
        return true;
    }
}
