// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktivní prostředí 문법. 파이프는 순차 Provést_příkaz, 환경은 같은 셸에서 공유한다. */
public final class prostředí_syntaxe {
    static int[] zdrojový_soubor = new int[4 * 4096], Druh_HODNOTA = new int[4 * 128], Spustit_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] proměnná_název = new int[16 * 32], proměnná_data = new int[16 * 256], 이름길이 = new int[16], HODNOTA_délka = new int[16];
    static int[] skript_HODNOTA = new int[4 * 16384];
    static int Stav_HODNOTA, 깊이, 쓴수;
    static boolean 연결중, skript_konec, přípona_chyba;
    static boolean název_znak(int bod_kódu) { return bod_kódu >= 'a' && bod_kódu <= 'z' || bod_kódu >= 'A' && bod_kódu <= 'Z' || bod_kódu == '_' || bod_kódu >= 128; }
    static boolean 이름뒤(int bod_kódu) { return název_znak(bod_kódu) || bod_kódu >= '0' && bod_kódu <= '9'; }
    static void chyba(String text) { Panel.입출력전환(0); 단말.Zápis("příkaz parsovat_HODNOTA: "); 단말.Zápis(text); 단말.문자(10); Stav_HODNOTA = 2; }
    static int Čtení(int položka_POČET, int 중첩깊이) {
        int dobrá_INDEX = 0, celkem_POČET = 0, BASE_pozice = 중첩깊이 * 4096, speciální_znak = 중첩깊이 * 128;
        while (dobrá_INDEX < položka_POČET) {
            while (dobrá_INDEX < položka_POČET && (zdrojový_soubor[BASE_pozice + dobrá_INDEX] == 32 || zdrojový_soubor[BASE_pozice + dobrá_INDEX] == 9)) dobrá_INDEX++;
            if (dobrá_INDEX == položka_POČET || zdrojový_soubor[BASE_pozice + dobrá_INDEX] == '#') break;
            if (celkem_POČET == 128) { chyba("낱말이 너무 많습니다"); return -1; }
            int START_pozice = dobrá_INDEX, bod_kódu = zdrojový_soubor[BASE_pozice + dobrá_INDEX], data_Druh = 0;
            if (bod_kódu == ';') { data_Druh = 1; dobrá_INDEX++; }
            else if (bod_kódu == '&') { if (dobrá_INDEX + 1 >= položka_POČET || zdrojový_soubor[BASE_pozice + dobrá_INDEX + 1] != '&') { chyba("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } data_Druh = 2; dobrá_INDEX += 2; }
            else if (bod_kódu == '|') { dobrá_INDEX++; data_Druh = dobrá_INDEX < položka_POČET && zdrojový_soubor[BASE_pozice + dobrá_INDEX] == '|' ? 3 : 4; if (data_Druh == 3) dobrá_INDEX++; }
            else if (bod_kódu == '>') { dobrá_INDEX++; data_Druh = dobrá_INDEX < položka_POČET && zdrojový_soubor[BASE_pozice + dobrá_INDEX] == '>' ? 6 : 5; if (data_Druh == 6) dobrá_INDEX++; }
            else if (bod_kódu == '<') { data_Druh = 7; dobrá_INDEX++; }
            else {
                int Citát = 0;
                while (dobrá_INDEX < položka_POČET) {
                    bod_kódu = zdrojový_soubor[BASE_pozice + dobrá_INDEX];
                    if (bod_kódu == '`' && Citát != 39 || bod_kódu == '$' && Citát != 39 && dobrá_INDEX + 1 < položka_POČET && zdrojový_soubor[BASE_pozice + dobrá_INDEX + 1] == '(') { chyba("příkaz VÝSLEDEK 치환은 지원하지 않습니다"); return -1; }
                    if (bod_kódu == '\\' && Citát != 39) { if (++dobrá_INDEX == položka_POČET) { chyba("vstupní_řádek 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } dobrá_INDEX++; continue; }
                    if (bod_kódu == Citát) { Citát = 0; dobrá_INDEX++; continue; }
                    if (Citát == 0 && (bod_kódu == 39 || bod_kódu == 34)) { Citát = bod_kódu; dobrá_INDEX++; continue; }
                    if (Citát == 0 && (bod_kódu == 32 || bod_kódu == 9 || bod_kódu == ';' || bod_kódu == '&' || bod_kódu == '|' || bod_kódu == '<' || bod_kódu == '>')) break;
                    dobrá_INDEX++;
                }
                if (Citát != 0) { chyba("따옴표가 닫히지 않았습니다"); return -1; }
                if (dobrá_INDEX < položka_POČET && (zdrojový_soubor[BASE_pozice + dobrá_INDEX] == '>' || zdrojový_soubor[BASE_pozice + dobrá_INDEX] == '<')) {
                    boolean 수치 = dobrá_INDEX > START_pozice;
                    for (int Loop_INDEX = START_pozice; Loop_INDEX < dobrá_INDEX; Loop_INDEX++) if (zdrojový_soubor[BASE_pozice + Loop_INDEX] < '0' || zdrojový_soubor[BASE_pozice + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { chyba("번호를 지정한 název_souboru popisovač_položka vstup_a_výstup 전환은 지원하지 않습니다"); return -1; }
                }
            }
            Druh_HODNOTA[speciální_znak + celkem_POČET] = data_Druh; Spustit_2[speciální_znak + celkem_POČET] = START_pozice; 끝[speciální_znak + celkem_POČET] = dobrá_INDEX; celkem_POČET++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < celkem_POČET; Loop_INDEX++) {
            int 임시값 = Druh_HODNOTA[speciální_znak + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == celkem_POČET || Druh_HODNOTA[speciální_znak + Loop_INDEX] != 0) { chyba("vstup_a_výstup 전환에 název_souboru 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == celkem_POČET - 1 && 임시값 != 1) { chyba("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (celkem_POČET > 0 && !낱말 && Druh_HODNOTA[speciální_znak + celkem_POČET - 1] != 1) { chyba("명령이 빠졌습니다"); return -1; }
        return celkem_POČET;
    }
    static boolean oblast_SMS(int[] data_pole, int místní_START, int položka_POČET, String znak_pozice) {
        if (položka_POČET != znak_pozice.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) if (data_pole[místní_START + Loop_INDEX] != znak_pozice.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int bajt_data) {
        if (쓴수 >= příkaz_interpret.token_HODNOTA.length) { if (!přípona_chyba) chyba("변수를 펼친 명령이 너무 깁니다"); přípona_chyba = true; return; }
        příkaz_interpret.token_HODNOTA[쓴수++] = bajt_data;
    }
    static void proměnná_HODNOTA(int[] data_pole, int START_pozice, int položka_POČET) {
        if (oblast_SMS(data_pole, START_pozice, položka_POČET, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Paměť_Files.dobrá_délka; Loop_INDEX++) 넣기(Paměť_Files.dobrá_zboží[Loop_INDEX]); return; }
        if (oblast_SMS(data_pole, START_pozice, položka_POČET, "HOME")) { 넣기('/'); return; }
        if (oblast_SMS(data_pole, START_pozice, položka_POČET, "?")) {
            int data_HODNOTA = Stav_HODNOTA, číslice = 100; boolean 시작여부 = false;
            while (číslice > 0) { int 뒷값 = data_HODNOTA / číslice; if (뒷값 != 0 || 시작여부 || číslice == 1) { 넣기('0' + 뒷값); 시작여부 = true; } data_HODNOTA %= číslice; číslice /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == položka_POČET) {
            boolean POZVYHLEDAT = true; for (int vnitřní_pozice = 0; vnitřní_pozice < položka_POČET; vnitřní_pozice++) if (proměnná_název[Loop_INDEX * 32 + vnitřní_pozice] != data_pole[START_pozice + vnitřní_pozice]) POZVYHLEDAT = false;
            if (POZVYHLEDAT) { for (int vnitřní_pozice = 0; vnitřní_pozice < HODNOTA_délka[Loop_INDEX]; vnitřní_pozice++) 넣기(proměnná_data[Loop_INDEX * 256 + vnitřní_pozice]); return; }
        }
    }
    static boolean Word_HODNOTA(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Spustit_2[중첩깊이 * 128 + 낱말번호], konec_pozice = 끝[중첩깊이 * 128 + 낱말번호], BASE_pozice = 중첩깊이 * 4096, Citát = 0;
        if (읽는자리 < konec_pozice && zdrojový_soubor[BASE_pozice + 읽는자리] == '~' && (읽는자리 + 1 == konec_pozice || zdrojový_soubor[BASE_pozice + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < konec_pozice) {
            int bod_kódu = zdrojový_soubor[BASE_pozice + 읽는자리++];
            if (bod_kódu == Citát) { Citát = 0; continue; }
            if (Citát == 0 && (bod_kódu == 39 || bod_kódu == 34)) { Citát = bod_kódu; continue; }
            if (bod_kódu == '\\' && Citát != 39) { int Další_pozice = zdrojový_soubor[BASE_pozice + 읽는자리++]; if (Citát == 34 && Další_pozice != '$' && Další_pozice != '"' && Další_pozice != '\\') 넣기('\\'); 넣기(Další_pozice); continue; }
            if (bod_kódu == '$' && Citát != 39 && 읽는자리 < konec_pozice) {
                boolean 중괄호자리 = zdrojový_soubor[BASE_pozice + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < konec_pozice && zdrojový_soubor[BASE_pozice + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < konec_pozice && 이름뒤(zdrojový_soubor[BASE_pozice + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == konec_pozice || zdrojový_soubor[BASE_pozice + 읽는자리] != '}')) { chyba("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                proměnná_HODNOTA(zdrojový_soubor, BASE_pozice + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(bod_kódu);
        }
        return !přípona_chyba;
    }
    static int prostředí_Nastavení(int argument_INDEX, boolean odebrat) {
        int místní_START = příkaz_interpret.시작점[argument_INDEX], konec_pozice = místní_START + příkaz_interpret.délka_HODNOTA[argument_INDEX], 같음자리 = místní_START;
        while (같음자리 < konec_pozice && příkaz_interpret.token_HODNOTA[같음자리] != '=') 같음자리++;
        int položka_POČET = 같음자리 - místní_START;
        if (položka_POČET < 1 || položka_POČET > 31 || !název_znak(příkaz_interpret.token_HODNOTA[místní_START]) || !odebrat && 같음자리 == konec_pozice || konec_pozice - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = místní_START; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(příkaz_interpret.token_HODNOTA[Loop_INDEX])) return 2;
        if (oblast_SMS(příkaz_interpret.token_HODNOTA, místní_START, položka_POČET, "PWD") || oblast_SMS(příkaz_interpret.token_HODNOTA, místní_START, položka_POČET, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != položka_POČET) continue;
            boolean POZVYHLEDAT = true; for (int vnitřní_pozice = 0; vnitřní_pozice < položka_POČET; vnitřní_pozice++) if (proměnná_název[Loop_INDEX * 32 + vnitřní_pozice] != příkaz_interpret.token_HODNOTA[místní_START + vnitřní_pozice]) POZVYHLEDAT = false;
            if (POZVYHLEDAT) 찾은여부 = Loop_INDEX;
        }
        if (odebrat) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = položka_POČET; HODNOTA_délka[찾은여부] = konec_pozice - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) proměnná_název[찾은여부 * 32 + Loop_INDEX] = příkaz_interpret.token_HODNOTA[místní_START + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < konec_pozice; Loop_INDEX++) proměnná_data[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = příkaz_interpret.token_HODNOTA[Loop_INDEX];
        return 0;
    }
    static void zobrazit_prostředí() {
        단말.Zápis("HOME=/\nPWD="); Paměť_Files.dobrá_zápis(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int vnitřní_pozice = 0; vnitřní_pozice < 이름길이[Loop_INDEX]; vnitřní_pozice++) Panel.직렬쓰기(proměnná_název[Loop_INDEX * 32 + vnitřní_pozice]); 단말.문자('=');
            for (int vnitřní_pozice = 0; vnitřní_pozice < HODNOTA_délka[Loop_INDEX]; vnitřní_pozice++) Panel.직렬쓰기(proměnná_data[Loop_INDEX * 256 + vnitřní_pozice]); 단말.문자(10);
        }
    }
    static void Provést_příkaz(int[] data_pole, int 시작변위, int položka_POČET, int 중첩깊이) {
        if (중첩깊이 >= 4 || položka_POČET > 4096) { chyba("příkaz 파일의 vnoření_HODNOTA 또는 vstupní_řádek délka_HODNOTA 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < položka_POČET; Loop_INDEX++) zdrojový_soubor[중첩깊이 * 4096 + Loop_INDEX] = data_pole[시작변위 + Loop_INDEX];
        int celkem_POČET = Čtení(položka_POČET, 중첩깊이); if (celkem_POČET < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < celkem_POČET) {
            int Skupina_konec = 읽는자리;
            while (Skupina_konec < celkem_POČET && (Druh_HODNOTA[중첩깊이 * 128 + Skupina_konec] == 0 || Druh_HODNOTA[중첩깊이 * 128 + Skupina_konec] >= 4)) Skupina_konec++;
            boolean Provést = 조건성립 == 1 || 조건성립 == 2 && Stav_HODNOTA == 0 || 조건성립 == 3 && Stav_HODNOTA != 0;
            if (Provést) {
                boolean Předchozí_zboží_INDEX = false;
                while (읽는자리 < Skupina_konec) {
                    int Další_pozice = 읽는자리; while (Další_pozice < Skupina_konec && Druh_HODNOTA[중첩깊이 * 128 + Další_pozice] != 4) Další_pozice++;
                    boolean spojit_tok = Další_pozice < Skupina_konec; int vstup_stránka = -1, výstup_stránka = -1, 출력방식 = 0;
                    příkaz_interpret.token_POČET = 0; 쓴수 = 0; přípona_chyba = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < Další_pozice; Loop_INDEX++) {
                        int data_Druh = Druh_HODNOTA[중첩깊이 * 128 + Loop_INDEX];
                        if (data_Druh >= 5) { if (data_Druh == 7) { if (vstup_stránka >= 0) { chyba("vstup_HODNOTA 전환이 겹쳤습니다"); return; } vstup_stránka = ++Loop_INDEX; } else { if (výstup_stránka >= 0) { chyba("výstupní_pozice 전환이 겹쳤습니다"); return; } výstup_stránka = ++Loop_INDEX; 출력방식 = data_Druh; } continue; }
                        if (příkaz_interpret.token_POČET == 32) { chyba("인수가 너무 많습니다"); return; }
                        int argument_INDEX = příkaz_interpret.token_POČET++; příkaz_interpret.시작점[argument_INDEX] = 쓴수;
                        if (!Word_HODNOTA(Loop_INDEX, 중첩깊이)) return;
                        příkaz_interpret.délka_HODNOTA[argument_INDEX] = 쓴수 - příkaz_interpret.시작점[argument_INDEX];
                    }
                    연결중 = Předchozí_zboží_INDEX || spojit_tok || vstup_stránka >= 0 || výstup_stránka >= 0;
                    if (연결중 && (příkaz_interpret.같음(0, "vi") || příkaz_interpret.같음(0, "edit") || příkaz_interpret.같음(0, "load") || příkaz_interpret.같음(0, "gui") || příkaz_interpret.같음(0, "terminal") || příkaz_interpret.같음(0, "sh") || příkaz_interpret.같음(0, "source"))) { chyba("interaktivní 명령과 příkaz 파일은 vstup_a_výstup 전환이나 tok_HODNOTA 연결에 쓸 číslo 없습니다"); return; }
                    셸입출력.Spustit_2(Předchozí_zboží_INDEX, spojit_tok);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int položka_pozice = 입출력바꿈 == 0 ? vstup_stránka : výstup_stránka; if (položka_pozice < 0) continue;
                        int START_pozice = 쓴수; if (!Word_HODNOTA(položka_pozice, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Paměť_Files.cesta_START(쓴수 - START_pozice);
                        for (int vnitřní_pozice = START_pozice; 처리값 >= 0 && vnitřní_pozice < 쓴수; vnitřní_pozice++) 처리값 = Paměť_Files.cesta_bajt(vnitřní_pozice - START_pozice, příkaz_interpret.token_HODNOTA[vnitřní_pozice]);
                        if (처리값 >= 0) 처리값 = Paměť_Files.Otevřít(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); příkaz_interpret.chyba(처리값); Stav_HODNOTA = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.vstupní_soubor = 처리값; else 셸입출력.výstupní_soubor = 처리값;
                    }
                    셸입출력.Povolit_interaktivní = 중첩깊이 == 0 && 읽는자리 == 0 && Další_pozice == celkem_POČET;
                    깊이 = 중첩깊이; příkaz_interpret.VÝSLEDEK = 0; Panel.입출력전환(1);
                    příkaz_interpret.příkaz();
                    Panel.interpret_příkazů(3);
                    int 반환값 = příkaz_interpret.VÝSLEDEK, tok_chyba = 셸입출력.selhání_HODNOTA;
                    셸입출력.끝(); 연결중 = false;
                    Stav_HODNOTA = tok_chyba < 0 ? 1 : 반환값;
                    if (tok_chyba < 0) { příkaz_interpret.chyba(tok_chyba); return; }
                    if (skript_konec || 반환값 == -1005) return;
                    Předchozí_zboží_INDEX = true; 읽는자리 = Další_pozice + 1;
                }
            }
            if (Skupina_konec < celkem_POČET) 조건성립 = Druh_HODNOTA[중첩깊이 * 128 + Skupina_konec];
            읽는자리 = Skupina_konec + 1;
        }
    }
    static void Provést_Soubor() {
        if (příkaz_interpret.token_POČET != 2 || 깊이 >= 3) { příkaz_interpret.VÝSLEDEK = 2; 단말.Zápis("사용법: sh název_souboru (vnoření_HODNOTA 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = příkaz_interpret.cesta_2(1); if (처리값 >= 0) 처리값 = Paměť_Files.Otevřít(0);
        if (처리값 < 0) { příkaz_interpret.chyba(처리값); return; }
        int položka_POČET = 0, bajt_data;
        while ((bajt_data = Paměť_Files.Čtení(처리값)) != 256 && bajt_data >= 0 && položka_POČET < 16384) skript_HODNOTA[중첩깊이 * 16384 + položka_POČET++] = bajt_data;
        Paměť_Files.Zavřené(처리값); Panel.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < položka_POČET && !skript_konec;) {
            int konec_pozice = 읽는자리; while (konec_pozice < položka_POČET && skript_HODNOTA[중첩깊이 * 16384 + konec_pozice] != 10) konec_pozice++;
            int platný_délka = konec_pozice - 읽는자리; if (platný_délka > 0 && skript_HODNOTA[중첩깊이 * 16384 + konec_pozice - 1] == 13) platný_délka--;
            Provést_příkaz(skript_HODNOTA, 중첩깊이 * 16384 + 읽는자리, platný_délka, 중첩깊이); 읽는자리 = konec_pozice + 1;
        }
        příkaz_interpret.VÝSLEDEK = Stav_HODNOTA; skript_konec = false; 깊이 = 중첩깊이 - 1;
    }
}
