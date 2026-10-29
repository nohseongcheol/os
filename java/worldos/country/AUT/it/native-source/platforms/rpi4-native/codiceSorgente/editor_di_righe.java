// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALORE 경계를 지키는 삽입/삭제, 방향키, comando LOG_riga, Tab Completate_VALORE. */
public final class editor_di_righe {
    static boolean riga_di_comando;
    static int[] LOG_riga = new int[16 * 1024], LOG_durata = new int[16], Store_VALORE = new int[4096], candidato = new int[64];
    static int LOG_CONTA_NUMERI, LOG_riga_chiudere, Cerca_VALORE, 저장길이, Dimensione, cursore_VALORE, candidato_CONTA_NUMERI, candidato_durata, START_finestra;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd SSH remoto_display run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] comando_candidato = new int[128];
    static void Aggiungi_comando_candidato(String voce_elenco, int START_funzione, int chiudere_funzione, int input_durata) {
        int byte_CONTA_NUMERI=0;
        for(int funzione_INDICE=START_funzione;funzione_INDICE<chiudere_funzione;funzione_INDICE++) {
            int punto_di_codice=voce_elenco.charAt(funzione_INDICE);
            if(punto_di_codice>=0xd800 && punto_di_codice<=0xdbff && funzione_INDICE+1<chiudere_funzione)punto_di_codice=0x10000+((punto_di_codice-0xd800)<<10)+voce_elenco.charAt(++funzione_INDICE)-0xdc00;
            int numero=punto_di_codice<128?1:punto_di_codice<2048?2:punto_di_codice<65536?3:4;
            if(byte_CONTA_NUMERI+numero>62)return;
            for(int SEQUENZA_VALORE=numero-1;SEQUENZA_VALORE>=0;SEQUENZA_VALORE--)comando_candidato[byte_CONTA_NUMERI++]=numero==1?punto_di_codice:SEQUENZA_VALORE==numero-1?(numero==2?0xc0:numero==3?0xe0:0xf0)|(punto_di_codice>>(6*SEQUENZA_VALORE)):0x80|((punto_di_codice>>(6*SEQUENZA_VALORE))&63);
        }
        if(byte_CONTA_NUMERI<input_durata)return;
        for(int funzione_INDICE=0;funzione_INDICE<input_durata;funzione_INDICE++)if(comando_candidato[funzione_INDICE]!=InterpreteComandi.riga_di_ingresso[funzione_INDICE])return;
        candidato_CONTA_NUMERI++;candidato_durata=byte_CONTA_NUMERI+1;
        for(int funzione_INDICE=0;funzione_INDICE<byte_CONTA_NUMERI;funzione_INDICE++)candidato[funzione_INDICE]=comando_candidato[funzione_INDICE];candidato[byte_CONTA_NUMERI]=' ';
    }
    static int frontale_VALORE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (InterpreteComandi.riga_di_ingresso[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_VALORE(int 읽는자리) { if (읽는자리 < Dimensione) { 읽는자리++; while (읽는자리 < Dimensione && (InterpreteComandi.riga_di_ingresso[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_funzione, int meta_VALORE_INDICE) {
        int 글칸수 = 0;
        for (int Loop_INDICE = START_funzione; Loop_INDICE < meta_VALORE_INDICE; Loop_INDICE++) { int byte_dati = InterpreteComandi.riga_di_ingresso[Loop_INDICE]; if ((byte_dati & 192) == 128) continue; 글칸수 += byte_dati >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void retry_VALORE() {
        단말.Scrittura("\r\u001b[2K");
        단말.Scrittura(riga_di_comando ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 riga_di_ingresso 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLONNE = scheda.terminale(13) & 65535; return COLONNE - (riga_di_comando ? 18 : 9); }
    static void 보이는줄() {
        if (cursore_VALORE < START_finestra) START_finestra = cursore_VALORE;
        while (폭(START_finestra, cursore_VALORE) > 보이는폭()) START_finestra = BACK_VALORE(START_finestra);
        int chiudere_funzione = START_finestra;
        while (chiudere_funzione < Dimensione && 폭(START_finestra, BACK_VALORE(chiudere_funzione)) <= 보이는폭()) chiudere_funzione = BACK_VALORE(chiudere_funzione);
        단말.Scrittura("\r\u001b["); 단말.numero(riga_di_comando ? 16 : 7); 단말.Scrittura("G\u001b[K");
        if (START_finestra > 0) 단말.문자('<');
        for (int Loop_INDICE = START_finestra; Loop_INDICE < chiudere_funzione; Loop_INDICE++) scheda.scrivere_seriale(InterpreteComandi.riga_di_ingresso[Loop_INDICE]);
        단말.문자(chiudere_funzione < Dimensione ? '>' : ' ');
        단말.Scrittura("\u001b["); 단말.numero(폭(cursore_VALORE, chiudere_funzione) + 1); 단말.문자('D');
        가로보기 = START_finestra > 0 || chiudere_funzione < Dimensione || 폭(0, Dimensione) > 보이는폭();
    }
    static void Aggiunta_LOG() {
        if (!riga_di_comando || Dimensione == 0 || Dimensione > 1024) return;
        if (LOG_CONTA_NUMERI > 0) {
            int 마지막자리 = (LOG_riga_chiudere + 15) % 16; boolean 같은여부 = LOG_durata[마지막자리] == Dimensione;
            for (int Loop_INDICE = 0; 같은여부 && Loop_INDICE < Dimensione; Loop_INDICE++) if (LOG_riga[마지막자리 * 1024 + Loop_INDICE] != InterpreteComandi.riga_di_ingresso[Loop_INDICE]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_durata[LOG_riga_chiudere] = Dimensione; for (int Loop_INDICE = 0; Loop_INDICE < Dimensione; Loop_INDICE++) LOG_riga[LOG_riga_chiudere * 1024 + Loop_INDICE] = InterpreteComandi.riga_di_ingresso[Loop_INDICE];
        LOG_riga_chiudere = (LOG_riga_chiudere + 1) % 16; if (LOG_CONTA_NUMERI < 16) LOG_CONTA_NUMERI++;
    }
    static void 기록이동(int DELTA_VALORE) {
        if (!riga_di_comando) return;
        if (Cerca_VALORE == 0 && DELTA_VALORE > 0) { 저장길이 = Dimensione; for (int Loop_INDICE = 0; Loop_INDICE < Dimensione; Loop_INDICE++) Store_VALORE[Loop_INDICE] = InterpreteComandi.riga_di_ingresso[Loop_INDICE]; }
        int Avanti_funzione = Cerca_VALORE + DELTA_VALORE; if (Avanti_funzione < 0 || Avanti_funzione > LOG_CONTA_NUMERI) return; Cerca_VALORE = Avanti_funzione;
        if (Cerca_VALORE == 0) { Dimensione = 저장길이; for (int Loop_INDICE = 0; Loop_INDICE < Dimensione; Loop_INDICE++) InterpreteComandi.riga_di_ingresso[Loop_INDICE] = Store_VALORE[Loop_INDICE]; }
        else { int 보관칸 = (LOG_riga_chiudere + 16 - Cerca_VALORE) % 16; Dimensione = LOG_durata[보관칸]; for (int Loop_INDICE = 0; Loop_INDICE < Dimensione; Loop_INDICE++) InterpreteComandi.riga_di_ingresso[Loop_INDICE] = LOG_riga[보관칸 * 1024 + Loop_INDICE]; }
        cursore_VALORE = Dimensione; retry_VALORE();
    }
    static void mostrare_LOG() {
        for (int voce_CONTA_NUMERI = 0; voce_CONTA_NUMERI < LOG_CONTA_NUMERI; voce_CONTA_NUMERI++) {
            int 보관칸 = (LOG_riga_chiudere + 16 - LOG_CONTA_NUMERI + voce_CONTA_NUMERI) % 16; 단말.numero(voce_CONTA_NUMERI + 1); 단말.Scrittura("  ");
            for (int Loop_INDICE = 0; Loop_INDICE < LOG_durata[보관칸]; Loop_INDICE++) scheda.scrivere_seriale(LOG_riga[보관칸 * 1024 + Loop_INDICE]); 단말.문자(10);
        }
    }
    static void Aggiungi_candidato(int[] dati_array, int START_funzione, int voce_CONTA_NUMERI, int 접두말, int totale_CONTA_NUMERI, boolean elenco_numero) {
        if (voce_CONTA_NUMERI < totale_CONTA_NUMERI || voce_CONTA_NUMERI > 62) return;
        for (int Loop_INDICE = 0; Loop_INDICE < totale_CONTA_NUMERI; Loop_INDICE++) if (dati_array[START_funzione + Loop_INDICE] != InterpreteComandi.riga_di_ingresso[접두말 + Loop_INDICE]) return;
        candidato_CONTA_NUMERI++; candidato_durata = voce_CONTA_NUMERI + 1;
        for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) candidato[Loop_INDICE] = dati_array[START_funzione + Loop_INDICE]; candidato[voce_CONTA_NUMERI] = elenco_numero ? '/' : ' ';
    }
    static void Completate_VALORE() {
        if (!riga_di_comando || cursore_VALORE != Dimensione) return;
        int 시작점 = Dimensione; while (시작점 > 0 && InterpreteComandi.riga_di_ingresso[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDICE = 시작점; Loop_INDICE < Dimensione; Loop_INDICE++) if (InterpreteComandi.riga_di_ingresso[Loop_INDICE] == '/' || InterpreteComandi.riga_di_ingresso[Loop_INDICE] == '"' || InterpreteComandi.riga_di_ingresso[Loop_INDICE] == 39 || InterpreteComandi.riga_di_ingresso[Loop_INDICE] == '\\') return;
        candidato_CONTA_NUMERI = 0; int voce_CONTA_NUMERI = Dimensione - 시작점;
        if (시작점 == 0) {
            for(int indice_di_elenco=0;indice_di_elenco<2;indice_di_elenco++) {
                String voce_elenco=indice_di_elenco==0?명령들:관리명령.Completate_Word();
                int 읽는자리=0;
                while(읽는자리<voce_elenco.length()) {
                    int chiudere_funzione=읽는자리;while(chiudere_funzione<voce_elenco.length() && voce_elenco.charAt(chiudere_funzione)!=' ')chiudere_funzione++;
                    Aggiungi_comando_candidato(voce_elenco,읽는자리,chiudere_funzione,voce_CONTA_NUMERI);읽는자리=chiudere_funzione+1;
                }
            }
        } else {
            FileMemoria.percorso_START(1); FileMemoria.percorso_byte(0, '.'); FileMemoria.normalizzare_VALORE();
            for (int Loop_INDICE = 0; Loop_INDICE < FileMemoria.File_CONTA_NUMERI; Loop_INDICE++) {
                int START_funzione = FileMemoria.voce_START(FileMemoria.Nome, Loop_INDICE * 64, FileMemoria.이름길이[Loop_INDICE]);
                if (START_funzione >= 0) Aggiungi_candidato(FileMemoria.Nome, Loop_INDICE * 64 + START_funzione, FileMemoria.이름길이[Loop_INDICE] - START_funzione, 시작점, voce_CONTA_NUMERI, false);
            }
            for (int Loop_INDICE = 0; Loop_INDICE < 16; Loop_INDICE++) {
                int START_funzione = FileMemoria.voce_START(FileMemoria.elenco_nome, Loop_INDICE * 64, FileMemoria.elenco_durata[Loop_INDICE]);
                if (START_funzione >= 0) Aggiungi_candidato(FileMemoria.elenco_nome, Loop_INDICE * 64 + START_funzione, FileMemoria.elenco_durata[Loop_INDICE] - START_funzione, 시작점, voce_CONTA_NUMERI, true);
            }
        }
        if (candidato_CONTA_NUMERI != 1) { scheda.scrivere_seriale(7); return; }
        for (int Loop_INDICE = voce_CONTA_NUMERI; Loop_INDICE < candidato_durata && Dimensione < InterpreteComandi.riga_di_ingresso.length - 1; Loop_INDICE++) {
            if (candidato[Loop_INDICE] == ' ' && Loop_INDICE != candidato_durata - 1) InterpreteComandi.riga_di_ingresso[Dimensione++] = '\\';
            InterpreteComandi.riga_di_ingresso[Dimensione++] = candidato[Loop_INDICE];
        }
        cursore_VALORE = Dimensione; retry_VALORE();
    }
    static int 탈출읽기() {
        int 시작점 = scheda.밀리초();
        while (scheda.밀리초() - 시작점 < 80) { int byte_dati = scheda.직렬읽기(); if (byte_dati >= 0) return byte_dati; scheda.REND_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int voce_CONTA_NUMERI = 0, chiudere_funzione = -1;
        for (int Loop_INDICE = 0; Loop_INDICE < 12; Loop_INDICE++) { int byte_dati = 탈출읽기(); if (byte_dati < 0) return; if (byte_dati >= '0' && byte_dati <= '9') voce_CONTA_NUMERI = voce_CONTA_NUMERI * 10 + byte_dati - '0'; else { chiudere_funzione = byte_dati; break; } }
        if (chiudere_funzione == 'A') 기록이동(1);
        else if (chiudere_funzione == 'B') 기록이동(-1);
        else if (chiudere_funzione == 'C') { cursore_VALORE = BACK_VALORE(cursore_VALORE); retry_VALORE(); }
        else if (chiudere_funzione == 'D') { cursore_VALORE = frontale_VALORE(cursore_VALORE); retry_VALORE(); }
        else if (chiudere_funzione == 'H' || chiudere_funzione == '~' && (voce_CONTA_NUMERI == 1 || voce_CONTA_NUMERI == 7)) { cursore_VALORE = 0; retry_VALORE(); }
        else if (chiudere_funzione == 'F' || chiudere_funzione == '~' && (voce_CONTA_NUMERI == 4 || voce_CONTA_NUMERI == 8)) { cursore_VALORE = Dimensione; retry_VALORE(); }
        else if (chiudere_funzione == '~' && voce_CONTA_NUMERI == 3 && cursore_VALORE < Dimensione) {
            int Avanti_funzione = BACK_VALORE(cursore_VALORE); for (int Loop_INDICE = Avanti_funzione; Loop_INDICE < Dimensione; Loop_INDICE++) InterpreteComandi.riga_di_ingresso[Loop_INDICE - Avanti_funzione + cursore_VALORE] = InterpreteComandi.riga_di_ingresso[Loop_INDICE]; Dimensione -= Avanti_funzione - cursore_VALORE; retry_VALORE();
        }
        else if (chiudere_funzione == '~' && (voce_CONTA_NUMERI == 5 || voce_CONTA_NUMERI == 6)) scheda.terminale(voce_CONTA_NUMERI == 5 ? 5 : 6);
        else if (chiudere_funzione == '~' && voce_CONTA_NUMERI == 24 && riga_di_comando) { InterpreteComandi.terminale(true); }
    }
    static int Lettura() {
        if (!finestra_sessione.이어읽기) { Dimensione = cursore_VALORE = Cerca_VALORE = START_finestra = 0; 가로보기 = false; }
        else { finestra_sessione.이어읽기 = false; retry_VALORE(); } boolean overflow = false;
        while (true) {
            int byte_dati = scheda.직렬읽기(); if (byte_dati == -4096) return -3;
            if (scheda.terminale(14) != 0) retry_VALORE(); if (byte_dati < 0) { scheda.REND_CPU(); continue; }
            if (byte_dati == 10 && InterpreteComandi.Indietro_riga) { InterpreteComandi.Indietro_riga = false; continue; } InterpreteComandi.Indietro_riga = byte_dati == 13;
            if (byte_dati == 27) { 탈출(); continue; }
            if (byte_dati == 3) { 단말.Scrittura("^C\n"); return -1; }
            if (byte_dati == 4 && Dimensione == 0 && riga_di_comando) { if (scheda.terminale(2) != 0) InterpreteComandi.terminale(true); return -1; }
            if (byte_dati == 13 || byte_dati == 10) { 단말.문자(10); if (!overflow) Aggiunta_LOG(); return overflow ? -2 : Dimensione; }
            if (byte_dati == 9 && riga_di_comando) { Completate_VALORE(); continue; }
            if (byte_dati == 1 || byte_dati == 5) { cursore_VALORE = byte_dati == 1 ? 0 : Dimensione; retry_VALORE(); continue; }
            if (byte_dati == 8 || byte_dati == 127 || byte_dati == 21) {
                if (byte_dati == 21) { for (int Loop_INDICE = cursore_VALORE; Loop_INDICE < Dimensione; Loop_INDICE++) InterpreteComandi.riga_di_ingresso[Loop_INDICE - cursore_VALORE] = InterpreteComandi.riga_di_ingresso[Loop_INDICE]; Dimensione -= cursore_VALORE; cursore_VALORE = 0; }
                else if (cursore_VALORE > 0) { int 변경전 = frontale_VALORE(cursore_VALORE); for (int Loop_INDICE = cursore_VALORE; Loop_INDICE < Dimensione; Loop_INDICE++) InterpreteComandi.riga_di_ingresso[Loop_INDICE - cursore_VALORE + 변경전] = InterpreteComandi.riga_di_ingresso[Loop_INDICE]; Dimensione -= cursore_VALORE - 변경전; cursore_VALORE = 변경전; }
                retry_VALORE(); continue;
            }
            if (byte_dati == 11) { Dimensione = cursore_VALORE; retry_VALORE(); continue; }
            if (byte_dati < 32 && byte_dati != 9) continue;
            if (Dimensione == InterpreteComandi.riga_di_ingresso.length) { overflow = true; continue; }
            for (int Loop_INDICE = Dimensione; Loop_INDICE > cursore_VALORE; Loop_INDICE--) InterpreteComandi.riga_di_ingresso[Loop_INDICE] = InterpreteComandi.riga_di_ingresso[Loop_INDICE - 1];
            InterpreteComandi.riga_di_ingresso[cursore_VALORE++] = byte_dati; Dimensione++;
            if (cursore_VALORE == Dimensione && !가로보기 && 폭(0, Dimensione) <= 보이는폭()) scheda.scrivere_seriale(byte_dati);
            else if (cursore_VALORE == Dimensione) 보이는줄(); else retry_VALORE();
        }
    }
}
