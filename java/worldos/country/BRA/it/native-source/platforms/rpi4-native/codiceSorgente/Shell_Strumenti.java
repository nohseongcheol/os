// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 Shell 내장 strumenti. */
public final class Shell_Strumenti {
    static int[] dati = new int[16384];
    static int file_di_input = -1;
    static int aperto_File(int argomento_INDICE, int Processi_MODA) {
        int 처리값 = InterpreteComandi.percorso(argomento_INDICE); return 처리값 < 0 ? 처리값 : FileMemoria.Apri(Processi_MODA);
    }
    static boolean Prepara_input(int argomento_INDICE) {
        file_di_input = -1;
        if (argomento_INDICE < InterpreteComandi.token_CONTA_NUMERI) {
            file_di_input = aperto_File(argomento_INDICE, 0);
            if (file_di_input < 0) { InterpreteComandi.errore(file_di_input); return false; }
        }
        return true;
    }
    static int Lettura() {
        if (file_di_input >= 3) return FileMemoria.Lettura(file_di_input);
        while (true) {
            int byte_dati = scheda.직렬읽기(); if (byte_dati == -2 || byte_dati == 4) return 256;
            if (byte_dati == 3) { InterpreteComandi.risultato = 130; return 256; }
            if (byte_dati >= 0) return byte_dati; scheda.REND_CPU();
        }
    }
    static void Chiudi() { if (file_di_input >= 3) FileMemoria.Chiudi(file_di_input); file_di_input = -1; }
    static void Vista_VALORE() {
        int 마지막자리 = InterpreteComandi.token_CONTA_NUMERI == 1 ? 2 : InterpreteComandi.token_CONTA_NUMERI;
        for (int argomento_INDICE = 1; argomento_INDICE < 마지막자리; argomento_INDICE++) {
            if (!Prepara_input(argomento_INDICE)) continue;
            int byte_dati; while ((byte_dati = Lettura()) != 256 && byte_dati >= 0) scheda.scrivere_seriale(byte_dati);
            if (byte_dati < 0) InterpreteComandi.errore(byte_dati); Chiudi();
        }
    }
    static void File_caso(String Action_numero) {
        if (InterpreteComandi.token_CONTA_NUMERI != 2) { InterpreteComandi.risultato = 2; 단말.Scrittura("사용법: mkdir/rmdir/touch file\n"); return; }
        int 처리값 = InterpreteComandi.percorso(1);
        if (처리값 >= 0) {
            if (Action_numero.charAt(0) == 'm') 처리값 = FileMemoria.Crea_elenco();
            else if (Action_numero.charAt(0) == 'r') 처리값 = FileMemoria.rimuovere_elenco();
            else { 처리값 = FileMemoria.Apri(65); if (처리값 >= 3) 처리값 = FileMemoria.Chiudi(처리값); }
        }
        if (처리값 < 0) InterpreteComandi.errore(처리값);
    }
    static void copiare_VALORE(boolean 이동여부) {
        if (InterpreteComandi.token_CONTA_NUMERI != 3) { InterpreteComandi.risultato = 2; 단말.Scrittura("사용법: cp/mv 원본 meta_endpoint (file)\n"); return; }
        int 처리값 = InterpreteComandi.percorso(1); if (처리값 >= 0) 처리값 = FileMemoria.normalizzare_VALORE();
        if (처리값 < 0) { InterpreteComandi.errore(처리값); return; }
        int 원본번호 = FileMemoria.TROVA_voce(); if (원본번호 < 0) { InterpreteComandi.errore(-2); return; }
        int voce_CONTA_NUMERI = FileMemoria.durata_VALORE[원본번호]; for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) dati[Loop_INDICE] = FileMemoria.자료읽기(원본번호, Loop_INDICE);
        처리값 = InterpreteComandi.percorso(2); if (처리값 >= 0) 처리값 = FileMemoria.normalizzare_VALORE();
        if (처리값 < 0) { InterpreteComandi.errore(처리값); return; }
        if (FileMemoria.TROVA_voce() == 원본번호) { if (!이동여부) InterpreteComandi.errore(-22); return; }
        if (이동여부) { 처리값 = FileMemoria.Rinomina_voce(원본번호); if (처리값 < 0) InterpreteComandi.errore(처리값); return; }
        int 열린파일번호 = FileMemoria.Apri(577); if (열린파일번호 < 0) { InterpreteComandi.errore(열린파일번호); return; }
        for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) { 처리값 = FileMemoria.Scrittura(열린파일번호, dati[Loop_INDICE]); if (처리값 < 0) { InterpreteComandi.errore(처리값); break; } }
        FileMemoria.Chiudi(열린파일번호);
    }
    static int cifra_VALORE(int argomento_INDICE) {
        if (argomento_INDICE >= InterpreteComandi.token_CONTA_NUMERI) return -1;
        int voce_CONTA_NUMERI = 0; for (int Loop_INDICE = 0; Loop_INDICE < InterpreteComandi.durata_VALORE[argomento_INDICE]; Loop_INDICE++) { int punto_di_codice = InterpreteComandi.token_VALORE[InterpreteComandi.시작점[argomento_INDICE] + Loop_INDICE]; if (punto_di_codice < '0' || punto_di_codice > '9' || voce_CONTA_NUMERI > 10000) return -1; voce_CONTA_NUMERI = voce_CONTA_NUMERI * 10 + punto_di_codice - '0'; } return voce_CONTA_NUMERI;
    }
    static void 세기() {
        int argomento_INDICE = 1, opzione = 0;
        if (InterpreteComandi.같음(1, "-c") || InterpreteComandi.같음(1, "-l") || InterpreteComandi.같음(1, "-w")) { opzione = InterpreteComandi.같음(1, "-c") ? 1 : InterpreteComandi.같음(1, "-l") ? 2 : 3; argomento_INDICE++; }
        if (InterpreteComandi.token_CONTA_NUMERI > argomento_INDICE + 1) { InterpreteComandi.risultato = 2; 단말.Scrittura("사용법: wc [-c|-l|-w] [file]\n"); return; }
        if (!Prepara_input(argomento_INDICE)) return;
        int byte_CONTA_NUMERI = 0, 줄수 = 0, 낱말수 = 0, byte_dati; boolean 낱말 = false;
        while ((byte_dati = Lettura()) >= 0 && byte_dati != 256) { byte_CONTA_NUMERI++; if (byte_dati == 10) 줄수++; boolean Space = byte_dati == 32 || byte_dati >= 9 && byte_dati <= 13; if (!Space && !낱말) 낱말수++; 낱말 = !Space; }
        Chiudi(); if (byte_dati < 0) { InterpreteComandi.errore(byte_dati); return; }
        if (opzione != 0) 단말.numero(opzione == 1 ? byte_CONTA_NUMERI : opzione == 2 ? 줄수 : 낱말수);
        else { 단말.numero(줄수); 단말.문자(' '); 단말.numero(낱말수); 단말.문자(' '); 단말.numero(byte_CONTA_NUMERI); } 단말.문자(10);
    }
    static void TROVA_voce() {
        if (InterpreteComandi.token_CONTA_NUMERI < 2 || InterpreteComandi.token_CONTA_NUMERI > 3) { InterpreteComandi.risultato = 2; 단말.Scrittura("사용법: grep 찾을문구 [file]\n"); return; }
        if (!Prepara_input(2)) return;
        int voce_CONTA_NUMERI = 0, byte_dati, 일치수 = 0;
        while (true) {
            byte_dati = Lettura();
            if (byte_dati == 10 || byte_dati == 256 || byte_dati < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDICE = 0; Loop_INDICE <= voce_CONTA_NUMERI - InterpreteComandi.durata_VALORE[1]; Loop_INDICE++) {
                    boolean 같은여부 = true; for (int inner_funzione = 0; inner_funzione < InterpreteComandi.durata_VALORE[1]; inner_funzione++) if (dati[Loop_INDICE + inner_funzione] != InterpreteComandi.token_VALORE[InterpreteComandi.시작점[1] + inner_funzione]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (voce_CONTA_NUMERI > 0 || byte_dati == 10)) { for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) scheda.scrivere_seriale(dati[Loop_INDICE]); 단말.문자(10); 일치수++; }
                voce_CONTA_NUMERI = 0; if (byte_dati != 10) break;
            } else if (voce_CONTA_NUMERI < dati.length) dati[voce_CONTA_NUMERI++] = byte_dati;
            else { InterpreteComandi.errore(-28); Chiudi(); return; }
        }
        Chiudi(); if (byte_dati < 0) InterpreteComandi.errore(byte_dati); else if (InterpreteComandi.risultato == 0) InterpreteComandi.risultato = 일치수 == 0 ? 1 : 0;
    }
    static void intestazione_VALORE(boolean 뒤쪽자리) {
        int argomento_INDICE = 1, 줄수 = 10;
        if (InterpreteComandi.같음(1, "-n")) { 줄수 = cifra_VALORE(2); argomento_INDICE = 3; }
        if (줄수 < 0 || InterpreteComandi.token_CONTA_NUMERI > argomento_INDICE + 1) { InterpreteComandi.risultato = 2; 단말.Scrittura("사용법: head/tail [-n 줄수] [file]\n"); return; }
        if (!Prepara_input(argomento_INDICE)) return;
        int voce_CONTA_NUMERI = 0, byte_dati;
        while ((byte_dati = Lettura()) != 256 && byte_dati >= 0) { if (voce_CONTA_NUMERI == dati.length) { InterpreteComandi.errore(-28); Chiudi(); return; } dati[voce_CONTA_NUMERI++] = byte_dati; }
        Chiudi(); if (byte_dati < 0) { InterpreteComandi.errore(byte_dati); return; }
        int locale_START = 0, chiudere_funzione = voce_CONTA_NUMERI;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int totale_CONTA_NUMERI = 0; for (int Loop_INDICE = voce_CONTA_NUMERI - 2; Loop_INDICE >= 0; Loop_INDICE--) if (dati[Loop_INDICE] == 10 && ++totale_CONTA_NUMERI == 줄수) { locale_START = Loop_INDICE + 1; break; } }
        else { int totale_CONTA_NUMERI = 0; for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) if (dati[Loop_INDICE] == 10 && ++totale_CONTA_NUMERI == 줄수) { chiudere_funzione = Loop_INDICE + 1; break; } }
        for (int Loop_INDICE = locale_START; Loop_INDICE < chiudere_funzione; Loop_INDICE++) scheda.scrivere_seriale(dati[Loop_INDICE]);
    }
    static void scrivere_Insieme() {
        boolean Aggiunta = InterpreteComandi.같음(1, "-a"); int argomento_INDICE = Aggiunta ? 2 : 1;
        if (InterpreteComandi.token_CONTA_NUMERI != argomento_INDICE + 1) { InterpreteComandi.risultato = 2; 단말.Scrittura("사용법: tee [-a] file\n"); return; }
        int 열린파일번호 = aperto_File(argomento_INDICE, Aggiunta ? 1089 : 577); if (열린파일번호 < 0) { InterpreteComandi.errore(열린파일번호); return; }
        file_di_input = -1; int byte_dati;
        while ((byte_dati = Lettura()) != 256 && byte_dati >= 0) { int 처리값 = FileMemoria.Scrittura(열린파일번호, byte_dati); if (처리값 < 0) { InterpreteComandi.errore(처리값); break; } scheda.scrivere_seriale(byte_dati); }
        FileMemoria.Chiudi(열린파일번호);
    }
}
