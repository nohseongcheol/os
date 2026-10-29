// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interattivo Shell 문법. 파이프는 순차 Esegui_comando, 환경은 같은 셸에서 공유한다. */
public final class Shell_sintassi {
    static int[] codiceSorgente = new int[4 * 4096], Kind_VALORE = new int[4 * 128], avvia = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] variabile_nome = new int[16 * 32], variabile_dati = new int[16 * 256], 이름길이 = new int[16], VALORE_durata = new int[16];
    static int[] script_VALORE = new int[4 * 16384];
    static int Stato_VALORE, 깊이, 쓴수;
    static boolean 연결중, script_chiudere, estensione_errore;
    static boolean nome_carattere(int punto_di_codice) { return punto_di_codice >= 'a' && punto_di_codice <= 'z' || punto_di_codice >= 'A' && punto_di_codice <= 'Z' || punto_di_codice == '_' || punto_di_codice >= 128; }
    static boolean 이름뒤(int punto_di_codice) { return nome_carattere(punto_di_codice) || punto_di_codice >= '0' && punto_di_codice <= '9'; }
    static void errore(String testo) { scheda.입출력전환(0); 단말.Scrittura("comando analizzare_VALORE: "); 단말.Scrittura(testo); 단말.문자(10); Stato_VALORE = 2; }
    static int Lettura(int voce_CONTA_NUMERI, int 중첩깊이) {
        int Regolari_INDICE = 0, totale_CONTA_NUMERI = 0, BASE_funzione = 중첩깊이 * 4096, carattere_speciale = 중첩깊이 * 128;
        while (Regolari_INDICE < voce_CONTA_NUMERI) {
            while (Regolari_INDICE < voce_CONTA_NUMERI && (codiceSorgente[BASE_funzione + Regolari_INDICE] == 32 || codiceSorgente[BASE_funzione + Regolari_INDICE] == 9)) Regolari_INDICE++;
            if (Regolari_INDICE == voce_CONTA_NUMERI || codiceSorgente[BASE_funzione + Regolari_INDICE] == '#') break;
            if (totale_CONTA_NUMERI == 128) { errore("낱말이 너무 많습니다"); return -1; }
            int START_funzione = Regolari_INDICE, punto_di_codice = codiceSorgente[BASE_funzione + Regolari_INDICE], dati_Kind = 0;
            if (punto_di_codice == ';') { dati_Kind = 1; Regolari_INDICE++; }
            else if (punto_di_codice == '&') { if (Regolari_INDICE + 1 >= voce_CONTA_NUMERI || codiceSorgente[BASE_funzione + Regolari_INDICE + 1] != '&') { errore("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } dati_Kind = 2; Regolari_INDICE += 2; }
            else if (punto_di_codice == '|') { Regolari_INDICE++; dati_Kind = Regolari_INDICE < voce_CONTA_NUMERI && codiceSorgente[BASE_funzione + Regolari_INDICE] == '|' ? 3 : 4; if (dati_Kind == 3) Regolari_INDICE++; }
            else if (punto_di_codice == '>') { Regolari_INDICE++; dati_Kind = Regolari_INDICE < voce_CONTA_NUMERI && codiceSorgente[BASE_funzione + Regolari_INDICE] == '>' ? 6 : 5; if (dati_Kind == 6) Regolari_INDICE++; }
            else if (punto_di_codice == '<') { dati_Kind = 7; Regolari_INDICE++; }
            else {
                int offerta = 0;
                while (Regolari_INDICE < voce_CONTA_NUMERI) {
                    punto_di_codice = codiceSorgente[BASE_funzione + Regolari_INDICE];
                    if (punto_di_codice == '`' && offerta != 39 || punto_di_codice == '$' && offerta != 39 && Regolari_INDICE + 1 < voce_CONTA_NUMERI && codiceSorgente[BASE_funzione + Regolari_INDICE + 1] == '(') { errore("comando risultato 치환은 지원하지 않습니다"); return -1; }
                    if (punto_di_codice == '\\' && offerta != 39) { if (++Regolari_INDICE == voce_CONTA_NUMERI) { errore("riga_di_ingresso 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } Regolari_INDICE++; continue; }
                    if (punto_di_codice == offerta) { offerta = 0; Regolari_INDICE++; continue; }
                    if (offerta == 0 && (punto_di_codice == 39 || punto_di_codice == 34)) { offerta = punto_di_codice; Regolari_INDICE++; continue; }
                    if (offerta == 0 && (punto_di_codice == 32 || punto_di_codice == 9 || punto_di_codice == ';' || punto_di_codice == '&' || punto_di_codice == '|' || punto_di_codice == '<' || punto_di_codice == '>')) break;
                    Regolari_INDICE++;
                }
                if (offerta != 0) { errore("따옴표가 닫히지 않았습니다"); return -1; }
                if (Regolari_INDICE < voce_CONTA_NUMERI && (codiceSorgente[BASE_funzione + Regolari_INDICE] == '>' || codiceSorgente[BASE_funzione + Regolari_INDICE] == '<')) {
                    boolean 수치 = Regolari_INDICE > START_funzione;
                    for (int Loop_INDICE = START_funzione; Loop_INDICE < Regolari_INDICE; Loop_INDICE++) if (codiceSorgente[BASE_funzione + Loop_INDICE] < '0' || codiceSorgente[BASE_funzione + Loop_INDICE] > '9') 수치 = false;
                    if (수치) { errore("번호를 지정한 file descrittore_voce I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            Kind_VALORE[carattere_speciale + totale_CONTA_NUMERI] = dati_Kind; avvia[carattere_speciale + totale_CONTA_NUMERI] = START_funzione; 끝[carattere_speciale + totale_CONTA_NUMERI] = Regolari_INDICE; totale_CONTA_NUMERI++;
        }
        boolean 낱말 = false;
        for (int Loop_INDICE = 0; Loop_INDICE < totale_CONTA_NUMERI; Loop_INDICE++) {
            int 임시값 = Kind_VALORE[carattere_speciale + Loop_INDICE];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDICE == totale_CONTA_NUMERI || Kind_VALORE[carattere_speciale + Loop_INDICE] != 0) { errore("I_O 전환에 file 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDICE == totale_CONTA_NUMERI - 1 && 임시값 != 1) { errore("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (totale_CONTA_NUMERI > 0 && !낱말 && Kind_VALORE[carattere_speciale + totale_CONTA_NUMERI - 1] != 1) { errore("명령이 빠졌습니다"); return -1; }
        return totale_CONTA_NUMERI;
    }
    static boolean intervallo_SMS(int[] dati_array, int locale_START, int voce_CONTA_NUMERI, String carattere_funzione) {
        if (voce_CONTA_NUMERI != carattere_funzione.length()) return false; for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) if (dati_array[locale_START + Loop_INDICE] != carattere_funzione.charAt(Loop_INDICE)) return false; return true;
    }
    static void 넣기(int byte_dati) {
        if (쓴수 >= InterpreteComandi.token_VALORE.length) { if (!estensione_errore) errore("변수를 펼친 명령이 너무 깁니다"); estensione_errore = true; return; }
        InterpreteComandi.token_VALORE[쓴수++] = byte_dati;
    }
    static void variabile_VALORE(int[] dati_array, int START_funzione, int voce_CONTA_NUMERI) {
        if (intervallo_SMS(dati_array, START_funzione, voce_CONTA_NUMERI, "PWD")) { 넣기('/'); for (int Loop_INDICE = 0; Loop_INDICE < FileMemoria.Regolari_durata; Loop_INDICE++) 넣기(FileMemoria.Regolari_articolo[Loop_INDICE]); return; }
        if (intervallo_SMS(dati_array, START_funzione, voce_CONTA_NUMERI, "HOME")) { 넣기('/'); return; }
        if (intervallo_SMS(dati_array, START_funzione, voce_CONTA_NUMERI, "?")) {
            int dati_VALORE = Stato_VALORE, cifra = 100; boolean 시작여부 = false;
            while (cifra > 0) { int finale_VALORE = dati_VALORE / cifra; if (finale_VALORE != 0 || 시작여부 || cifra == 1) { 넣기('0' + finale_VALORE); 시작여부 = true; } dati_VALORE %= cifra; cifra /= 10; } return;
        }
        for (int Loop_INDICE = 0; Loop_INDICE < 16; Loop_INDICE++) if (이름길이[Loop_INDICE] == voce_CONTA_NUMERI) {
            boolean match = true; for (int inner_funzione = 0; inner_funzione < voce_CONTA_NUMERI; inner_funzione++) if (variabile_nome[Loop_INDICE * 32 + inner_funzione] != dati_array[START_funzione + inner_funzione]) match = false;
            if (match) { for (int inner_funzione = 0; inner_funzione < VALORE_durata[Loop_INDICE]; inner_funzione++) 넣기(variabile_dati[Loop_INDICE * 256 + inner_funzione]); return; }
        }
    }
    static boolean Word_VALORE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = avvia[중첩깊이 * 128 + 낱말번호], chiudere_funzione = 끝[중첩깊이 * 128 + 낱말번호], BASE_funzione = 중첩깊이 * 4096, offerta = 0;
        if (읽는자리 < chiudere_funzione && codiceSorgente[BASE_funzione + 읽는자리] == '~' && (읽는자리 + 1 == chiudere_funzione || codiceSorgente[BASE_funzione + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < chiudere_funzione) {
            int punto_di_codice = codiceSorgente[BASE_funzione + 읽는자리++];
            if (punto_di_codice == offerta) { offerta = 0; continue; }
            if (offerta == 0 && (punto_di_codice == 39 || punto_di_codice == 34)) { offerta = punto_di_codice; continue; }
            if (punto_di_codice == '\\' && offerta != 39) { int Avanti_funzione = codiceSorgente[BASE_funzione + 읽는자리++]; if (offerta == 34 && Avanti_funzione != '$' && Avanti_funzione != '"' && Avanti_funzione != '\\') 넣기('\\'); 넣기(Avanti_funzione); continue; }
            if (punto_di_codice == '$' && offerta != 39 && 읽는자리 < chiudere_funzione) {
                boolean 중괄호자리 = codiceSorgente[BASE_funzione + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < chiudere_funzione && codiceSorgente[BASE_funzione + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < chiudere_funzione && 이름뒤(codiceSorgente[BASE_funzione + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == chiudere_funzione || codiceSorgente[BASE_funzione + 읽는자리] != '}')) { errore("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                variabile_VALORE(codiceSorgente, BASE_funzione + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(punto_di_codice);
        }
        return !estensione_errore;
    }
    static int ambiente_Impostazioni(int argomento_INDICE, boolean rimuovere) {
        int locale_START = InterpreteComandi.시작점[argomento_INDICE], chiudere_funzione = locale_START + InterpreteComandi.durata_VALORE[argomento_INDICE], 같음자리 = locale_START;
        while (같음자리 < chiudere_funzione && InterpreteComandi.token_VALORE[같음자리] != '=') 같음자리++;
        int voce_CONTA_NUMERI = 같음자리 - locale_START;
        if (voce_CONTA_NUMERI < 1 || voce_CONTA_NUMERI > 31 || !nome_carattere(InterpreteComandi.token_VALORE[locale_START]) || !rimuovere && 같음자리 == chiudere_funzione || chiudere_funzione - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDICE = locale_START; Loop_INDICE < 같음자리; Loop_INDICE++) if (!이름뒤(InterpreteComandi.token_VALORE[Loop_INDICE])) return 2;
        if (intervallo_SMS(InterpreteComandi.token_VALORE, locale_START, voce_CONTA_NUMERI, "PWD") || intervallo_SMS(InterpreteComandi.token_VALORE, locale_START, voce_CONTA_NUMERI, "HOME")) return 2;
        int 찾은여부 = -1, reparto_IT_vuota_Stato = -1;
        for (int Loop_INDICE = 0; Loop_INDICE < 16; Loop_INDICE++) {
            if (이름길이[Loop_INDICE] == 0) reparto_IT_vuota_Stato = Loop_INDICE;
            if (이름길이[Loop_INDICE] != voce_CONTA_NUMERI) continue;
            boolean match = true; for (int inner_funzione = 0; inner_funzione < voce_CONTA_NUMERI; inner_funzione++) if (variabile_nome[Loop_INDICE * 32 + inner_funzione] != InterpreteComandi.token_VALORE[locale_START + inner_funzione]) match = false;
            if (match) 찾은여부 = Loop_INDICE;
        }
        if (rimuovere) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = reparto_IT_vuota_Stato; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = voce_CONTA_NUMERI; VALORE_durata[찾은여부] = chiudere_funzione - 같음자리 - 1;
        for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) variabile_nome[찾은여부 * 32 + Loop_INDICE] = InterpreteComandi.token_VALORE[locale_START + Loop_INDICE];
        for (int Loop_INDICE = 같음자리 + 1; Loop_INDICE < chiudere_funzione; Loop_INDICE++) variabile_dati[찾은여부 * 256 + Loop_INDICE - 같음자리 - 1] = InterpreteComandi.token_VALORE[Loop_INDICE];
        return 0;
    }
    static void mostrare_ambiente() {
        단말.Scrittura("HOME=/\nPWD="); FileMemoria.Regolari_scrivere(); 단말.문자(10);
        for (int Loop_INDICE = 0; Loop_INDICE < 16; Loop_INDICE++) if (이름길이[Loop_INDICE] > 0) {
            for (int inner_funzione = 0; inner_funzione < 이름길이[Loop_INDICE]; inner_funzione++) scheda.scrivere_seriale(variabile_nome[Loop_INDICE * 32 + inner_funzione]); 단말.문자('=');
            for (int inner_funzione = 0; inner_funzione < VALORE_durata[Loop_INDICE]; inner_funzione++) scheda.scrivere_seriale(variabile_dati[Loop_INDICE * 256 + inner_funzione]); 단말.문자(10);
        }
    }
    static void Esegui_comando(int[] dati_array, int 시작변위, int voce_CONTA_NUMERI, int 중첩깊이) {
        if (중첩깊이 >= 4 || voce_CONTA_NUMERI > 4096) { errore("comando 파일의 annidamento_VALORE 또는 riga_di_ingresso durata_VALORE 제한을 넘었습니다"); return; }
        for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) codiceSorgente[중첩깊이 * 4096 + Loop_INDICE] = dati_array[시작변위 + Loop_INDICE];
        int totale_CONTA_NUMERI = Lettura(voce_CONTA_NUMERI, 중첩깊이); if (totale_CONTA_NUMERI < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < totale_CONTA_NUMERI) {
            int gruppo_chiudere = 읽는자리;
            while (gruppo_chiudere < totale_CONTA_NUMERI && (Kind_VALORE[중첩깊이 * 128 + gruppo_chiudere] == 0 || Kind_VALORE[중첩깊이 * 128 + gruppo_chiudere] >= 4)) gruppo_chiudere++;
            boolean Esegui_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && Stato_VALORE == 0 || 조건성립 == 3 && Stato_VALORE != 0;
            if (Esegui_cc685ae5) {
                boolean Indietro_articolo_INDICE = false;
                while (읽는자리 < gruppo_chiudere) {
                    int Avanti_funzione = 읽는자리; while (Avanti_funzione < gruppo_chiudere && Kind_VALORE[중첩깊이 * 128 + Avanti_funzione] != 4) Avanti_funzione++;
                    boolean CONNETTI_Stream = Avanti_funzione < gruppo_chiudere; int input_pagina = -1, output_pagina = -1, 출력방식 = 0;
                    InterpreteComandi.token_CONTA_NUMERI = 0; 쓴수 = 0; estensione_errore = false;
                    for (int Loop_INDICE = 읽는자리; Loop_INDICE < Avanti_funzione; Loop_INDICE++) {
                        int dati_Kind = Kind_VALORE[중첩깊이 * 128 + Loop_INDICE];
                        if (dati_Kind >= 5) { if (dati_Kind == 7) { if (input_pagina >= 0) { errore("input_VALORE 전환이 겹쳤습니다"); return; } input_pagina = ++Loop_INDICE; } else { if (output_pagina >= 0) { errore("uscitaTesto 전환이 겹쳤습니다"); return; } output_pagina = ++Loop_INDICE; 출력방식 = dati_Kind; } continue; }
                        if (InterpreteComandi.token_CONTA_NUMERI == 32) { errore("인수가 너무 많습니다"); return; }
                        int argomento_INDICE = InterpreteComandi.token_CONTA_NUMERI++; InterpreteComandi.시작점[argomento_INDICE] = 쓴수;
                        if (!Word_VALORE(Loop_INDICE, 중첩깊이)) return;
                        InterpreteComandi.durata_VALORE[argomento_INDICE] = 쓴수 - InterpreteComandi.시작점[argomento_INDICE];
                    }
                    연결중 = Indietro_articolo_INDICE || CONNETTI_Stream || input_pagina >= 0 || output_pagina >= 0;
                    if (연결중 && (InterpreteComandi.같음(0, "vi") || InterpreteComandi.같음(0, "edit") || InterpreteComandi.같음(0, "load") || InterpreteComandi.같음(0, "gui") || InterpreteComandi.같음(0, "terminal") || InterpreteComandi.같음(0, "sh") || InterpreteComandi.같음(0, "source"))) { errore("interattivo 명령과 comando 파일은 I_O 전환이나 Stream_VALORE 연결에 쓸 numero 없습니다"); return; }
                    셸입출력.avvia(Indietro_articolo_INDICE, CONNETTI_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int voce_funzione = 입출력바꿈 == 0 ? input_pagina : output_pagina; if (voce_funzione < 0) continue;
                        int START_funzione = 쓴수; if (!Word_VALORE(voce_funzione, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = FileMemoria.percorso_START(쓴수 - START_funzione);
                        for (int inner_funzione = START_funzione; 처리값 >= 0 && inner_funzione < 쓴수; inner_funzione++) 처리값 = FileMemoria.percorso_byte(inner_funzione - START_funzione, InterpreteComandi.token_VALORE[inner_funzione]);
                        if (처리값 >= 0) 처리값 = FileMemoria.Apri(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); InterpreteComandi.errore(처리값); Stato_VALORE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.file_di_input = 처리값; else 셸입출력.file_di_output = 처리값;
                    }
                    셸입출력.Consenti_interattivo = 중첩깊이 == 0 && 읽는자리 == 0 && Avanti_funzione == totale_CONTA_NUMERI;
                    깊이 = 중첩깊이; InterpreteComandi.risultato = 0; scheda.입출력전환(1);
                    InterpreteComandi.comando();
                    scheda.terminale(3);
                    int 반환값 = InterpreteComandi.risultato, Stream_errore = 셸입출력.errore_VALORE;
                    셸입출력.끝(); 연결중 = false;
                    Stato_VALORE = Stream_errore < 0 ? 1 : 반환값;
                    if (Stream_errore < 0) { InterpreteComandi.errore(Stream_errore); return; }
                    if (script_chiudere || 반환값 == -1005) return;
                    Indietro_articolo_INDICE = true; 읽는자리 = Avanti_funzione + 1;
                }
            }
            if (gruppo_chiudere < totale_CONTA_NUMERI) 조건성립 = Kind_VALORE[중첩깊이 * 128 + gruppo_chiudere];
            읽는자리 = gruppo_chiudere + 1;
        }
    }
    static void Esegui_File() {
        if (InterpreteComandi.token_CONTA_NUMERI != 2 || 깊이 >= 3) { InterpreteComandi.risultato = 2; 단말.Scrittura("사용법: sh file (annidamento_VALORE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = InterpreteComandi.percorso(1); if (처리값 >= 0) 처리값 = FileMemoria.Apri(0);
        if (처리값 < 0) { InterpreteComandi.errore(처리값); return; }
        int voce_CONTA_NUMERI = 0, byte_dati;
        while ((byte_dati = FileMemoria.Lettura(처리값)) != 256 && byte_dati >= 0 && voce_CONTA_NUMERI < 16384) script_VALORE[중첩깊이 * 16384 + voce_CONTA_NUMERI++] = byte_dati;
        FileMemoria.Chiudi(처리값); scheda.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < voce_CONTA_NUMERI && !script_chiudere;) {
            int chiudere_funzione = 읽는자리; while (chiudere_funzione < voce_CONTA_NUMERI && script_VALORE[중첩깊이 * 16384 + chiudere_funzione] != 10) chiudere_funzione++;
            int valido_durata = chiudere_funzione - 읽는자리; if (valido_durata > 0 && script_VALORE[중첩깊이 * 16384 + chiudere_funzione - 1] == 13) valido_durata--;
            Esegui_comando(script_VALORE, 중첩깊이 * 16384 + 읽는자리, valido_durata, 중첩깊이); 읽는자리 = chiudere_funzione + 1;
        }
        InterpreteComandi.risultato = Stato_VALORE; script_chiudere = false; 깊이 = 중첩깊이 - 1;
    }
}
