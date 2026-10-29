// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. file/operando_Pila/fonti/ramo 경계를 Esegui_comando 중 검사한다. */
public final class 자바가상기계 {
    static int[] file = new int[16384], nome_file_SMS = new int[64];
    static int[] costante_tag = new int[512], 상가 = new int[512], costante_SECONDO_VALORE = new int[512], stringa_fonti = new int[512];
    static int[] metodo_nome_SMS = new int[32], metodo_TIPO = new int[32], metodo_accesso = new int[32];
    static int[] metodo_START = new int[32], metodo_chiudere = new int[32], metodo_Pila = new int[32], 함수지역 = new int[32];
    static int[] metodo_argomento_CONTA_NUMERI = new int[32], metodo_argomento_TIPO = new int[512], metodo_Reso = new int[32];
    static int[] limite_VALORE = new int[16384];
    static int[] locale_VALORE = new int[4096], locale_TIPO = new int[4096], operando_Pila_VALORE = new int[4096], operando_Pila_TIPO = new int[4096];
    static int[] frame_metodo = new int[32], frame_funzione = new int[32], frame_Pila = new int[32];
    static int[] heap_VALORE = new int[8192];
    static int Dimensione, 읽기위치, costante_CONTA_NUMERI, metodo_CONTA_NUMERI, nome_della_classe, frame_INDICE = -1, heap_chiudere_funzione = 1, tipo_restituito;
    static boolean errore;

    static void errore_VALORE(String Word_SMS) {
        if (!errore) { spazio_utente.Scrittura("JVM error: "); spazio_utente.Scrittura(Word_SMS); spazio_utente.scrivere_carattere_VALORE(10); }
        errore = true;
    }
    static boolean ritagliare(int avvia, int durata_VALORE) { return avvia >= 0 && durata_VALORE >= 0 && avvia <= Dimensione - durata_VALORE; }
    static int byte_VALORE() {
        if (!ritagliare(읽기위치, 1)) { errore_VALORE("truncated class file"); return 0; }
        return file[읽기위치++];
    }
    static int 짧은수() { return byte_VALORE() << 8 | byte_VALORE(); }
    static int intero() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int durata_VALORE) { if (!ritagliare(읽기위치, durata_VALORE)) errore_VALORE("invalid attribute size"); else 읽기위치 += durata_VALORE; }
    static boolean assegno_costante(int numero, int Kind_VALORE) {
        if (numero <= 0 || numero >= costante_CONTA_NUMERI || costante_tag[numero] != Kind_VALORE) { errore_VALORE("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean SMS_intervallo(int avvia, int durata_VALORE, String Word_SMS) {
        if (!ritagliare(avvia, durata_VALORE) || durata_VALORE != Word_SMS.length()) return false;
        for (int numero = 0; numero < durata_VALORE; numero++) if (file[avvia + numero] != Word_SMS.charAt(numero)) return false;
        return true;
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
    static void ignorare_attributo() {
        int articolo_CONTA_NUMERI = 짧은수();
        for (int numero = 0; numero < articolo_CONTA_NUMERI && !errore; numero++) { assegno_costante(짧은수(), 1); 건너(intero()); }
    }
    static int comando_durata(int VALORE) {
        if (VALORE == 16 || VALORE == 18 || VALORE == 21 || VALORE == 25 || VALORE == 54 || VALORE == 58 || VALORE == 188) return 2;
        if (VALORE == 17 || VALORE == 19 || VALORE == 132 || VALORE >= 153 && VALORE <= 167
            || VALORE >= 178 && VALORE <= 184 || VALORE == 187 || VALORE == 189 || VALORE == 192 || VALORE == 198 || VALORE == 199) return 3;
        if (VALORE >= 0 && VALORE <= 8 || VALORE >= 26 && VALORE <= 29 || VALORE >= 42 && VALORE <= 46 || VALORE == 50
            || VALORE >= 59 && VALORE <= 62 || VALORE >= 75 && VALORE <= 79 || VALORE == 83 || VALORE == 87 || VALORE == 89 || VALORE == 95
            || VALORE == 96 || VALORE == 100 || VALORE == 104 || VALORE == 108 || VALORE == 112 || VALORE == 116
            || VALORE == 120 || VALORE == 122 || VALORE == 124 || VALORE == 126 || VALORE == 128 || VALORE == 130
            || VALORE >= 145 && VALORE <= 147 || VALORE == 172 || VALORE == 176 || VALORE == 177 || VALORE == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (intero() != 0xcafebabe) errore_VALORE("not a class file");
        int 부판 = 짧은수(), versione_VALORE = 짧은수();
        if (versione_VALORE < 45 || versione_VALORE > 52 || 부판 != 0) errore_VALORE("supported class versions: 45..52, minor 0");
        costante_CONTA_NUMERI = 짧은수();
        if (costante_CONTA_NUMERI < 1 || costante_CONTA_NUMERI > 512) { errore_VALORE("constant pool limit (511)"); return; }
        for (int numero = 1; numero < costante_CONTA_NUMERI && !errore; numero++) {
            int Kind_VALORE = byte_VALORE(); costante_tag[numero] = Kind_VALORE;
            if (Kind_VALORE == 1) { costante_SECONDO_VALORE[numero] = 짧은수(); 상가[numero] = 읽기위치; 건너(costante_SECONDO_VALORE[numero]); }
            else if (Kind_VALORE == 3) 상가[numero] = intero();
            else if (Kind_VALORE == 7 || Kind_VALORE == 8) 상가[numero] = 짧은수();
            else if (Kind_VALORE == 9 || Kind_VALORE == 10 || Kind_VALORE == 12) { 상가[numero] = 짧은수(); costante_SECONDO_VALORE[numero] = 짧은수(); }
            else errore_VALORE("unsupported constant type");
        }
        int privilegio_VALORE = 짧은수();
        if ((privilegio_VALORE & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) errore_VALORE("unsupported class flags");
        nome_della_classe = nome_della_classe_SMS(짧은수());
        if (!Word_SMS(nome_della_classe_SMS(짧은수()), "java/lang/Object")) errore_VALORE("inheritance unsupported");
        if (짧은수() != 0) errore_VALORE("interfaces unsupported");
        if (짧은수() != 0) errore_VALORE("fields unsupported");
        metodo_CONTA_NUMERI = 짧은수();
        if (metodo_CONTA_NUMERI < 1 || metodo_CONTA_NUMERI > 32) { errore_VALORE("method count limit (32)"); return; }
        for (int numero = 0; numero < metodo_CONTA_NUMERI && !errore; numero++) {
            metodo_accesso[numero] = 짧은수(); metodo_nome_SMS[numero] = 짧은수(); metodo_TIPO[numero] = 짧은수();
            assegno_costante(metodo_nome_SMS[numero], 1); 서술읽기(numero);
            if ((metodo_accesso[numero] & (0x100 | 0x400 | 0x20)) != 0) errore_VALORE("native, abstract and synchronized methods unsupported");
            if ((metodo_accesso[numero] & 8) == 0 && !Word_SMS(metodo_nome_SMS[numero], "<init>")) errore_VALORE("instance methods unsupported");
            if (Word_SMS(metodo_nome_SMS[numero], "<clinit>")) errore_VALORE("class initializers unsupported");
            for (int frontale_VALORE = 0; frontale_VALORE < numero; frontale_VALORE++) if (collegamento_movimenti_Word(metodo_nome_SMS[frontale_VALORE], metodo_nome_SMS[numero]) && collegamento_movimenti_Word(metodo_TIPO[frontale_VALORE], metodo_TIPO[numero])) errore_VALORE("duplicate method");
            int articolo_CONTA_NUMERI = 짧은수();
            for (int valore_dell_attributo = 0; valore_dell_attributo < articolo_CONTA_NUMERI && !errore; valore_dell_attributo++) {
                int Nome = 짧은수(), durata_VALORE = intero(), avvia = 읽기위치;
                if (!ritagliare(avvia, durata_VALORE)) { errore_VALORE("truncated method attribute"); break; }
                if (Word_SMS(Nome, "Code")) {
                    if (metodo_START[numero] != 0) errore_VALORE("duplicate Code attribute");
                    metodo_Pila[numero] = 짧은수(); 함수지역[numero] = 짧은수(); int CODICE_durata = intero();
                    if (metodo_Pila[numero] > 128 || 함수지역[numero] > 128 || 함수지역[numero] < metodo_argomento_CONTA_NUMERI[numero]
                        || CODICE_durata < 1 || CODICE_durata > 8192) errore_VALORE("method memory limits exceeded");
                    metodo_START[numero] = 읽기위치; 건너(CODICE_durata); metodo_chiudere[numero] = 읽기위치;
                    if (짧은수() != 0) errore_VALORE("exception handlers unsupported");
                    ignorare_attributo();
                    if (읽기위치 != avvia + durata_VALORE) errore_VALORE("Code attribute size mismatch");
                } else 건너(durata_VALORE);
            }
            if (metodo_START[numero] == 0) errore_VALORE("missing Code attribute");
            int slot_voce = metodo_START[numero];
            while (slot_voce < metodo_chiudere[numero] && !errore) {
                int durata_VALORE = comando_durata(file[slot_voce]);
                if (durata_VALORE == 0 || durata_VALORE > metodo_chiudere[numero] - slot_voce) { errore_VALORE("unsupported or truncated bytecode"); break; }
                limite_VALORE[slot_voce] = numero + 1; slot_voce += durata_VALORE;
            }
            // 실행하지 않는 경로에도 잘못된 ramo 목적지를 허용하지 않는다.
            slot_voce = metodo_START[numero];
            while (slot_voce < metodo_chiudere[numero] && !errore) {
                int VALORE = file[slot_voce];
                if (VALORE >= 153 && VALORE <= 167 || VALORE == 198 || VALORE == 199) {
                    int meta_VALORE = slot_voce + (short)(file[slot_voce + 1] << 8 | file[slot_voce + 2]);
                    if (meta_VALORE < metodo_START[numero] || meta_VALORE >= metodo_chiudere[numero] || limite_VALORE[meta_VALORE] != numero + 1) errore_VALORE("invalid branch target");
                }
                slot_voce += comando_durata(VALORE);
            }
        }
        if (!errore) ignorare_attributo();
        if (읽기위치 != Dimensione) errore_VALORE("extra class file data");
    }
    static int allocare_Memoria(int Kind_VALORE, int durata_VALORE) {
        if (durata_VALORE < 0 || durata_VALORE > heap_VALORE.length - heap_chiudere_funzione - 2) { errore_VALORE("object heap exhausted or negative array size"); return 0; }
        int fonti = heap_chiudere_funzione; heap_chiudere_funzione += durata_VALORE + 2; heap_VALORE[fonti] = Kind_VALORE; heap_VALORE[fonti + 1] = durata_VALORE;
        return fonti;
    }
    static boolean oggetto_VALORE(int fonti, int Kind_VALORE) {
        if (fonti < 1 || fonti >= heap_chiudere_funzione - 1 || heap_VALORE[fonti] != Kind_VALORE) { errore_VALORE("null or invalid object reference"); return false; }
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
        if (frame_INDICE == 31) { errore_VALORE("call stack limit (32)"); return; }
        int Avanti_articolo = frame_INDICE + 1;
        for (int numero = 0; numero < 128; numero++) locale_TIPO[Avanti_articolo * 128 + numero] = 0;
        for (int numero = metodo_argomento_CONTA_NUMERI[FUNZIONE_VALORE] - 1; numero >= 0; numero--) {
            locale_VALORE[Avanti_articolo * 128 + numero] = 빼기(metodo_argomento_TIPO[FUNZIONE_VALORE * 16 + numero]); locale_TIPO[Avanti_articolo * 128 + numero] = metodo_argomento_TIPO[FUNZIONE_VALORE * 16 + numero];
        }
        frame_INDICE = Avanti_articolo; frame_metodo[frame_INDICE] = FUNZIONE_VALORE; frame_funzione[frame_INDICE] = metodo_START[FUNZIONE_VALORE]; frame_Pila[frame_INDICE] = 0;
    }
    static void Reso_KR(int TIPO_VALORE) {
        if (TIPO_VALORE != metodo_Reso[frame_metodo[frame_INDICE]]) { errore_VALORE("return type mismatch"); return; }
        int VALORE = TIPO_VALORE == 0 ? 0 : 빼기(TIPO_VALORE);
        frame_INDICE--; if (frame_INDICE >= 0 && TIPO_VALORE != 0) 넣기(VALORE, TIPO_VALORE);
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
                if (VALORE < 1 || VALORE > 127) { errore_VALORE("file stream paths currently require ASCII"); return; }
                Stream_nome_file[slot_voce] = VALORE;
            }
            Stream_nome_file[durata_VALORE] = 0;
            int descrittore_voce = spazio_utente.aperto_File_descrittore(Stream_nome_file, uscitaTesto ? (이어 ? 1089 : 577) : 0);
            if (descrittore_voce < 0) { errore_VALORE("FileNotFoundException: file open failed"); return; }
            heap_VALORE[Stream_VALORE + 2] = descrittore_voce; heap_VALORE[Stream_VALORE + 3] = 1;
            return;
        }
        if (comando != 182) { errore_VALORE("invalid file stream invocation"); return; }
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
            if (risultato < -1) errore_VALORE("IOException: read failed"); else 넣기(risultato, 1);
        } else if (spazio_utente.파일한바이트쓰기(descrittore_voce, VALORE) != 1) errore_VALORE("IOException: write failed");
    }
    static void Chiama_metodo(int INDICE, int comando) {
        if (!assegno_costante(INDICE, 10)) return;
        int proprietario_VALORE = nome_della_classe_SMS(상가[INDICE]), Nome = fonti_nome(costante_SECONDO_VALORE[INDICE]), formato_VALORE = tipo_riferimento(costante_SECONDO_VALORE[INDICE]);
        if (errore) return;
        if (collegamento_movimenti_Word(proprietario_VALORE, nome_della_classe)) {
            if (comando != 184) { errore_VALORE("only static user methods are supported"); return; }
            for (int numero = 0; numero < metodo_CONTA_NUMERI; numero++) if (collegamento_movimenti_Word(Nome, metodo_nome_SMS[numero]) && collegamento_movimenti_Word(formato_VALORE, metodo_TIPO[numero])) {
                if ((metodo_accesso[numero] & 8) == 0) errore_VALORE("method is not static"); else 호출(numero);
                return;
            }
            errore_VALORE("NoSuchMethodError"); return;
        }
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
        errore_VALORE("unsupported library method");
    }
    static int array_slot(int fonti, int pedice_VALORE, int TIPO_VALORE) {
        if (!oggetto_VALORE(fonti, TIPO_VALORE)) return 0;
        if (pedice_VALORE < 0 || pedice_VALORE >= heap_VALORE[fonti + 1]) { errore_VALORE("ArrayIndexOutOfBoundsException"); return 0; }
        return fonti + 2 + pedice_VALORE;
    }
    static void Esegui_comando() {
        int 남음 = 500000;
        while (frame_INDICE >= 0 && !errore) {
            if (--남음 == 0) { errore_VALORE("instruction limit (500000)"); break; }
            int avvia = frame_funzione[frame_INDICE], VALORE = 명바();
            if (errore) break;
            if (VALORE == 0) continue;
            if (VALORE == 1) { 넣기(0, 2); continue; }
            if (VALORE >= 2 && VALORE <= 8) { 넣기(VALORE - 3, 1); continue; }
            if (VALORE == 16) { 넣기((byte)명바(), 1); continue; }
            if (VALORE == 17) { 넣기((short)명짧(), 1); continue; }
            if (VALORE == 18 || VALORE == 19) {
                int numero = VALORE == 18 ? 명바() : 명짧();
                if (numero <= 0 || numero >= costante_CONTA_NUMERI) errore_VALORE("invalid ldc constant");
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
            if (VALORE == 46 || VALORE == 50) {
                int pedice_VALORE = 빼기(1), fonti = 빼기(2), slot_voce = array_slot(fonti, pedice_VALORE, VALORE == 46 ? 2 : 3);
                if (!errore) 넣기(heap_VALORE[slot_voce], VALORE == 46 ? 1 : 2); continue;
            }
            if (VALORE == 79 || VALORE == 83) {
                int articolo_elemento = 빼기(VALORE == 79 ? 1 : 2), pedice_VALORE = 빼기(1), fonti = 빼기(2), slot_voce = array_slot(fonti, pedice_VALORE, VALORE == 79 ? 2 : 3);
                if (VALORE == 83 && articolo_elemento != 0) oggetto_VALORE(articolo_elemento, 1);
                if (!errore) heap_VALORE[slot_voce] = articolo_elemento; continue;
            }
            if (VALORE == 87) { 빼기(0); continue; }
            if (VALORE == 89) { int 가 = 빼기(0), TIPO_VALORE = tipo_restituito; 넣기(가, TIPO_VALORE); 넣기(가, TIPO_VALORE); continue; }
            if (VALORE == 95) { int 가 = 빼기(0), 가형 = tipo_restituito, SECONDO_operando = 빼기(0), SECONDO_operando_TIPO = tipo_restituito; 넣기(가, 가형); 넣기(SECONDO_operando, SECONDO_operando_TIPO); continue; }
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
            if (VALORE == 178) {
                int numero = 명짧(); if (!assegno_costante(numero, 9)) continue;
                if (!Word_SMS(nome_della_classe_SMS(상가[numero]), "java/lang/System") || !Word_SMS(fonti_nome(costante_SECONDO_VALORE[numero]), "out")
                    || !Word_SMS(tipo_riferimento(costante_SECONDO_VALORE[numero]), "Ljava/io/PrintStream;")) errore_VALORE("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (VALORE == 182 || VALORE == 183 || VALORE == 184) { Chiama_metodo(명짧(), VALORE); continue; }
            if (VALORE == 187) {
                int Nome = nome_della_classe_SMS(명짧());
                if (Word_SMS(Nome, "java/lang/StringBuilder")) 넣기(allocare_Memoria(4, 1), 2);
                else if (Word_SMS(Nome, "java/io/FileInputStream") || Word_SMS(Nome, "java/io/FileOutputStream")) {
                    int fonti = allocare_Memoria(Word_SMS(Nome, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!errore) { heap_VALORE[fonti + 2] = -1; 넣기(fonti, 2); }
                } else errore_VALORE("unsupported object construction");
                continue;
            }
            if (VALORE == 188 || VALORE == 189) {
                if (VALORE == 188) { if (명바() != 10) errore_VALORE("only int[] newarray is supported"); }
                else if (!Word_SMS(nome_della_classe_SMS(명짧()), "java/lang/String")) errore_VALORE("only String[] anewarray is supported");
                int durata_VALORE = 빼기(1); 넣기(allocare_Memoria(VALORE == 188 ? 2 : 3, durata_VALORE), 2); continue;
            }
            if (VALORE == 190) {
                int fonti = 빼기(2);
                if (fonti < 1 || fonti >= heap_chiudere_funzione - 1 || (heap_VALORE[fonti] != 2 && heap_VALORE[fonti] != 3)) errore_VALORE("null or invalid array");
                else 넣기(heap_VALORE[fonti + 1], 1); continue;
            }
            if (VALORE == 192) {
                int Nome = nome_della_classe_SMS(명짧()), fonti = 빼기(2);
                if (!Word_SMS(Nome, "java/lang/String")) errore_VALORE("unsupported checkcast");
                else if (fonti != 0) oggetto_VALORE(fonti, 1);
                넣기(fonti, 2); continue;
            }
            errore_VALORE("unsupported bytecode");
        }
    }
    public static int avvia() {
        if (spazio_utente.인수개수() == 1 && 자바도구.같음(spazio_utente.argomenti(0), "-version")) {
            spazio_utente.Scrittura("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (spazio_utente.인수개수() < 1) { spazio_utente.Scrittura("Usage: java CLASS [ARGS]\n"); return 2; }
        int durata_VALORE = 자바도구.Nome(nome_file_SMS, spazio_utente.argomenti(0));
        if (durata_VALORE < 1 || durata_VALORE > 57) { spazio_utente.Scrittura("java: invalid class name\n"); return 2; }
        nome_file_SMS[durata_VALORE] = '.'; nome_file_SMS[durata_VALORE + 1] = 'c'; nome_file_SMS[durata_VALORE + 2] = 'l'; nome_file_SMS[durata_VALORE + 3] = 'a'; nome_file_SMS[durata_VALORE + 4] = 's'; nome_file_SMS[durata_VALORE + 5] = 's';
        Dimensione = spazio_utente.파일읽기(nome_file_SMS, file);
        if (Dimensione < 0) { spazio_utente.Scrittura("java: cannot read class: "); 자바도구.scrivere_numero(Dimensione); spazio_utente.scrivere_carattere_VALORE(10); return 1; }
        클래스읽기(); if (errore) return 1;
        int carattere_nome = costante_SMS(nome_della_classe);
        if (!errore && heap_VALORE[carattere_nome + 1] != durata_VALORE) errore_VALORE("class name does not match file");
        for (int numero = 0; numero < durata_VALORE && !errore; numero++) if (heap_VALORE[carattere_nome + 2 + numero] != nome_file_SMS[numero]) errore_VALORE("class name does not match file");
        int punto_di_ingresso_VALORE = -1;
        for (int numero = 0; numero < metodo_CONTA_NUMERI; numero++) if (Word_SMS(metodo_nome_SMS[numero], "main") && Word_SMS(metodo_TIPO[numero], "([Ljava/lang/String;)V") && (metodo_accesso[numero] & 9) == 9) punto_di_ingresso_VALORE = numero;
        if (punto_di_ingresso_VALORE < 0) errore_VALORE("public static void main(String[] args) required");
        if (errore) return 1;
        int argomenti = allocare_Memoria(3, spazio_utente.인수개수() - 1);
        for (int numero = 1; numero < spazio_utente.인수개수() && !errore; numero++) heap_VALORE[argomenti + 1 + numero] = host_carattere(spazio_utente.argomenti(numero));
        frame_INDICE = 0; frame_metodo[0] = punto_di_ingresso_VALORE; frame_funzione[0] = metodo_START[punto_di_ingresso_VALORE]; locale_VALORE[0] = argomenti; locale_TIPO[0] = 2;
        Esegui_comando(); return errore ? 1 : 0;
    }
}
