// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 riga_di_comando. offerta, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class InterpreteComandi {
    static int[] riga_di_ingresso = new int[4096], token_VALORE = new int[4096], 시작점 = new int[32], durata_VALORE = new int[32];
    static int[] Modificati_Sommario = new int[16384], Modifica_nome = new int[63];
    static int token_CONTA_NUMERI, Modifica_nome_durata, risultato;
    static boolean Indietro_riga;
    static void 원바이트(int VALORE) { scheda.scrivere_seriale(VALORE); }
    static int leggi_riga_di_ingresso() { return editor_di_righe.Lettura(); }
    static boolean 나누기(int Dimensione) {
        int posizione = 0, 끝 = 0; token_CONTA_NUMERI = 0;
        while (posizione < Dimensione) {
            while (posizione < Dimensione && (riga_di_ingresso[posizione] == 32 || riga_di_ingresso[posizione] == 9)) posizione++;
            if (posizione == Dimensione) break;
            if (token_CONTA_NUMERI == 16) { 단말.Scrittura("comando analizzare_VALORE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_CONTA_NUMERI] = 끝; int offerta_VALORE = 0;
            while (posizione < Dimensione) {
                int VALORE = riga_di_ingresso[posizione++];
                if (offerta_VALORE == 0 && (VALORE == 32 || VALORE == 9)) break;
                if (VALORE == offerta_VALORE) { offerta_VALORE = 0; continue; }
                if (offerta_VALORE == 0 && (VALORE == 39 || VALORE == 34)) { offerta_VALORE = VALORE; continue; }
                token_VALORE[끝++] = VALORE;
            }
            if (offerta_VALORE != 0) { 단말.Scrittura("comando analizzare_VALORE: 따옴표가 닫히지 않았습니다\n"); return false; }
            durata_VALORE[token_CONTA_NUMERI] = 끝 - 시작점[token_CONTA_NUMERI]; token_CONTA_NUMERI++;
        }
        return true;
    }
    static boolean 같음(int INDICE, String Word_SMS) {
        if (INDICE >= token_CONTA_NUMERI) return false;
        int funzione_INDICE=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int punto_di_codice=Word_SMS.charAt(순번);
            if (punto_di_codice>=0xd800 && punto_di_codice<=0xdbff && 순번+1<Word_SMS.length()) punto_di_codice=0x10000+((punto_di_codice-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int byte_CONTA_NUMERI=punto_di_codice<128?1:punto_di_codice<2048?2:punto_di_codice<65536?3:4;
            for (int SEQUENZA_VALORE=byte_CONTA_NUMERI-1; SEQUENZA_VALORE>=0; SEQUENZA_VALORE--) {
                int VALORE=byte_CONTA_NUMERI==1?punto_di_codice:SEQUENZA_VALORE==byte_CONTA_NUMERI-1?(byte_CONTA_NUMERI==2?0xc0:byte_CONTA_NUMERI==3?0xe0:0xf0)|(punto_di_codice>>(6*SEQUENZA_VALORE)):0x80|((punto_di_codice>>(6*SEQUENZA_VALORE))&63);
                if (funzione_INDICE>=durata_VALORE[INDICE] || token_VALORE[시작점[INDICE]+funzione_INDICE++]!=VALORE) return false;
            }
        }
        return funzione_INDICE==durata_VALORE[INDICE];
    }
    static int percorso(int INDICE) {
        if (INDICE >= token_CONTA_NUMERI) return -22;
        int risultato = FileMemoria.percorso_START(durata_VALORE[INDICE]); if (risultato < 0) return risultato;
        for (int Loop_INDICE = 0; Loop_INDICE < durata_VALORE[INDICE]; Loop_INDICE++) {
            risultato = FileMemoria.percorso_byte(Loop_INDICE, token_VALORE[시작점[INDICE] + Loop_INDICE]); if (risultato < 0) return risultato;
        }
        return 0;
    }
    static void errore(int INDICE) { risultato = 1; 단말.Scrittura("errore "); 단말.numero(INDICE); 단말.문자(10); }
    static void Vista_VALORE() {
        if (token_CONTA_NUMERI != 2) { 단말.Scrittura("사용법: cat file\n"); return; }
        int risultato = percorso(1); if (risultato < 0) { errore(risultato); return; }
        int file = FileMemoria.Apri(0); if (file < 0) { errore(file); return; }
        while (true) { int VALORE = FileMemoria.Lettura(file); if (VALORE == 256) break; if (VALORE < 0) { errore(VALORE); break; } 원바이트(VALORE); }
        FileMemoria.Chiudi(file); 단말.문자(10);
    }
    static void Modifica_VALORE() {
        if (token_CONTA_NUMERI != 2) { 단말.Scrittura("사용법: edit file\n"); return; }
        int risultato = percorso(1); if (risultato < 0) { errore(risultato); return; }
        Modifica_nome_durata = durata_VALORE[1];
        for (int Loop_INDICE = 0; Loop_INDICE < Modifica_nome_durata; Loop_INDICE++) Modifica_nome[Loop_INDICE] = token_VALORE[시작점[1] + Loop_INDICE];
        단말.Scrittura("EDIT: file 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Dimensione = 0;
        while (true) {
            단말.Scrittura("edit> "); int input_VALORE = leggi_riga_di_ingresso();
            if (input_VALORE < 0) { 단말.Scrittura("EDIT CANCELLED\n"); return; }
            if (input_VALORE == 1 && riga_di_ingresso[0] == '.') break;
            if (input_VALORE + 1 > Modificati_Sommario.length - Dimensione) { 단말.Scrittura("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDICE = 0; Loop_INDICE < input_VALORE; Loop_INDICE++) Modificati_Sommario[Dimensione++] = riga_di_ingresso[Loop_INDICE];
            Modificati_Sommario[Dimensione++] = 10;
        }
        FileMemoria.percorso_START(Modifica_nome_durata);
        for (int Loop_INDICE = 0; Loop_INDICE < Modifica_nome_durata; Loop_INDICE++) FileMemoria.percorso_byte(Loop_INDICE, Modifica_nome[Loop_INDICE]);
        int file = FileMemoria.Apri(577); if (file < 0) { errore(file); return; }
        for (int Loop_INDICE = 0; Loop_INDICE < Dimensione; Loop_INDICE++) FileMemoria.Scrittura(file, Modificati_Sommario[Loop_INDICE]);
        FileMemoria.Chiudi(file); 단말.Scrittura("SAVED "); 단말.numero(Dimensione); 단말.Scrittura("byte_VALORE(주기억 file)\n");
    }
    static int valore_esadecimale(int VALORE) {
        if (VALORE >= '0' && VALORE <= '9') return VALORE - '0';
        if (VALORE >= 'a' && VALORE <= 'f') return VALORE - 'a' + 10;
        if (VALORE >= 'A' && VALORE <= 'F') return VALORE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_CONTA_NUMERI != 2) { 단말.Scrittura("사용법: load file | hex file\n"); return; }
        int risultato = percorso(1); if (risultato < 0) { errore(risultato); return; }
        if (!넣기) {
            int file = FileMemoria.Apri(0); if (file < 0) { errore(file); return; }
            단말.Scrittura("HEX BEGIN "); 단말.numero(FileMemoria.Dimensione(file)); 단말.문자(10);
            int voce_CONTA_NUMERI = 0;
            while (true) {
                int VALORE = FileMemoria.Lettura(file); if (VALORE < 0 || VALORE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALORE >> 4)); 단말.문자("0123456789abcdef".charAt(VALORE & 15));
                if (++voce_CONTA_NUMERI % 32 == 0) 단말.문자(10);
            }
            if (voce_CONTA_NUMERI % 32 != 0) 단말.문자(10);
            FileMemoria.Chiudi(file); 단말.Scrittura("HEX END\n"); return;
        }
        Modifica_nome_durata = durata_VALORE[1];
        for (int Loop_INDICE = 0; Loop_INDICE < Modifica_nome_durata; Loop_INDICE++) Modifica_nome[Loop_INDICE] = token_VALORE[시작점[1] + Loop_INDICE];
        단말.Scrittura("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Dimensione = 0;
        while (true) {
            단말.Scrittura("hex> "); int input_VALORE = leggi_riga_di_ingresso();
            if (input_VALORE < 0) { 단말.Scrittura("LOAD CANCELLED\n"); return; }
            if (input_VALORE == 1 && riga_di_ingresso[0] == '.') break;
            int frontale_VALORE = -1;
            for (int Loop_INDICE = 0; Loop_INDICE < input_VALORE; Loop_INDICE++) {
                if (riga_di_ingresso[Loop_INDICE] == 32 || riga_di_ingresso[Loop_INDICE] == 9) continue;
                int VALORE = valore_esadecimale(riga_di_ingresso[Loop_INDICE]);
                if (VALORE < 0 || Dimensione >= Modificati_Sommario.length) { 단말.Scrittura("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (frontale_VALORE < 0) frontale_VALORE = VALORE; else { Modificati_Sommario[Dimensione++] = frontale_VALORE * 16 + VALORE; frontale_VALORE = -1; }
            }
            if (frontale_VALORE >= 0) { 단말.Scrittura("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        FileMemoria.percorso_START(Modifica_nome_durata);
        for (int Loop_INDICE = 0; Loop_INDICE < Modifica_nome_durata; Loop_INDICE++) FileMemoria.percorso_byte(Loop_INDICE, Modifica_nome[Loop_INDICE]);
        int file = FileMemoria.Apri(577); if (file < 0) { errore(file); return; }
        for (int Loop_INDICE = 0; Loop_INDICE < Dimensione; Loop_INDICE++) FileMemoria.Scrittura(file, Modificati_Sommario[Loop_INDICE]);
        FileMemoria.Chiudi(file); 단말.Scrittura("LOADED "); 단말.numero(Dimensione); 단말.Scrittura("byte_VALORE(주기억 file)\n");
    }
    static int strumenti(int INDICE) {
        return strumento_voce(INDICE, 1);
    }
    static int strumento_voce(int INDICE, int avvia) {
        if (token_CONTA_NUMERI - avvia > 8) return -22;
        scheda.인수준비(token_CONTA_NUMERI - avvia);
        for (int 첫값 = avvia; 첫값 < token_CONTA_NUMERI; 첫값++) {
            if (durata_VALORE[첫값] > 255) return -36;
            for (int Loop_INDICE = 0; Loop_INDICE < durata_VALORE[첫값]; Loop_INDICE++) scheda.argomento_byte(첫값 - avvia, Loop_INDICE, token_VALORE[시작점[첫값] + Loop_INDICE]);
        }
        return INDICE == -2 ? scheda.리눅스파일실행() : INDICE < 0 ? scheda.Esegui_USER_File() : scheda.eseguire_USER_app(INDICE);
    }
    static int PYTHON_aggregare() {
        if (token_CONTA_NUMERI > 8) return -22;
        scheda.인수준비(token_CONTA_NUMERI);
        String percorso = "/lib/aggregare.py";
        // Java 문자열을 셸의 UTF-8 argomenti 버퍼에 기록한다.
        int funzione_INDICE = 0;
        for (int 순번 = 0; 순번 < percorso.length(); 순번++) {
            int carattere_VALORE = percorso.charAt(순번);
            if (carattere_VALORE < 128) scheda.argomento_byte(0, funzione_INDICE++, carattere_VALORE);
            else { scheda.argomento_byte(0, funzione_INDICE++, 0xe0 | (carattere_VALORE >> 12)); scheda.argomento_byte(0, funzione_INDICE++, 0x80 | ((carattere_VALORE >> 6) & 63)); scheda.argomento_byte(0, funzione_INDICE++, 0x80 | (carattere_VALORE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_CONTA_NUMERI; 순번++) {
            if (durata_VALORE[순번] > 255) return -36;
            for (int carattere_VALORE = 0; carattere_VALORE < durata_VALORE[순번]; carattere_VALORE++) scheda.argomento_byte(순번, carattere_VALORE, token_VALORE[시작점[순번] + carattere_VALORE]);
        }
        return scheda.eseguire_USER_app(12);
    }
    static int esecuzione_formato() {
        int 처리값 = percorso(0); if (처리값 < 0) return 처리값;
        int file = FileMemoria.Apri(0); if (file < 0) return file;
        int 첫값 = FileMemoria.Lettura(file), byte_dati = FileMemoria.Lettura(file), punto_di_codice = FileMemoria.Lettura(file), finale_VALORE = FileMemoria.Lettura(file);
        FileMemoria.Chiudi(file);
        if (첫값 == 127 && byte_dati == 'E' && punto_di_codice == 'L' && finale_VALORE == 'F') return 1;
        if (첫값 == 'P' && byte_dati == 'K' && punto_di_codice == 3 && finale_VALORE == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDICE, String argomenti) {
        scheda.인수준비(1);
        for (int Loop_INDICE = 0; Loop_INDICE < argomenti.length(); Loop_INDICE++) scheda.argomento_byte(0, Loop_INDICE, argomenti.charAt(Loop_INDICE));
        return scheda.eseguire_USER_app(INDICE);
    }
    static void SMS_byte(int file, int VALORE) { FileMemoria.Scrittura(file, VALORE); }
    static void statico_File(String Nome, String Contenuto_VALORE) {
        // aggregare 파일명은 ASCII. file 내용은 UTF-8로 저장한다.
        FileMemoria.percorso_START(Nome.length());
        for (int Loop_INDICE = 0; Loop_INDICE < Nome.length(); Loop_INDICE++) FileMemoria.percorso_byte(Loop_INDICE, Nome.charAt(Loop_INDICE));
        int file = FileMemoria.Apri(193); if (file < 0) return;
        for (int Loop_INDICE = 0; Loop_INDICE < Contenuto_VALORE.length(); Loop_INDICE++) {
            int punto_di_codice = Contenuto_VALORE.charAt(Loop_INDICE);
            if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdbff && Loop_INDICE + 1 < Contenuto_VALORE.length()) punto_di_codice = 0x10000 + ((punto_di_codice - 0xd800) << 10) + Contenuto_VALORE.charAt(++Loop_INDICE) - 0xdc00;
            if (punto_di_codice < 128) SMS_byte(file, punto_di_codice);
            else {
                int numero = punto_di_codice < 2048 ? 2 : punto_di_codice < 65536 ? 3 : 4;
                SMS_byte(file, (numero == 2 ? 0xc0 : numero == 3 ? 0xe0 : 0xf0) | (punto_di_codice >> (6 * (numero - 1))));
                for (int voce_CONTA_NUMERI = numero - 1; voce_CONTA_NUMERI > 0; voce_CONTA_NUMERI--) SMS_byte(file, 0x80 | ((punto_di_codice >> (6 * (voce_CONTA_NUMERI - 1))) & 63));
            }
        }
        FileMemoria.Chiudi(file);
    }
    static void 한글도움말() {
        단말.Scrittura("F9 o Shift+Space attiva la scrittura in italiano.\n");
        단말.Scrittura("  [IT] keyboard; [EN] ASCII\n");
        단말.Scrittura("  # → £\n");
        단말.Scrittura("  F9: EN ↔ it | Ctrl+Shift+V: UTF-8\n");
        단말.Scrittura("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Scrittura("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nome) {
        int byte_CONTA_NUMERI = 0;
        for (int Loop_INDICE = 0; Loop_INDICE < Nome.length(); Loop_INDICE++) { int punto_di_codice = Nome.charAt(Loop_INDICE); if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdfff) return -22; byte_CONTA_NUMERI += punto_di_codice < 128 ? 1 : punto_di_codice < 2048 ? 2 : 3; }
        int 처리값 = FileMemoria.percorso_START(byte_CONTA_NUMERI); if (처리값 < 0) return 처리값;
        int funzione_INDICE = 0;
        for (int Loop_INDICE = 0; Loop_INDICE < Nome.length(); Loop_INDICE++) {
            int punto_di_codice = Nome.charAt(Loop_INDICE);
            if (punto_di_codice < 128) FileMemoria.percorso_byte(funzione_INDICE++, punto_di_codice);
            else if (punto_di_codice < 2048) { FileMemoria.percorso_byte(funzione_INDICE++, 0xc0 | (punto_di_codice >> 6)); FileMemoria.percorso_byte(funzione_INDICE++, 0x80 | (punto_di_codice & 63)); }
            else { FileMemoria.percorso_byte(funzione_INDICE++, 0xe0 | (punto_di_codice >> 12)); FileMemoria.percorso_byte(funzione_INDICE++, 0x80 | ((punto_di_codice >> 6) & 63)); FileMemoria.percorso_byte(funzione_INDICE++, 0x80 | (punto_di_codice & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nome) {
        int 처리값 = 예제경로(Nome); if (처리값 < 0) return 처리값;
        처리값 = FileMemoria.Crea_elenco(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nome, String dati) {
        int 처리값 = 예제경로(Nome); if (처리값 < 0) return 처리값;
        int file = FileMemoria.Apri(193); if (file == -17) return 0; if (file < 0) return file;
        for (int Loop_INDICE = 0; Loop_INDICE < dati.length(); Loop_INDICE += 2) {
            처리값 = FileMemoria.Scrittura(file, valore_esadecimale(dati.charAt(Loop_INDICE)) * 16 + valore_esadecimale(dati.charAt(Loop_INDICE + 1)));
            if (처리값 < 0) { FileMemoria.Chiudi(file); return 처리값; }
        }
        return FileMemoria.Chiudi(file);
    }
    static void mostra_aiuto() {
        Sistema_strumento.mostra_aiuto();
        단말.Scrittura("sshd / SSH start|stop|status: SSH :22 (user, 장치별 password_VALORE)\n");
        단말.Scrittura("vncd / remoto_display start|stop|status: VNC :5900 (장치별 password_VALORE)\n");
        단말.Scrittura("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Scrittura("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Scrittura("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Scrittura("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Scrittura("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Scrittura("모서리 + 왼쪽 버튼 trascinare_VALORE: terminale Dimensione cambiare_VALORE; terminal size: colonna_VALORE/riga_VALORE\n");
        단말.Scrittura("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Scrittura("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Scrittura("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Scrittura("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Scrittura("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Scrittura("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Scrittura("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Scrittura("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Scrittura("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Scrittura("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Scrittura("pip: MicroPython fonte_albero installare_VALORE; host --network --pip 필요; /lib는 RAM\n");
        단말.Scrittura("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Scrittura("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Scrittura("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Scrittura("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void terminale(boolean 전환여부) {
        if (전환여부 && scheda.terminale(2) != 0) { scheda.terminale(0); 단말.Scrittura("TERMINAL CLOSED\n"); }
        else if (scheda.terminale(1) < 0) errore(-19);
        else 단말.Scrittura("TERMINAL READY — it terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void comando() {
        if (token_CONTA_NUMERI == 0) return;
        if (Sistema_strumento.Esegui_comando()) return;
        if (같음(0,"sshd") || 같음(0,"SSH") || 같음(0,"vncd") || 같음(0,"remoto_display")) {
            int Kind_VALORE=같음(0,"vncd")||같음(0,"remoto_display")?1:0;
            int Azione=같음(1,"start")||같음(1,"avvia")?1:같음(1,"stop")||같음(1,"Ferma")?0:2;
            int Stato_VALORE=scheda.shadowing(Kind_VALORE,Azione);
            if(Stato_VALORE<0)errore(Stato_VALORE);else 단말.Scrittura(scheda.shadowing(Kind_VALORE,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else mostra_aiuto(); }
        else if (같음(0, "info") || 같음(0, "i")) Nucleo.msinfo32_exe();
        else if (같음(0, "pwd")) { FileMemoria.Regolari_scrivere(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_CONTA_NUMERI == 1) { FileMemoria.percorso_START(1); 처리값 = FileMemoria.percorso_byte(0, '/'); } else 처리값 = token_CONTA_NUMERI == 2 ? percorso(1) : -22;
            if (처리값 >= 0) 처리값 = FileMemoria.cambiare_elenco(); if (처리값 < 0) errore(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argomento_INDICE = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_CONTA_NUMERI == argomento_INDICE) { FileMemoria.percorso_START(1); 처리값 = FileMemoria.percorso_byte(0, '.'); } else 처리값 = token_CONTA_NUMERI == argomento_INDICE + 1 ? percorso(argomento_INDICE) : -22;
            if (처리값 >= 0) 처리값 = FileMemoria.경로목록(); if (처리값 < 0) errore(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) Shell_Strumenti.File_caso(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) Shell_Strumenti.copiare_VALORE(같음(0, "mv"));
        else if (같음(0, "cat")) Shell_Strumenti.Vista_VALORE();
        else if (같음(0, "wc")) Shell_Strumenti.세기();
        else if (같음(0, "grep")) Shell_Strumenti.TROVA_voce();
        else if (같음(0, "head") || 같음(0, "tail")) Shell_Strumenti.intestazione_VALORE(같음(0, "tail"));
        else if (같음(0, "tee")) Shell_Strumenti.scrivere_Insieme();
        else if (같음(0, "env")) Shell_sintassi.mostrare_ambiente();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_CONTA_NUMERI == 1) Shell_sintassi.mostrare_ambiente();
            for (int Loop_INDICE = 1; Loop_INDICE < token_CONTA_NUMERI; Loop_INDICE++) { int 처리값 = Shell_sintassi.ambiente_Impostazioni(Loop_INDICE, 같음(0, "unset")); if (처리값 != 0) { risultato = 처리값; 단말.Scrittura("comando analizzare_VALORE: variabile_VALORE 이름이 잘못되었거나 예약된 이름이거나 ambiente 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) Shell_sintassi.Esegui_File();
        else if (같음(0, "true")) risultato = 0;
        else if (같음(0, "false")) risultato = 1;
        else if (같음(0, "history")) editor_di_righe.mostrare_LOG();
        else if (같음(0, "exit")) {
            if (Shell_sintassi.깊이 > 0) { risultato = token_CONTA_NUMERI == 1 ? Shell_sintassi.Stato_VALORE : Shell_Strumenti.cifra_VALORE(1); if (risultato < 0 || risultato > 255) risultato = 2; Shell_sintassi.script_chiudere = true; }
            else if (scheda.terminale(2) != 0) terminale(true);
            else 단말.Scrittura("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Modifica_VALORE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_CONTA_NUMERI < 2) { risultato = 2; 단말.Scrittura("사용법: rm file...\n"); }
            for (int Loop_INDICE = 1; Loop_INDICE < token_CONTA_NUMERI; Loop_INDICE++) { int 처리값 = percorso(Loop_INDICE); if (처리값 == 0) 처리값 = FileMemoria.cancellare_voce(); if (처리값 < 0) errore(처리값); }
        }
        else if (같음(0, "echo")) {
            int START_funzione = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = START_funzione; 첫값 < token_CONTA_NUMERI; 첫값++) { if (첫값 > START_funzione) 단말.문자(32); for (int Loop_INDICE = 0; Loop_INDICE < durata_VALORE[첫값]; Loop_INDICE++) scheda.scrivere_seriale(token_VALORE[시작점[첫값] + Loop_INDICE]); }
            if (START_funzione == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Scrittura("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_aggregare() : strumenti(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); risultato = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !Shell_sintassi.연결중) { 단말.Scrittura("exit "); 단말.numero(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = strumenti(13); risultato = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = strumenti(15); risultato = 처리값 < 0 ? 126 : 처리값; if (!Shell_sintassi.연결중) { 단말.Scrittura("exit "); 단말.numero(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = strumenti(16); risultato = 처리값 < 0 ? 126 : 처리값; if (!Shell_sintassi.연결중) { 단말.Scrittura("exit "); 단말.numero(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Dimensione = scheda.terminale(13); 단말.Scrittura("TERMINAL SIZE "); 단말.numero(Dimensione & 65535); 단말.문자('x'); 단말.numero(Dimensione >>> 16); 단말.문자(10); }
            else terminale(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { scheda.terminale(9); PC.Esegui_comando(); }
        else if (같음(0, "c")) Nucleo.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) Nucleo.test_Tasks();
        else if (같음(0, "g")) Nucleo.schermata();
        else if (같음(0, "selftest") || 같음(0, "u")) Nucleo.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = scheda.eseguire_USER_app(0); if (처리값 == 0) 단말.Scrittura("ELF DEMO PASS\n"); else errore(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? strumento_voce(-2, 2) : strumenti(-1); risultato = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !Shell_sintassi.연결중) { 단말.Scrittura("exit "); 단말.numero(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) Nucleo.test_Rete();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = scheda.trasferimento_di_file_servizio(1); if (처리값 < 0) errore(처리값); else { 단말.Scrittura("FTP listening "); Sistema_strumento.scrivere_e_mail(scheda.rete_stato(0,0)); 단말.Scrittura(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { scheda.trasferimento_di_file_servizio(0); 단말.Scrittura("FTP stopped\n"); }
            else 단말.Scrittura(scheda.trasferimento_di_file_servizio(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { aggregare.Prepara(); 단말.Scrittura("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Lingua = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_CONTA_NUMERI != 2 || Lingua < 0) 단말.Scrittura("example java|c|python: uscitaTesto, file, 네트워크, 그래픽, Java Swing Finestra 예제\n");
            else { int 처리값 = 예제꾸러미.installare_VALORE(Lingua); if (처리값 < 0) { errore(처리값); if (처리값 == -28) 단말.Scrittura("RAM full: remove unused files, then retry example\n"); } else 단말.Scrittura("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formato_VALORE = esecuzione_formato();
            if (formato_VALORE == 1 || formato_VALORE == 2) {
                int 처리값 = strumento_voce(formato_VALORE == 1 ? -1 : 14, 0); risultato = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !Shell_sintassi.연결중) { 단말.Scrittura("exit "); 단말.numero(처리값); 단말.문자(10); }
            } else if (formato_VALORE == 0) { risultato = 126; 단말.Scrittura("실행할 numero 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { risultato = 127; 단말.Scrittura("Unknown command. help: commands\n"); }
        }
    }
    public static void Esegui_comando() {
        aggregare.Prepara();
        for (int Lingua = 0; Lingua < 3; Lingua++) { int 처리값 = 예제꾸러미.installare_VALORE(Lingua); if (처리값 < 0) errore(처리값); }
        mostra_aiuto();
        while (true) {
            finestra_sessione.Processi_VALORE_voce(); if (finestra_sessione.CV_esecuzione()) continue;
            if (!finestra_sessione.이어읽기) 단말.Scrittura("jkoros-native> "); editor_di_righe.riga_di_comando = true; scheda.remoto_aspetta(1); int Dimensione = leggi_riga_di_ingresso(); scheda.remoto_aspetta(0); editor_di_righe.riga_di_comando = false;
            if (Dimensione == -3) continue;
            if (Dimensione == -2) 단말.Scrittura("comando analizzare_VALORE: 명령줄이 너무 깁니다\n");
            if (Dimensione >= 0) { Shell_sintassi.script_chiudere = false; Shell_sintassi.Esegui_comando(riga_di_ingresso, 0, Dimensione, 0); } else Shell_sintassi.Stato_VALORE = 130;
            scheda.chiudere_remoto_comando(Shell_sintassi.Stato_VALORE);
            editor_di_righe.Dimensione = editor_di_righe.cursore_VALORE = editor_di_righe.START_finestra = 0;
        }
    }
}
