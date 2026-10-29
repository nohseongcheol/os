// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. file/operando_Pila/fonti/ramo 경계를 Esegui_comando 중 검사한다. */
public final class 자바가상기계 {
    static int[] file = new int[16 * 16384], file_temporaneo = new int[16384], nome_file_SMS = new int[512];
    static int[] costante_tag = new int[8192], 상가 = new int[8192], costante_SECONDO_VALORE = new int[8192], stringa_fonti = new int[8192];
    static int[] metodo_nome_SMS = new int[512], metodo_TIPO = new int[512], metodo_accesso = new int[512], metodo_proprietario = new int[512];
    static int[] metodo_START = new int[512], metodo_chiudere = new int[512], metodo_Pila = new int[512], 함수지역 = new int[512];
    static int[] metodo_argomento_CONTA_NUMERI = new int[512], metodo_argomento_TIPO = new int[8192], metodo_Reso = new int[512];
    static int[] limite_VALORE = new int[16 * 16384];
    static int[] locale_VALORE = new int[16384], locale_TIPO = new int[16384], operando_Pila_VALORE = new int[16384], operando_Pila_TIPO = new int[16384];
    static int[] frame_metodo = new int[128], frame_funzione = new int[128], frame_Pila = new int[128], frame_istruzione = new int[128], inizializzare_frame = new int[128];
    static int[] Corso_definizione_nome = new int[16], Corso_definizione_ridimensionare = new int[16], Corso_definizione_padre = new int[16], Corso_definizione_Stato = new int[16], Corso_slot_CONTA_NUMERI = new int[16], inizializzare_Corso_definizione = new int[16];
    static int[] Corso_interfaccia = new int[16 * 16], Corso_interfaccia_CONTA_NUMERI = new int[16];
    static int[] slot_nome = new int[512], slot_TIPO = new int[512], slot_proprietario = new int[512], slot_Autorizzazioni = new int[512], slot_funzione = new int[512], slot_dati = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] heap_VALORE = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], heap_fonti = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], elemento_di_matrice = new int[32768], Store_intero = new int[256];
    static int Dimensione, 읽기위치, metodo_CONTA_NUMERI, nome_della_classe, frame_INDICE = -1, heap_chiudere_funzione = 1, tipo_restituito;
    static int Corso_definizione_CONTA_NUMERI, slot_CONTA_NUMERI, 잡기수, 현재읽는종, 던진객체, 잠시수, display_CONTA_NUMERI, album_CONTA_NUMERI;
    static int Regolari_thread, Conteggio_dei_thread = 1, voce_Corso_definizione;
    static int[] thread_frame = new int[4], thread_Stato = new int[4], thread_oggetto = new int[4], thread_target = new int[4], 가닥대기 = new int[4];
    static boolean errore, richiesta_di_modifica;
    static int[] blocco_proprietario = new int[32768], 잠금깊이 = new int[32768], frame_blocco = new int[128], Corso_blocco = new int[16], Corso_thread = new int[16];

    static void errore_VALORE(String Word_SMS) {
        if (errore) return;
        int area_CODICE = 0;
        if (자바도구.같음(Word_SMS, "ArithmeticException: / by zero")) area_CODICE = 4;
        if (자바도구.같음(Word_SMS, "NullPointerException") || 자바도구.같음(Word_SMS, "null or invalid array")) area_CODICE = 5;
        if (자바도구.같음(Word_SMS, "ArrayIndexOutOfBoundsException")) area_CODICE = 7;
        if (자바도구.같음(Word_SMS, "StringIndexOutOfBoundsException")) area_CODICE = 8;
        if (자바도구.같음(Word_SMS, "NumberFormatException")) area_CODICE = 10;
        if (자바도구.같음(Word_SMS, "FileNotFoundException: file open failed")) area_CODICE = 12;
        if (자바도구.같음(Word_SMS, "IOException: stream closed") || 자바도구.같음(Word_SMS, "IOException: read failed") || 자바도구.같음(Word_SMS, "IOException: write failed")) area_CODICE = 11;
        if (자바도구.같음(Word_SMS, "ClassCastException")) area_CODICE = 14;
        if (자바도구.같음(Word_SMS, "NegativeArraySizeException")) area_CODICE = 15;
        if (area_CODICE != 0 && frame_INDICE >= 0) { 예외던짐(area_CODICE, Word_SMS); return; }
        spazio_utente.Scrittura("JVM error: "); spazio_utente.Scrittura(Word_SMS); spazio_utente.scrivere_carattere_VALORE(10); errore = true;
    }
    static boolean ritagliare(int avvia, int durata_VALORE) {
        if (avvia < 0 || avvia >= file.length || durata_VALORE < 0) return false;
        int Corso_definizione = avvia / 16384;
        return avvia % 16384 <= Corso_definizione_ridimensionare[Corso_definizione] && durata_VALORE <= Corso_definizione_ridimensionare[Corso_definizione] - avvia % 16384;
    }
    static int byte_VALORE() {
        if (!ritagliare(읽기위치, 1)) { errore_VALORE("truncated class file"); return 0; }
        return file[읽기위치++];
    }
    static int 짧은수() { return byte_VALORE() << 8 | byte_VALORE(); }
    static int intero() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int durata_VALORE) { if (!ritagliare(읽기위치, durata_VALORE)) errore_VALORE("invalid attribute size"); else 읽기위치 += durata_VALORE; }
    static boolean assegno_costante(int numero, int Kind_VALORE) {
        if (numero <= 0 || numero >= costante_tag.length || costante_tag[numero] != Kind_VALORE) { errore_VALORE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_intervallo(int avvia, int durata_VALORE, String Word_SMS) {
        if (!ritagliare(avvia, durata_VALORE)) return false;
        int 읽는자리 = avvia, 끝 = avvia + durata_VALORE;
        for (int Loop_INDICE = 0; Loop_INDICE < Word_SMS.length(); Loop_INDICE++) {
            int punto_di_codice = Word_SMS.charAt(Loop_INDICE);
            if (punto_di_codice > 0 && punto_di_codice < 128) { if (읽는자리 >= 끝 || file[읽는자리++] != punto_di_codice) return false; }
            else if (punto_di_codice < 2048) {
                if (읽는자리 + 2 > 끝 || file[읽는자리++] != (192 | (punto_di_codice >> 6)) || file[읽는자리++] != (128 | (punto_di_codice & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || file[읽는자리++] != (224 | (punto_di_codice >> 12)) || file[읽는자리++] != (128 | ((punto_di_codice >> 6) & 63)) || file[읽는자리++] != (128 | (punto_di_codice & 63))) return false;
        }
        return 읽는자리 == 끝;
    }
    static boolean Word_SMS(int costante_VALORE, String Word_SMS) { return assegno_costante(costante_VALORE, 1) && SMS_intervallo(상가[costante_VALORE], costante_SECONDO_VALORE[costante_VALORE], Word_SMS); }
    static boolean collegamento_movimenti_Word(int 가, int SECONDO_operando) {
        if (!assegno_costante(가, 1) || !assegno_costante(SECONDO_operando, 1) || costante_SECONDO_VALORE[가] != costante_SECONDO_VALORE[SECONDO_operando]) return false;
        for (int numero = 0; numero < costante_SECONDO_VALORE[가]; numero++) if (file[상가[가] + numero] != file[상가[SECONDO_operando] + numero]) return false;
        return true;
    }
    static int nome_della_classe_SMS(int numero) { return assegno_costante(numero, 7) && assegno_costante(상가[numero], 1) ? 상가[numero] : 0; }
    static int fonti_nome(int numero) { return assegno_costante(numero, 12) && assegno_costante(상가[numero], 1) ? 상가[numero] : 0; }
    static int tipo_riferimento(int numero) { return assegno_costante(numero, 12) && assegno_costante(costante_SECONDO_VALORE[numero], 1) ? costante_SECONDO_VALORE[numero] : 0; }
    static int descrittore_TIPO(int 끝, boolean vuota_TIPO) {
        if (읽기위치 >= 끝) { errore_VALORE("invalid descriptor"); return 0; }
        int VALORE = byte_VALORE();
        if (VALORE == 'V' && vuota_TIPO) return 0;
        if (VALORE == 'I' || VALORE == 'B' || VALORE == 'C' || VALORE == 'S' || VALORE == 'Z') return 1;
        if (VALORE == '[') { descrittore_TIPO(끝, false); return 2; }
        if (VALORE == 'L') {
            int avvia = 읽기위치;
            while (읽기위치 < 끝 && file[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == avvia) errore_VALORE("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        errore_VALORE("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int FUNZIONE_VALORE) {
        int Indietro_articolo = 읽기위치, numero = metodo_TIPO[FUNZIONE_VALORE];
        if (!assegno_costante(numero, 1)) return;
        읽기위치 = 상가[numero]; int 끝 = 읽기위치 + costante_SECONDO_VALORE[numero];
        if (byte_VALORE() != '(') errore_VALORE("invalid method descriptor");
        int articolo_CONTA_NUMERI = 0;
        while (!errore && 읽기위치 < 끝 && file[읽기위치] != ')') {
            if (articolo_CONTA_NUMERI == 16) { errore_VALORE("too many method arguments"); break; }
            metodo_argomento_TIPO[FUNZIONE_VALORE * 16 + articolo_CONTA_NUMERI++] = descrittore_TIPO(끝, false);
        }
        if (읽기위치 >= 끝 || byte_VALORE() != ')') errore_VALORE("invalid method descriptor");
        metodo_Reso[FUNZIONE_VALORE] = descrittore_TIPO(끝, true); metodo_argomento_CONTA_NUMERI[FUNZIONE_VALORE] = articolo_CONTA_NUMERI;
        if (읽기위치 != 끝) errore_VALORE("invalid method descriptor");
        읽기위치 = Indietro_articolo;
    }
    static int 상번호() { int VALORE = 짧은수(); return VALORE == 0 ? 0 : 현재읽는종 * 512 + VALORE; }
    static int 명상수() { return metodo_proprietario[frame_metodo[frame_INDICE]] * 512 + 명짧(); }
    static void ignorare_attributo() {
        int articolo_CONTA_NUMERI = 짧은수();
        for (int numero = 0; numero < articolo_CONTA_NUMERI && !errore; numero++) { assegno_costante(상번호(), 1); 건너(intero()); }
    }
    static int comando_durata(int VALORE) {
        if (VALORE == 16 || VALORE == 18 || VALORE == 21 || VALORE == 25 || VALORE == 54 || VALORE == 58 || VALORE == 188) return 2;
        if (VALORE == 17 || VALORE == 19 || VALORE == 132 || VALORE >= 153 && VALORE <= 167
            || VALORE >= 178 && VALORE <= 184 || VALORE == 187 || VALORE == 189 || VALORE == 192 || VALORE == 193 || VALORE == 198 || VALORE == 199) return 3;
        if (VALORE == 185 || VALORE == 200) return 5;
        if (VALORE >= 0 && VALORE <= 8 || VALORE >= 26 && VALORE <= 29 || VALORE >= 42 && VALORE <= 46 || VALORE >= 50 && VALORE <= 53
            || VALORE >= 59 && VALORE <= 62 || VALORE >= 75 && VALORE <= 79 || VALORE >= 83 && VALORE <= 95
            || VALORE == 96 || VALORE == 100 || VALORE == 104 || VALORE == 108 || VALORE == 112 || VALORE == 116
            || VALORE == 120 || VALORE == 122 || VALORE == 124 || VALORE == 126 || VALORE == 128 || VALORE == 130
            || VALORE >= 145 && VALORE <= 147 || VALORE == 172 || VALORE == 176 || VALORE == 177 || VALORE == 190 || VALORE == 191
            || VALORE == 194 || VALORE == 195) return 1;
        return 0;
    }
    static int funzione_intero(int 읽는자리) {
        if (!ritagliare(읽는자리, 4)) { errore_VALORE("truncated bytecode operand"); return 0; }
        return file[읽는자리] << 24 | file[읽는자리 + 1] << 16 | file[읽는자리 + 2] << 8 | file[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int avvia, int 끝) {
        int VALORE = file[읽는자리], durata_VALORE = comando_durata(VALORE);
        if (VALORE == 170 || VALORE == 171) {
            int BASE_funzione = 읽는자리 + 1;
            while ((BASE_funzione - avvia) % 4 != 0) BASE_funzione++;
            if (끝 - BASE_funzione < (VALORE == 170 ? 12 : 8)) return 0;
            int voce_CONTA_NUMERI = VALORE == 170 ? funzione_intero(BASE_funzione + 8) - funzione_intero(BASE_funzione + 4) + 1 : funzione_intero(BASE_funzione + 4);
            if (voce_CONTA_NUMERI < 0 || voce_CONTA_NUMERI > 2048) return 0;
            durata_VALORE = BASE_funzione - 읽는자리 + (VALORE == 170 ? 12 + 4 * voce_CONTA_NUMERI : 8 + 8 * voce_CONTA_NUMERI);
        }
        if (VALORE == 196 && 읽는자리 + 1 < 끝) {
            int Word_dati = file[읽는자리 + 1]; durata_VALORE = Word_dati == 132 ? 6 : (Word_dati == 21 || Word_dati == 25 || Word_dati == 54 || Word_dati == 58) ? 4 : 0;
        }
        return durata_VALORE > 0 && durata_VALORE <= 끝 - 읽는자리 ? durata_VALORE : 0;
    }
    static void assegno_meta_VALORE(int meta_VALORE, int FUNZIONE_VALORE) {
        if (meta_VALORE < metodo_START[FUNZIONE_VALORE] || meta_VALORE >= metodo_chiudere[FUNZIONE_VALORE] || limite_VALORE[meta_VALORE] != FUNZIONE_VALORE + 1) errore_VALORE("invalid branch target");
    }
    static void 클래스읽기(int Corso_definizione) {
        현재읽는종 = Corso_definizione; 읽기위치 = Corso_definizione * 16384; Dimensione = 읽기위치 + Corso_definizione_ridimensionare[Corso_definizione];
        if (intero() != 0xcafebabe) { errore_VALORE("not a class file"); return; }
        int 부판 = 짧은수(), versione_VALORE = 짧은수();
        if (versione_VALORE < 45 || versione_VALORE > 52 || 부판 != 0) { errore_VALORE("supported class versions: 45..52, minor 0"); return; }
        int costante_CONTA_NUMERI = 짧은수(), BASE_funzione = Corso_definizione * 512;
        if (costante_CONTA_NUMERI < 1 || costante_CONTA_NUMERI > 512) { errore_VALORE("constant pool limit (511)"); return; }
        for (int voce_CONTA_NUMERI = 1; voce_CONTA_NUMERI < costante_CONTA_NUMERI && !errore; voce_CONTA_NUMERI++) {
            int numero = BASE_funzione + voce_CONTA_NUMERI, Kind_VALORE = byte_VALORE(); costante_tag[numero] = Kind_VALORE;
            if (Kind_VALORE == 1) { costante_SECONDO_VALORE[numero] = 짧은수(); 상가[numero] = 읽기위치; 건너(costante_SECONDO_VALORE[numero]); }
            else if (Kind_VALORE == 3) 상가[numero] = intero();
            else if (Kind_VALORE == 7 || Kind_VALORE == 8) 상가[numero] = 상번호();
            else if (Kind_VALORE == 9 || Kind_VALORE == 10 || Kind_VALORE == 11 || Kind_VALORE == 12) { 상가[numero] = 상번호(); costante_SECONDO_VALORE[numero] = 상번호(); }
            else errore_VALORE("unsupported constant type");
        }
        int privilegio_VALORE = 짧은수();
        if ((privilegio_VALORE & (0x2000 | 0x4000)) != 0) errore_VALORE("annotation/enum class unsupported");
        Corso_definizione_nome[Corso_definizione] = nome_della_classe_SMS(상번호());
        Corso_definizione_padre[Corso_definizione] = nome_della_classe_SMS(상번호());
        int interfaccia_CONTA_NUMERI = 짧은수(); if (interfaccia_CONTA_NUMERI > 16) { errore_VALORE("interface count limit"); return; }
        Corso_interfaccia_CONTA_NUMERI[Corso_definizione] = interfaccia_CONTA_NUMERI;
        for (int Loop_INDICE = 0; Loop_INDICE < interfaccia_CONTA_NUMERI; Loop_INDICE++) Corso_interfaccia[Corso_definizione * 16 + Loop_INDICE] = nome_della_classe_SMS(상번호());
        int campo_CONTA_NUMERI = 짧은수();
        if (campo_CONTA_NUMERI > 512 - slot_CONTA_NUMERI) { errore_VALORE("field count limit (512)"); return; }
        for (int Loop_INDICE = 0; Loop_INDICE < campo_CONTA_NUMERI && !errore; Loop_INDICE++) {
            int File_INDICE = slot_CONTA_NUMERI++; slot_proprietario[File_INDICE] = Corso_definizione; slot_Autorizzazioni[File_INDICE] = 짧은수(); slot_nome[File_INDICE] = 상번호(); slot_TIPO[File_INDICE] = 상번호();
            assegno_costante(slot_nome[File_INDICE], 1); assegno_costante(slot_TIPO[File_INDICE], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[slot_TIPO[File_INDICE]]; int area_CODICE = descrittore_TIPO(읽기위치 + costante_SECONDO_VALORE[slot_TIPO[File_INDICE]], false); 읽기위치 = 보존값;
            if ((slot_Autorizzazioni[File_INDICE] & 8) == 0) slot_funzione[File_INDICE] = Corso_slot_CONTA_NUMERI[Corso_definizione]++;
            int attributo_dati = 짧은수();
            for (int inner_funzione = 0; inner_funzione < attributo_dati && !errore; inner_funzione++) {
                int nome_costante = 상번호(), valido_durata = intero();
                if (Word_SMS(nome_costante, "ConstantValue") && valido_durata == 2) {
                    int dati_VALORE = 상번호();
                    if (area_CODICE == 1 && assegno_costante(dati_VALORE, 3)) slot_dati[File_INDICE] = 상가[dati_VALORE];
                    else if (area_CODICE == 2 && assegno_costante(dati_VALORE, 8)) slot_dati[File_INDICE] = costante_SMS(상가[dati_VALORE]);
                } else 건너(valido_durata);
            }
        }
        int articolo_CONTA_NUMERI = 짧은수();
        if (articolo_CONTA_NUMERI > 512 - metodo_CONTA_NUMERI) { errore_VALORE("method count limit (512)"); return; }
        for (int Loop_INDICE = 0; Loop_INDICE < articolo_CONTA_NUMERI && !errore; Loop_INDICE++) {
            int numero = metodo_CONTA_NUMERI++; metodo_proprietario[numero] = Corso_definizione;
            metodo_accesso[numero] = 짧은수(); metodo_nome_SMS[numero] = 상번호(); metodo_TIPO[numero] = 상번호();
            assegno_costante(metodo_nome_SMS[numero], 1); 서술읽기(numero);
            if ((metodo_accesso[numero] & 8) == 0) {
                if (metodo_argomento_CONTA_NUMERI[numero] == 16) { errore_VALORE("too many instance method arguments"); return; }
                for (int Confronto_funzione = metodo_argomento_CONTA_NUMERI[numero]; Confronto_funzione > 0; Confronto_funzione--) metodo_argomento_TIPO[numero * 16 + Confronto_funzione] = metodo_argomento_TIPO[numero * 16 + Confronto_funzione - 1];
                metodo_argomento_TIPO[numero * 16] = 2; metodo_argomento_CONTA_NUMERI[numero]++;
            }
            if ((metodo_accesso[numero] & 0x100) != 0) errore_VALORE("user native method unsupported");
            if (Word_SMS(metodo_nome_SMS[numero], "<clinit>")) inizializzare_Corso_definizione[Corso_definizione] = numero + 1;
            for (int frontale_VALORE = 0; frontale_VALORE < numero; frontale_VALORE++) if (metodo_proprietario[frontale_VALORE] == Corso_definizione && collegamento_movimenti_Word(metodo_nome_SMS[frontale_VALORE], metodo_nome_SMS[numero]) && collegamento_movimenti_Word(metodo_TIPO[frontale_VALORE], metodo_TIPO[numero])) errore_VALORE("duplicate method");
            int attributo_CONTA_NUMERI = 짧은수();
            for (int valore_dell_attributo = 0; valore_dell_attributo < attributo_CONTA_NUMERI && !errore; valore_dell_attributo++) {
                int Nome = 상번호(), durata_VALORE = intero(), avvia = 읽기위치;
                if (!ritagliare(avvia, durata_VALORE)) { errore_VALORE("truncated method attribute"); break; }
                if (Word_SMS(Nome, "Code")) {
                    if (metodo_START[numero] != 0) errore_VALORE("duplicate Code attribute");
                    metodo_Pila[numero] = 짧은수(); 함수지역[numero] = 짧은수(); int CODICE_durata = intero();
                    if (metodo_Pila[numero] > 128 || 함수지역[numero] > 128 || 함수지역[numero] < metodo_argomento_CONTA_NUMERI[numero]
                        || CODICE_durata < 1 || CODICE_durata > 8192) errore_VALORE("method memory limits exceeded");
                    metodo_START[numero] = 읽기위치; 건너(CODICE_durata); metodo_chiudere[numero] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { errore_VALORE("exception table limit"); return; }
                    for (int inner_funzione = 0; inner_funzione < 잡는수; inner_funzione++) {
                        int errore_fonti = 잡기수++; 잡기함수[errore_fonti] = numero;
                        잡기시작[errore_fonti] = metodo_START[numero] + 짧은수(); 잡기끝[errore_fonti] = metodo_START[numero] + 짧은수();
                        잡기위치[errore_fonti] = metodo_START[numero] + 짧은수(); int 부호값 = 상번호(); 잡기종[errore_fonti] = 부호값 == 0 ? 0 : nome_della_classe_SMS(부호값);
                    }
                    ignorare_attributo();
                    if (읽기위치 != avvia + durata_VALORE) errore_VALORE("Code attribute size mismatch");
                } else 건너(durata_VALORE);
            }
            if ((metodo_accesso[numero] & 0x400) != 0) continue;
            if (metodo_START[numero] == 0) errore_VALORE("missing Code attribute");
            int slot_voce = metodo_START[numero];
            while (slot_voce < metodo_chiudere[numero] && !errore) {
                int durata_VALORE = 길이읽기(slot_voce, metodo_START[numero], metodo_chiudere[numero]);
                if (durata_VALORE == 0) { errore_VALORE("unsupported or truncated bytecode"); break; }
                limite_VALORE[slot_voce] = numero + 1; slot_voce += durata_VALORE;
            }
            slot_voce = metodo_START[numero];
            while (slot_voce < metodo_chiudere[numero] && !errore) {
                int VALORE = file[slot_voce];
                if (VALORE >= 153 && VALORE <= 167 || VALORE == 198 || VALORE == 199) assegno_meta_VALORE(slot_voce + (short)(file[slot_voce + 1] << 8 | file[slot_voce + 2]), numero);
                if (VALORE == 200) assegno_meta_VALORE(slot_voce + funzione_intero(slot_voce + 1), numero);
                if (VALORE == 170 || VALORE == 171) {
                    int 읽는자리 = slot_voce + 1; while ((읽는자리 - metodo_START[numero]) % 4 != 0) 읽는자리++;
                    assegno_meta_VALORE(slot_voce + funzione_intero(읽는자리), numero);
                    int voce_CONTA_NUMERI = VALORE == 170 ? funzione_intero(읽는자리 + 8) - funzione_intero(읽는자리 + 4) + 1 : funzione_intero(읽는자리 + 4);
                    읽는자리 += VALORE == 170 ? 12 : 8;
                    for (int inner_funzione = 0; inner_funzione < voce_CONTA_NUMERI; inner_funzione++) assegno_meta_VALORE(slot_voce + funzione_intero(읽는자리 + inner_funzione * (VALORE == 170 ? 4 : 8) + (VALORE == 170 ? 0 : 4)), numero);
                }
                slot_voce += 길이읽기(slot_voce, metodo_START[numero], metodo_chiudere[numero]);
            }
            for (int inner_funzione = 0; inner_funzione < 잡기수; inner_funzione++) if (잡기함수[inner_funzione] == numero) {
                assegno_meta_VALORE(잡기시작[inner_funzione], numero); assegno_meta_VALORE(잡기위치[inner_funzione], numero);
                if (잡기끝[inner_funzione] != metodo_chiudere[numero]) assegno_meta_VALORE(잡기끝[inner_funzione], numero);
                if (잡기시작[inner_funzione] >= 잡기끝[inner_funzione]) errore_VALORE("invalid exception range");
            }
        }
        if (!errore) ignorare_attributo();
        if (읽기위치 != Dimensione) errore_VALORE("extra class file data");
    }
    static int allocare_Memoria(int Kind_VALORE, int durata_VALORE) { return 새기억(Kind_VALORE, durata_VALORE); }
    static boolean oggetto_VALORE(int fonti, int Kind_VALORE) {
        if (!reparto_IT_valido_oggetto(fonti)) return false;
        if (heap_VALORE[fonti] != Kind_VALORE) { errore_VALORE("object type mismatch"); return false; }
        return true;
    }
    static int costante_SMS(int INDICE) {
        if (!assegno_costante(INDICE, 1)) return 0;
        if (stringa_fonti[INDICE] != 0) return stringa_fonti[INDICE];
        int fonti = allocare_Memoria(1, costante_SECONDO_VALORE[INDICE]); if (errore) return 0;
        int 끝 = 상가[INDICE] + costante_SECONDO_VALORE[INDICE], numero = 상가[INDICE], durata_VALORE = 0;
        while (numero < 끝 && !errore) {
            int VALORE = file[numero++];
            if (VALORE == 0) errore_VALORE("invalid modified UTF-8");
            else if (VALORE >= 192 && VALORE <= 223 && numero < 끝) {
                int Avanti_articolo = file[numero++];
                if ((Avanti_articolo & 192) != 128) errore_VALORE("invalid modified UTF-8");
                VALORE = (VALORE & 31) << 6 | Avanti_articolo & 63;
                if (VALORE != 0 && VALORE < 128) errore_VALORE("overlong modified UTF-8");
            } else if (VALORE >= 224 && VALORE <= 239 && numero + 1 < 끝) {
                int 가 = file[numero++], SECONDO_operando = file[numero++];
                if ((가 & 192) != 128 || (SECONDO_operando & 192) != 128) errore_VALORE("invalid modified UTF-8");
                VALORE = (VALORE & 15) << 12 | (가 & 63) << 6 | SECONDO_operando & 63;
                if (VALORE < 2048) errore_VALORE("overlong modified UTF-8");
            } else if (VALORE >= 128) errore_VALORE("invalid modified UTF-8");
            heap_VALORE[fonti + 2 + durata_VALORE++] = VALORE;
        }
        heap_VALORE[fonti + 1] = durata_VALORE; stringa_fonti[INDICE] = fonti; return fonti;
    }
    static int host_carattere(String VALORE) {
        int fonti = allocare_Memoria(1, VALORE.length()); if (errore) return 0;
        for (int numero = 0; numero < VALORE.length(); numero++) heap_VALORE[fonti + 2 + numero] = VALORE.charAt(numero);
        return fonti;
    }
    static void scrivere_SMS(int fonti) {
        if (fonti == 0) { spazio_utente.Scrittura("null"); return; }
        if (!oggetto_VALORE(fonti, 1)) return;
        for (int numero = 0; numero < heap_VALORE[fonti + 1]; numero++) spazio_utente.scrivere_carattere_VALORE(heap_VALORE[fonti + 2 + numero]);
    }
    static int cifra_carattere(int VALORE) {
        int fonti = allocare_Memoria(1, 11); if (errore) return 0;
        int durata_VALORE = 0;
        if (VALORE < 0) heap_VALORE[fonti + 2 + durata_VALORE++] = '-'; else VALORE = -VALORE;
        int funzione_INDICE = 1000000000; boolean avvia = false;
        while (funzione_INDICE != 0) {
            int numero = -(VALORE / funzione_INDICE);
            if (numero != 0 || avvia || funzione_INDICE == 1) { heap_VALORE[fonti + 2 + durata_VALORE++] = '0' + numero; avvia = true; }
            VALORE %= funzione_INDICE; funzione_INDICE /= 10;
        }
        heap_VALORE[fonti + 1] = durata_VALORE; return fonti;
    }
    static int 정수해독(int fonti) {
        if (!oggetto_VALORE(fonti, 1)) return 0;
        int durata_VALORE = heap_VALORE[fonti + 1], numero = 0, VALORE = 0; boolean negativo_VALORE = false;
        if (durata_VALORE > 0 && (heap_VALORE[fonti + 2] == '-' || heap_VALORE[fonti + 2] == '+')) { negativo_VALORE = heap_VALORE[fonti + 2] == '-'; numero++; }
        if (numero == durata_VALORE) errore_VALORE("NumberFormatException");
        for (; numero < durata_VALORE && !errore; numero++) {
            int cifra_VALORE = heap_VALORE[fonti + 2 + numero] - '0';
            if (cifra_VALORE < 0 || cifra_VALORE > 9 || VALORE < -214748364 || VALORE == -214748364 && cifra_VALORE > (negativo_VALORE ? 8 : 7)) errore_VALORE("NumberFormatException");
            VALORE = VALORE * 10 - cifra_VALORE;
        }
        return negativo_VALORE ? VALORE : -VALORE;
    }
    static void 넣기(int VALORE, int TIPO_VALORE) {
        if (errore) return;
        if (frame_INDICE < 0 || frame_Pila[frame_INDICE] >= metodo_Pila[frame_metodo[frame_INDICE]]) { errore_VALORE("operand stack overflow"); return; }
        int slot_voce = frame_INDICE * 128 + frame_Pila[frame_INDICE]++; operando_Pila_VALORE[slot_voce] = VALORE; operando_Pila_TIPO[slot_voce] = TIPO_VALORE;
    }
    static int 빼기(int TIPO_VALORE) {
        if (errore) return 0;
        if (frame_INDICE < 0 || frame_Pila[frame_INDICE] < 1) { errore_VALORE("operand stack underflow"); return 0; }
        int slot_voce = frame_INDICE * 128 + --frame_Pila[frame_INDICE]; tipo_restituito = operando_Pila_TIPO[slot_voce];
        if (TIPO_VALORE != 0 && tipo_restituito != TIPO_VALORE) errore_VALORE("operand type mismatch");
        if (tipo_restituito == 2) proteggere_VALORE(operando_Pila_VALORE[slot_voce]);
        return operando_Pila_VALORE[slot_voce];
    }
    static void 지역읽기(int INDICE, int TIPO_VALORE) {
        if (INDICE >= 함수지역[frame_metodo[frame_INDICE]] || INDICE < 0 || locale_TIPO[frame_INDICE * 128 + INDICE] != TIPO_VALORE) { errore_VALORE("invalid or uninitialized local"); return; }
        넣기(locale_VALORE[frame_INDICE * 128 + INDICE], TIPO_VALORE);
    }
    static void scrivere_locale(int INDICE, int TIPO_VALORE) {
        if (INDICE >= 함수지역[frame_metodo[frame_INDICE]] || INDICE < 0) { errore_VALORE("local index out of range"); return; }
        int VALORE = 빼기(TIPO_VALORE); locale_VALORE[frame_INDICE * 128 + INDICE] = VALORE; locale_TIPO[frame_INDICE * 128 + INDICE] = TIPO_VALORE;
    }
    static int 명바() {
        int posizione = frame_funzione[frame_INDICE];
        if (posizione < metodo_START[frame_metodo[frame_INDICE]] || posizione >= metodo_chiudere[frame_metodo[frame_INDICE]]) { errore_VALORE("instruction pointer out of range"); return 0; }
        frame_funzione[frame_INDICE]++; return file[posizione];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void spostare_VALORE(int posizione) {
        int FUNZIONE_VALORE = frame_metodo[frame_INDICE];
        if (posizione < metodo_START[FUNZIONE_VALORE] || posizione >= metodo_chiudere[FUNZIONE_VALORE] || limite_VALORE[posizione] != FUNZIONE_VALORE + 1) errore_VALORE("invalid branch target");
        else frame_funzione[frame_INDICE] = posizione;
    }
    static void 호출(int FUNZIONE_VALORE) {
        if (frame_INDICE % 32 == 31) { errore_VALORE("call stack limit (32)"); return; }
        int Avanti_articolo = frame_INDICE + 1;
        for (int numero = 0; numero < 128; numero++) locale_TIPO[Avanti_articolo * 128 + numero] = 0;
        for (int numero = metodo_argomento_CONTA_NUMERI[FUNZIONE_VALORE] - 1; numero >= 0; numero--) {
            locale_VALORE[Avanti_articolo * 128 + numero] = 빼기(metodo_argomento_TIPO[FUNZIONE_VALORE * 16 + numero]); locale_TIPO[Avanti_articolo * 128 + numero] = metodo_argomento_TIPO[FUNZIONE_VALORE * 16 + numero];
        }
        if (errore) return;
        frame_INDICE = Avanti_articolo; inizializzare_frame[frame_INDICE] = 0; frame_metodo[frame_INDICE] = FUNZIONE_VALORE; frame_funzione[frame_INDICE] = metodo_START[FUNZIONE_VALORE]; frame_Pila[frame_INDICE] = 0;
    }
    static void Reso_KR(int TIPO_VALORE) {
        if (TIPO_VALORE != metodo_Reso[frame_metodo[frame_INDICE]]) { errore_VALORE("return type mismatch"); return; }
        int VALORE = TIPO_VALORE == 0 ? 0 : 빼기(TIPO_VALORE);
        if (inizializzare_frame[frame_INDICE] != 0) Corso_definizione_Stato[inizializzare_frame[frame_INDICE] - 1] = 2;
        if (frame_blocco[frame_INDICE] != 0) { release_blocco(frame_blocco[frame_INDICE]); frame_blocco[frame_INDICE] = 0; }
        frame_INDICE--; if (frame_INDICE >= Regolari_thread * 32 && TIPO_VALORE != 0) 넣기(VALORE, TIPO_VALORE);
    }
    static int[] Stream_nome_file = new int[64];
    static void File_Stream_Chiama(int proprietario_VALORE, int Nome, int formato_VALORE, int comando) {
        boolean uscitaTesto = Word_SMS(proprietario_VALORE, "java/io/FileOutputStream");
        int Kind_VALORE = uscitaTesto ? 6 : 5;
        if (comando == 183 && Word_SMS(Nome, "<init>")) {
            boolean 이어 = false;
            if (uscitaTesto && Word_SMS(formato_VALORE, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Word_SMS(formato_VALORE, "(Ljava/lang/String;)V")) { errore_VALORE("unsupported file stream constructor"); return; }
            int File_voce_nome = 빼기(2), Stream_VALORE = 빼기(2);
            if (!oggetto_VALORE(File_voce_nome, 1) || !oggetto_VALORE(Stream_VALORE, Kind_VALORE) || errore) return;
            if (heap_VALORE[Stream_VALORE + 3] != 0) { errore_VALORE("file stream already initialized"); return; }
            int durata_VALORE = heap_VALORE[File_voce_nome + 1];
            if (durata_VALORE < 1 || durata_VALORE > 63) { errore_VALORE("invalid file name length"); return; }
            for (int slot_voce = 0; slot_voce < durata_VALORE; slot_voce++) {
                int VALORE = heap_VALORE[File_voce_nome + 2 + slot_voce];
                if (VALORE < 1) { errore_VALORE("invalid file stream path"); return; }
                Stream_nome_file[slot_voce] = VALORE;
            }
            Stream_nome_file[durata_VALORE] = 0;
            int descrittore_voce = spazio_utente.aperto_File_descrittore(Stream_nome_file, uscitaTesto ? (이어 ? 1089 : 577) : 0);
            if (descrittore_voce < 0) { errore_VALORE("FileNotFoundException: file open failed"); return; }
            heap_VALORE[Stream_VALORE + 2] = descrittore_voce; heap_VALORE[Stream_VALORE + 3] = 1;
            return;
        }
        if (comando != 182) { errore_VALORE("invalid file stream invocation"); return; }
        if ((uscitaTesto && Word_SMS(Nome, "write") || !uscitaTesto && Word_SMS(Nome, "read"))
            && (Word_SMS(formato_VALORE, uscitaTesto ? "([B)V" : "([B)I") || Word_SMS(formato_VALORE, uscitaTesto ? "([BII)V" : "([BII)I"))) {
            boolean ritagliare_VALORE = Word_SMS(formato_VALORE, uscitaTesto ? "([BII)V" : "([BII)I");
            int voce_CONTA_NUMERI = ritagliare_VALORE ? 빼기(1) : 0, 시작점 = ritagliare_VALORE ? 빼기(1) : 0, dati_array = 빼기(2), oggetto_fonti = 빼기(2);
            if (!oggetto_VALORE(dati_array, 20) || !oggetto_VALORE(oggetto_fonti, Kind_VALORE)) return;
            if (!ritagliare_VALORE) voce_CONTA_NUMERI = heap_VALORE[dati_array + 1];
            if (시작점 < 0 || voce_CONTA_NUMERI < 0 || 시작점 > heap_VALORE[dati_array + 1] - voce_CONTA_NUMERI) { 예외던짐(6, "file buffer bounds"); return; }
            if (heap_VALORE[oggetto_fonti + 3] == 0 || heap_VALORE[oggetto_fonti + 2] < 0) { errore_VALORE("IOException: stream closed"); return; }
            int Completate_CONTA_NUMERI = 0;
            while (Completate_CONTA_NUMERI < voce_CONTA_NUMERI && !errore) {
                int 반환값 = uscitaTesto ? spazio_utente.파일한바이트쓰기(heap_VALORE[oggetto_fonti + 2], heap_VALORE[dati_array + 2 + 시작점 + Completate_CONTA_NUMERI]) : spazio_utente.파일한바이트읽기(heap_VALORE[oggetto_fonti + 2]);
                if (반환값 < 0) { errore_VALORE(uscitaTesto ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!uscitaTesto && 반환값 == 256) break;
                if (!uscitaTesto) heap_VALORE[dati_array + 2 + 시작점 + Completate_CONTA_NUMERI] = (byte)반환값;
                Completate_CONTA_NUMERI++;
            }
            if (!uscitaTesto) 넣기(voce_CONTA_NUMERI != 0 && Completate_CONTA_NUMERI == 0 ? -1 : Completate_CONTA_NUMERI, 1);
            return;
        }
        if (uscitaTesto && Word_SMS(Nome, "flush") && Word_SMS(formato_VALORE, "()V")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, Kind_VALORE) && heap_VALORE[oggetto_fonti + 2] < 0) errore_VALORE("IOException: stream closed"); return; }
        int Azione = -1, VALORE = 0;
        if (Word_SMS(Nome, "close") && Word_SMS(formato_VALORE, "()V")) Azione = 0;
        if (!uscitaTesto && Word_SMS(Nome, "read") && Word_SMS(formato_VALORE, "()I")) Azione = 1;
        if (uscitaTesto && Word_SMS(Nome, "write") && Word_SMS(formato_VALORE, "(I)V")) { Azione = 2; VALORE = 빼기(1); }
        if (Azione < 0) { errore_VALORE("unsupported file stream method"); return; }
        int Stream_VALORE = 빼기(2);
        if (!oggetto_VALORE(Stream_VALORE, Kind_VALORE) || errore) return;
        if (heap_VALORE[Stream_VALORE + 3] == 0) { errore_VALORE("uninitialized file stream"); return; }
        int descrittore_voce = heap_VALORE[Stream_VALORE + 2];
        if (Azione == 0) {
            if (descrittore_voce >= 0 && spazio_utente.Chiudi_File_descrittore(descrittore_voce) < 0) errore_VALORE("IOException: close failed");
            heap_VALORE[Stream_VALORE + 2] = -1; return;
        }
        if (descrittore_voce < 0) { errore_VALORE("IOException: stream closed"); return; }
        if (Azione == 1) {
            int risultato = spazio_utente.파일한바이트읽기(descrittore_voce);
            if (risultato < -1) errore_VALORE("IOException: read failed"); else 넣기(risultato == 256 ? -1 : risultato, 1);
        } else if (spazio_utente.파일한바이트쓰기(descrittore_voce, VALORE) != 1) errore_VALORE("IOException: write failed");
    }
    static void Chiama_metodo(int INDICE, int comando) {
        if (INDICE <= 0 || INDICE >= costante_tag.length || (costante_tag[INDICE] != 10 && costante_tag[INDICE] != 11)) { errore_VALORE("invalid method reference"); return; }
        int proprietario_VALORE = nome_della_classe_SMS(상가[INDICE]), Nome = fonti_nome(costante_SECONDO_VALORE[INDICE]), formato_VALORE = tipo_riferimento(costante_SECONDO_VALORE[INDICE]);
        if (errore) return;
        if (기본호출(proprietario_VALORE, Nome, formato_VALORE, comando)) return;
        if (Word_SMS(proprietario_VALORE, "java/io/FileInputStream") || Word_SMS(proprietario_VALORE, "java/io/FileOutputStream")) {
            File_Stream_Chiama(proprietario_VALORE, Nome, formato_VALORE, comando); return;
        }
        if (comando == 184 && Word_SMS(proprietario_VALORE, "java/lang/Integer") && Word_SMS(Nome, "parseInt") && Word_SMS(formato_VALORE, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (comando == 182 && Word_SMS(proprietario_VALORE, "java/io/PrintStream") && (Word_SMS(Nome, "println") || Word_SMS(Nome, "print"))) {
            int TIPO_VALORE = 0, VALORE = 0;
            if (Word_SMS(formato_VALORE, "(I)V")) { TIPO_VALORE = 1; VALORE = 빼기(1); }
            else if (Word_SMS(formato_VALORE, "(Z)V")) { TIPO_VALORE = 2; VALORE = 빼기(1); }
            else if (Word_SMS(formato_VALORE, "(C)V")) { TIPO_VALORE = 3; VALORE = 빼기(1); }
            else if (Word_SMS(formato_VALORE, "(Ljava/lang/String;)V")) { TIPO_VALORE = 4; VALORE = 빼기(2); }
            else if (!Word_SMS(formato_VALORE, "()V") || !Word_SMS(Nome, "println")) errore_VALORE("unsupported print descriptor");
            if (빼기(2) != -1) errore_VALORE("invalid PrintStream receiver");
            if (errore) return;
            if (TIPO_VALORE == 1) 자바도구.scrivere_numero(VALORE);
            if (TIPO_VALORE == 2) spazio_utente.Scrittura(VALORE == 0 ? "false" : "true");
            if (TIPO_VALORE == 3) spazio_utente.scrivere_carattere_VALORE(VALORE & 65535);
            if (TIPO_VALORE == 4) scrivere_SMS(VALORE);
            if (Word_SMS(Nome, "println")) spazio_utente.scrivere_carattere_VALORE(10);
            return;
        }
        if (comando == 182 && Word_SMS(proprietario_VALORE, "java/lang/String")) {
            if (Word_SMS(Nome, "length") && Word_SMS(formato_VALORE, "()I")) {
                int fonti = 빼기(2); if (oggetto_VALORE(fonti, 1)) 넣기(heap_VALORE[fonti + 1], 1); return;
            }
            if (Word_SMS(Nome, "charAt") && Word_SMS(formato_VALORE, "(I)C")) {
                int pedice_VALORE = 빼기(1), fonti = 빼기(2);
                if (oggetto_VALORE(fonti, 1)) {
                    if (pedice_VALORE < 0 || pedice_VALORE >= heap_VALORE[fonti + 1]) errore_VALORE("StringIndexOutOfBoundsException"); else 넣기(heap_VALORE[fonti + 2 + pedice_VALORE], 1);
                }
                return;
            }
        }
        if (Word_SMS(proprietario_VALORE, "java/lang/StringBuilder")) {
            if (comando == 183 && Word_SMS(Nome, "<init>") && Word_SMS(formato_VALORE, "()V")) { oggetto_VALORE(빼기(2), 4); return; }
            if (comando == 182 && Word_SMS(Nome, "toString") && Word_SMS(formato_VALORE, "()Ljava/lang/String;")) {
                int fonti = 빼기(2); if (oggetto_VALORE(fonti, 4)) 넣기(heap_VALORE[fonti + 2] == 0 ? host_carattere("") : heap_VALORE[fonti + 2], 2); return;
            }
            if (comando == 182 && Word_SMS(Nome, "append")) {
                int testo = 0;
                if (Word_SMS(formato_VALORE, "(I)Ljava/lang/StringBuilder;")) testo = cifra_carattere(빼기(1));
                else if (Word_SMS(formato_VALORE, "(Z)Ljava/lang/StringBuilder;")) testo = host_carattere(빼기(1) == 0 ? "false" : "true");
                else if (Word_SMS(formato_VALORE, "(C)Ljava/lang/StringBuilder;")) {
                    int VALORE = 빼기(1); testo = allocare_Memoria(1, 1); if (!errore) heap_VALORE[testo + 2] = VALORE & 65535;
                }
                else if (Word_SMS(formato_VALORE, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { testo = 빼기(2); if (testo == 0) testo = host_carattere("null"); }
                else { errore_VALORE("unsupported StringBuilder append"); return; }
                int fonti = 빼기(2); if (!oggetto_VALORE(fonti, 4) || !oggetto_VALORE(testo, 1)) return;
                int frontale_VALORE = heap_VALORE[fonti + 2], frontale_VALORE_durata = frontale_VALORE == 0 ? 0 : heap_VALORE[frontale_VALORE + 1], BACK_VALORE_durata = heap_VALORE[testo + 1];
                int 새글 = allocare_Memoria(1, frontale_VALORE_durata + BACK_VALORE_durata); if (errore) return;
                for (int numero = 0; numero < frontale_VALORE_durata; numero++) heap_VALORE[새글 + 2 + numero] = heap_VALORE[frontale_VALORE + 2 + numero];
                for (int numero = 0; numero < BACK_VALORE_durata; numero++) heap_VALORE[새글 + 2 + frontale_VALORE_durata + numero] = heap_VALORE[testo + 2 + numero];
                heap_VALORE[fonti + 2] = 새글; 넣기(fonti, 2); return;
            }
        }
        int Corso_definizione = TROVA_Corso_definizione(proprietario_VALORE); if (Corso_definizione < 0 || errore) return;
        int File_INDICE = TROVA_metodo(Corso_definizione, Nome, formato_VALORE);
        if (File_INDICE < 0) {
            for (int punto_di_codice = Corso_definizione, voce_CONTA_NUMERI = 0; punto_di_codice >= 0 && voce_CONTA_NUMERI < 16; voce_CONTA_NUMERI++, punto_di_codice = padre_Corso(punto_di_codice))
                if (Word_SMS(Corso_definizione_padre[punto_di_codice], "java/lang/Thread")) { 가닥호출(Nome, formato_VALORE, comando); return; }
            errore_VALORE("NoSuchMethodError"); return;
        }
        if (((metodo_accesso[File_INDICE] & 8) != 0) != (comando == 184)) { errore_VALORE("method static/instance mismatch"); return; }
        if (comando == 184) { if (!inizializza(metodo_proprietario[File_INDICE], frame_istruzione[frame_INDICE])) return; }
        else {
            int 읽는자리 = frame_Pila[frame_INDICE] - metodo_argomento_CONTA_NUMERI[File_INDICE];
            if (읽는자리 < 0 || operando_Pila_TIPO[frame_INDICE * 128 + 읽는자리] != 2) { errore_VALORE("invalid method receiver"); return; }
            int oggetto_fonti = operando_Pila_VALORE[frame_INDICE * 128 + 읽는자리];
            if (!reparto_IT_valido_oggetto(oggetto_fonti)) return;
            if (heap_VALORE[oggetto_fonti] < 32 || !종포함(heap_VALORE[oggetto_fonti] - 32, proprietario_VALORE)) { errore_VALORE("method receiver type mismatch"); return; }
            if (comando != 183) File_INDICE = TROVA_metodo(heap_VALORE[oggetto_fonti] - 32, Nome, formato_VALORE);
        }
        if (File_INDICE < 0 || (metodo_accesso[File_INDICE] & 0x400) != 0) { errore_VALORE("AbstractMethodError"); return; }
        int blocco_fonti = 0;
        if ((metodo_accesso[File_INDICE] & 32) != 0) {
            if (comando == 184) { int punto_di_codice = metodo_proprietario[File_INDICE]; if (Corso_blocco[punto_di_codice] == 0) Corso_blocco[punto_di_codice] = allocare_Memoria(8, 0); blocco_fonti = Corso_blocco[punto_di_codice]; }
            else blocco_fonti = operando_Pila_VALORE[frame_INDICE * 128 + frame_Pila[frame_INDICE] - metodo_argomento_CONTA_NUMERI[File_INDICE]];
            if (!잠금얻기(blocco_fonti)) { if (!errore) frame_funzione[frame_INDICE] = frame_istruzione[frame_INDICE]; return; }
        }
        호출(File_INDICE); if (!errore) frame_blocco[frame_INDICE] = blocco_fonti;
    }
    static boolean 배열저장가능(int array_fonti, int dati_VALORE) {
        if (dati_VALORE == 0 || elemento_di_matrice[array_fonti] == 0) return true;
        boolean 성공여부 = elemento_di_matrice[array_fonti] == -1 ? (dati_VALORE > 0 && dati_VALORE < heap_chiudere_funzione && heap_VALORE[dati_VALORE] == 1) : collegamento_movimenti_oggetto(dati_VALORE, elemento_di_matrice[array_fonti]);
        if (!성공여부 && !errore) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int array_slot(int fonti, int pedice_VALORE, int TIPO_VALORE) {
        if (!oggetto_VALORE(fonti, TIPO_VALORE)) return 0;
        if (pedice_VALORE < 0 || pedice_VALORE >= heap_VALORE[fonti + 1]) { errore_VALORE("ArrayIndexOutOfBoundsException"); return 0; }
        return fonti + 2 + pedice_VALORE;
    }
    static void Esegui_comando() {
        int 남음 = 500000, blocco_VALORE_652d4b53 = 100;
        while (true) {
            if (errore) { if (던진객체 != 0) handle_eccezione(); if (errore || frame_INDICE < Regolari_thread * 32) break; }
            if (frame_INDICE < Regolari_thread * 32 || richiesta_di_modifica || --blocco_VALORE_652d4b53 == 0) { if (!SWITCH_thread()) break; blocco_VALORE_652d4b53 = 100; }
            if (frame_INDICE == 0 && Corso_definizione_Stato[voce_Corso_definizione] != 2 && !inizializza(voce_Corso_definizione, frame_funzione[frame_INDICE])) continue;
            if (frame_INDICE == Regolari_thread * 32 && Regolari_thread != 0 && (metodo_accesso[frame_metodo[frame_INDICE]] & 32) != 0 && frame_blocco[frame_INDICE] == 0) {
                int oggetto_fonti = thread_target[Regolari_thread]; if (!잠금얻기(oggetto_fonti)) { if (errore) break; continue; } frame_blocco[frame_INDICE] = oggetto_fonti;
            }
            잠시수 = 0;
            if (--남음 == 0) { errore_VALORE("instruction limit (500000)"); break; }
            int avvia = frame_funzione[frame_INDICE]; frame_istruzione[frame_INDICE] = avvia; int VALORE = 명바();
            if (errore) break;
            if (VALORE == 0) continue;
            if (VALORE == 1) { 넣기(0, 2); continue; }
            if (VALORE >= 2 && VALORE <= 8) { 넣기(VALORE - 3, 1); continue; }
            if (VALORE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALORE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALORE == 18 || VALORE == 19) {
                int numero = metodo_proprietario[frame_metodo[frame_INDICE]] * 512 + (VALORE == 18 ? 명바() : 명짧());
                if (numero <= 0 || numero >= costante_tag.length) errore_VALORE("invalid ldc constant");
                else if (costante_tag[numero] == 3) 넣기(상가[numero], 1);
                else if (costante_tag[numero] == 8) 넣기(costante_SMS(상가[numero]), 2);
                else errore_VALORE("unsupported ldc constant");
                continue;
            }
            if (VALORE == 21 || VALORE == 25) { 지역읽기(명바(), VALORE == 21 ? 1 : 2); continue; }
            if (VALORE >= 26 && VALORE <= 29) { 지역읽기(VALORE - 26, 1); continue; }
            if (VALORE >= 42 && VALORE <= 45) { 지역읽기(VALORE - 42, 2); continue; }
            if (VALORE == 54 || VALORE == 58) { scrivere_locale(명바(), VALORE == 54 ? 1 : 2); continue; }
            if (VALORE >= 59 && VALORE <= 62) { scrivere_locale(VALORE - 59, 1); continue; }
            if (VALORE >= 75 && VALORE <= 78) { scrivere_locale(VALORE - 75, 2); continue; }
            if (VALORE == 46 || VALORE >= 50 && VALORE <= 53) {
                int voce_funzione = 빼기(1), oggetto_fonti = 빼기(2), area_CODICE = VALORE == 46 ? 2 : VALORE == 50 ? 3 : VALORE == 51 ? 20 : VALORE == 52 ? 22 : 23;
                if (VALORE == 51 && oggetto_fonti > 0 && oggetto_fonti < heap_chiudere_funzione && heap_VALORE[oggetto_fonti] == 21) area_CODICE = 21;
                int 읽는자리 = array_slot(oggetto_fonti, voce_funzione, area_CODICE); if (!errore) 넣기(heap_VALORE[읽는자리], VALORE == 50 ? 2 : 1); continue;
            }
            if (VALORE == 79 || VALORE >= 83 && VALORE <= 86) {
                int voce_fonti = 빼기(VALORE == 83 ? 2 : 1), voce_funzione = 빼기(1), oggetto_fonti = 빼기(2), area_CODICE = VALORE == 79 ? 2 : VALORE == 83 ? 3 : VALORE == 84 ? 20 : VALORE == 85 ? 22 : 23;
                if (VALORE == 84 && oggetto_fonti > 0 && oggetto_fonti < heap_chiudere_funzione && heap_VALORE[oggetto_fonti] == 21) area_CODICE = 21;
                int 읽는자리 = array_slot(oggetto_fonti, voce_funzione, area_CODICE);
                if (!errore && area_CODICE == 3 && !배열저장가능(oggetto_fonti, voce_fonti)) continue;
                if (!errore) heap_VALORE[읽는자리] = area_CODICE == 20 ? (byte)voce_fonti : area_CODICE == 21 ? voce_fonti & 1 : area_CODICE == 22 ? (char)voce_fonti : area_CODICE == 23 ? (short)voce_fonti : voce_fonti;
                continue;
            }
            if (VALORE >= 87 && VALORE <= 95) { Pila_istruzione(VALORE); continue; }
            if (VALORE == 96 || VALORE == 100 || VALORE == 104 || VALORE == 108 || VALORE == 112 || VALORE == 120
                || VALORE == 122 || VALORE == 124 || VALORE == 126 || VALORE == 128 || VALORE == 130) {
                int SECONDO_operando = 빼기(1), 가 = 빼기(1), risultato = 0;
                if ((VALORE == 108 || VALORE == 112) && SECONDO_operando == 0) { errore_VALORE("ArithmeticException: / by zero"); continue; }
                if (VALORE == 96) risultato = 가 + SECONDO_operando;
                if (VALORE == 100) risultato = 가 - SECONDO_operando;
                if (VALORE == 104) risultato = 가 * SECONDO_operando;
                if (VALORE == 108) risultato = 가 / SECONDO_operando;
                if (VALORE == 112) risultato = 가 % SECONDO_operando;
                if (VALORE == 120) risultato = 가 << SECONDO_operando;
                if (VALORE == 122) risultato = 가 >> SECONDO_operando;
                if (VALORE == 124) risultato = 가 >>> SECONDO_operando;
                if (VALORE == 126) risultato = 가 & SECONDO_operando;
                if (VALORE == 128) risultato = 가 | SECONDO_operando;
                if (VALORE == 130) risultato = 가 ^ SECONDO_operando;
                넣기(risultato, 1); continue;
            }
            if (VALORE == 116) { 넣기(-빼기(1), 1); continue; }
            if (VALORE == 132) {
                int locale_Scope = 명바(), incremento_passaggio = (byte)명바(); 지역읽기(locale_Scope, 1); 넣기(빼기(1) + incremento_passaggio, 1); scrivere_locale(locale_Scope, 1); continue;
            }
            if (VALORE >= 145 && VALORE <= 147) {
                int numero = 빼기(1); 넣기(VALORE == 145 ? (byte)numero : VALORE == 146 ? (char)numero : (short)numero, 1); continue;
            }
            if (VALORE >= 153 && VALORE <= 167 || VALORE == 198 || VALORE == 199) {
                int meta_VALORE = avvia + (short)명짧(); boolean 갈까 = VALORE == 167;
                if (VALORE >= 153 && VALORE <= 158) {
                    int numero = 빼기(1); 갈까 = VALORE == 153 ? numero == 0 : VALORE == 154 ? numero != 0 : VALORE == 155 ? numero < 0 : VALORE == 156 ? numero >= 0 : VALORE == 157 ? numero > 0 : numero <= 0;
                } else if (VALORE >= 159 && VALORE <= 166) {
                    int SECONDO_operando = 빼기(VALORE >= 165 ? 2 : 1), 가 = 빼기(VALORE >= 165 ? 2 : 1);
                    갈까 = VALORE == 159 || VALORE == 165 ? 가 == SECONDO_operando : VALORE == 160 || VALORE == 166 ? 가 != SECONDO_operando : VALORE == 161 ? 가 < SECONDO_operando : VALORE == 162 ? 가 >= SECONDO_operando : VALORE == 163 ? 가 > SECONDO_operando : 가 <= SECONDO_operando;
                } else if (VALORE == 198 || VALORE == 199) { int numero = 빼기(2); 갈까 = VALORE == 198 ? numero == 0 : numero != 0; }
                if (갈까) spostare_VALORE(meta_VALORE); continue;
            }
            if (VALORE == 172 || VALORE == 176 || VALORE == 177) { Reso_KR(VALORE == 172 ? 1 : VALORE == 176 ? 2 : 0); continue; }
            if (VALORE >= 178 && VALORE <= 181) { 필드호출(명상수(), VALORE, avvia); continue; }
            if (VALORE >= 182 && VALORE <= 185) {
                int 부호값 = 명상수();
                if (VALORE == 185) { int totale_CONTA_NUMERI = 명바(); if (totale_CONTA_NUMERI == 0 || 명바() != 0) { errore_VALORE("invalid invokeinterface operands"); continue; } }
                Chiama_metodo(부호값, VALORE); continue;
            }
            if (VALORE == 187) { 새객체(nome_della_classe_SMS(명상수()), avvia); continue; }
            if (VALORE == 188 || VALORE == 189) {
                int area_CODICE = 3, componente = 0;
                if (VALORE == 188) { int 임시값 = 명바(); area_CODICE = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else componente = nome_della_classe_SMS(명상수());
                if (area_CODICE == 0) { errore_VALORE("unsupported primitive array type"); continue; }
                int valido_durata = 빼기(1), oggetto_fonti = allocare_Memoria(area_CODICE, valido_durata); if (!errore) elemento_di_matrice[oggetto_fonti] = componente; 넣기(oggetto_fonti, 2); continue;
            }
            if (VALORE == 190) {
                int oggetto_fonti = 빼기(2);
                if (reparto_IT_valido_oggetto(oggetto_fonti)) { int Confronto_funzione = heap_VALORE[oggetto_fonti]; if (Confronto_funzione != 2 && Confronto_funzione != 3 && (Confronto_funzione < 20 || Confronto_funzione > 23)) errore_VALORE("not an array"); else 넣기(heap_VALORE[oggetto_fonti + 1], 1); }
                continue;
            }
            if (VALORE == 191) {
                int oggetto_fonti = 빼기(2); if (reparto_IT_valido_oggetto(oggetto_fonti)) { if (heap_VALORE[oggetto_fonti] != 9) errore_VALORE("athrow requires supported Throwable"); else { 던진객체 = oggetto_fonti; errore = true; } }
                continue;
            }
            if (VALORE == 192 || VALORE == 193) {
                int nome_costante = nome_della_classe_SMS(명상수()), oggetto_fonti = 빼기(2); boolean match = collegamento_movimenti_oggetto(oggetto_fonti, nome_costante);
                if (VALORE == 193) 넣기(oggetto_fonti != 0 && match ? 1 : 0, 1);
                else { if (!match && !errore) errore_VALORE("ClassCastException"); 넣기(oggetto_fonti, 2); }
                continue;
            }
            if (VALORE == 170 || VALORE == 171) {
                int 읽는자리 = avvia + 1, File_INDICE = frame_metodo[frame_INDICE], tasto_fonti = 빼기(1);
                while ((읽는자리 - metodo_START[File_INDICE]) % 4 != 0) 읽는자리++;
                int target_e_mail = funzione_intero(읽는자리);
                if (VALORE == 170) { int 낮은값 = funzione_intero(읽는자리 + 4), 높은값 = funzione_intero(읽는자리 + 8); if (tasto_fonti >= 낮은값 && tasto_fonti <= 높은값) target_e_mail = funzione_intero(읽는자리 + 12 + (tasto_fonti - 낮은값) * 4); }
                else { int totale_CONTA_NUMERI = funzione_intero(읽는자리 + 4); for (int Loop_INDICE = 0; Loop_INDICE < totale_CONTA_NUMERI; Loop_INDICE++) if (funzione_intero(읽는자리 + 8 + Loop_INDICE * 8) == tasto_fonti) target_e_mail = funzione_intero(읽는자리 + 12 + Loop_INDICE * 8); }
                spostare_VALORE(avvia + target_e_mail); continue;
            }
            if (VALORE == 200) { spostare_VALORE(avvia + funzione_intero(avvia + 1)); continue; }
            if (VALORE == 194 || VALORE == 195) {
                int oggetto_fonti = 빼기(2);
                if (VALORE == 195) release_blocco(oggetto_fonti);
                else if (!잠금얻기(oggetto_fonti) && !errore) { 넣기(oggetto_fonti, 2); frame_funzione[frame_INDICE] = avvia; }
                continue;
            }
            if (VALORE == 196) {
                int comando_CODICE = 명바(), voce_funzione = 명짧();
                if (comando_CODICE == 21 || comando_CODICE == 25) 지역읽기(voce_funzione, comando_CODICE == 21 ? 1 : 2);
                else if (comando_CODICE == 54 || comando_CODICE == 58) scrivere_locale(voce_funzione, comando_CODICE == 54 ? 1 : 2);
                else if (comando_CODICE == 132) { int DELTA_VALORE = (short)명짧(); 지역읽기(voce_funzione, 1); 넣기(빼기(1) + DELTA_VALORE, 1); scrivere_locale(voce_funzione, 1); }
                else errore_VALORE("unsupported wide opcode");
                continue;
            }
            errore_VALORE("unsupported bytecode");
        }
    }
    static int TROVA_Corso_definizione(int Nome) {
        for (int Loop_INDICE = 0; Loop_INDICE < Corso_definizione_CONTA_NUMERI; Loop_INDICE++) if (Corso_definizione_nome[Loop_INDICE] != 0 && collegamento_movimenti_Word(Corso_definizione_nome[Loop_INDICE], Nome)) return Loop_INDICE;
        return carico_Corso_definizione(costante_SMS(Nome));
    }
    static int carico_Corso_definizione(int nome_stringa) {
        if (!oggetto_VALORE(nome_stringa, 1)) return -1;
        int durata_VALORE = heap_VALORE[nome_stringa + 1];
        if (durata_VALORE < 1 || durata_VALORE > 505 || Corso_definizione_CONTA_NUMERI == 16) { errore_VALORE("class name/count limit"); return -1; }
        for (int Loop_INDICE = 0; Loop_INDICE < durata_VALORE; Loop_INDICE++) { int punto_di_codice = heap_VALORE[nome_stringa + 2 + Loop_INDICE]; nome_file_SMS[Loop_INDICE] = punto_di_codice == '/' ? '.' : punto_di_codice; }
        nome_file_SMS[durata_VALORE] = '.'; nome_file_SMS[durata_VALORE + 1] = 'c'; nome_file_SMS[durata_VALORE + 2] = 'l'; nome_file_SMS[durata_VALORE + 3] = 'a'; nome_file_SMS[durata_VALORE + 4] = 's'; nome_file_SMS[durata_VALORE + 5] = 's'; nome_file_SMS[durata_VALORE + 6] = 0;
        int Dimensione = spazio_utente.파일읽기(nome_file_SMS, file_temporaneo);
        if (Dimensione < 0) { errore_VALORE("ClassNotFoundException"); return -1; }
        int Corso_definizione = Corso_definizione_CONTA_NUMERI++; Corso_definizione_ridimensionare[Corso_definizione] = Dimensione;
        for (int Loop_INDICE = 0; Loop_INDICE < Dimensione; Loop_INDICE++) file[Corso_definizione * 16384 + Loop_INDICE] = file_temporaneo[Loop_INDICE];
        클래스읽기(Corso_definizione); if (errore) return -1;
        int effettivo_dati = costante_SMS(Corso_definizione_nome[Corso_definizione]);
        if (!testi_uguali(effettivo_dati, nome_stringa, true)) { errore_VALORE("class name does not match file"); return -1; }
        int padre_VALORE = Corso_definizione_padre[Corso_definizione];
        if (padre_VALORE != 0 && !Word_SMS(padre_VALORE, "java/lang/Object") && !Word_SMS(padre_VALORE, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 retry_VALORE 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = TROVA_Corso_definizione(padre_VALORE);
            if (errore || 위 < 0) return -1;
            int 읽는자리 = 위, area_CONTA_NUMERI = 0;
            while (읽는자리 >= 0 && area_CONTA_NUMERI++ < 16) {
                if (읽는자리 == Corso_definizione) { errore_VALORE("cyclic inheritance"); return -1; }
                읽는자리 = padre_Corso(읽는자리);
            }
            int 시작변위 = Corso_slot_CONTA_NUMERI[위];
            for (int File_INDICE = 0; File_INDICE < slot_CONTA_NUMERI; File_INDICE++) if (slot_proprietario[File_INDICE] == Corso_definizione && (slot_Autorizzazioni[File_INDICE] & 8) == 0) slot_funzione[File_INDICE] += 시작변위;
            Corso_slot_CONTA_NUMERI[Corso_definizione] += 시작변위;
        }
        return Corso_definizione;
    }
    static int padre_Corso(int Corso_definizione) {
        int Nome = Corso_definizione_padre[Corso_definizione];
        for (int Loop_INDICE = 0; Loop_INDICE < Corso_definizione_CONTA_NUMERI; Loop_INDICE++) if (Nome != 0 && Corso_definizione_nome[Loop_INDICE] != 0 && collegamento_movimenti_Word(Corso_definizione_nome[Loop_INDICE], Nome)) return Loop_INDICE;
        return -1;
    }
    static int TROVA_metodo(int Corso_definizione, int Nome, int formato_VALORE) {
        for (int 깊이 = 0; Corso_definizione >= 0 && 깊이 < 16; 깊이++, Corso_definizione = padre_Corso(Corso_definizione)) {
            for (int Loop_INDICE = 0; Loop_INDICE < metodo_CONTA_NUMERI; Loop_INDICE++) if (metodo_proprietario[Loop_INDICE] == Corso_definizione && collegamento_movimenti_Word(metodo_nome_SMS[Loop_INDICE], Nome) && collegamento_movimenti_Word(metodo_TIPO[Loop_INDICE], formato_VALORE)) return Loop_INDICE;
        }
        return -1;
    }
    static int nome_metodo(int Corso_definizione, String Nome, String formato_VALORE) {
        for (int 깊이 = 0; Corso_definizione >= 0 && 깊이 < 16; 깊이++, Corso_definizione = padre_Corso(Corso_definizione))
            for (int Loop_INDICE = 0; Loop_INDICE < metodo_CONTA_NUMERI; Loop_INDICE++) if (metodo_proprietario[Loop_INDICE] == Corso_definizione && Word_SMS(metodo_nome_SMS[Loop_INDICE], Nome) && Word_SMS(metodo_TIPO[Loop_INDICE], formato_VALORE)) return Loop_INDICE;
        return -1;
    }
    static int TIPO_Kind(int Nome) { return file[상가[Nome]] == 'L' || file[상가[Nome]] == '[' ? 2 : 1; }
    static boolean inizializza(int Corso_definizione, int comando_START) {
        if (Corso_definizione < 0 || errore) return false;
        if (Corso_definizione_Stato[Corso_definizione] == 3) { errore_VALORE("NoClassDefFoundError: initialization failed"); return false; }
        if (Corso_definizione_Stato[Corso_definizione] == 1 && Corso_thread[Corso_definizione] != Regolari_thread) { frame_funzione[frame_INDICE] = comando_START; richiesta_di_modifica = true; return false; }
        if (Corso_definizione_Stato[Corso_definizione] != 0) return true;
        int 위 = padre_Corso(Corso_definizione);
        if (위 >= 0 && !inizializza(위, comando_START)) return false;
        Corso_definizione_Stato[Corso_definizione] = 1; Corso_thread[Corso_definizione] = Regolari_thread;
        if (inizializzare_Corso_definizione[Corso_definizione] != 0) {
            frame_funzione[frame_INDICE] = comando_START;
            호출(inizializzare_Corso_definizione[Corso_definizione] - 1); if (!errore) inizializzare_frame[frame_INDICE] = Corso_definizione + 1;
            return false;
        }
        Corso_definizione_Stato[Corso_definizione] = 2; return true;
    }
    static void 필드호출(int INDICE, int comando, int avvia) {
        if (!assegno_costante(INDICE, 9)) return;
        int proprietario_VALORE = nome_della_classe_SMS(상가[INDICE]), Nome = fonti_nome(costante_SECONDO_VALORE[INDICE]), formato_VALORE = tipo_riferimento(costante_SECONDO_VALORE[INDICE]);
        if (Word_SMS(proprietario_VALORE, "java/lang/System") && (Word_SMS(Nome, "out") || Word_SMS(Nome, "err")) && Word_SMS(formato_VALORE, "Ljava/io/PrintStream;") && comando == 178) { 넣기(-1, 2); return; }
        int Corso_definizione = TROVA_Corso_definizione(proprietario_VALORE); if (Corso_definizione < 0 || errore) return;
        int 찾음 = -1;
        for (int 읽는자리 = Corso_definizione, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = padre_Corso(읽는자리))
            for (int File_INDICE = 0; File_INDICE < slot_CONTA_NUMERI; File_INDICE++) if (slot_proprietario[File_INDICE] == 읽는자리 && collegamento_movimenti_Word(slot_nome[File_INDICE], Nome) && collegamento_movimenti_Word(slot_TIPO[File_INDICE], formato_VALORE)) 찾음 = File_INDICE;
        if (찾음 < 0) { errore_VALORE("NoSuchFieldError"); return; }
        boolean statico_VALORE = comando == 178 || comando == 179;
        if (statico_VALORE != ((slot_Autorizzazioni[찾음] & 8) != 0)) { errore_VALORE("field static/instance mismatch"); return; }
        if (statico_VALORE && !inizializza(slot_proprietario[찾음], avvia)) return;
        int TIPO_VALORE = TIPO_Kind(formato_VALORE), VALORE = 0;
        if (comando == 179 || comando == 181) VALORE = 빼기(TIPO_VALORE);
        if (statico_VALORE) { if (comando == 178) 넣기(slot_dati[찾음], TIPO_VALORE); else if (!errore) slot_dati[찾음] = VALORE; return; }
        int oggetto_fonti = 빼기(2);
        if (!reparto_IT_valido_oggetto(oggetto_fonti)) return;
        if (heap_VALORE[oggetto_fonti] < 32 || !종포함(heap_VALORE[oggetto_fonti] - 32, proprietario_VALORE)) { errore_VALORE("field receiver type mismatch"); return; }
        int 보관칸 = oggetto_fonti + 2 + slot_funzione[찾음];
        if (comando == 180) 넣기(heap_VALORE[보관칸], TIPO_VALORE);
        else if (!errore) { heap_VALORE[보관칸] = VALORE; heap_fonti[보관칸] = TIPO_VALORE == 2 ? 1 : 0; }
    }
    static boolean 종포함(int Corso_definizione, int Nome) {
        for (int 중첩깊이 = 0; Corso_definizione >= 0 && 중첩깊이 < 16; 중첩깊이++, Corso_definizione = padre_Corso(Corso_definizione)) {
            if (collegamento_movimenti_Word(Corso_definizione_nome[Corso_definizione], Nome) || (Corso_definizione_padre[Corso_definizione] != 0 && collegamento_movimenti_Word(Corso_definizione_padre[Corso_definizione], Nome))) return true;
            for (int inner_funzione = 0; inner_funzione < Corso_interfaccia_CONTA_NUMERI[Corso_definizione]; inner_funzione++) if (collegamento_movimenti_Word(Corso_interfaccia[Corso_definizione * 16 + inner_funzione], Nome)) return true;
        }
        return false;
    }
    static boolean testi_uguali(int 첫값, int byte_dati, boolean percorso) {
        if (첫값 == byte_dati) return true;
        if (첫값 <= 0 || byte_dati <= 0 || heap_VALORE[첫값] != 1 || heap_VALORE[byte_dati] != 1 || heap_VALORE[첫값 + 1] != heap_VALORE[byte_dati + 1]) return false;
        for (int Loop_INDICE = 0; Loop_INDICE < heap_VALORE[첫값 + 1]; Loop_INDICE++) {
            int coordinata_x = heap_VALORE[첫값 + 2 + Loop_INDICE], Y_coordinata = heap_VALORE[byte_dati + 2 + Loop_INDICE];
            if (percorso) { if (coordinata_x == '.') coordinata_x = '/'; if (Y_coordinata == '.') Y_coordinata = '/'; }
            if (coordinata_x != Y_coordinata) return false;
        }
        return true;
    }
    static boolean reparto_IT_valido_oggetto(int oggetto_fonti) {
        if (oggetto_fonti == 0) { errore_VALORE("NullPointerException"); return false; }
        if (oggetto_fonti < 1 || oggetto_fonti >= heap_chiudere_funzione || 힙폭[oggetto_fonti] < 2 || heap_VALORE[oggetto_fonti] == 0) { errore_VALORE("invalid object reference"); return false; }
        return true;
    }
    static void proteggere_VALORE(int oggetto_fonti) {
        if (oggetto_fonti > 0 && oggetto_fonti < heap_chiudere_funzione && 힙폭[oggetto_fonti] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = oggetto_fonti;
    }
    static void mostrare_VALORE(int oggetto_fonti) {
        if (oggetto_fonti > 0 && oggetto_fonti < heap_chiudere_funzione && 힙폭[oggetto_fonti] >= 2 && heap_VALORE[oggetto_fonti] != 0 && 힙표시[oggetto_fonti] == 0) {
            힙표시[oggetto_fonti] = 1; 표시대기[display_CONTA_NUMERI++] = oggetto_fonti;
        }
    }
    static void 수거() {
        display_CONTA_NUMERI = 0; album_CONTA_NUMERI++;
        for (int assegno_funzione = 1; assegno_funzione < heap_chiudere_funzione; assegno_funzione += 힙폭[assegno_funzione]) 힙표시[assegno_funzione] = 0;
        for (int Loop_INDICE = 0; Loop_INDICE < stringa_fonti.length; Loop_INDICE++) mostrare_VALORE(stringa_fonti[Loop_INDICE]);
        for (int Loop_INDICE = 0; Loop_INDICE < slot_CONTA_NUMERI; Loop_INDICE++) if ((slot_Autorizzazioni[Loop_INDICE] & 8) != 0 && TIPO_Kind(slot_TIPO[Loop_INDICE]) == 2) mostrare_VALORE(slot_dati[Loop_INDICE]);
        for (int 임시값 = 0; 임시값 < Conteggio_dei_thread; 임시값++) {
            mostrare_VALORE(thread_oggetto[임시값]); mostrare_VALORE(thread_target[임시값]);
            int 꼭대기자리 = 임시값 == Regolari_thread ? frame_INDICE : thread_frame[임시값];
            for (int File_INDICE = 임시값 * 32; File_INDICE <= 꼭대기자리; File_INDICE++) {
                for (int inner_funzione = 0; inner_funzione < 함수지역[frame_metodo[File_INDICE]]; inner_funzione++) if (locale_TIPO[File_INDICE * 128 + inner_funzione] == 2) mostrare_VALORE(locale_VALORE[File_INDICE * 128 + inner_funzione]);
                for (int inner_funzione = 0; inner_funzione < frame_Pila[File_INDICE]; inner_funzione++) if (operando_Pila_TIPO[File_INDICE * 128 + inner_funzione] == 2) mostrare_VALORE(operando_Pila_VALORE[File_INDICE * 128 + inner_funzione]);
            }
        }
        for (int Loop_INDICE = 0; Loop_INDICE < schermata_fonti.length; Loop_INDICE++) mostrare_VALORE(schermata_fonti[Loop_INDICE]);
        for (int Loop_INDICE = 0; Loop_INDICE < 나중수; Loop_INDICE++) mostrare_VALORE(나중실행[Loop_INDICE]);
        for (int Loop_INDICE = 0; Loop_INDICE < Store_intero.length; Loop_INDICE++) mostrare_VALORE(Store_intero[Loop_INDICE]);
        for (int Loop_INDICE = 0; Loop_INDICE < Corso_definizione_CONTA_NUMERI; Loop_INDICE++) mostrare_VALORE(Corso_blocco[Loop_INDICE]);
        for (int assegno_funzione = 1; assegno_funzione < heap_chiudere_funzione; assegno_funzione += 힙폭[assegno_funzione]) if (잠금깊이[assegno_funzione] > 0) mostrare_VALORE(assegno_funzione);
        mostrare_VALORE(던진객체);
        for (int Loop_INDICE = 0; Loop_INDICE < 잠시수; Loop_INDICE++) mostrare_VALORE(잠시참조[Loop_INDICE]);
        while (display_CONTA_NUMERI > 0) {
            int oggetto_fonti = 표시대기[--display_CONTA_NUMERI], area_CODICE = heap_VALORE[oggetto_fonti];
            for (int Loop_INDICE = oggetto_fonti + 2; Loop_INDICE < oggetto_fonti + 힙폭[oggetto_fonti]; Loop_INDICE++) if (area_CODICE == 3 || area_CODICE == 4 || heap_fonti[Loop_INDICE] != 0) mostrare_VALORE(heap_VALORE[Loop_INDICE]);
        }
        for (int assegno_funzione = 1; assegno_funzione < heap_chiudere_funzione; assegno_funzione += 힙폭[assegno_funzione]) if (힙표시[assegno_funzione] == 0) heap_VALORE[assegno_funzione] = 0;
        for (int assegno_funzione = 1; assegno_funzione < heap_chiudere_funzione; assegno_funzione += 힙폭[assegno_funzione]) if (heap_VALORE[assegno_funzione] == 0) {
            while (assegno_funzione + 힙폭[assegno_funzione] < heap_chiudere_funzione && heap_VALORE[assegno_funzione + 힙폭[assegno_funzione]] == 0) { int Avanti_funzione = assegno_funzione + 힙폭[assegno_funzione]; 힙폭[assegno_funzione] += 힙폭[Avanti_funzione]; 힙폭[Avanti_funzione] = 0; }
            if (assegno_funzione + 힙폭[assegno_funzione] == heap_chiudere_funzione) { heap_chiudere_funzione = assegno_funzione; break; }
        }
    }
    static int 새기억(int Kind_VALORE, int durata_VALORE) {
        if (durata_VALORE < 0) { errore_VALORE("NegativeArraySizeException"); return 0; }
        if (durata_VALORE > heap_VALORE.length - 3) { errore_VALORE("object heap exhausted"); return 0; }
        int 필요수 = durata_VALORE + 2, oggetto_fonti = 0;
        if (필요수 <= heap_VALORE.length - heap_chiudere_funzione) { oggetto_fonti = heap_chiudere_funzione; heap_chiudere_funzione += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < heap_chiudere_funzione; 읽는자리 += 힙폭[읽는자리]) if (heap_VALORE[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { oggetto_fonti = 읽는자리; break; }
            if (oggetto_fonti != 0) {
                int 남은길이 = 힙폭[oggetto_fonti] - 필요수;
                if (남은길이 >= 2) { 힙폭[oggetto_fonti + 필요수] = 남은길이; heap_VALORE[oggetto_fonti + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= heap_VALORE.length - heap_chiudere_funzione) { oggetto_fonti = heap_chiudere_funzione; heap_chiudere_funzione += 필요수; }
        }
        if (oggetto_fonti == 0) { errore_VALORE("object heap exhausted"); return 0; }
        for (int Loop_INDICE = 0; Loop_INDICE < 필요수; Loop_INDICE++) { heap_VALORE[oggetto_fonti + Loop_INDICE] = 0; heap_fonti[oggetto_fonti + Loop_INDICE] = 0; 힙폭[oggetto_fonti + Loop_INDICE] = 0; }
        elemento_di_matrice[oggetto_fonti] = 0;
        힙폭[oggetto_fonti] = 필요수; heap_VALORE[oggetto_fonti] = Kind_VALORE; heap_VALORE[oggetto_fonti + 1] = durata_VALORE; proteggere_VALORE(oggetto_fonti); return oggetto_fonti;
    }
    static int eccezione_Corso(String nome_costante) {
        if (자바도구.같음(nome_costante, "java/lang/Throwable")) return 1;
        if (자바도구.같음(nome_costante, "java/lang/Exception")) return 2;
        if (자바도구.같음(nome_costante, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(nome_costante, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(nome_costante, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(nome_costante, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(nome_costante, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(nome_costante, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(nome_costante, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(nome_costante, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(nome_costante, "java/io/IOException")) return 11;
        if (자바도구.같음(nome_costante, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(nome_costante, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(nome_costante, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(nome_costante, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int eccezione_costante(int Nome) {
        for (int Loop_INDICE = 1; Loop_INDICE <= 41; Loop_INDICE++) if (Word_SMS(Nome, eccezione_nome(Loop_INDICE))) return Loop_INDICE;
        return 0;
    }
    static String eccezione_nome(int account_VALORE) {
        if (account_VALORE == 40) return "java/lang/InterruptedException";
        if (account_VALORE == 41) return "Italiano/nativo/대기중단예외";
        if (account_VALORE == 39) return "java/net/SocketException";
        if (account_VALORE == 20) return "Italiano/nativo/eccezione";
        if (account_VALORE == 21) return "Italiano/nativo/esecuzione_eccezione";
        if (account_VALORE == 22) return "Italiano/nativo/I_O_eccezione";
        if (account_VALORE == 23) return "Italiano/nativo/aspetta_TIMEOUT_eccezione";
        if (account_VALORE == 24) return "Italiano/nativo/e_mail_CERCA_eccezione";
        if (account_VALORE == 25) return "Italiano/nativo/파일없음예외";
        if (account_VALORE == 26) return "Italiano/nativo/comunicazione_eccezione";
        if (account_VALORE == 27) return "Italiano/nativo/non_valida_argomento_eccezione";
        if (account_VALORE == 28) return "Italiano/nativo/numero_formato_errore";
        if (account_VALORE == 29) return "Italiano/nativo/범위예외";
        if (account_VALORE == 30) return "Italiano/nativo/배열범위예외";
        if (account_VALORE == 31) return "Italiano/nativo/문자열범위예외";
        if (account_VALORE == 32) return "Italiano/nativo/riferimento_Null_eccezione";
        if (account_VALORE == 33) return "Italiano/nativo/aritmetico_errore";
        if (account_VALORE == 34) return "Italiano/nativo/Stato_eccezione";
        if (account_VALORE == 35) return "Italiano/nativo/TIPO_cast_eccezione";
        if (account_VALORE == 36) return "Italiano/nativo/negativo_array_ridimensionare_errore";
        if (account_VALORE == 37) return "Italiano/nativo/array_Store_errore";
        if (account_VALORE == 38) return "Italiano/nativo/thread_Stato_eccezione";
        if (account_VALORE == 1) return "java/lang/Throwable"; if (account_VALORE == 2) return "java/lang/Exception";
        if (account_VALORE == 3) return "java/lang/RuntimeException"; if (account_VALORE == 4) return "java/lang/ArithmeticException";
        if (account_VALORE == 5) return "java/lang/NullPointerException"; if (account_VALORE == 6) return "java/lang/IndexOutOfBoundsException";
        if (account_VALORE == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (account_VALORE == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (account_VALORE == 9) return "java/lang/IllegalArgumentException"; if (account_VALORE == 10) return "java/lang/NumberFormatException";
        if (account_VALORE == 11) return "java/io/IOException"; if (account_VALORE == 12) return "java/io/FileNotFoundException";
        if (account_VALORE == 17) return "java/lang/ArrayStoreException";
        if (account_VALORE == 18) return "java/net/UnknownHostException";
        if (account_VALORE == 19) return "java/net/SocketTimeoutException";
        if (account_VALORE == 16) return "java/lang/IllegalThreadStateException";
        if (account_VALORE == 13) return "java/lang/IllegalStateException"; if (account_VALORE == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int eccezione_padre(int account_VALORE) {
        if (account_VALORE == 40) return 2;
        if (account_VALORE == 41) return 40;
        if (account_VALORE == 39) return 11;
        if (account_VALORE == 1) return 0;
        if (account_VALORE == 2) return 1;
        if (account_VALORE == 3) return 2;
        if (account_VALORE == 4) return 3;
        if (account_VALORE == 5) return 3;
        if (account_VALORE == 6) return 3;
        if (account_VALORE == 7) return 6;
        if (account_VALORE == 8) return 6;
        if (account_VALORE == 9) return 3;
        if (account_VALORE == 10) return 9;
        if (account_VALORE == 11) return 2;
        if (account_VALORE == 12) return 11;
        if (account_VALORE == 13) return 3;
        if (account_VALORE == 14) return 3;
        if (account_VALORE == 15) return 3;
        if (account_VALORE == 16) return 9;
        if (account_VALORE == 17) return 3;
        if (account_VALORE == 18) return 11;
        if (account_VALORE == 19) return 11;
        if (account_VALORE == 20) return 2;
        if (account_VALORE == 21) return 3;
        if (account_VALORE == 22) return 11;
        if (account_VALORE == 23) return 22;
        if (account_VALORE == 24) return 22;
        if (account_VALORE == 25) return 22;
        if (account_VALORE == 26) return 22;
        if (account_VALORE == 27) return 9;
        if (account_VALORE == 28) return 27;
        if (account_VALORE == 29) return 6;
        if (account_VALORE == 30) return 29;
        if (account_VALORE == 31) return 29;
        if (account_VALORE == 32) return 5;
        if (account_VALORE == 33) return 4;
        if (account_VALORE == 34) return 13;
        if (account_VALORE == 35) return 14;
        if (account_VALORE == 36) return 15;
        if (account_VALORE == 37) return 17;
        if (account_VALORE == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int valore_effettivo, int 요구값) {
        for (int 깊이 = 0; valore_effettivo != 0 && 깊이 < 16; 깊이++, valore_effettivo = eccezione_padre(valore_effettivo))
            if (valore_effettivo == 요구값) return true;
        return false;
    }
    static void 예외던짐(int account_VALORE, String README_fonti) {
        int oggetto_fonti = 새기억(9, 2); if (errore) return;
        heap_VALORE[oggetto_fonti + 2] = account_VALORE; heap_VALORE[oggetto_fonti + 3] = host_carattere(README_fonti); heap_fonti[oggetto_fonti + 3] = 1;
        던진객체 = oggetto_fonti; errore = true;
    }
    static boolean collegamento_movimenti_oggetto(int oggetto_fonti, int Nome) {
        if (oggetto_fonti == 0) return true;
        if (!reparto_IT_valido_oggetto(oggetto_fonti)) return false;
        int area_CODICE = heap_VALORE[oggetto_fonti];
        if (Word_SMS(Nome, "java/lang/Object")) return true;
        if (area_CODICE >= 32) return 종포함(area_CODICE - 32, Nome);
        if (area_CODICE == 9) { int target_e_mail = eccezione_costante(Nome); return target_e_mail != 0 && 예외포함(heap_VALORE[oggetto_fonti + 2], target_e_mail); }
        if (area_CODICE == 1) return Word_SMS(Nome, "java/lang/String") || Word_SMS(Nome, "java/lang/CharSequence");
        if (area_CODICE == 4) return Word_SMS(Nome, "java/lang/StringBuilder") || Word_SMS(Nome, "java/lang/CharSequence");
        if (area_CODICE == 10) return Word_SMS(Nome, "java/util/ArrayList") || Word_SMS(Nome, "java/util/List");
        if (area_CODICE == 11) return Word_SMS(Nome, "java/util/HashMap") || Word_SMS(Nome, "java/util/Map");
        if (area_CODICE == 12) return Word_SMS(Nome, "java/lang/Integer") || Word_SMS(Nome, "java/lang/Number");
        if (area_CODICE >= 24 && area_CODICE <= 28 && heap_VALORE[oggetto_fonti + 13] != 0) return 한국어화면종(Nome) == area_CODICE || Word_SMS(Nome, "Italiano/nativo/schermata_elemento");
        if (area_CODICE >= 24 && area_CODICE <= 28) return (한국어화면종(Nome) == 0 && schermata_Corso(Nome) == area_CODICE) || Word_SMS(Nome, "java/awt/Component") || Word_SMS(Nome, "java/awt/Container") || Word_SMS(Nome, "javax/swing/JComponent");
        if (area_CODICE == 29) return Word_SMS(Nome, heap_VALORE[oggetto_fonti + 3] != 0 ? "Italiano/nativo/Action_informativa" : "java/awt/event/ActionEvent");
        if (area_CODICE == 30) return Word_SMS(Nome, "java/awt/FlowLayout") || Word_SMS(Nome, "java/awt/LayoutManager");
        if (area_CODICE == 17) return Word_SMS(Nome, "java/net/Socket");
        if (area_CODICE == 18) return Word_SMS(Nome, "java/net/ServerSocket");
        if (area_CODICE == 19) return Word_SMS(Nome, heap_VALORE[oggetto_fonti + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (area_CODICE == 14) return Word_SMS(Nome, "java/net/InetAddress");
        if (area_CODICE == 15) return Word_SMS(Nome, "java/net/DatagramSocket");
        if (area_CODICE == 16) return Word_SMS(Nome, "java/net/DatagramPacket");
        if (area_CODICE == 13) return Word_SMS(Nome, heap_VALORE[oggetto_fonti + 3] != 0 ? "Italiano/nativo/esecutoreAsincrono" : "java/lang/Thread");
        if (area_CODICE == 2) return Word_SMS(Nome, "[I"); if (area_CODICE == 20) return Word_SMS(Nome, "[B"); if (area_CODICE == 21) return Word_SMS(Nome, "[Z");
        if (area_CODICE == 22) return Word_SMS(Nome, "[C"); if (area_CODICE == 23) return Word_SMS(Nome, "[S");
        if (area_CODICE != 3) return false;
        if (Word_SMS(Nome, "[Ljava/lang/Object;")) return true;
        int componente = elemento_di_matrice[oggetto_fonti];
        if (componente == -1) return Word_SMS(Nome, "[Ljava/lang/String;") || Word_SMS(Nome, "[Ljava/lang/CharSequence;");
        if (componente == 0) return false;
        if (배열종비교(componente, Nome)) return true;
        if ((Word_SMS(componente, "java/lang/String") || Word_SMS(componente, "java/lang/StringBuilder")) && Word_SMS(Nome, "[Ljava/lang/CharSequence;")) return true;
        for (int Loop_INDICE = 0; Loop_INDICE < Corso_definizione_CONTA_NUMERI; Loop_INDICE++) if (collegamento_movimenti_Word(Corso_definizione_nome[Loop_INDICE], componente)) {
            for (int punto_di_codice = Loop_INDICE, 중첩깊이 = 0; punto_di_codice >= 0 && 중첩깊이 < 16; 중첩깊이++, punto_di_codice = padre_Corso(punto_di_codice)) {
                if (배열종비교(Corso_definizione_padre[punto_di_codice], Nome)) return true;
                for (int inner_funzione = 0; inner_funzione < Corso_interfaccia_CONTA_NUMERI[punto_di_codice]; inner_funzione++) if (배열종비교(Corso_interfaccia[punto_di_codice * 16 + inner_funzione], Nome)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int nome_costante, int descrittore) {
        int assegno_funzione = 상가[descrittore], voce_CONTA_NUMERI = costante_SECONDO_VALORE[descrittore];
        if (nome_costante == 0 || voce_CONTA_NUMERI < 4 || file[assegno_funzione] != '[' || file[assegno_funzione + 1] != 'L' || file[assegno_funzione + voce_CONTA_NUMERI - 1] != ';' || costante_SECONDO_VALORE[nome_costante] != voce_CONTA_NUMERI - 3) return false;
        for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI - 3; Loop_INDICE++) if (file[상가[nome_costante] + Loop_INDICE] != file[assegno_funzione + 2 + Loop_INDICE]) return false;
        return true;
    }
    static void handle_eccezione() {
        if (던진객체 == 0) return;
        errore = false;
        while (frame_INDICE >= Regolari_thread * 32) {
            int File_INDICE = frame_metodo[frame_INDICE], 읽는자리 = frame_istruzione[frame_INDICE];
            for (int Loop_INDICE = 0; Loop_INDICE < 잡기수; Loop_INDICE++) if (잡기함수[Loop_INDICE] == File_INDICE && 읽는자리 >= 잡기시작[Loop_INDICE] && 읽는자리 < 잡기끝[Loop_INDICE]
                && (잡기종[Loop_INDICE] == 0 || collegamento_movimenti_oggetto(던진객체, 잡기종[Loop_INDICE]))) {
                frame_funzione[frame_INDICE] = 잡기위치[Loop_INDICE]; frame_Pila[frame_INDICE] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (inizializzare_frame[frame_INDICE] != 0) Corso_definizione_Stato[inizializzare_frame[frame_INDICE] - 1] = 3;
            if (frame_blocco[frame_INDICE] != 0) { release_blocco(frame_blocco[frame_INDICE]); frame_blocco[frame_INDICE] = 0; }
            frame_INDICE--;
        }
        spazio_utente.Scrittura("Uncaught ");
        if (heap_VALORE[던진객체] == 9) { spazio_utente.Scrittura(eccezione_nome(heap_VALORE[던진객체 + 2])); spazio_utente.Scrittura(": "); scrivere_SMS(heap_VALORE[던진객체 + 3]); }
        else spazio_utente.Scrittura("user exception");
        spazio_utente.scrivere_carattere_VALORE(10); 던진객체 = 0; errore = true;
    }
    // 이 JVM의 operando_Pila 항목은 Regolari_articolo category-1(int/reference)만 허용한다.
    static void Pila_istruzione(int comando_CODICE) {
        int 첫값 = 빼기(0), 첫형식 = tipo_restituito;
        if (comando_CODICE == 87) return;
        if (comando_CODICE == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int byte_dati = 빼기(0), SECONDO_formato = tipo_restituito;
        if (comando_CODICE == 88) return;
        if (comando_CODICE == 90) { 넣기(첫값, 첫형식); 넣기(byte_dati, SECONDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CODICE == 92) { 넣기(byte_dati, SECONDO_formato); 넣기(첫값, 첫형식); 넣기(byte_dati, SECONDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CODICE == 95) { 넣기(첫값, 첫형식); 넣기(byte_dati, SECONDO_formato); return; }
        int punto_di_codice = 빼기(0), 셋째형식 = tipo_restituito;
        if (comando_CODICE == 91) { 넣기(첫값, 첫형식); 넣기(punto_di_codice, 셋째형식); 넣기(byte_dati, SECONDO_formato); 넣기(첫값, 첫형식); return; }
        if (comando_CODICE == 93) { 넣기(byte_dati, SECONDO_formato); 넣기(첫값, 첫형식); 넣기(punto_di_codice, 셋째형식); 넣기(byte_dati, SECONDO_formato); 넣기(첫값, 첫형식); return; }
        int finale_VALORE = 빼기(0), 넷째형식 = tipo_restituito;
        넣기(byte_dati, SECONDO_formato); 넣기(첫값, 첫형식); 넣기(finale_VALORE, 넷째형식); 넣기(punto_di_codice, 셋째형식); 넣기(byte_dati, SECONDO_formato); 넣기(첫값, 첫형식);
    }
    static void 새객체(int nome_costante, int 시작점) {
        int area_CODICE = 0, valido_durata = 0, eccezione_fonti = eccezione_costante(nome_costante);
        if (Word_SMS(nome_costante, "java/lang/StringBuilder")) { area_CODICE = 4; valido_durata = 1; }
        if (Word_SMS(nome_costante, "java/io/FileInputStream")) { area_CODICE = 5; valido_durata = 2; }
        if (Word_SMS(nome_costante, "java/io/FileOutputStream")) { area_CODICE = 6; valido_durata = 2; }
        if (eccezione_fonti != 0) { area_CODICE = 9; valido_durata = 2; }
        if (Word_SMS(nome_costante, "java/util/ArrayList")) { area_CODICE = 10; valido_durata = 2; }
        if (Word_SMS(nome_costante, "java/util/HashMap")) { area_CODICE = 11; valido_durata = 2; }
        if (Word_SMS(nome_costante, "java/lang/Integer")) { area_CODICE = 12; valido_durata = 1; }
        if (Word_SMS(nome_costante, "java/net/Socket")) { area_CODICE = 17; valido_durata = 5; }
        if (Word_SMS(nome_costante, "java/net/ServerSocket")) { area_CODICE = 18; valido_durata = 5; }
        if (Word_SMS(nome_costante, "java/net/DatagramSocket")) { area_CODICE = 15; valido_durata = 3; }
        if (Word_SMS(nome_costante, "java/net/DatagramPacket")) { area_CODICE = 16; valido_durata = 4; }
        if (Word_SMS(nome_costante, "java/lang/Thread") || Word_SMS(nome_costante, "Italiano/nativo/esecutoreAsincrono")) { area_CODICE = 13; valido_durata = 2; }
        if (Word_SMS(nome_costante, "java/lang/Object")) { area_CODICE = 8; }
        if (area_CODICE == 0 && schermata_Corso(nome_costante) != 0) { area_CODICE = schermata_Corso(nome_costante); valido_durata = 12; }
        if (area_CODICE == 0) {
            int punto_di_codice = TROVA_Corso_definizione(nome_costante); if (punto_di_codice < 0 || errore || !inizializza(punto_di_codice, 시작점)) return;
            area_CODICE = 32 + punto_di_codice; valido_durata = Corso_slot_CONTA_NUMERI[punto_di_codice];
        }
        int oggetto_fonti = allocare_Memoria(area_CODICE, valido_durata); if (errore) return;
        if (area_CODICE == 13 && Word_SMS(nome_costante, "Italiano/nativo/esecutoreAsincrono")) heap_VALORE[oggetto_fonti + 3] = 1;
        if (area_CODICE >= 24 && area_CODICE <= 28 && 한국어화면종(nome_costante) != 0) heap_VALORE[oggetto_fonti + 13] = 1;
        if (area_CODICE == 5 || area_CODICE == 6 || area_CODICE == 15 || area_CODICE == 17 || area_CODICE == 18) heap_VALORE[oggetto_fonti + 2] = -1;
        if (area_CODICE == 9) heap_VALORE[oggetto_fonti + 2] = eccezione_fonti;
        넣기(oggetto_fonti, 2);
    }
    static boolean 값같음(int 첫값, int byte_dati) {
        if (첫값 == byte_dati) return true;
        if (첫값 == 0 || byte_dati == 0 || 첫값 < 0 || byte_dati < 0 || 첫값 >= heap_chiudere_funzione || byte_dati >= heap_chiudere_funzione) return false;
        if (heap_VALORE[첫값] == 1 && heap_VALORE[byte_dati] == 1) return testi_uguali(첫값, byte_dati, false);
        return heap_VALORE[첫값] == 12 && heap_VALORE[byte_dati] == 12 && heap_VALORE[첫값 + 2] == heap_VALORE[byte_dati + 2];
    }
    static int SMS_blocco(int oggetto_fonti, int START_funzione, int chiudere_funzione) {
        if (!oggetto_VALORE(oggetto_fonti, 1)) return 0;
        if (START_funzione < 0 || chiudere_funzione < START_funzione || chiudere_funzione > heap_VALORE[oggetto_fonti + 1]) { errore_VALORE("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = allocare_Memoria(1, chiudere_funzione - START_funzione); if (errore) return 0;
        for (int Loop_INDICE = START_funzione; Loop_INDICE < chiudere_funzione; Loop_INDICE++) heap_VALORE[반환값 + 2 + Loop_INDICE - START_funzione] = heap_VALORE[oggetto_fonti + 2 + Loop_INDICE];
        return 반환값;
    }
    static int join_SMS(int 첫값, int byte_dati) {
        if (!oggetto_VALORE(첫값, 1) || !oggetto_VALORE(byte_dati, 1)) return 0;
        int voce_CONTA_NUMERI = heap_VALORE[첫값 + 1], metodo_INDICE = heap_VALORE[byte_dati + 1], 반환값 = allocare_Memoria(1, voce_CONTA_NUMERI + metodo_INDICE); if (errore) return 0;
        for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) heap_VALORE[반환값 + 2 + Loop_INDICE] = heap_VALORE[첫값 + 2 + Loop_INDICE];
        for (int Loop_INDICE = 0; Loop_INDICE < metodo_INDICE; Loop_INDICE++) heap_VALORE[반환값 + 2 + voce_CONTA_NUMERI + Loop_INDICE] = heap_VALORE[byte_dati + 2 + Loop_INDICE];
        return 반환값;
    }
    static boolean 기본호출(int proprietario, int nome_costante, int descrittore_costante, int comando_CODICE) {
        if (Word_SMS(proprietario, "Italiano/nativo/실행인수") && comando_CODICE == 184) {
            if (Word_SMS(nome_costante, "articolo_CONTA_NUMERI") && Word_SMS(descrittore_costante, "()I")) { 넣기(spazio_utente.인수개수() - 1, 1); return true; }
            if (Word_SMS(nome_costante, "testo") && Word_SMS(descrittore_costante, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= spazio_utente.인수개수() - 1) 예외던짐(29, "Esegui_comando argomenti 범위를 벗어났습니다");
                else 넣기(host_carattere(spazio_utente.argomenti(순번 + 1)), 2);
                return true;
            }
            errore_VALORE("지원하지 않는 Italiano Esegui_comando argomenti 호출"); return true;
        }
        if (Word_SMS(proprietario, "Italiano/nativo/esecutoreAsincrono")) { Processi_thread(nome_costante, descrittore_costante, comando_CODICE, true); return true; }
        if (한국어화면소유(proprietario)) { 한국어화면호출(proprietario, nome_costante, descrittore_costante, comando_CODICE); return true; }
        if (schermata_proprietario(proprietario)) { 화면호출(proprietario, nome_costante, descrittore_costante, comando_CODICE); return true; }
        if (Word_SMS(proprietario, "java/net/Socket") || Word_SMS(proprietario, "java/net/ServerSocket") || Word_SMS(proprietario, "java/io/InputStream") || Word_SMS(proprietario, "java/io/OutputStream")) { 흐름호출(proprietario, nome_costante, descrittore_costante, comando_CODICE); return true; }
        if (Word_SMS(proprietario, "Italiano/nativo/kernel_VALORE") && comando_CODICE == 184) {
            if (Word_SMS(nome_costante, "화면너비") && Word_SMS(descrittore_costante, "()I")) { 넣기(spazio_utente.화면너비(), 1); return true; }
            if (Word_SMS(nome_costante, "schermata_altezza") && Word_SMS(descrittore_costante, "()I")) { 넣기(spazio_utente.schermata_altezza(), 1); return true; }
            if (Word_SMS(nome_costante, "밀리초") && Word_SMS(descrittore_costante, "()I")) { 넣기(spazio_utente.밀리초(), 1); return true; }
            if (Word_SMS(nome_costante, "그림대기") && Word_SMS(descrittore_costante, "()I")) { 넣기(spazio_utente.그림대기(), 1); return true; }
            if (Word_SMS(nome_costante, "rettangolo") && Word_SMS(descrittore_costante, "(IIIII)I")) { int 색상 = 빼기(1), altezza_VALORE = 빼기(1), 너비 = 빼기(1), Y_coordinata = 빼기(1), coordinata_x = 빼기(1); 넣기(spazio_utente.rettangolo(coordinata_x, Y_coordinata, 너비, altezza_VALORE, 색상), 1); return true; }
        }
        if (Word_SMS(proprietario, "java/net/InetAddress") || Word_SMS(proprietario, "java/net/DatagramPacket") || Word_SMS(proprietario, "java/net/DatagramSocket")) { 통신호출(proprietario, nome_costante, descrittore_costante, comando_CODICE); return true; }
        if (Word_SMS(proprietario, "java/lang/Thread")) { 가닥호출(nome_costante, descrittore_costante, comando_CODICE); return true; }
        if (Word_SMS(proprietario, "java/lang/Object")) {
            if (Word_SMS(nome_costante, "<init>") && Word_SMS(descrittore_costante, "()V") && comando_CODICE == 183) { reparto_IT_valido_oggetto(빼기(2)); return true; }
            if (Word_SMS(nome_costante, "equals") && Word_SMS(descrittore_costante, "(Ljava/lang/Object;)Z")) { int byte_dati = 빼기(2), 첫값 = 빼기(2); if (reparto_IT_valido_oggetto(첫값)) 넣기(첫값 == byte_dati ? 1 : 0, 1); return true; }
        }
        if (eccezione_costante(proprietario) != 0) {
            if (Word_SMS(nome_costante, "<init>") && comando_CODICE == 183 && (Word_SMS(descrittore_costante, "()V") || Word_SMS(descrittore_costante, "(Ljava/lang/String;)V"))) {
                int prompt = Word_SMS(descrittore_costante, "()V") ? 0 : 빼기(2), oggetto_fonti = 빼기(2);
                if (oggetto_VALORE(oggetto_fonti, 9)) { heap_VALORE[oggetto_fonti + 3] = prompt; heap_fonti[oggetto_fonti + 3] = 1; } return true;
            }
            if ((Word_SMS(nome_costante, "getMessage") || Word_SMS(nome_costante, "설명")) && Word_SMS(descrittore_costante, "()Ljava/lang/String;")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, 9)) 넣기(heap_VALORE[oggetto_fonti + 3], 2); return true; }
        }
        if (Word_SMS(proprietario, "java/lang/String")) {
            if (comando_CODICE == 182 && Word_SMS(nome_costante, "getBytes") && (Word_SMS(descrittore_costante, "()[B") || Word_SMS(descrittore_costante, "(Ljava/lang/String;)[B"))) {
                int Codifica_nome = Word_SMS(descrittore_costante, "()[B") ? 0 : 빼기(2), oggetto_fonti = 빼기(2);
                if (!oggetto_VALORE(oggetto_fonti, 1)) return true;
                if (Codifica_nome != 0 && !testi_uguali(Codifica_nome, host_carattere("UTF-8"), false) && !testi_uguali(Codifica_nome, host_carattere("UTF8"), false) && !testi_uguali(Codifica_nome, host_carattere("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int voce_CONTA_NUMERI = heap_VALORE[oggetto_fonti + 1], 반환값 = allocare_Memoria(20, voce_CONTA_NUMERI * 3), 사용수 = 0; if (errore) return true;
                for (int inner_funzione = 0; inner_funzione < voce_CONTA_NUMERI; inner_funzione++) {
                    int punto_di_codice = heap_VALORE[oggetto_fonti + 2 + inner_funzione];
                    if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdbff && inner_funzione + 1 < voce_CONTA_NUMERI && heap_VALORE[oggetto_fonti + 3 + inner_funzione] >= 0xdc00 && heap_VALORE[oggetto_fonti + 3 + inner_funzione] <= 0xdfff) punto_di_codice = 0x10000 + ((punto_di_codice - 0xd800) << 10) + heap_VALORE[oggetto_fonti + 2 + ++inner_funzione] - 0xdc00;
                    else if (punto_di_codice >= 0xd800 && punto_di_codice <= 0xdfff) punto_di_codice = '?';
                    if (punto_di_codice < 128) heap_VALORE[반환값 + 2 + 사용수++] = punto_di_codice;
                    else { int byte_CONTA_NUMERI = punto_di_codice < 2048 ? 2 : punto_di_codice < 65536 ? 3 : 4; heap_VALORE[반환값 + 2 + 사용수++] = (byte)((byte_CONTA_NUMERI == 2 ? 192 : byte_CONTA_NUMERI == 3 ? 224 : 240) | punto_di_codice >> (6 * (byte_CONTA_NUMERI - 1))); for (int Confronto_funzione = byte_CONTA_NUMERI - 1; Confronto_funzione > 0; Confronto_funzione--) heap_VALORE[반환값 + 2 + 사용수++] = (byte)(128 | punto_di_codice >> (6 * (Confronto_funzione - 1)) & 63); }
                }
                heap_VALORE[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "valueOf") && Word_SMS(descrittore_costante, "(I)Ljava/lang/String;")) { 넣기(cifra_carattere(빼기(1)), 2); return true; }
            if (comando_CODICE != 182) return false;
            if (Word_SMS(nome_costante, "equals") && Word_SMS(descrittore_costante, "(Ljava/lang/Object;)Z")) { int byte_dati = 빼기(2), 첫값 = 빼기(2); if (oggetto_VALORE(첫값, 1)) 넣기(testi_uguali(첫값, byte_dati, false) ? 1 : 0, 1); return true; }
            if (Word_SMS(nome_costante, "isEmpty") && Word_SMS(descrittore_costante, "()Z")) { int 첫값 = 빼기(2); if (oggetto_VALORE(첫값, 1)) 넣기(heap_VALORE[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Word_SMS(nome_costante, "substring") && (Word_SMS(descrittore_costante, "(I)Ljava/lang/String;") || Word_SMS(descrittore_costante, "(II)Ljava/lang/String;"))) {
                boolean SECONDO_VALORE = Word_SMS(descrittore_costante, "(II)Ljava/lang/String;"); int chiudere_funzione = SECONDO_VALORE ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (oggetto_VALORE(첫값, 1)) 넣기(SMS_blocco(첫값, 시작점, SECONDO_VALORE ? chiudere_funzione : heap_VALORE[첫값 + 1]), 2); return true;
            }
            if (Word_SMS(nome_costante, "concat") && Word_SMS(descrittore_costante, "(Ljava/lang/String;)Ljava/lang/String;")) { int byte_dati = 빼기(2), 첫값 = 빼기(2); 넣기(join_SMS(첫값, byte_dati), 2); return true; }
            if (Word_SMS(nome_costante, "hashCode") && Word_SMS(descrittore_costante, "()I")) { int 첫값 = 빼기(2), hash_VALORE = 0; if (oggetto_VALORE(첫값, 1)) { for (int Loop_INDICE = 0; Loop_INDICE < heap_VALORE[첫값 + 1]; Loop_INDICE++) hash_VALORE = hash_VALORE * 31 + heap_VALORE[첫값 + 2 + Loop_INDICE]; 넣기(hash_VALORE, 1); } return true; }
            if (Word_SMS(nome_costante, "toString") && Word_SMS(descrittore_costante, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (oggetto_VALORE(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Word_SMS(proprietario, "java/lang/Integer")) {
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "valueOf") && Word_SMS(descrittore_costante, "(I)Ljava/lang/Integer;")) { int dati_VALORE = 빼기(1), oggetto_fonti = dati_VALORE >= -128 && dati_VALORE <= 127 ? Store_intero[dati_VALORE + 128] : 0; if (oggetto_fonti == 0) { oggetto_fonti = allocare_Memoria(12, 1); if (!errore) { heap_VALORE[oggetto_fonti + 2] = dati_VALORE; if (dati_VALORE >= -128 && dati_VALORE <= 127) Store_intero[dati_VALORE + 128] = oggetto_fonti; } } 넣기(oggetto_fonti, 2); return true; }
            if (comando_CODICE == 183 && Word_SMS(nome_costante, "<init>") && Word_SMS(descrittore_costante, "(I)V")) { int dati_VALORE = 빼기(1), oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, 12)) heap_VALORE[oggetto_fonti + 2] = dati_VALORE; return true; }
            if (comando_CODICE == 182 && Word_SMS(nome_costante, "intValue") && Word_SMS(descrittore_costante, "()I")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, 12)) 넣기(heap_VALORE[oggetto_fonti + 2], 1); return true; }
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "toString") && Word_SMS(descrittore_costante, "(I)Ljava/lang/String;")) { 넣기(cifra_carattere(빼기(1)), 2); return true; }
        }
        if (Word_SMS(proprietario, "java/lang/Math") && comando_CODICE == 184) {
            if (Word_SMS(nome_costante, "abs") && Word_SMS(descrittore_costante, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Word_SMS(nome_costante, "min") || Word_SMS(nome_costante, "max")) && Word_SMS(descrittore_costante, "(II)I")) { int byte_dati = 빼기(1), 첫값 = 빼기(1); 넣기(Word_SMS(nome_costante, "min") ? (첫값 < byte_dati ? 첫값 : byte_dati) : (첫값 > byte_dati ? 첫값 : byte_dati), 1); return true; }
        }
        if (Word_SMS(proprietario, "java/lang/System") && comando_CODICE == 184) {
            if (Word_SMS(nome_costante, "gc") && Word_SMS(descrittore_costante, "()V")) { 수거(); return true; }
            if (Word_SMS(nome_costante, "arraycopy") && Word_SMS(descrittore_costante, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int voce_CONTA_NUMERI = 빼기(1), meta_VALORE_INDICE = 빼기(1), byte_dati = 빼기(2), START_funzione = 빼기(1), 첫값 = 빼기(2);
                if (reparto_IT_valido_oggetto(첫값) && reparto_IT_valido_oggetto(byte_dati)) {
                    int area_CODICE = heap_VALORE[첫값];
                    if (heap_VALORE[byte_dati] != area_CODICE || (area_CODICE != 2 && area_CODICE != 3 && (area_CODICE < 20 || area_CODICE > 23))) errore_VALORE("arraycopy type mismatch");
                    else if (voce_CONTA_NUMERI < 0 || START_funzione < 0 || meta_VALORE_INDICE < 0 || START_funzione > heap_VALORE[첫값 + 1] - voce_CONTA_NUMERI || meta_VALORE_INDICE > heap_VALORE[byte_dati + 1] - voce_CONTA_NUMERI) errore_VALORE("ArrayIndexOutOfBoundsException");
                    else if (첫값 == byte_dati && meta_VALORE_INDICE > START_funzione) { for (int Loop_INDICE = voce_CONTA_NUMERI - 1; Loop_INDICE >= 0; Loop_INDICE--) heap_VALORE[byte_dati + 2 + meta_VALORE_INDICE + Loop_INDICE] = heap_VALORE[첫값 + 2 + START_funzione + Loop_INDICE]; }
                    else { for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI && !errore; Loop_INDICE++) { int dati_VALORE = heap_VALORE[첫값 + 2 + START_funzione + Loop_INDICE]; if (area_CODICE != 3 || 배열저장가능(byte_dati, dati_VALORE)) heap_VALORE[byte_dati + 2 + meta_VALORE_INDICE + Loop_INDICE] = dati_VALORE; } }
                }
                return true;
            }
        }
        if (Word_SMS(proprietario, "java/util/ArrayList") || Word_SMS(proprietario, "java/util/List") || Word_SMS(proprietario, "java/util/HashMap") || Word_SMS(proprietario, "java/util/Map")) {
            모음호출(proprietario, nome_costante, descrittore_costante, comando_CODICE); return true;
        }
        return false;
    }
    static void 모음늘리기(int oggetto_fonti, int 필요수) {
        int Indietro_VALORE = heap_VALORE[oggetto_fonti + 2], capacità_dati = Indietro_VALORE == 0 ? 0 : heap_VALORE[Indietro_VALORE + 1];
        if (capacità_dati >= 필요수) return;
        int Avanti_funzione = capacità_dati < 8 ? 8 : capacità_dati * 2; if (Avanti_funzione < 필요수) Avanti_funzione = 필요수;
        int dati_array = allocare_Memoria(3, Avanti_funzione); if (errore) return;
        for (int Loop_INDICE = 0; Loop_INDICE < capacità_dati; Loop_INDICE++) heap_VALORE[dati_array + 2 + Loop_INDICE] = heap_VALORE[Indietro_VALORE + 2 + Loop_INDICE];
        heap_VALORE[oggetto_fonti + 2] = dati_array; heap_fonti[oggetto_fonti + 2] = 1;
    }
    static void 모음호출(int proprietario, int nome_costante, int descrittore_costante, int comando_CODICE) {
        boolean 대응참조 = Word_SMS(proprietario, "java/util/HashMap") || Word_SMS(proprietario, "java/util/Map"); int area_CODICE = 대응참조 ? 11 : 10;
        if (Word_SMS(nome_costante, "<init>") && comando_CODICE == 183 && Word_SMS(descrittore_costante, "()V")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, area_CODICE)) 모음늘리기(oggetto_fonti, 8); return; }
        if (comando_CODICE != 182 && comando_CODICE != 185) { errore_VALORE("invalid collection invocation"); return; }
        if (Word_SMS(nome_costante, "size") && Word_SMS(descrittore_costante, "()I") || Word_SMS(nome_costante, "isEmpty") && Word_SMS(descrittore_costante, "()Z")) {
            int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, area_CODICE)) 넣기(Word_SMS(nome_costante, "size") ? heap_VALORE[oggetto_fonti + 3] : heap_VALORE[oggetto_fonti + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Word_SMS(nome_costante, "clear") && Word_SMS(descrittore_costante, "()V")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, area_CODICE)) { int dati_array = heap_VALORE[oggetto_fonti + 2]; for (int Loop_INDICE = 0; Loop_INDICE < heap_VALORE[dati_array + 1]; Loop_INDICE++) heap_VALORE[dati_array + 2 + Loop_INDICE] = 0; heap_VALORE[oggetto_fonti + 3] = 0; } return; }
        if (!대응참조 && Word_SMS(nome_costante, "add") && Word_SMS(descrittore_costante, "(Ljava/lang/Object;)Z")) {
            int dati_VALORE = 빼기(2), oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 10)) return;
            int voce_CONTA_NUMERI = heap_VALORE[oggetto_fonti + 3]; 모음늘리기(oggetto_fonti, voce_CONTA_NUMERI + 1); if (!errore) { heap_VALORE[heap_VALORE[oggetto_fonti + 2] + 2 + voce_CONTA_NUMERI] = dati_VALORE; heap_VALORE[oggetto_fonti + 3] = voce_CONTA_NUMERI + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Word_SMS(nome_costante, "get") || Word_SMS(nome_costante, "remove")) && Word_SMS(descrittore_costante, "(I)Ljava/lang/Object;") || !대응참조 && Word_SMS(nome_costante, "set") && Word_SMS(descrittore_costante, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean reparto_IT_Assegnato = Word_SMS(nome_costante, "set"); int dati_VALORE = reparto_IT_Assegnato ? 빼기(2) : 0, voce_funzione = 빼기(1), oggetto_fonti = 빼기(2);
            if (!oggetto_VALORE(oggetto_fonti, 10)) return;
            int voce_CONTA_NUMERI = heap_VALORE[oggetto_fonti + 3], dati_array = heap_VALORE[oggetto_fonti + 2];
            if (voce_funzione < 0 || voce_funzione >= voce_CONTA_NUMERI) { 예외던짐(6, "list index"); return; }
            int Indietro_VALORE = heap_VALORE[dati_array + 2 + voce_funzione];
            if (reparto_IT_Assegnato) heap_VALORE[dati_array + 2 + voce_funzione] = dati_VALORE;
            if (Word_SMS(nome_costante, "remove")) { for (int Loop_INDICE = voce_funzione + 1; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) heap_VALORE[dati_array + 1 + Loop_INDICE] = heap_VALORE[dati_array + 2 + Loop_INDICE]; heap_VALORE[dati_array + 1 + voce_CONTA_NUMERI] = 0; heap_VALORE[oggetto_fonti + 3] = voce_CONTA_NUMERI - 1; }
            넣기(Indietro_VALORE, 2); return;
        }
        if (대응참조 && (Word_SMS(nome_costante, "get") || Word_SMS(nome_costante, "remove")) && Word_SMS(descrittore_costante, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nome_costante, "put") && Word_SMS(descrittore_costante, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Word_SMS(nome_costante, "containsKey") && Word_SMS(descrittore_costante, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Word_SMS(nome_costante, "put"), rimuovere = Word_SMS(nome_costante, "remove");
            int dati_VALORE = 넣기여부 ? 빼기(2) : 0, tasto_fonti = 빼기(2), oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 11)) return;
            int voce_CONTA_NUMERI = heap_VALORE[oggetto_fonti + 3], dati_array = heap_VALORE[oggetto_fonti + 2], 찾은여부 = -1;
            for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) if (값같음(tasto_fonti, heap_VALORE[dati_array + 2 + 2 * Loop_INDICE])) { 찾은여부 = Loop_INDICE; break; }
            int Indietro_VALORE = 찾은여부 < 0 ? 0 : heap_VALORE[dati_array + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(oggetto_fonti, (voce_CONTA_NUMERI + 1) * 2); dati_array = heap_VALORE[oggetto_fonti + 2]; 찾은여부 = voce_CONTA_NUMERI; if (!errore) heap_VALORE[oggetto_fonti + 3] = voce_CONTA_NUMERI + 1; }
                if (!errore) { heap_VALORE[dati_array + 2 + 2 * 찾은여부] = tasto_fonti; heap_VALORE[dati_array + 3 + 2 * 찾은여부] = dati_VALORE; }
            }
            if (rimuovere && 찾은여부 >= 0) { for (int Loop_INDICE = 찾은여부 + 1; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) { heap_VALORE[dati_array + 2 * Loop_INDICE] = heap_VALORE[dati_array + 2 + 2 * Loop_INDICE]; heap_VALORE[dati_array + 1 + 2 * Loop_INDICE] = heap_VALORE[dati_array + 3 + 2 * Loop_INDICE]; } heap_VALORE[dati_array + 2 * voce_CONTA_NUMERI] = 0; heap_VALORE[dati_array + 1 + 2 * voce_CONTA_NUMERI] = 0; heap_VALORE[oggetto_fonti + 3] = voce_CONTA_NUMERI - 1; }
            if (Word_SMS(nome_costante, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(Indietro_VALORE, 2);
            return;
        }
        errore_VALORE("unsupported collection method");
    }
    static boolean 잠금얻기(int oggetto_fonti) {
        if (!reparto_IT_valido_oggetto(oggetto_fonti)) return false;
        if (잠금깊이[oggetto_fonti] != 0 && blocco_proprietario[oggetto_fonti] != Regolari_thread + 1) { richiesta_di_modifica = true; return false; }
        blocco_proprietario[oggetto_fonti] = Regolari_thread + 1; 잠금깊이[oggetto_fonti]++; return true;
    }
    static void release_blocco(int oggetto_fonti) {
        if (!reparto_IT_valido_oggetto(oggetto_fonti)) return;
        if (잠금깊이[oggetto_fonti] == 0 || blocco_proprietario[oggetto_fonti] != Regolari_thread + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[oggetto_fonti] == 0) blocco_proprietario[oggetto_fonti] = 0;
    }
    static boolean SWITCH_thread() {
        thread_frame[Regolari_thread] = frame_INDICE;
        if (frame_INDICE < Regolari_thread * 32) thread_Stato[Regolari_thread] = 3;
        for (int Loop_INDICE = 0; Loop_INDICE < Conteggio_dei_thread; Loop_INDICE++) if (thread_Stato[Loop_INDICE] == 2 && thread_Stato[가닥대기[Loop_INDICE]] == 3) thread_Stato[Loop_INDICE] = 1;
        for (int Loop_INDICE = 1; Loop_INDICE <= Conteggio_dei_thread; Loop_INDICE++) {
            int Avanti_funzione = (Regolari_thread + Loop_INDICE) % Conteggio_dei_thread;
            if (thread_Stato[Avanti_funzione] == 1) { Regolari_thread = Avanti_funzione; frame_INDICE = thread_frame[Avanti_funzione]; richiesta_di_modifica = false; return true; }
        }
        for (int Loop_INDICE = 0; Loop_INDICE < Conteggio_dei_thread; Loop_INDICE++) if (thread_Stato[Loop_INDICE] != 3) { errore_VALORE("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int nome_costante, int descrittore_costante, int comando_CODICE) { Processi_thread(nome_costante, descrittore_costante, comando_CODICE, false); }
    static void Processi_thread(int nome_costante, int descrittore_costante, int comando_CODICE, boolean Italiano) {
        if (comando_CODICE == 184 && Word_SMS(nome_costante, Italiano ? "REND_task" : "yield") && Word_SMS(descrittore_costante, "()V")) { richiesta_di_modifica = true; return; }
        if (comando_CODICE == 184 && Word_SMS(nome_costante, "currentThread") && Word_SMS(descrittore_costante, "()Ljava/lang/Thread;")) { 넣기(thread_oggetto[Regolari_thread], 2); return; }
        if (comando_CODICE == 183 && Word_SMS(nome_costante, "<init>") && (Word_SMS(descrittore_costante, "()V") || Word_SMS(descrittore_costante, Italiano ? "(LItaliano/nativo/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int target_e_mail = Word_SMS(descrittore_costante, "()V") ? 0 : 빼기(2), oggetto_fonti = 빼기(2);
            if (!reparto_IT_valido_oggetto(oggetto_fonti)) return;
            if (heap_VALORE[oggetto_fonti] == 13) { heap_VALORE[oggetto_fonti + 2] = target_e_mail; heap_fonti[oggetto_fonti + 2] = 1; }
            else if (target_e_mail != 0) errore_VALORE("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (comando_CODICE == 182 && (Word_SMS(nome_costante, Italiano ? "START_task" : "start") || Word_SMS(nome_costante, Italiano ? "기다리기" : "join")) && Word_SMS(descrittore_costante, "()V") || comando_CODICE == 182 && Word_SMS(nome_costante, Italiano ? "살아있는가" : "isAlive") && Word_SMS(descrittore_costante, "()Z")) {
            int oggetto_fonti = 빼기(2); if (!reparto_IT_valido_oggetto(oggetto_fonti)) return;
            int account_VALORE = -1; for (int Loop_INDICE = 0; Loop_INDICE < Conteggio_dei_thread; Loop_INDICE++) if (thread_oggetto[Loop_INDICE] == oggetto_fonti) account_VALORE = Loop_INDICE;
            if (Word_SMS(nome_costante, Italiano ? "살아있는가" : "isAlive")) { 넣기(account_VALORE >= 0 && thread_Stato[account_VALORE] != 3 ? 1 : 0, 1); return; }
            if (Word_SMS(nome_costante, Italiano ? "기다리기" : "join")) { if (account_VALORE >= 0 && thread_Stato[account_VALORE] != 3) { 가닥대기[Regolari_thread] = account_VALORE; thread_Stato[Regolari_thread] = 2; richiesta_di_modifica = true; } return; }
            if (account_VALORE >= 0) { 예외던짐(Italiano ? 38 : 16, "thread already started"); return; }
            if (Conteggio_dei_thread == 4) { errore_VALORE("thread limit (4 including main)"); return; }
            int target_e_mail = heap_VALORE[oggetto_fonti] == 13 ? heap_VALORE[oggetto_fonti + 2] : oggetto_fonti;
            int File_INDICE = target_e_mail > 0 && heap_VALORE[target_e_mail] >= 32 ? nome_metodo(heap_VALORE[target_e_mail] - 32, Italiano ? "Esegui" : "run", "()V") : -1;
            if (target_e_mail != 0 && File_INDICE < 0) { errore_VALORE("Runnable.run required"); return; }
            account_VALORE = Conteggio_dei_thread++; thread_oggetto[account_VALORE] = oggetto_fonti; thread_target[account_VALORE] = target_e_mail;
            int frame = account_VALORE * 32; thread_frame[account_VALORE] = File_INDICE < 0 ? frame - 1 : frame; thread_Stato[account_VALORE] = File_INDICE < 0 ? 3 : 1;
            if (File_INDICE >= 0) { frame_metodo[frame] = File_INDICE; frame_funzione[frame] = metodo_START[File_INDICE]; locale_VALORE[frame * 128] = target_e_mail; locale_TIPO[frame * 128] = 2; }
            return;
        }
        errore_VALORE("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], e_mail_SMS = new int[16];
    static int locale_e_mail() { return e_mail_oggetto(0x7f000001); }
    static int e_mail_oggetto(int VALORE) { int oggetto_fonti = allocare_Memoria(14, 1); if (!errore) heap_VALORE[oggetto_fonti + 2] = VALORE; return oggetto_fonti; }
    static int 주소해독(int oggetto_fonti) {
        if (oggetto_fonti == 0 || testi_uguali(oggetto_fonti, host_carattere("localhost"), false)) return 0x7f000001;
        if (!oggetto_VALORE(oggetto_fonti, 1)) return 0;
        int dati_VALORE = 0, totale_CONTA_NUMERI = 0, e_mail_byte = 0, 자릿수 = 0, voce_CONTA_NUMERI = heap_VALORE[oggetto_fonti + 1];
        for (int Loop_INDICE = 0; Loop_INDICE <= voce_CONTA_NUMERI; Loop_INDICE++) {
            int punto_di_codice = Loop_INDICE == voce_CONTA_NUMERI ? '.' : heap_VALORE[oggetto_fonti + 2 + Loop_INDICE];
            if (punto_di_codice == '.') { if (자릿수 == 0 || totale_CONTA_NUMERI == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } dati_VALORE = dati_VALORE << 8 | e_mail_byte; totale_CONTA_NUMERI++; e_mail_byte = 자릿수 = 0; }
            else { if (punto_di_codice < '0' || punto_di_codice > '9' || ++자릿수 > 3 || (e_mail_byte = e_mail_byte * 10 + punto_di_codice - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (totale_CONTA_NUMERI != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return dati_VALORE;
    }
    static int e_mail_carattere(int dati_VALORE) {
        int voce_CONTA_NUMERI = 0;
        for (int scorrere = 24; scorrere >= 0; scorrere -= 8) {
            int e_mail_byte = dati_VALORE >>> scorrere & 255;
            if (e_mail_byte >= 100) e_mail_SMS[voce_CONTA_NUMERI++] = '0' + e_mail_byte / 100;
            if (e_mail_byte >= 10) e_mail_SMS[voce_CONTA_NUMERI++] = '0' + e_mail_byte / 10 % 10;
            e_mail_SMS[voce_CONTA_NUMERI++] = '0' + e_mail_byte % 10; if (scorrere != 0) e_mail_SMS[voce_CONTA_NUMERI++] = '.';
        }
        int oggetto_fonti = allocare_Memoria(1, voce_CONTA_NUMERI); if (!errore) for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) heap_VALORE[oggetto_fonti + 2 + Loop_INDICE] = e_mail_SMS[Loop_INDICE]; return oggetto_fonti;
    }
    static void 통신호출(int proprietario, int nome_costante, int descrittore_costante, int comando_CODICE) {
        if (Word_SMS(proprietario, "java/net/InetAddress")) {
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "getLoopbackAddress") && Word_SMS(descrittore_costante, "()Ljava/net/InetAddress;")) { 넣기(locale_e_mail(), 2); return; }
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "getByName") && Word_SMS(descrittore_costante, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int dati_VALORE = 주소해독(빼기(2)); if (던진객체 == 0 && !errore) 넣기(e_mail_oggetto(dati_VALORE), 2); return;
            }
            if (comando_CODICE == 182 && Word_SMS(nome_costante, "getHostAddress") && Word_SMS(descrittore_costante, "()Ljava/lang/String;")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, 14)) 넣기(e_mail_carattere(heap_VALORE[oggetto_fonti + 2]), 2); return; }
        }
        if (Word_SMS(proprietario, "java/net/DatagramPacket")) {
            if (comando_CODICE == 183 && Word_SMS(nome_costante, "<init>") && (Word_SMS(descrittore_costante, "([BI)V") || Word_SMS(descrittore_costante, "([BILjava/net/InetAddress;I)V"))) {
                boolean meta_VALORE_fonti = Word_SMS(descrittore_costante, "([BILjava/net/InetAddress;I)V"); int numero_di_porta = meta_VALORE_fonti ? 빼기(1) : 0, e_mail_fonti = meta_VALORE_fonti ? 빼기(2) : 0;
                int voce_CONTA_NUMERI = 빼기(1), dati_array = 빼기(2), oggetto_fonti = 빼기(2);
                if (!oggetto_VALORE(oggetto_fonti, 16) || !oggetto_VALORE(dati_array, 20)) return;
                if (voce_CONTA_NUMERI < 0 || voce_CONTA_NUMERI > heap_VALORE[dati_array + 1] || numero_di_porta < 0 || numero_di_porta > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (e_mail_fonti != 0 && !oggetto_VALORE(e_mail_fonti, 14)) return;
                heap_VALORE[oggetto_fonti + 2] = dati_array; heap_fonti[oggetto_fonti + 2] = 1; heap_VALORE[oggetto_fonti + 3] = voce_CONTA_NUMERI;
                heap_VALORE[oggetto_fonti + 4] = e_mail_fonti; heap_fonti[oggetto_fonti + 4] = 1; heap_VALORE[oggetto_fonti + 5] = numero_di_porta; return;
            }
            if (comando_CODICE == 182 && Word_SMS(nome_costante, "setLength") && Word_SMS(descrittore_costante, "(I)V")) {
                int voce_CONTA_NUMERI = 빼기(1), oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 16)) return;
                if (voce_CONTA_NUMERI < 0 || voce_CONTA_NUMERI > heap_VALORE[heap_VALORE[oggetto_fonti + 2] + 1]) 예외던짐(9, "invalid datagram length"); else heap_VALORE[oggetto_fonti + 3] = voce_CONTA_NUMERI; return;
            }
            if (comando_CODICE == 182 && (Word_SMS(nome_costante, "getData") && Word_SMS(descrittore_costante, "()[B") || Word_SMS(nome_costante, "getLength") && Word_SMS(descrittore_costante, "()I") || Word_SMS(nome_costante, "getAddress") && Word_SMS(descrittore_costante, "()Ljava/net/InetAddress;") || Word_SMS(nome_costante, "getPort") && Word_SMS(descrittore_costante, "()I"))) {
                int oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 16)) return;
                int voce_funzione = Word_SMS(nome_costante, "getData") ? 2 : Word_SMS(nome_costante, "getLength") ? 3 : Word_SMS(nome_costante, "getAddress") ? 4 : 5;
                넣기(heap_VALORE[oggetto_fonti + voce_funzione], voce_funzione == 2 || voce_funzione == 4 ? 2 : 1); return;
            }
        }
        if (Word_SMS(proprietario, "java/net/DatagramSocket")) {
            if (comando_CODICE == 183 && Word_SMS(nome_costante, "<init>") && (Word_SMS(descrittore_costante, "()V") || Word_SMS(descrittore_costante, "(I)V"))) {
                int numero_di_porta = Word_SMS(descrittore_costante, "()V") ? 0 : 빼기(1), oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 15)) return;
                if (numero_di_porta < 0 || numero_di_porta > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = spazio_utente.aperto_rete(numero_di_porta); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else heap_VALORE[oggetto_fonti + 2] = 열린파일번호; return;
            }
            if (comando_CODICE == 182 && Word_SMS(nome_costante, "setSoTimeout") && Word_SMS(descrittore_costante, "(I)V")) {
                int 밀리초값 = 빼기(1), oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_VALORE[oggetto_fonti + 3] = 밀리초값; return;
            }
            if (comando_CODICE == 182 && Word_SMS(nome_costante, "getLocalPort") && Word_SMS(descrittore_costante, "()I")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, 15)) 넣기(heap_VALORE[oggetto_fonti + 2] < 0 ? -1 : spazio_utente.rete_porta(heap_VALORE[oggetto_fonti + 2]), 1); return; }
            if (comando_CODICE == 182 && Word_SMS(nome_costante, "isClosed") && Word_SMS(descrittore_costante, "()Z")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, 15)) 넣기(heap_VALORE[oggetto_fonti + 2] < 0 ? 1 : 0, 1); return; }
            if (comando_CODICE == 182 && Word_SMS(nome_costante, "close") && Word_SMS(descrittore_costante, "()V")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, 15) && heap_VALORE[oggetto_fonti + 2] >= 0) { spazio_utente.Chiudi_File_descrittore(heap_VALORE[oggetto_fonti + 2]); heap_VALORE[oggetto_fonti + 2] = -1; } return; }
            if (comando_CODICE == 182 && (Word_SMS(nome_costante, "send") || Word_SMS(nome_costante, "receive")) && Word_SMS(descrittore_costante, "(Ljava/net/DatagramPacket;)V")) {
                int pacchetto = 빼기(2), oggetto_fonti = 빼기(2); if (!oggetto_VALORE(pacchetto, 16) || !oggetto_VALORE(oggetto_fonti, 15)) return;
                int dati_array = heap_VALORE[pacchetto + 2], valido_durata = heap_VALORE[pacchetto + 3], 열린파일번호 = heap_VALORE[oggetto_fonti + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Word_SMS(nome_costante, "send")) {
                    if (!oggetto_VALORE(heap_VALORE[pacchetto + 4], 14)) return;
                    if (valido_durata > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int Loop_INDICE = 0; Loop_INDICE < valido_durata; Loop_INDICE++) 통신임시[Loop_INDICE] = heap_VALORE[dati_array + 2 + Loop_INDICE];
                    if (spazio_utente.inviare_rete(열린파일번호, heap_VALORE[heap_VALORE[pacchetto + 4] + 2], heap_VALORE[pacchetto + 5], 통신임시, valido_durata) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int voce_CONTA_NUMERI = spazio_utente.ricevere_rete(열린파일번호, 통신임시, valido_durata > 512 ? 512 : valido_durata);
                    if (voce_CONTA_NUMERI == -11) {
                        int posizione_corrente = spazio_utente.밀리초();
                        if (heap_VALORE[oggetto_fonti + 4] == 0) heap_VALORE[oggetto_fonti + 4] = posizione_corrente + 1;
                        if (heap_VALORE[oggetto_fonti + 3] > 0 && posizione_corrente - (heap_VALORE[oggetto_fonti + 4] - 1) >= heap_VALORE[oggetto_fonti + 3]) { heap_VALORE[oggetto_fonti + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(oggetto_fonti, 2); 넣기(pacchetto, 2); frame_funzione[frame_INDICE] = frame_istruzione[frame_INDICE]; richiesta_di_modifica = true; return;
                    }
                    heap_VALORE[oggetto_fonti + 4] = 0;
                    if (voce_CONTA_NUMERI < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) heap_VALORE[dati_array + 2 + Loop_INDICE] = (byte)통신임시[Loop_INDICE];
                    heap_VALORE[pacchetto + 3] = voce_CONTA_NUMERI; heap_VALORE[pacchetto + 4] = e_mail_oggetto(통신임시[513]); heap_fonti[pacchetto + 4] = 1; heap_VALORE[pacchetto + 5] = 통신임시[512];
                }
                return;
            }
        }
        errore_VALORE("unsupported java.net method");
    }
    static boolean 흐름대기(int oggetto_fonti) {
        int posizione_corrente = spazio_utente.밀리초();
        if (heap_VALORE[oggetto_fonti + 5] == 0) heap_VALORE[oggetto_fonti + 5] = posizione_corrente + 1;
        if (heap_VALORE[oggetto_fonti + 3] > 0 && posizione_corrente - (heap_VALORE[oggetto_fonti + 5] - 1) >= heap_VALORE[oggetto_fonti + 3]) { heap_VALORE[oggetto_fonti + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        frame_funzione[frame_INDICE] = frame_istruzione[frame_INDICE]; richiesta_di_modifica = true; return true;
    }
    static void 흐름호출(int proprietario, int nome_costante, int descrittore_costante, int comando_CODICE) {
        boolean ricevere_pagina = Word_SMS(proprietario, "java/net/ServerSocket"), Stream = Word_SMS(proprietario, "java/io/InputStream") || Word_SMS(proprietario, "java/io/OutputStream");
        if (!Stream && comando_CODICE == 183 && Word_SMS(nome_costante, "<init>")) {
            boolean reparto_IT_vuota_Stato = Word_SMS(descrittore_costante, "()V"), 이름지정여부 = Word_SMS(descrittore_costante, "(Ljava/lang/String;I)V"), 주소지정여부 = Word_SMS(descrittore_costante, "(Ljava/net/InetAddress;I)V");
            if (!(reparto_IT_vuota_Stato || ricevere_pagina && Word_SMS(descrittore_costante, "(I)V") || !ricevere_pagina && (이름지정여부 || 주소지정여부))) { errore_VALORE("unsupported socket constructor"); return; }
            int numero_di_porta = reparto_IT_vuota_Stato ? 0 : 빼기(1), e_mail_fonti = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, oggetto_fonti = 빼기(2);
            if (!oggetto_VALORE(oggetto_fonti, ricevere_pagina ? 18 : 17)) return;
            if (numero_di_porta < 0 || numero_di_porta > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !oggetto_VALORE(e_mail_fonti, 14)) return;
            int ID_rete = 이름지정여부 ? 주소해독(e_mail_fonti) : 주소지정여부 ? heap_VALORE[e_mail_fonti + 2] : 0x7f000001;
            if (errore || 던진객체 != 0) return;
            int 열린파일번호 = spazio_utente.Stream_controllo(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = reparto_IT_vuota_Stato ? 0 : ricevere_pagina ? spazio_utente.Stream_controllo(1, 열린파일번호, numero_di_porta) : spazio_utente.CONNETTI_Stream(열린파일번호, ID_rete, numero_di_porta);
            if (처리값 < 0) { spazio_utente.Chiudi_File_descrittore(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            heap_VALORE[oggetto_fonti + 2] = 열린파일번호; heap_VALORE[oggetto_fonti + 4] = numero_di_porta; heap_VALORE[oggetto_fonti + 6] = reparto_IT_vuota_Stato ? 0 : 1; return;
        }
        if (!Stream && Word_SMS(nome_costante, "setSoTimeout") && Word_SMS(descrittore_costante, "(I)V")) { int 밀리초값 = 빼기(1), oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, ricevere_pagina ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else heap_VALORE[oggetto_fonti + 3] = 밀리초값; return; }
        if (!Stream && Word_SMS(nome_costante, "close") && Word_SMS(descrittore_costante, "()V")) { int oggetto_fonti = 빼기(2); if (oggetto_VALORE(oggetto_fonti, ricevere_pagina ? 18 : 17) && heap_VALORE[oggetto_fonti + 2] >= 0) { spazio_utente.Chiudi_File_descrittore(heap_VALORE[oggetto_fonti + 2]); heap_VALORE[oggetto_fonti + 2] = -1; } return; }
        if (!Stream && (Word_SMS(nome_costante, "getLocalPort") || Word_SMS(nome_costante, "getPort") || Word_SMS(nome_costante, "isClosed") || Word_SMS(nome_costante, "isConnected"))) {
            int oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, ricevere_pagina ? 18 : 17)) return;
            넣기(Word_SMS(nome_costante, "isClosed") ? heap_VALORE[oggetto_fonti + 2] < 0 ? 1 : 0 : Word_SMS(nome_costante, "isConnected") ? heap_VALORE[oggetto_fonti + 6] : Word_SMS(nome_costante, "getPort") ? heap_VALORE[oggetto_fonti + 4] : heap_VALORE[oggetto_fonti + 2] < 0 ? -1 : spazio_utente.Stream_controllo(4, heap_VALORE[oggetto_fonti + 2], 0), 1); return;
        }
        if (ricevere_pagina && Word_SMS(nome_costante, "accept") && Word_SMS(descrittore_costante, "()Ljava/net/Socket;")) {
            int oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 18)) return; int 열린파일번호 = spazio_utente.Stream_controllo(3, heap_VALORE[oggetto_fonti + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(oggetto_fonti)) 넣기(oggetto_fonti, 2); return; }
            heap_VALORE[oggetto_fonti + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = allocare_Memoria(17, 5); if (errore) { spazio_utente.Chiudi_File_descrittore(열린파일번호); return; } heap_VALORE[반환값 + 2] = 열린파일번호; heap_VALORE[반환값 + 4] = spazio_utente.Stream_controllo(5, 열린파일번호, 0); heap_VALORE[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!ricevere_pagina && !Stream && ((Word_SMS(nome_costante, "getInputStream") && Word_SMS(descrittore_costante, "()Ljava/io/InputStream;")) || (Word_SMS(nome_costante, "getOutputStream") && Word_SMS(descrittore_costante, "()Ljava/io/OutputStream;")))) {
            int oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 17)) return; if (heap_VALORE[oggetto_fonti + 2] < 0 || heap_VALORE[oggetto_fonti + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = allocare_Memoria(19, 4); if (errore) return; heap_VALORE[반환값 + 2] = oggetto_fonti; heap_fonti[반환값 + 2] = 1; heap_VALORE[반환값 + 3] = Word_SMS(nome_costante, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Word_SMS(nome_costante, "read"), reparto_IT_scrivere_operazione = Word_SMS(nome_costante, "write"), Blocca = Word_SMS(descrittore_costante, "([B)I") || Word_SMS(descrittore_costante, "([B)V"), reparto_IT_MATRICE_SECONDARIA = Word_SMS(descrittore_costante, "([BII)I") || Word_SMS(descrittore_costante, "([BII)V");
            int voce_CONTA_NUMERI = reparto_IT_MATRICE_SECONDARIA ? 빼기(1) : 0, 시작변위 = reparto_IT_MATRICE_SECONDARIA ? 빼기(1) : 0, dati_array = Blocca || reparto_IT_MATRICE_SECONDARIA ? 빼기(2) : 0;
            int dati_VALORE = reparto_IT_scrivere_operazione && Word_SMS(descrittore_costante, "(I)V") ? 빼기(1) : 0, oggetto_fonti = 빼기(2);
            if (!oggetto_VALORE(oggetto_fonti, 19)) return; int padre_fonti = heap_VALORE[oggetto_fonti + 2], 열린파일번호 = heap_VALORE[padre_fonti + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Word_SMS(nome_costante, "close") && Word_SMS(descrittore_costante, "()V")) { spazio_utente.Chiudi_File_descrittore(열린파일번호); heap_VALORE[padre_fonti + 2] = -1; return; }
            if (Word_SMS(nome_costante, "flush") && Word_SMS(descrittore_costante, "()V")) return;
            if ((!읽기여부 && !reparto_IT_scrivere_operazione) || 읽기여부 != (heap_VALORE[oggetto_fonti + 3] == 0)) { errore_VALORE("unsupported stream operation"); return; }
            if (Blocca || reparto_IT_MATRICE_SECONDARIA) { if (!oggetto_VALORE(dati_array, 20)) return; if (Blocca) voce_CONTA_NUMERI = heap_VALORE[dati_array + 1]; if (시작변위 < 0 || voce_CONTA_NUMERI < 0 || 시작변위 > heap_VALORE[dati_array + 1] - voce_CONTA_NUMERI) { 예외던짐(6, "stream array bounds"); return; } }
            else voce_CONTA_NUMERI = 1;
            if (voce_CONTA_NUMERI == 0) { if (읽기여부) 넣기(0, 1); return; }
            int Completate_CONTA_NUMERI = reparto_IT_scrivere_operazione ? heap_VALORE[oggetto_fonti + 4] : 0, 처리값 = 0;
            while (Completate_CONTA_NUMERI < voce_CONTA_NUMERI) {
                처리값 = 읽기여부 ? spazio_utente.파일한바이트읽기(열린파일번호) : spazio_utente.파일한바이트쓰기(열린파일번호, Blocca || reparto_IT_MATRICE_SECONDARIA ? heap_VALORE[dati_array + 2 + 시작변위 + Completate_CONTA_NUMERI] : dati_VALORE);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (Blocca || reparto_IT_MATRICE_SECONDARIA)) heap_VALORE[dati_array + 2 + 시작변위 + Completate_CONTA_NUMERI] = (byte)처리값;
                Completate_CONTA_NUMERI++; if (읽기여부 && !(Blocca || reparto_IT_MATRICE_SECONDARIA)) break;
            }
            if (처리값 == -11 && (reparto_IT_scrivere_operazione || Completate_CONTA_NUMERI == 0)) {
                heap_VALORE[oggetto_fonti + 4] = Completate_CONTA_NUMERI;
                if (흐름대기(padre_fonti)) { 넣기(oggetto_fonti, 2); if (Blocca || reparto_IT_MATRICE_SECONDARIA) 넣기(dati_array, 2); if (reparto_IT_MATRICE_SECONDARIA) { 넣기(시작변위, 1); 넣기(voce_CONTA_NUMERI, 1); } if (reparto_IT_scrivere_operazione && !(Blocca || reparto_IT_MATRICE_SECONDARIA)) 넣기(dati_VALORE, 1); } return;
            }
            heap_VALORE[oggetto_fonti + 4] = 0; heap_VALORE[padre_fonti + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(Completate_CONTA_NUMERI == 0 && 처리값 == 256 ? -1 : Blocca || reparto_IT_MATRICE_SECONDARIA ? Completate_CONTA_NUMERI : 처리값, 1); return;
        }
        errore_VALORE("unsupported Socket/ServerSocket method");
    }
    static int[] schermata_fonti = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int nome_costante) {
        if (Word_SMS(nome_costante, "Italiano/nativo/Finestra")) return 24;
        if (Word_SMS(nome_costante, "Italiano/nativo/Etichetta")) return 26;
        if (Word_SMS(nome_costante, "Italiano/nativo/pulsante")) return 27;
        if (Word_SMS(nome_costante, "Italiano/nativo/campo_di_testo")) return 28;
        if (Word_SMS(nome_costante, "Italiano/nativo/Action_informativa")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int nome_costante) {
        return 한국어화면종(nome_costante) != 0 || Word_SMS(nome_costante, "Italiano/nativo/schermata_elemento") || Word_SMS(nome_costante, "Italiano/nativo/evento_coda");
    }
    static int schermata_Corso(int nome_costante) {
        int 한국어종 = 한국어화면종(nome_costante); if (한국어종 != 0) return 한국어종;
        if (Word_SMS(nome_costante, "javax/swing/JFrame")) return 24;
        if (Word_SMS(nome_costante, "javax/swing/JPanel")) return 25;
        if (Word_SMS(nome_costante, "javax/swing/JLabel")) return 26;
        if (Word_SMS(nome_costante, "javax/swing/JButton")) return 27;
        if (Word_SMS(nome_costante, "javax/swing/JTextField")) return 28;
        if (Word_SMS(nome_costante, "java/awt/event/ActionEvent")) return 29;
        if (Word_SMS(nome_costante, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean schermata_proprietario(int nome_costante) {
        return schermata_Corso(nome_costante) != 0 || Word_SMS(nome_costante, "java/awt/Component") || Word_SMS(nome_costante, "java/awt/Container") || Word_SMS(nome_costante, "javax/swing/JComponent") || Word_SMS(nome_costante, "javax/swing/AbstractButton") || Word_SMS(nome_costante, "javax/swing/text/JTextComponent") || Word_SMS(nome_costante, "javax/swing/SwingUtilities");
    }
    static boolean schermata_oggetto(int oggetto_fonti) { if (!reparto_IT_valido_oggetto(oggetto_fonti)) return false; if (heap_VALORE[oggetto_fonti] < 24 || heap_VALORE[oggetto_fonti] > 28) { errore_VALORE("unsupported Swing receiver"); return false; } return true; }
    static void set_schermata_carattere(int oggetto_fonti, int SMS_fonti) {
        if (SMS_fonti != 0 && !oggetto_VALORE(SMS_fonti, 1)) return;
        int voce_CONTA_NUMERI = SMS_fonti == 0 ? 0 : heap_VALORE[SMS_fonti + 1]; if (voce_CONTA_NUMERI > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) 화면글임시[Loop_INDICE] = heap_VALORE[SMS_fonti + 2 + Loop_INDICE];
        if (spazio_utente.schermata_SMS(heap_VALORE[oggetto_fonti + 2], 화면글임시, voce_CONTA_NUMERI) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        heap_VALORE[oggetto_fonti + 3] = SMS_fonti; heap_fonti[oggetto_fonti + 3] = 1;
    }
    static int 화면문자읽기(int oggetto_fonti) {
        int account_VALORE = heap_VALORE[oggetto_fonti + 2], voce_CONTA_NUMERI = spazio_utente.schermata_connessione(8, account_VALORE, 0, 0, 0, 0), 사용수 = 0;
        if (voce_CONTA_NUMERI < 0) { errore_VALORE("GUI text read failed"); return 0; }
        for (int Loop_INDICE = 0; Loop_INDICE < voce_CONTA_NUMERI; Loop_INDICE++) { int 부호값 = spazio_utente.schermata_connessione(9, account_VALORE, Loop_INDICE, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = allocare_Memoria(1, 사용수); if (!errore) for (int Loop_INDICE = 0; Loop_INDICE < 사용수; Loop_INDICE++) heap_VALORE[반환값 + 2 + Loop_INDICE] = 화면글임시[Loop_INDICE]; return 반환값;
    }
    /* Italiano 객체를 직접 만들고 kernel_VALORE schermata 기능에 연결한다. Swing oggetto_VALORE/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int proprietario, int nome_costante, int descrittore_costante, int comando_CODICE) {
        if (Word_SMS(proprietario, "Italiano/nativo/evento_coda")) {
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "나중에실행") && Word_SMS(descrittore_costante, "(LItaliano/nativo/실행할일;)V")) {
                int task_Action = 빼기(2); if (!reparto_IT_valido_oggetto(task_Action)) return;
                if (나중수 == 8) { errore_VALORE("schermata 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = task_Action; return;
            }
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "사건처리중인가") && Word_SMS(descrittore_costante, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            errore_VALORE("지원하지 않는 Italiano schermata 일정 호출"); return;
        }
        if (Word_SMS(proprietario, "Italiano/nativo/Action_informativa")) {
            int informativa = 빼기(2); if (!oggetto_VALORE(informativa, 29) || heap_VALORE[informativa + 3] == 0) return;
            if (Word_SMS(nome_costante, "origine_evento") && Word_SMS(descrittore_costante, "()LItaliano/nativo/schermata_elemento;")) 넣기(heap_VALORE[informativa + 2], 2);
            else if (Word_SMS(nome_costante, "comando_SMS") && Word_SMS(descrittore_costante, "()Ljava/lang/String;")) 넣기(화면문자읽기(heap_VALORE[informativa + 2]), 2);
            else if (Word_SMS(nome_costante, "INDICE") && Word_SMS(descrittore_costante, "()I")) 넣기(1001, 1);
            else errore_VALORE("지원하지 않는 Italiano Azione informativa 호출"); return;
        }
        if (comando_CODICE == 183 && Word_SMS(nome_costante, "<init>")) {
            int Kind_VALORE = 한국어화면종(proprietario), 받이 = 0, 가로 = 0, Verticale_funzione = 0, 폭 = 0, altezza_VALORE = 0;
            if (Kind_VALORE == 24 && Word_SMS(descrittore_costante, "(Ljava/lang/String;II)V")) {
                altezza_VALORE = 빼기(1); 폭 = 빼기(1); 가로 = (spazio_utente.화면너비() - 폭) / 2; Verticale_funzione = (spazio_utente.schermata_altezza() - altezza_VALORE) / 2;
            } else if ((Kind_VALORE == 26 || Kind_VALORE == 28) && Word_SMS(descrittore_costante, "(Ljava/lang/String;IIII)V") || Kind_VALORE == 27 && Word_SMS(descrittore_costante, "(Ljava/lang/String;IIIILItaliano/nativo/동작받이;)V")) {
                if (Kind_VALORE == 27) 받이 = 빼기(2);
                altezza_VALORE = 빼기(1); 폭 = 빼기(1); Verticale_funzione = 빼기(1); 가로 = 빼기(1);
            } else { errore_VALORE("지원하지 않는 Italiano schermata 생성자"); return; }
            int testo = 빼기(2), elemento_VALORE = 빼기(2); if (!schermata_oggetto(elemento_VALORE)) return;
            if (폭 < 1 || altezza_VALORE < 1 || 가로 < 0 || Verticale_funzione < 0 || 폭 > spazio_utente.화면너비() - 가로 || altezza_VALORE > spazio_utente.schermata_altezza() - Verticale_funzione) { 예외던짐(27, "schermata 영역을 벗어난 크기입니다"); return; }
            int INDICE = spazio_utente.schermata_connessione(0, Kind_VALORE - 23, 0, 0, 0, 0);
            if (INDICE < 1 || INDICE > 32) { errore_VALORE("schermata elemento_VALORE 자리가 가득 찼습니다"); return; }
            heap_VALORE[elemento_VALORE + 2] = INDICE; schermata_fonti[INDICE - 1] = elemento_VALORE;
            heap_VALORE[elemento_VALORE + 5] = 가로; heap_VALORE[elemento_VALORE + 6] = Verticale_funzione; heap_VALORE[elemento_VALORE + 7] = 폭; heap_VALORE[elemento_VALORE + 8] = altezza_VALORE; heap_VALORE[elemento_VALORE + 10] = 2;
            heap_VALORE[elemento_VALORE + 4] = 받이; heap_fonti[elemento_VALORE + 4] = 1; heap_VALORE[elemento_VALORE + 12] = 1;
            spazio_utente.schermata_connessione(1, INDICE, 가로, Verticale_funzione, 폭, altezza_VALORE);
            if (Kind_VALORE == 24) spazio_utente.schermata_connessione(7, INDICE, 2, 0, 0, 0);
            set_schermata_carattere(elemento_VALORE, testo); return;
        }
        if (comando_CODICE != 182) { errore_VALORE("잘못된 Italiano schermata 호출 comando"); return; }
        if (Word_SMS(nome_costante, "scrivere_SMS") && Word_SMS(descrittore_costante, "(Ljava/lang/String;)V")) {
            int testo = 빼기(2), elemento_VALORE = 빼기(2); if (schermata_oggetto(elemento_VALORE)) set_schermata_carattere(elemento_VALORE, testo); return;
        }
        if (Word_SMS(nome_costante, "글읽기") && Word_SMS(descrittore_costante, "()Ljava/lang/String;")) {
            int elemento_VALORE = 빼기(2); if (schermata_oggetto(elemento_VALORE)) 넣기(화면문자읽기(elemento_VALORE), 2); return;
        }
        if (Word_SMS(nome_costante, "동작맡기기") && Word_SMS(descrittore_costante, "(LItaliano/nativo/동작받이;)V")) {
            int 받이 = 빼기(2), elemento_VALORE = 빼기(2);
            if (schermata_oggetto(elemento_VALORE)) { heap_VALORE[elemento_VALORE + 4] = 받이; heap_fonti[elemento_VALORE + 4] = 1; heap_VALORE[elemento_VALORE + 12] = 1; } return;
        }
        if (Word_SMS(nome_costante, "Aggiungi_elemento") && Word_SMS(descrittore_costante, "(LItaliano/nativo/schermata_elemento;)V")) {
            int figlio_VALORE = 빼기(2), padre_VALORE = 빼기(2); if (!schermata_oggetto(figlio_VALORE) || !schermata_oggetto(padre_VALORE)) return;
            if (spazio_utente.schermata_connessione(2, heap_VALORE[padre_VALORE + 2], heap_VALORE[figlio_VALORE + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 schermata 부모입니다"); return; }
            heap_VALORE[figlio_VALORE + 11] = padre_VALORE; heap_fonti[figlio_VALORE + 11] = 1; return;
        }
        if (Word_SMS(nome_costante, "자리정하기") && Word_SMS(descrittore_costante, "(IIII)V")) {
            int altezza_VALORE = 빼기(1), 폭 = 빼기(1), Verticale_funzione = 빼기(1), 가로 = 빼기(1), elemento_VALORE = 빼기(2); if (!schermata_oggetto(elemento_VALORE)) return;
            if (spazio_utente.schermata_connessione(1, heap_VALORE[elemento_VALORE + 2], 가로, Verticale_funzione, 폭, altezza_VALORE) < 0) { 예외던짐(27, "schermata 영역을 벗어난 자리입니다"); return; }
            heap_VALORE[elemento_VALORE + 5] = 가로; heap_VALORE[elemento_VALORE + 6] = Verticale_funzione; heap_VALORE[elemento_VALORE + 7] = 폭; heap_VALORE[elemento_VALORE + 8] = altezza_VALORE; return;
        }
        if ((Word_SMS(nome_costante, "mostrare_finestra") || Word_SMS(nome_costante, "Chiudi")) && Word_SMS(descrittore_costante, "()V")) {
            boolean Visibilità_VALORE = Word_SMS(nome_costante, "mostrare_finestra"); int elemento_VALORE = 빼기(2); if (!schermata_oggetto(elemento_VALORE)) return;
            if (spazio_utente.schermata_connessione(Visibilità_VALORE ? 3 : 4, heap_VALORE[elemento_VALORE + 2], Visibilità_VALORE ? 1 : 0, 0, 0, 0) < 0) { errore_VALORE("화면은 interattivo 명령에서 실행해야 합니다"); return; }
            heap_VALORE[elemento_VALORE + 9] = Visibilità_VALORE ? 1 : 0; return;
        }
        if (Word_SMS(nome_costante, "보이는가") && Word_SMS(descrittore_costante, "()Z")) { int elemento_VALORE = 빼기(2); if (schermata_oggetto(elemento_VALORE)) 넣기(heap_VALORE[elemento_VALORE + 9], 1); return; }
        errore_VALORE("지원하지 않는 Italiano schermata metodo_VALORE");
    }
    static void 화면호출(int proprietario, int nome_costante, int descrittore_costante, int comando_CODICE) {
        if (Word_SMS(proprietario, "javax/swing/SwingUtilities")) {
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "invokeLater") && Word_SMS(descrittore_costante, "(Ljava/lang/Runnable;)V")) { int oggetto_fonti = 빼기(2); if (!reparto_IT_valido_oggetto(oggetto_fonti)) return; if (나중수 == 8) { errore_VALORE("invokeLater queue full"); return; } 나중실행[나중수++] = oggetto_fonti; return; }
            if (comando_CODICE == 184 && Word_SMS(nome_costante, "isEventDispatchThread") && Word_SMS(descrittore_costante, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            errore_VALORE("unsupported SwingUtilities method"); return;
        }
        if (Word_SMS(proprietario, "java/awt/event/ActionEvent")) {
            int oggetto_fonti = 빼기(2); if (!oggetto_VALORE(oggetto_fonti, 29)) return;
            if (Word_SMS(nome_costante, "getSource") && Word_SMS(descrittore_costante, "()Ljava/lang/Object;")) 넣기(heap_VALORE[oggetto_fonti + 2], 2);
            else if (Word_SMS(nome_costante, "getActionCommand") && Word_SMS(descrittore_costante, "()Ljava/lang/String;")) 넣기(화면문자읽기(heap_VALORE[oggetto_fonti + 2]), 2);
            else if (Word_SMS(nome_costante, "getID") && Word_SMS(descrittore_costante, "()I")) 넣기(1001, 1);
            else errore_VALORE("unsupported ActionEvent method"); return;
        }
        if (comando_CODICE == 183 && Word_SMS(nome_costante, "<init>")) {
            int COLONNE = 0, SMS_fonti = 0;
            if (Word_SMS(descrittore_costante, "(I)V")) COLONNE = 빼기(1);
            else if (Word_SMS(descrittore_costante, "(Ljava/lang/String;I)V")) { COLONNE = 빼기(1); SMS_fonti = 빼기(2); }
            else if (Word_SMS(descrittore_costante, "(Ljava/lang/String;)V")) SMS_fonti = 빼기(2);
            else if (Word_SMS(descrittore_costante, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Word_SMS(descrittore_costante, "()V")) { errore_VALORE("unsupported Swing constructor"); return; }
            int oggetto_fonti = 빼기(2); if (!reparto_IT_valido_oggetto(oggetto_fonti)) return;
            if (heap_VALORE[oggetto_fonti] == 30) { errore_VALORE("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!schermata_oggetto(oggetto_fonti) || COLONNE < 0) return;
            int account_VALORE = spazio_utente.schermata_connessione(0, heap_VALORE[oggetto_fonti] - 23, 0, 0, 0, 0);
            if (account_VALORE < 1 || account_VALORE > 32) { errore_VALORE("GUI widget slots exhausted"); return; }
            heap_VALORE[oggetto_fonti + 2] = account_VALORE; schermata_fonti[account_VALORE - 1] = oggetto_fonti; heap_VALORE[oggetto_fonti + 5] = heap_VALORE[oggetto_fonti] == 24 ? 130 : 16; heap_VALORE[oggetto_fonti + 6] = heap_VALORE[oggetto_fonti] == 24 ? 110 : 16;
            heap_VALORE[oggetto_fonti + 7] = heap_VALORE[oggetto_fonti] == 24 ? 380 : 220; heap_VALORE[oggetto_fonti + 8] = heap_VALORE[oggetto_fonti] == 24 ? 240 : 28; heap_VALORE[oggetto_fonti + 10] = 1;
            set_schermata_carattere(oggetto_fonti, SMS_fonti); return;
        }
        if (Word_SMS(nome_costante, "setText") || Word_SMS(nome_costante, "setTitle")) { int SMS_fonti = 빼기(2), oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti) && Word_SMS(descrittore_costante, "(Ljava/lang/String;)V")) set_schermata_carattere(oggetto_fonti, SMS_fonti); return; }
        if (Word_SMS(nome_costante, "getText") || Word_SMS(nome_costante, "getTitle")) { int oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti) && Word_SMS(descrittore_costante, "()Ljava/lang/String;")) 넣기(화면문자읽기(oggetto_fonti), 2); return; }
        if (Word_SMS(nome_costante, "addActionListener") && Word_SMS(descrittore_costante, "(Ljava/awt/event/ActionListener;)V")) { int ricevere_fonti = 빼기(2), oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti)) { heap_VALORE[oggetto_fonti + 4] = ricevere_fonti; heap_fonti[oggetto_fonti + 4] = 1; } return; }
        if (Word_SMS(nome_costante, "getContentPane") && Word_SMS(descrittore_costante, "()Ljava/awt/Container;")) { int oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti)) 넣기(oggetto_fonti, 2); return; }
        if (Word_SMS(nome_costante, "setLayout") && Word_SMS(descrittore_costante, "(Ljava/awt/LayoutManager;)V")) { int Layout_fonti = 빼기(2), oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti) && Layout_fonti != 0) errore_VALORE("only absolute layout (null) is supported"); return; }
        if (Word_SMS(nome_costante, "add") && (Word_SMS(descrittore_costante, "(Ljava/awt/Component;)Ljava/awt/Component;") || Word_SMS(descrittore_costante, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Layout_condizione = Word_SMS(descrittore_costante, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Layout_condizione) 빼기(2);
            int figlio_fonti = 빼기(2), oggetto_fonti = 빼기(2); if (!schermata_oggetto(figlio_fonti) || !schermata_oggetto(oggetto_fonti)) return;
            if (spazio_utente.schermata_connessione(2, heap_VALORE[oggetto_fonti + 2], heap_VALORE[figlio_fonti + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            heap_VALORE[figlio_fonti + 11] = oggetto_fonti; heap_fonti[figlio_fonti + 11] = 1; if (!Layout_condizione) 넣기(figlio_fonti, 2); return;
        }
        if (Word_SMS(nome_costante, "setBounds") && Word_SMS(descrittore_costante, "(IIII)V")) {
            int altezza_VALORE = 빼기(1), 너비 = 빼기(1), Y_coordinata = 빼기(1), coordinata_x = 빼기(1), oggetto_fonti = 빼기(2); if (!schermata_oggetto(oggetto_fonti)) return;
            if (spazio_utente.schermata_connessione(1, heap_VALORE[oggetto_fonti + 2], coordinata_x, Y_coordinata, 너비, altezza_VALORE) < 0) { 예외던짐(9, "GUI bounds"); return; }
            heap_VALORE[oggetto_fonti + 5] = coordinata_x; heap_VALORE[oggetto_fonti + 6] = Y_coordinata; heap_VALORE[oggetto_fonti + 7] = 너비; heap_VALORE[oggetto_fonti + 8] = altezza_VALORE; return;
        }
        if (Word_SMS(nome_costante, "setSize") && Word_SMS(descrittore_costante, "(II)V")) {
            int altezza_VALORE = 빼기(1), 너비 = 빼기(1), oggetto_fonti = 빼기(2); if (!schermata_oggetto(oggetto_fonti)) return;
            if (spazio_utente.schermata_connessione(1, heap_VALORE[oggetto_fonti + 2], heap_VALORE[oggetto_fonti + 5], heap_VALORE[oggetto_fonti + 6], 너비, altezza_VALORE) < 0) 예외던짐(9, "GUI size"); else { heap_VALORE[oggetto_fonti + 7] = 너비; heap_VALORE[oggetto_fonti + 8] = altezza_VALORE; } return;
        }
        if (Word_SMS(nome_costante, "setLocationRelativeTo") && Word_SMS(descrittore_costante, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), oggetto_fonti = 빼기(2); if (!schermata_oggetto(oggetto_fonti)) return; if (상대배치 != 0) { errore_VALORE("only screen centering supported"); return; } heap_VALORE[oggetto_fonti + 5] = (spazio_utente.화면너비() - heap_VALORE[oggetto_fonti + 7]) / 2; heap_VALORE[oggetto_fonti + 6] = (spazio_utente.schermata_altezza() - heap_VALORE[oggetto_fonti + 8]) / 2; spazio_utente.schermata_connessione(1, heap_VALORE[oggetto_fonti + 2], heap_VALORE[oggetto_fonti + 5], heap_VALORE[oggetto_fonti + 6], heap_VALORE[oggetto_fonti + 7], heap_VALORE[oggetto_fonti + 8]); return; }
        if (Word_SMS(nome_costante, "setDefaultCloseOperation") && Word_SMS(descrittore_costante, "(I)V")) { int norma = 빼기(1), oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti)) { if (norma < 0 || norma > 3) 예외던짐(9, "close policy"); else { heap_VALORE[oggetto_fonti + 10] = norma; spazio_utente.schermata_connessione(7, heap_VALORE[oggetto_fonti + 2], norma, 0, 0, 0); } } return; }
        if (Word_SMS(nome_costante, "setVisible") && Word_SMS(descrittore_costante, "(Z)V")) { int dati_VALORE = 빼기(1), oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti)) { int 처리값 = spazio_utente.schermata_connessione(3, heap_VALORE[oggetto_fonti + 2], dati_VALORE, 0, 0, 0); if (처리값 < 0) errore_VALORE("Swing requires a standalone interactive command"); else heap_VALORE[oggetto_fonti + 9] = dati_VALORE; } return; }
        if (Word_SMS(nome_costante, "dispose") && Word_SMS(descrittore_costante, "()V")) { int oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti)) { spazio_utente.schermata_connessione(4, heap_VALORE[oggetto_fonti + 2], 0, 0, 0, 0); heap_VALORE[oggetto_fonti + 9] = 0; } return; }
        if (Word_SMS(nome_costante, "repaint") || Word_SMS(nome_costante, "validate")) { int oggetto_fonti = 빼기(2); if (!schermata_oggetto(oggetto_fonti) || !Word_SMS(descrittore_costante, "()V")) return; spazio_utente.schermata_connessione(1, heap_VALORE[oggetto_fonti + 2], heap_VALORE[oggetto_fonti + 5], heap_VALORE[oggetto_fonti + 6], heap_VALORE[oggetto_fonti + 7], heap_VALORE[oggetto_fonti + 8]); return; }
        if (Word_SMS(nome_costante, "isVisible") && Word_SMS(descrittore_costante, "()Z")) { int oggetto_fonti = 빼기(2); if (schermata_oggetto(oggetto_fonti)) 넣기(heap_VALORE[oggetto_fonti + 9], 1); return; }
        errore_VALORE("unsupported Swing method (native subset)");
    }
    static void approntare_evento(int target_e_mail, int evento_numero, boolean Italiano) {
        if (target_e_mail < 1 || heap_VALORE[target_e_mail] < 32) { errore_VALORE("Java event listener required"); return; }
        int File_INDICE = nome_metodo(heap_VALORE[target_e_mail] - 32, evento_numero == 0 ? (Italiano ? "Esegui" : "run") : (Italiano ? "ricevere_Action" : "actionPerformed"), evento_numero == 0 ? "()V" : (Italiano ? "(LItaliano/nativo/Action_informativa;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (File_INDICE < 0) { errore_VALORE("event callback missing"); return; }
        Regolari_thread = 0; Conteggio_dei_thread = 1; frame_INDICE = 0; thread_Stato[0] = 1; frame_Pila[0] = 0; frame_blocco[0] = inizializzare_frame[0] = 0; richiesta_di_modifica = false;
        for (int Loop_INDICE = 0; Loop_INDICE < 128; Loop_INDICE++) { locale_VALORE[Loop_INDICE] = locale_TIPO[Loop_INDICE] = 0; }
        frame_metodo[0] = File_INDICE; frame_funzione[0] = metodo_START[File_INDICE]; locale_VALORE[0] = target_e_mail; locale_TIPO[0] = 2;
        if (evento_numero != 0) { locale_VALORE[1] = evento_numero; locale_TIPO[1] = 2; }
        사건중 = true; Esegui_comando(); 사건중 = false;
    }
    static void schermata_Eventi() {
        while (!errore) {
            if (나중수 > 0) { int target_e_mail = 나중실행[0], Italiano = 나중한국어[0]; for (int Loop_INDICE = 1; Loop_INDICE < 나중수; Loop_INDICE++) { 나중실행[Loop_INDICE - 1] = 나중실행[Loop_INDICE]; 나중한국어[Loop_INDICE - 1] = 나중한국어[Loop_INDICE]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; approntare_evento(target_e_mail, 0, Italiano != 0); continue; }
            if (spazio_utente.schermata_connessione(6, 0, 0, 0, 0, 0) == 0) return;
            int evento_numero = spazio_utente.schermata_connessione(5, 0, 0, 0, 0, 0); if (evento_numero == 0) continue;
            if (evento_numero < 0) { errore_VALORE("GUI event I/O failed"); return; }
            int account_VALORE = evento_numero & 65535; if (account_VALORE < 1 || account_VALORE > 32) continue; int oggetto_fonti = schermata_fonti[account_VALORE - 1]; if (oggetto_fonti == 0) continue;
            if ((evento_numero & 65536) != 0) {
                if (heap_VALORE[oggetto_fonti + 10] != 0) heap_VALORE[oggetto_fonti + 9] = 0;
                if (heap_VALORE[oggetto_fonti + 10] == 3) for (int Loop_INDICE = 0; Loop_INDICE < 32; Loop_INDICE++) if (schermata_fonti[Loop_INDICE] != 0 && heap_VALORE[schermata_fonti[Loop_INDICE]] == 24) spazio_utente.schermata_connessione(4, Loop_INDICE + 1, 0, 0, 0, 0);
            } else if (heap_VALORE[oggetto_fonti + 4] != 0) {
                int README_fonti = allocare_Memoria(29, 2); if (errore) return; heap_VALORE[README_fonti + 2] = oggetto_fonti; heap_VALORE[README_fonti + 3] = heap_VALORE[oggetto_fonti + 12]; heap_fonti[README_fonti + 2] = 1; approntare_evento(heap_VALORE[oggetto_fonti + 4], README_fonti, heap_VALORE[oggetto_fonti + 12] != 0);
            }
        }
    }
    public static int avvia() {
        if (spazio_utente.인수개수() == 1 && 자바도구.같음(spazio_utente.argomenti(0), "-version")) {
            spazio_utente.Scrittura("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (spazio_utente.인수개수() < 1) { spazio_utente.Scrittura("Usage: java CLASS [ARGS]\n"); return 2; }
        voce_Corso_definizione = carico_Corso_definizione(host_carattere(spazio_utente.argomenti(0))); if (errore || voce_Corso_definizione < 0) return 1;
        int punto_di_ingresso_VALORE = nome_metodo(voce_Corso_definizione, "avvia", "()V");
        boolean 한국어진입 = punto_di_ingresso_VALORE >= 0 && (metodo_accesso[punto_di_ingresso_VALORE] & 9) == 9;
        if (!한국어진입) punto_di_ingresso_VALORE = nome_metodo(voce_Corso_definizione, "main", "([Ljava/lang/String;)V");
        if (punto_di_ingresso_VALORE < 0 || (metodo_accesso[punto_di_ingresso_VALORE] & 9) != 9) errore_VALORE("public static void avvia() or main(String[] args) required");
        if (errore) return 1;
        int argomenti = allocare_Memoria(3, spazio_utente.인수개수() - 1); elemento_di_matrice[argomenti] = -1;
        for (int numero = 1; numero < spazio_utente.인수개수() && !errore; numero++) heap_VALORE[argomenti + 1 + numero] = host_carattere(spazio_utente.argomenti(numero));
        frame_INDICE = 0; frame_metodo[0] = punto_di_ingresso_VALORE; frame_funzione[0] = metodo_START[punto_di_ingresso_VALORE]; locale_VALORE[0] = 한국어진입 ? 0 : argomenti; locale_TIPO[0] = 한국어진입 ? 0 : 2;
        thread_Stato[0] = 1; thread_oggetto[0] = allocare_Memoria(13, 2);
        Esegui_comando(); if (!errore) schermata_Eventi(); return errore ? 1 : 0;
    }
}
