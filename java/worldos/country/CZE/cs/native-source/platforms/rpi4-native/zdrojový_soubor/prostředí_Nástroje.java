// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 prostředí 내장 nástroje. */
public final class prostředí_Nástroje {
    static int[] data = new int[16384];
    static int vstupní_soubor = -1;
    static int otevřít_Soubor(int argument_INDEX, int Proces_MODE) {
        int 처리값 = příkaz_interpret.cesta_2(argument_INDEX); return 처리값 < 0 ? 처리값 : Paměť_Files.Otevřít(Proces_MODE);
    }
    static boolean Připravit_vstup(int argument_INDEX) {
        vstupní_soubor = -1;
        if (argument_INDEX < příkaz_interpret.token_POČET) {
            vstupní_soubor = otevřít_Soubor(argument_INDEX, 0);
            if (vstupní_soubor < 0) { příkaz_interpret.chyba(vstupní_soubor); return false; }
        }
        return true;
    }
    static int Čtení() {
        if (vstupní_soubor >= 3) return Paměť_Files.Čtení(vstupní_soubor);
        while (true) {
            int bajt_data = Panel.직렬읽기(); if (bajt_data == -2 || bajt_data == 4) return 256;
            if (bajt_data == 3) { příkaz_interpret.VÝSLEDEK = 130; return 256; }
            if (bajt_data >= 0) return bajt_data; Panel.YIELD_CPU();
        }
    }
    static void Zavřené() { if (vstupní_soubor >= 3) Paměť_Files.Zavřené(vstupní_soubor); vstupní_soubor = -1; }
    static void pohled_HODNOTA() {
        int 마지막자리 = příkaz_interpret.token_POČET == 1 ? 2 : příkaz_interpret.token_POČET;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!Připravit_vstup(argument_INDEX)) continue;
            int bajt_data; while ((bajt_data = Čtení()) != 256 && bajt_data >= 0) Panel.직렬쓰기(bajt_data);
            if (bajt_data < 0) příkaz_interpret.chyba(bajt_data); Zavřené();
        }
    }
    static void Soubor_Úkol(String Akce_číslo) {
        if (příkaz_interpret.token_POČET != 2) { příkaz_interpret.VÝSLEDEK = 2; 단말.Zápis("사용법: mkdir/rmdir/touch název_souboru\n"); return; }
        int 처리값 = příkaz_interpret.cesta_2(1);
        if (처리값 >= 0) {
            if (Akce_číslo.charAt(0) == 'm') 처리값 = Paměť_Files.Create_Adresář();
            else if (Akce_číslo.charAt(0) == 'r') 처리값 = Paměť_Files.odebrat_Adresář();
            else { 처리값 = Paměť_Files.Otevřít(65); if (처리값 >= 3) 처리값 = Paměť_Files.Zavřené(처리값); }
        }
        if (처리값 < 0) příkaz_interpret.chyba(처리값);
    }
    static void instance_HODNOTA(boolean 이동여부) {
        if (příkaz_interpret.token_POČET != 3) { příkaz_interpret.VÝSLEDEK = 2; 단말.Zápis("사용법: cp/mv 원본 cíl_účastník (název_souboru)\n"); return; }
        int 처리값 = příkaz_interpret.cesta_2(1); if (처리값 >= 0) 처리값 = Paměť_Files.normalizovat_HODNOTA();
        if (처리값 < 0) { příkaz_interpret.chyba(처리값); return; }
        int 원본번호 = Paměť_Files.NAJÍT_položka(); if (원본번호 < 0) { příkaz_interpret.chyba(-2); return; }
        int položka_POČET = Paměť_Files.délka_HODNOTA[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) data[Loop_INDEX] = Paměť_Files.자료읽기(원본번호, Loop_INDEX);
        처리값 = příkaz_interpret.cesta_2(2); if (처리값 >= 0) 처리값 = Paměť_Files.normalizovat_HODNOTA();
        if (처리값 < 0) { příkaz_interpret.chyba(처리값); return; }
        if (Paměť_Files.NAJÍT_položka() == 원본번호) { if (!이동여부) příkaz_interpret.chyba(-22); return; }
        if (이동여부) { 처리값 = Paměť_Files.Odebrat_položka(원본번호); if (처리값 < 0) příkaz_interpret.chyba(처리값); return; }
        int 열린파일번호 = Paměť_Files.Otevřít(577); if (열린파일번호 < 0) { příkaz_interpret.chyba(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) { 처리값 = Paměť_Files.Zápis(열린파일번호, data[Loop_INDEX]); if (처리값 < 0) { příkaz_interpret.chyba(처리값); break; } }
        Paměť_Files.Zavřené(열린파일번호);
    }
    static int číslice_HODNOTA(int argument_INDEX) {
        if (argument_INDEX >= příkaz_interpret.token_POČET) return -1;
        int položka_POČET = 0; for (int Loop_INDEX = 0; Loop_INDEX < příkaz_interpret.délka_HODNOTA[argument_INDEX]; Loop_INDEX++) { int bod_kódu = příkaz_interpret.token_HODNOTA[příkaz_interpret.시작점[argument_INDEX] + Loop_INDEX]; if (bod_kódu < '0' || bod_kódu > '9' || položka_POČET > 10000) return -1; položka_POČET = položka_POČET * 10 + bod_kódu - '0'; } return položka_POČET;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (příkaz_interpret.같음(1, "-c") || příkaz_interpret.같음(1, "-l") || příkaz_interpret.같음(1, "-w")) { 선택번호 = příkaz_interpret.같음(1, "-c") ? 1 : příkaz_interpret.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (příkaz_interpret.token_POČET > argument_INDEX + 1) { příkaz_interpret.VÝSLEDEK = 2; 단말.Zápis("사용법: wc [-c|-l|-w] [název_souboru]\n"); return; }
        if (!Připravit_vstup(argument_INDEX)) return;
        int bajt_POČET = 0, 줄수 = 0, 낱말수 = 0, bajt_data; boolean 낱말 = false;
        while ((bajt_data = Čtení()) >= 0 && bajt_data != 256) { bajt_POČET++; if (bajt_data == 10) 줄수++; boolean Space = bajt_data == 32 || bajt_data >= 9 && bajt_data <= 13; if (!Space && !낱말) 낱말수++; 낱말 = !Space; }
        Zavřené(); if (bajt_data < 0) { příkaz_interpret.chyba(bajt_data); return; }
        if (선택번호 != 0) 단말.číslo(선택번호 == 1 ? bajt_POČET : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.číslo(줄수); 단말.문자(' '); 단말.číslo(낱말수); 단말.문자(' '); 단말.číslo(bajt_POČET); } 단말.문자(10);
    }
    static void NAJÍT_položka() {
        if (příkaz_interpret.token_POČET < 2 || příkaz_interpret.token_POČET > 3) { příkaz_interpret.VÝSLEDEK = 2; 단말.Zápis("사용법: grep 찾을문구 [název_souboru]\n"); return; }
        if (!Připravit_vstup(2)) return;
        int položka_POČET = 0, bajt_data, 일치수 = 0;
        while (true) {
            bajt_data = Čtení();
            if (bajt_data == 10 || bajt_data == 256 || bajt_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= položka_POČET - příkaz_interpret.délka_HODNOTA[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int vnitřní_pozice = 0; vnitřní_pozice < příkaz_interpret.délka_HODNOTA[1]; vnitřní_pozice++) if (data[Loop_INDEX + vnitřní_pozice] != příkaz_interpret.token_HODNOTA[příkaz_interpret.시작점[1] + vnitřní_pozice]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (položka_POČET > 0 || bajt_data == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) Panel.직렬쓰기(data[Loop_INDEX]); 단말.문자(10); 일치수++; }
                položka_POČET = 0; if (bajt_data != 10) break;
            } else if (položka_POČET < data.length) data[položka_POČET++] = bajt_data;
            else { příkaz_interpret.chyba(-28); Zavřené(); return; }
        }
        Zavřené(); if (bajt_data < 0) příkaz_interpret.chyba(bajt_data); else if (příkaz_interpret.VÝSLEDEK == 0) příkaz_interpret.VÝSLEDEK = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (příkaz_interpret.같음(1, "-n")) { 줄수 = číslice_HODNOTA(2); argument_INDEX = 3; }
        if (줄수 < 0 || příkaz_interpret.token_POČET > argument_INDEX + 1) { příkaz_interpret.VÝSLEDEK = 2; 단말.Zápis("사용법: head/tail [-n 줄수] [název_souboru]\n"); return; }
        if (!Připravit_vstup(argument_INDEX)) return;
        int položka_POČET = 0, bajt_data;
        while ((bajt_data = Čtení()) != 256 && bajt_data >= 0) { if (položka_POČET == data.length) { příkaz_interpret.chyba(-28); Zavřené(); return; } data[položka_POČET++] = bajt_data; }
        Zavřené(); if (bajt_data < 0) { příkaz_interpret.chyba(bajt_data); return; }
        int místní_START = 0, konec_pozice = položka_POČET;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int celkem_POČET = 0; for (int Loop_INDEX = položka_POČET - 2; Loop_INDEX >= 0; Loop_INDEX--) if (data[Loop_INDEX] == 10 && ++celkem_POČET == 줄수) { místní_START = Loop_INDEX + 1; break; } }
        else { int celkem_POČET = 0; for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) if (data[Loop_INDEX] == 10 && ++celkem_POČET == 줄수) { konec_pozice = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = místní_START; Loop_INDEX < konec_pozice; Loop_INDEX++) Panel.직렬쓰기(data[Loop_INDEX]);
    }
    static void zápis_Společné_chvíle() {
        boolean Připojit_f1444605 = příkaz_interpret.같음(1, "-a"); int argument_INDEX = Připojit_f1444605 ? 2 : 1;
        if (příkaz_interpret.token_POČET != argument_INDEX + 1) { příkaz_interpret.VÝSLEDEK = 2; 단말.Zápis("사용법: tee [-a] název_souboru\n"); return; }
        int 열린파일번호 = otevřít_Soubor(argument_INDEX, Připojit_f1444605 ? 1089 : 577); if (열린파일번호 < 0) { příkaz_interpret.chyba(열린파일번호); return; }
        vstupní_soubor = -1; int bajt_data;
        while ((bajt_data = Čtení()) != 256 && bajt_data >= 0) { int 처리값 = Paměť_Files.Zápis(열린파일번호, bajt_data); if (처리값 < 0) { příkaz_interpret.chyba(처리값); break; } Panel.직렬쓰기(bajt_data); }
        Paměť_Files.Zavřené(열린파일번호);
    }
}
