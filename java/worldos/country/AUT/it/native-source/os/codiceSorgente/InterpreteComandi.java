// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Scrittura 없이 동작하는 작은 seriale_VALORE/PS2 InterpreteComandi. */
public final class InterpreteComandi {
    static int[] input_VALORE = new int[128];
    static int durata_VALORE = 0;
    static boolean 앞줄복귀 = false;
    static boolean riga_overflow = false;

    static boolean comando(String Nome) {
        if (durata_VALORE < Nome.length()) return false;
        for (int INDICE = 0; INDICE < Nome.length(); INDICE++)
            if (input_VALORE[INDICE] != Nome.charAt(INDICE)) return false;
        return durata_VALORE == Nome.length() || input_VALORE[Nome.length()] == ' ';
    }

    static void mostra_aiuto() {
        SMS_Terminale.Scrittura("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminale.Scrittura("apps | run NAME [ARGS] | net\n");
        SMS_Terminale.Scrittura("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminale.Scrittura("sync (연결된 JKSTORE1 Store_VALORE 장치에 file 보존)\n");
    }

    static void Processi_VALORE_voce() {
        if (durata_VALORE == 0) return;
        if (comando("help")) mostra_aiuto();
        else if (comando("sync")) {
            int risultato = 파일보존.sincronizzare();
            SMS_Terminale.Scrittura("Sync: "); SMS_Terminale.scrivere_numero(risultato); SMS_Terminale.문자(10);
        }
        else if (comando("ls")) Memoria_file_system.voce_elenco();
        else if (comando("edit")) Memoria_file_system.comando(input_VALORE, 4, durata_VALORE, 0);
        else if (comando("cat")) Memoria_file_system.comando(input_VALORE, 3, durata_VALORE, 1);
        else if (comando("rm")) Memoria_file_system.comando(input_VALORE, 2, durata_VALORE, 2);
        else if (comando("java") || comando("javac")) {
            int risultato = esecuzione_manager.Esegui_comando(input_VALORE, 0, durata_VALORE);
            SMS_Terminale.Scrittura("Exit: "); SMS_Terminale.scrivere_numero(risultato); SMS_Terminale.문자(10);
        }
        else if (comando("apps")) esecuzione_manager.voce_elenco();
        else if (comando("net")) rete_Pila.Stato_VALORE();
        else if (comando("run")) {
            int risultato = esecuzione_manager.Esegui_comando(input_VALORE, 3, durata_VALORE);
            SMS_Terminale.Scrittura("Exit: "); SMS_Terminale.scrivere_numero(risultato); SMS_Terminale.Scrittura("\n");
        } else if (comando("info")) {
            SMS_Terminale.Scrittura("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (comando("mem")) {
            SMS_Terminale.Scrittura("위쪽 Memoria_VALORE e_mail_area(KiB): "); SMS_Terminale.scrivere_numero(Memoria_area.MAIUSC_Memoria_ridimensionare());
            SMS_Terminale.Scrittura("\n배열 동적 Memoria_VALORE e_mail_area(byte_VALORE): "); SMS_Terminale.scrivere_numero(cellulare_VALORE.array_utilizzo());
            SMS_Terminale.Scrittura(" / 262144\n작업 e_mail_area sezione_VALORE: "); SMS_Terminale.scrivere_numero(Memoria_area.사용개수());
            SMS_Terminale.Scrittura(" / 8 (각 4096바이트)\n");
        } else if (comando("alloc")) {
            int INDICE = Memoria_area.allocare_Memoria();
            SMS_Terminale.Scrittura("sezione_VALORE INDICE: "); SMS_Terminale.scrivere_numero(INDICE); SMS_Terminale.Scrittura("\n");
        } else if (comando("free")) {
            if (durata_VALORE == 6 && input_VALORE[4] == ' ' && input_VALORE[5] >= '0' && input_VALORE[5] <= '7') {
                SMS_Terminale.Scrittura(Memoria_area.Reso_KR(input_VALORE[5] - '0') ? "반환됨\n" : "할당되지 않은 sezione_VALORE\n");
            } else SMS_Terminale.Scrittura("사용법: free 0..7\n");
        } else if (comando("echo")) {
            for (int INDICE = 5; INDICE < durata_VALORE; INDICE++) SMS_Terminale.문자(input_VALORE[INDICE]);
            SMS_Terminale.문자(10);
        } else if (comando("clear")) SMS_Terminale.cancellare_voce();
        else if (comando("test")) Nucleo.prove();
        else if (comando("halt")) {
            SMS_Terminale.Scrittura("HALTED\n");
            cellulare_VALORE.정지();
        } else SMS_Terminale.Scrittura("알 numero 없는 명령입니다. help를 입력하세요.\n");
    }

    static void accettare_E_scrivere(int VALORE) {
        if (VALORE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALORE == 13;
        if (VALORE == 10 || VALORE == 13) {
            SMS_Terminale.문자(10);
            if (Memoria_file_system.편집중) Memoria_file_system.Modificati_riga(input_VALORE, durata_VALORE, riga_overflow);
            else Processi_VALORE_voce();
            durata_VALORE = 0;
            riga_overflow = false;
            SMS_Terminale.Scrittura(Memoria_file_system.편집중 ? "...> " : "jkoros> ");
        } else if (VALORE == 8 || VALORE == 127) {
            if (durata_VALORE > 0) {
                durata_VALORE--;
                SMS_Terminale.seriale_byte(8); SMS_Terminale.seriale_byte(32); SMS_Terminale.seriale_byte(8);
                SMS_Terminale.schermata_carattere(8);
            }
        } else if (VALORE >= 32 && VALORE < 127 && durata_VALORE < input_VALORE.length) {
            input_VALORE[durata_VALORE++] = VALORE;
            SMS_Terminale.문자(VALORE);
        } else if (VALORE >= 32 && VALORE < 127) riga_overflow = true;
    }

    static void avvia() {
        mostra_aiuto();
        SMS_Terminale.Scrittura("READY\njkoros> ");
        while (true) {
            int VALORE = SMS_Terminale.직렬읽기();
            if (VALORE < 0) VALORE = tastiera.Lettura();
            if (VALORE >= 0) accettare_E_scrivere(VALORE);
            else { rete_Pila.verificare(); cellulare_VALORE.잠시양보(); }
        }
    }
}
