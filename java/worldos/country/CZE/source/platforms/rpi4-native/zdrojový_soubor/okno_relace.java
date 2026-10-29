// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 prostředí Stav_HODNOTA. název_souboru 저장소는 공유하고 cesta_2/proměnná_HODNOTA/LOGZ_ZÁZNAM/입력은 분리한다. */
public final class okno_relace {
    static int[] 보관 = new int[4 * 30000], Připravit = new int[4];
    static int dobrá_zboží, pozice;
    static boolean 이어읽기;
    static void pole_HODNOTA(int[] data, boolean Store_HODNOTA) {
        for (int Loop_INDEX = 0; Loop_INDEX < data.length; Loop_INDEX++) { if (Store_HODNOTA) 보관[pozice++] = data[Loop_INDEX]; else data[Loop_INDEX] = 보관[pozice++]; }
    }
    static int HODNOTA(int data_HODNOTA, boolean 저장여부) { if (저장여부) { 보관[pozice++] = data_HODNOTA; return data_HODNOTA; } return 보관[pozice++]; }
    static void hledat_pozice(int 보관칸, boolean 저장여부) {
        pozice = 보관칸 * 30000;
        pole_HODNOTA(Paměť_Files.dobrá_zboží, 저장여부); Paměť_Files.dobrá_délka = HODNOTA(Paměť_Files.dobrá_délka, 저장여부);
        pole_HODNOTA(prostředí_syntaxe.proměnná_název, 저장여부); pole_HODNOTA(prostředí_syntaxe.proměnná_data, 저장여부); pole_HODNOTA(prostředí_syntaxe.이름길이, 저장여부); pole_HODNOTA(prostředí_syntaxe.HODNOTA_délka, 저장여부);
        prostředí_syntaxe.Stav_HODNOTA = HODNOTA(prostředí_syntaxe.Stav_HODNOTA, 저장여부);
        pole_HODNOTA(čára_Editor.LOGZ_ZÁZNAM, 저장여부); pole_HODNOTA(čára_Editor.LOGZ_délka, 저장여부); pole_HODNOTA(čára_Editor.Store_HODNOTA, 저장여부); pole_HODNOTA(příkaz_interpret.vstupní_řádek, 저장여부);
        čára_Editor.LOGZ_POČET = HODNOTA(čára_Editor.LOGZ_POČET, 저장여부); čára_Editor.LOGZ_ZÁZNAM_konec = HODNOTA(čára_Editor.LOGZ_ZÁZNAM_konec, 저장여부);
        čára_Editor.HLEDAT_HODNOTA = HODNOTA(čára_Editor.HLEDAT_HODNOTA, 저장여부); čára_Editor.저장길이 = HODNOTA(čára_Editor.저장길이, 저장여부);
        čára_Editor.Velikost = HODNOTA(čára_Editor.Velikost, 저장여부); čára_Editor.kurzor_HODNOTA = HODNOTA(čára_Editor.kurzor_HODNOTA, 저장여부); čára_Editor.START_okno = HODNOTA(čára_Editor.START_okno, 저장여부);
        Připravit[보관칸] = 1;
    }
    static void Proces_HODNOTA_položka() {
        int událost_číslo = Panel.interpret_příkazů(12); if (událost_číslo == 0) return;
        hledat_pozice(dobrá_zboží, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((událost_číslo & (1 << (8 + Loop_INDEX))) != 0) { Panel.řízení_uživatel_program(32 + Loop_INDEX); Připravit[Loop_INDEX] = 0; }
            if ((událost_číslo & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != dobrá_zboží) Připravit[Loop_INDEX] = 0;
        }
        int Další_pozice = (událost_číslo & 15) - 1; if (Další_pozice < 0) Další_pozice = 0;
        if (Připravit[Další_pozice] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Další_pozice * 30000 + Loop_INDEX] = 0;
        dobrá_zboží = Další_pozice; hledat_pozice(dobrá_zboží, false); Panel.interpret_příkazů(100 + dobrá_zboží); 이어읽기 = true;
        단말.Zápis("\nTERMINAL FOCUS "); 단말.číslo(dobrá_zboží + 1); 단말.문자(10);
    }
    static boolean pokračovat_spuštění() {
        if (Panel.řízení_uživatel_program(16 + dobrá_zboží) == 0) return false;
        셸입출력.Povolit_interaktivní = true; 셸입출력.Spustit_2(false, false); Panel.입출력전환(1);
        int 처리값 = Panel.řízení_uživatel_program(dobrá_zboží); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; prostředí_syntaxe.Stav_HODNOTA = 처리값 < 0 ? 126 : 처리값; 단말.Zápis("exit "); 단말.číslo(처리값); 단말.문자(10); Panel.interpret_příkazů(3); }
        return true;
    }
}
