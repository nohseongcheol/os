// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java fonte_albero -> 표준 버전 49 class compilatore. */
public final class 자바컴파일러 {
    static int[] codiceSorgente = new int[16384], uscitaTesto = new int[16384], CODICE_VALORE = new int[4096];
    static int[] token_Kind = new int[2048], token_funzione = new int[2048], token_durata = new int[2048];
    static int[] costante_VALORE = new int[4096], costante_SCARTO = new int[512];
    static int[] 문자 = new int[512], nome_file_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int fonte_ridimensionare, token_CONTA_NUMERI, posizione, CODICE_ridimensionare, costante_ridimensionare, costante_CONTA_NUMERI = 1, output_ridimensionare, carattere_durata;
    static boolean errore;
    static int Corso_token, Corso_costante, padre_costante, CODICE_costante;
    static int[] metodo_voce_nome = new int[32], metodo_Reso = new int[32], metodo_argomento_CONTA_NUMERI = new int[32];
    static int[] metodo_argomento_nome = new int[512], metodo_argomento_TIPO = new int[512];
    static int[] corpo_del_metodo = new int[32], metodo_chiudere = new int[32], metodo_CODICE = new int[32];
    static int[] metodo_durata = new int[32], 함수지역 = new int[32], metodo_nome_costante = new int[32], metodo_descrittore_costante = new int[32];
    static int[] metodo_accesso = new int[32];
    static int metodo_CONTA_NUMERI, Regolari_metodo, locale_CONTA_NUMERI, 깊이, 식깊이;
    static int[] locale_nome = new int[128], locale_TIPO = new int[128], 지역깊이 = new int[128];

    static void errore_VALORE(String 이유) {
        if (!errore) {
            spazio_utente.Scrittura("javac error: "); spazio_utente.Scrittura(이유);
            spazio_utente.Scrittura(" at line ");
            int riga_di_ingresso = 1, 끝 = posizione < token_CONTA_NUMERI ? token_funzione[posizione] : fonte_ridimensionare;
            for (int numero = 0; numero < 끝; numero++) if (codiceSorgente[numero] == 10) riga_di_ingresso++;
            자바도구.scrivere_numero(riga_di_ingresso); spazio_utente.scrivere_carattere_VALORE(10);
        }
        errore = true;
    }
    static boolean carattere_VALORE(int VALORE) { return 문자이름규칙.첫글자(VALORE); }
    static boolean cifra_VALORE(int VALORE) { return VALORE >= '0' && VALORE <= '9'; }
    static boolean 이름같음(int 가, int SECONDO_operando) {
        if (가 < 0 || SECONDO_operando < 0 || 가 >= token_CONTA_NUMERI || SECONDO_operando >= token_CONTA_NUMERI || token_durata[가] != token_durata[SECONDO_operando]) return false;
        for (int numero = 0; numero < token_durata[가]; numero++) if (codiceSorgente[token_funzione[가] + numero] != codiceSorgente[token_funzione[SECONDO_operando] + numero]) return false;
        return true;
    }
    static boolean Word_VALORE(int token_VALORE, String Word_SMS) {
        if (token_VALORE < 0 || token_VALORE >= token_CONTA_NUMERI || token_durata[token_VALORE] != Word_SMS.length()) return false;
        for (int numero = 0; numero < Word_SMS.length(); numero++) if (codiceSorgente[token_funzione[token_VALORE] + numero] != Word_SMS.charAt(numero)) return false;
        return true;
    }
    static int Kind_VALORE() { return posizione < token_CONTA_NUMERI ? token_Kind[posizione] : 0; }
    static boolean ricevere(int VALORE) { if (Kind_VALORE() != VALORE) return false; posizione++; return true; }
    static void requisito_VALORE(int VALORE) { if (!ricevere(VALORE)) errore_VALORE("unexpected token"); }
    static boolean INCLUDI_Word(String Word_SMS) { if (!Word_VALORE(posizione, Word_SMS)) return false; posizione++; return true; }
    static void 말요구(String Word_SMS) { if (!INCLUDI_Word(Word_SMS)) errore_VALORE(Word_SMS); }
    static int identificatore_VALORE() {
        int risultato = posizione;
        if (Kind_VALORE() != 256) errore_VALORE("identifier required"); else posizione++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int avvia = 0;
        for (int numero = 0; numero <= 예약어.length(); numero++) {
            if (numero == 예약어.length() || 예약어.charAt(numero) == ' ') {
                boolean 같음 = numero - avvia == token_durata[risultato];
                for (int slot_voce = avvia; 같음 && slot_voce < numero; slot_voce++) if (예약어.charAt(slot_voce) != codiceSorgente[token_funzione[risultato] + slot_voce - avvia]) 같음 = false;
                if (같음) errore_VALORE("reserved word cannot be an identifier");
                avvia = numero + 1;
            }
        }
        return risultato;
    }
    static void tagliare_VALORE() {
        int numero = 0;
        while (numero < fonte_ridimensionare && !errore) {
            int VALORE = codiceSorgente[numero], avvia = numero, Kind_VALORE = VALORE;
            if (VALORE == 32 || VALORE == 9 || VALORE == 10 || VALORE == 13) { numero++; continue; }
            if (VALORE == '/' && numero + 1 < fonte_ridimensionare && codiceSorgente[numero + 1] == '/') {
                while (numero < fonte_ridimensionare && codiceSorgente[numero] != 10) numero++;
                continue;
            }
            if (VALORE == '/' && numero + 1 < fonte_ridimensionare && codiceSorgente[numero + 1] == '*') {
                numero += 2;
                while (numero + 1 < fonte_ridimensionare && !(codiceSorgente[numero] == '*' && codiceSorgente[numero + 1] == '/')) numero++;
                if (numero + 1 >= fonte_ridimensionare) { errore_VALORE("unterminated comment"); break; }
                numero += 2; continue;
            }
            if (carattere_VALORE(VALORE)) { Kind_VALORE = 256; while (numero < fonte_ridimensionare && 문자이름규칙.이어진글자(codiceSorgente[numero])) numero++; }
            else if (cifra_VALORE(VALORE)) { Kind_VALORE = 257; while (numero < fonte_ridimensionare && cifra_VALORE(codiceSorgente[numero])) numero++; }
            else if (VALORE == '"' || VALORE == '\'') {
                Kind_VALORE = VALORE == '"' ? 258 : 259; numero++;
                while (numero < fonte_ridimensionare && codiceSorgente[numero] != VALORE && codiceSorgente[numero] != 10 && codiceSorgente[numero] != 13) {
                    if (codiceSorgente[numero] == '\\') numero++;
                    numero++;
                }
                if (numero >= fonte_ridimensionare || codiceSorgente[numero] != VALORE) { errore_VALORE("unterminated literal"); break; }
                numero++;
            } else {
                numero++;
                if (numero < fonte_ridimensionare) {
                    int Avanti_articolo = codiceSorgente[numero];
                    if (VALORE == '=' && Avanti_articolo == '=') Kind_VALORE = 300;
                    if (VALORE == '!' && Avanti_articolo == '=') Kind_VALORE = 301;
                    if (VALORE == '<' && Avanti_articolo == '=') Kind_VALORE = 302;
                    if (VALORE == '>' && Avanti_articolo == '=') Kind_VALORE = 303;
                    if (VALORE == '&' && Avanti_articolo == '&') Kind_VALORE = 304;
                    if (VALORE == '|' && Avanti_articolo == '|') Kind_VALORE = 305;
                    if (VALORE == '+' && Avanti_articolo == '+') Kind_VALORE = 306;
                    if (VALORE == '-' && Avanti_articolo == '-') Kind_VALORE = 307;
                    if (VALORE == '+' && Avanti_articolo == '=') Kind_VALORE = 308;
                    if (VALORE == '-' && Avanti_articolo == '=') Kind_VALORE = 309;
                    if (VALORE == '*' && Avanti_articolo == '=') Kind_VALORE = 310;
                    if (VALORE == '/' && Avanti_articolo == '=') Kind_VALORE = 311;
                    if (VALORE == '%' && Avanti_articolo == '=') Kind_VALORE = 312;
                    if (Kind_VALORE >= 300) numero++;
                }
            }
            if (token_CONTA_NUMERI == token_Kind.length - 1) { errore_VALORE("too many tokens (2047 maximum)"); break; }
            token_Kind[token_CONTA_NUMERI] = Kind_VALORE; token_funzione[token_CONTA_NUMERI] = avvia; token_durata[token_CONTA_NUMERI++] = numero - avvia;
        }
    }
    static void scrivere_costante_byte(int VALORE) {
        if (costante_ridimensionare == costante_VALORE.length) { errore_VALORE("constant pool too large"); return; }
        costante_VALORE[costante_ridimensionare++] = VALORE & 255;
    }
    static void 상짧(int VALORE) { scrivere_costante_byte(VALORE >> 8); scrivere_costante_byte(VALORE); }
    static int registro_costante(int avvia) {
        for (int numero = 1; numero < costante_CONTA_NUMERI; numero++) {
            int frontale_VALORE = costante_SCARTO[numero], durata_VALORE = (numero + 1 < costante_CONTA_NUMERI ? costante_SCARTO[numero + 1] : avvia) - frontale_VALORE;
            if (durata_VALORE != costante_ridimensionare - avvia) continue;
            boolean 같음 = true;
            for (int slot_voce = 0; slot_voce < durata_VALORE; slot_voce++) if (costante_VALORE[frontale_VALORE + slot_voce] != costante_VALORE[avvia + slot_voce]) 같음 = false;
            if (같음) { costante_ridimensionare = avvia; return numero; }
        }
        if (costante_CONTA_NUMERI == costante_SCARTO.length) { errore_VALORE("too many constants"); return 0; }
        costante_SCARTO[costante_CONTA_NUMERI] = avvia;
        return costante_CONTA_NUMERI++;
    }
    static void Aggiunta_SMS(int VALORE) {
        if (carattere_durata == 문자.length) { errore_VALORE("text too long"); return; }
        문자[carattere_durata++] = VALORE;
    }
    static void Aggiunta_Word(String Word_SMS) { for (int numero = 0; numero < Word_SMS.length(); numero++) Aggiunta_SMS(Word_SMS.charAt(numero)); }
    static int carattere_costante() {
        int avvia = costante_ridimensionare; scrivere_costante_byte(1); 상짧(0);
        for (int numero = 0; numero < carattere_durata; numero++) {
            int VALORE = 문자[numero];
            if (VALORE > 0 && VALORE < 128) scrivere_costante_byte(VALORE);
            else if (VALORE < 2048) { scrivere_costante_byte(192 | VALORE >> 6); scrivere_costante_byte(128 | VALORE & 63); }
            else { scrivere_costante_byte(224 | VALORE >> 12); scrivere_costante_byte(128 | VALORE >> 6 & 63); scrivere_costante_byte(128 | VALORE & 63); }
        }
        if (errore) return 0;
        int durata_VALORE = costante_ridimensionare - avvia - 3;
        costante_VALORE[avvia + 1] = durata_VALORE >> 8; costante_VALORE[avvia + 2] = durata_VALORE & 255;
        return registro_costante(avvia);
    }
    static int Word_costante(String Word_SMS) { carattere_durata = 0; Aggiunta_Word(Word_SMS); return carattere_costante(); }
    static int token_costante(int token_VALORE) {
        carattere_durata = 0;
        for (int numero = 0; numero < token_durata[token_VALORE]; numero++) Aggiunta_SMS(codiceSorgente[token_funzione[token_VALORE] + numero]);
        return carattere_costante();
    }
    static int fonti(int Kind_VALORE, int 가, int SECONDO_operando) {
        int avvia = costante_ridimensionare; scrivere_costante_byte(Kind_VALORE); 상짧(가);
        if (Kind_VALORE == 9 || Kind_VALORE == 10 || Kind_VALORE == 12) 상짧(SECONDO_operando);
        return registro_costante(avvia);
    }
    static int esterno_fonti(int Kind_VALORE, String proprietario_VALORE, String Nome, String 서술) {
        int proprietario_identificatore = fonti(7, Word_costante(proprietario_VALORE), 0);
        int nome_CONTA_NUMERI = Word_costante(Nome), formato_CONTA_NUMERI = Word_costante(서술);
        return fonti(Kind_VALORE, proprietario_identificatore, fonti(12, nome_CONTA_NUMERI, formato_CONTA_NUMERI));
    }
    static void 내보내기(int VALORE) {
        if (CODICE_ridimensionare == CODICE_VALORE.length) { errore_VALORE("bytecode too large"); return; }
        CODICE_VALORE[CODICE_ridimensionare++] = VALORE & 255;
    }
    static void comando(int VALORE, int argomenti) { 내보내기(VALORE); 내보내기(argomenti >> 8); 내보내기(argomenti); }
    static void 수상수(int VALORE) {
        if (VALORE >= -1 && VALORE <= 5) { 내보내기(VALORE + 3); return; }
        int avvia = costante_ridimensionare; scrivere_costante_byte(3); 상짧(VALORE >>> 16); 상짧(VALORE);
        comando(19, registro_costante(avvia));
    }
    static int ramo(int comando) { int risultato = CODICE_ridimensionare; comando(comando, 0); return risultato; }
    static void link_VALORE(int ramo, int target_oggetto) {
        if (errore) return;
        int 거리 = target_oggetto - ramo;
        if (거리 < -32768 || 거리 > 32767 || ramo < 0 || ramo + 2 >= CODICE_ridimensionare) { errore_VALORE("invalid branch"); return; }
        CODICE_VALORE[ramo + 1] = 거리 >> 8 & 255; CODICE_VALORE[ramo + 2] = 거리 & 255;
    }
    static void Confronto_VALORE(int comando) {
        int VERO_VALORE = ramo(comando); 내보내기(3); int 끝 = ramo(167);
        link_VALORE(VERO_VALORE, CODICE_ridimensionare); 내보내기(4); link_VALORE(끝, CODICE_ridimensionare);
    }
    static int formato_VALORE() {
        if (INCLUDI_Word("void")) return 0;
        if (INCLUDI_Word("int")) return 1;
        if (INCLUDI_Word("boolean")) return 2;
        if (INCLUDI_Word("char")) return 5;
        if (INCLUDI_Word("FileInputStream")) return 6;
        if (INCLUDI_Word("FileOutputStream")) return 7;
        if (INCLUDI_Word("String")) { if (ricevere('[')) { requisito_VALORE(']'); return 4; } return 3; }
        errore_VALORE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Aggiungi_formato(int TIPO_VALORE) {
        if (TIPO_VALORE == 0) Aggiunta_SMS('V');
        if (TIPO_VALORE == 1) Aggiunta_SMS('I');
        if (TIPO_VALORE == 2) Aggiunta_SMS('Z');
        if (TIPO_VALORE == 3) Aggiunta_Word("Ljava/lang/String;");
        if (TIPO_VALORE == 4) Aggiunta_Word("[Ljava/lang/String;");
        if (TIPO_VALORE == 5) Aggiunta_SMS('C');
        if (TIPO_VALORE == 6) Aggiunta_Word("Ljava/io/FileInputStream;");
        if (TIPO_VALORE == 7) Aggiunta_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws dichiarazione. eccezione Processi_VALORE_voce 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = INCLUDI_Word("Italiano");
        if (한국어묶음) { requisito_VALORE('.'); 말요구("nativo"); requisito_VALORE('.'); }
        if (!한국어묶음 && (INCLUDI_Word("Exception") || INCLUDI_Word("IOException"))) return;
        if (INCLUDI_Word("eccezione") || INCLUDI_Word("esecuzione_eccezione") || INCLUDI_Word("I_O_eccezione") || INCLUDI_Word("aspetta_TIMEOUT_eccezione") || INCLUDI_Word("e_mail_CERCA_eccezione") || INCLUDI_Word("파일없음예외") || INCLUDI_Word("comunicazione_eccezione") || INCLUDI_Word("non_valida_argomento_eccezione") || INCLUDI_Word("numero_formato_errore") || INCLUDI_Word("범위예외") || INCLUDI_Word("배열범위예외") || INCLUDI_Word("문자열범위예외") || INCLUDI_Word("riferimento_Null_eccezione") || INCLUDI_Word("aritmetico_errore") || INCLUDI_Word("Stato_eccezione") || INCLUDI_Word("TIPO_cast_eccezione") || INCLUDI_Word("negativo_array_ridimensionare_errore") || INCLUDI_Word("array_Store_errore") || INCLUDI_Word("thread_Stato_eccezione") || INCLUDI_Word("대기중단예외")) return;
        errore_VALORE("unsupported throws type");
    }
    static void 선언읽기() {
        while (INCLUDI_Word("import")) {
            if (Word_VALORE(posizione, "Italiano")) 예외이름읽기();
            else {
                말요구("java"); requisito_VALORE('.'); 말요구("io"); requisito_VALORE('.');
                if (!(INCLUDI_Word("FileInputStream") || INCLUDI_Word("FileOutputStream") || INCLUDI_Word("IOException"))) errore_VALORE("unsupported import");
            }
            requisito_VALORE(';');
        }
        INCLUDI_Word("public"); INCLUDI_Word("final"); 말요구("class"); Corso_token = identificatore_VALORE();
        Corso_costante = fonti(7, token_costante(Corso_token), 0);
        padre_costante = fonti(7, Word_costante("java/lang/Object"), 0); CODICE_costante = Word_costante("Code"); requisito_VALORE('{');
        while (!errore && Kind_VALORE() != '}') {
            if (metodo_CONTA_NUMERI == 32) { errore_VALORE("too many methods"); break; }
            int accesso_voce = INCLUDI_Word("public") ? 1 : INCLUDI_Word("private") ? 2 : 0; 말요구("static");
            int FUNZIONE_VALORE = metodo_CONTA_NUMERI++;
            metodo_accesso[FUNZIONE_VALORE] = accesso_voce | 8;
            metodo_Reso[FUNZIONE_VALORE] = formato_VALORE(); metodo_voce_nome[FUNZIONE_VALORE] = identificatore_VALORE(); requisito_VALORE('(');
            for (int frontale_VALORE = 0; frontale_VALORE < FUNZIONE_VALORE; frontale_VALORE++) if (이름같음(metodo_voce_nome[frontale_VALORE], metodo_voce_nome[FUNZIONE_VALORE])) errore_VALORE("duplicate method (overloading unsupported)");
            while (!errore && Kind_VALORE() != ')') {
                int numero = metodo_argomento_CONTA_NUMERI[FUNZIONE_VALORE];
                if (numero == 16) { errore_VALORE("too many parameters"); break; }
                int TIPO_VALORE = formato_VALORE(); if (TIPO_VALORE == 0) errore_VALORE("void parameter");
                metodo_argomento_TIPO[FUNZIONE_VALORE * 16 + numero] = TIPO_VALORE; metodo_argomento_nome[FUNZIONE_VALORE * 16 + numero] = identificatore_VALORE();
                metodo_argomento_CONTA_NUMERI[FUNZIONE_VALORE]++;
                if (!ricevere(',')) break;
            }
            requisito_VALORE(')');
            if (INCLUDI_Word("throws")) {
                do { 예외이름읽기(); } while (!errore && ricevere(','));
            }
            corpo_del_metodo[FUNZIONE_VALORE] = posizione; requisito_VALORE('{');
            int annidamento_VALORE = 1;
            while (posizione < token_CONTA_NUMERI && annidamento_VALORE > 0) {
                if (Kind_VALORE() == '{') annidamento_VALORE++;
                if (Kind_VALORE() == '}') annidamento_VALORE--;
                posizione++;
            }
            if (annidamento_VALORE != 0) errore_VALORE("unclosed method body");
            metodo_chiudere[FUNZIONE_VALORE] = posizione;
            metodo_nome_costante[FUNZIONE_VALORE] = token_costante(metodo_voce_nome[FUNZIONE_VALORE]);
            carattere_durata = 0; Aggiunta_SMS('(');
            for (int numero = 0; numero < metodo_argomento_CONTA_NUMERI[FUNZIONE_VALORE]; numero++) Aggiungi_formato(metodo_argomento_TIPO[FUNZIONE_VALORE * 16 + numero]);
            Aggiunta_SMS(')'); Aggiungi_formato(metodo_Reso[FUNZIONE_VALORE]); metodo_descrittore_costante[FUNZIONE_VALORE] = carattere_costante();
        }
        requisito_VALORE('}'); if (posizione != token_CONTA_NUMERI) errore_VALORE("extra input after class");
    }
    static int TROVA_locale(int Nome) {
        for (int numero = locale_CONTA_NUMERI - 1; numero >= 0; numero--) if (지역깊이[numero] >= 0 && 이름같음(locale_nome[numero], Nome)) return numero;
        errore_VALORE("unknown variable"); return 0;
    }
    static int Aggiungi_locale(int Nome, int TIPO_VALORE) {
        for (int numero = 0; numero < locale_CONTA_NUMERI; numero++) if (지역깊이[numero] >= 0 && 이름같음(locale_nome[numero], Nome)) errore_VALORE("duplicate local variable");
        if (locale_CONTA_NUMERI == 128) { errore_VALORE("too many locals"); return 0; }
        locale_nome[locale_CONTA_NUMERI] = Nome; locale_TIPO[locale_CONTA_NUMERI] = TIPO_VALORE; 지역깊이[locale_CONTA_NUMERI] = 깊이;
        return locale_CONTA_NUMERI++;
    }
    static boolean intero_TIPO(int TIPO_VALORE) { return TIPO_VALORE == 1 || TIPO_VALORE == 5; }
    static void 지역읽기(int numero) { 내보내기(locale_TIPO[numero] <= 2 || locale_TIPO[numero] == 5 ? 21 : 25); 내보내기(numero); }
    static void scrivere_locale(int numero) { 내보내기(locale_TIPO[numero] <= 2 || locale_TIPO[numero] == 5 ? 54 : 58); 내보내기(numero); }
    static void verificare_TIPO(int effettivo_dati, int 기대) { if (effettivo_dati != 기대 && !(effettivo_dati == 5 && 기대 == 1)) errore_VALORE("type mismatch"); }
    static void 문자읽기(int token_VALORE) {
        carattere_durata = 0; int avvia = token_funzione[token_VALORE] + 1, 끝 = token_funzione[token_VALORE] + token_durata[token_VALORE] - 1;
        while (avvia < 끝 && !errore) {
            int VALORE = codiceSorgente[avvia++];
            if (VALORE == '\\') {
                if (avvia == 끝) { errore_VALORE("invalid escape"); break; }
                VALORE = codiceSorgente[avvia++];
                if (VALORE == 'n') VALORE = 10;
                else if (VALORE == 'r') VALORE = 13;
                else if (VALORE == 't') VALORE = 9;
                else if (VALORE == 'b') VALORE = 8;
                else if (VALORE == 'f') VALORE = 12;
                else if (VALORE != '\\' && VALORE != '"' && VALORE != '\'') errore_VALORE("unsupported escape");
            }
            Aggiunta_SMS(VALORE);
        }
    }
    static int analizzare_intero(int token_VALORE, boolean negativo_VALORE) {
        if (token_durata[token_VALORE] > 1 && codiceSorgente[token_funzione[token_VALORE]] == '0') errore_VALORE("octal literals unsupported");
        int VALORE = 0;
        for (int numero = 0; numero < token_durata[token_VALORE]; numero++) {
            int cifra_articolo = codiceSorgente[token_funzione[token_VALORE] + numero] - '0';
            if (VALORE < -214748364 || VALORE == -214748364 && cifra_articolo > (negativo_VALORE ? 8 : 7)) errore_VALORE("integer literal out of range");
            VALORE = VALORE * 10 - cifra_articolo;
        }
        return negativo_VALORE ? VALORE : -VALORE;
    }
    static int 기본식() {
        if (INCLUDI_Word("new")) {
            int TIPO_VALORE = formato_VALORE();
            if (TIPO_VALORE != 6 && TIPO_VALORE != 7) { errore_VALORE("only file streams supported by new in source"); return 0; }
            String proprietario_VALORE = TIPO_VALORE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            comando(187, fonti(7, Word_costante(proprietario_VALORE), 0)); 내보내기(89);
            requisito_VALORE('('); verificare_TIPO(espressione_VALORE(), 3); boolean 이어 = false;
            if (ricevere(',')) { if (TIPO_VALORE != 7) errore_VALORE("input stream constructor arguments"); verificare_TIPO(espressione_VALORE(), 2); 이어 = true; }
            requisito_VALORE(')');
            comando(183, esterno_fonti(10, proprietario_VALORE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TIPO_VALORE;
        }
        if (ricevere('(')) { int TIPO_VALORE = espressione_VALORE(); requisito_VALORE(')'); return TIPO_VALORE; }
        if (Kind_VALORE() == 257) { 수상수(analizzare_intero(posizione++, false)); return 1; }
        if (Kind_VALORE() == 258) { 문자읽기(posizione++); comando(19, fonti(8, carattere_costante(), 0)); return 3; }
        if (Kind_VALORE() == 259) { 문자읽기(posizione++); if (carattere_durata != 1) errore_VALORE("character literal length"); 수상수(문자[0]); return 5; }
        if (INCLUDI_Word("true")) { 내보내기(4); return 2; }
        if (INCLUDI_Word("false")) { 내보내기(3); return 2; }
        if (INCLUDI_Word("Italiano")) {
            requisito_VALORE('.'); 말요구("nativo"); requisito_VALORE('.');
            String proprietario_VALORE = "", metodo_VALORE = "", 서술 = ""; int 가 = 0, SECONDO_operando = 0, 다 = 0, 라 = 0, 마 = 0, risultato = 0;
            if (INCLUDI_Word("uscitaTesto")) {
                proprietario_VALORE = "Italiano/nativo/uscitaTesto"; requisito_VALORE('.');
                if (INCLUDI_Word("scrivere_riga")) { metodo_VALORE = "scrivere_riga"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (INCLUDI_Word("Scrittura")) { metodo_VALORE = "Scrittura"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (INCLUDI_Word("scrivere_numero")) { metodo_VALORE = "scrivere_numero"; 서술 = "(I)V"; 가 = 1; }
                else errore_VALORE("unknown Korean output method");
            } else if (INCLUDI_Word("문자")) {
                proprietario_VALORE = "Italiano/nativo/문자"; requisito_VALORE('.'); 가 = 3;
                if (INCLUDI_Word("durata_VALORE")) { metodo_VALORE = "durata_VALORE"; 서술 = "(Ljava/lang/String;)I"; risultato = 1; }
                else if (INCLUDI_Word("punto_di_codice_CONTA_NUMERI")) { metodo_VALORE = "punto_di_codice_CONTA_NUMERI"; 서술 = "(Ljava/lang/String;)I"; risultato = 1; }
                else if (INCLUDI_Word("analizzare_intero")) { metodo_VALORE = "analizzare_intero"; 서술 = "(Ljava/lang/String;)I"; risultato = 1; }
                else if (INCLUDI_Word("scrivere_intero_VALORE")) { metodo_VALORE = "scrivere_intero_VALORE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; risultato = 3; }
                else if (INCLUDI_Word("같음")) { metodo_VALORE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECONDO_operando = 3; risultato = 2; }
                else if (INCLUDI_Word("incollare_SMS")) { metodo_VALORE = "incollare_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECONDO_operando = 3; risultato = 3; }
                else if (INCLUDI_Word("tagliare_VALORE")) { metodo_VALORE = "tagliare_VALORE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECONDO_operando = 1; 다 = 1; risultato = 3; }
                else errore_VALORE("unknown Korean text method");
            } else if (INCLUDI_Word("file")) {
                proprietario_VALORE = "Italiano/nativo/file"; requisito_VALORE('.'); 가 = 3;
                if (INCLUDI_Word("Lettura")) { metodo_VALORE = "Lettura"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; risultato = 3; }
                else if (INCLUDI_Word("Scrittura")) { metodo_VALORE = "Scrittura"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECONDO_operando = 3; }
                else errore_VALORE("unknown Korean file method");
            } else if (INCLUDI_Word("schermata")) {
                proprietario_VALORE = "Italiano/nativo/schermata"; requisito_VALORE('.');
                if (INCLUDI_Word("너비")) { metodo_VALORE = "너비"; 서술 = "()I"; risultato = 1; }
                else if (INCLUDI_Word("altezza_VALORE")) { metodo_VALORE = "altezza_VALORE"; 서술 = "()I"; risultato = 1; }
                else if (INCLUDI_Word("rettangolo")) { metodo_VALORE = "rettangolo"; 서술 = "(IIIII)V"; 가 = 1; SECONDO_operando = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (INCLUDI_Word("cancellare_voce")) { metodo_VALORE = "cancellare_voce"; 서술 = "(I)V"; 가 = 1; }
                else if (INCLUDI_Word("기다리기")) { metodo_VALORE = "기다리기"; 서술 = "()V"; }
                else errore_VALORE("unknown Korean framebuffer method");
            } else errore_VALORE("unsupported Korean library class");
            requisito_VALORE('('); if (가 != 0) verificare_TIPO(espressione_VALORE(), 가);
            if (SECONDO_operando != 0) { requisito_VALORE(','); verificare_TIPO(espressione_VALORE(), SECONDO_operando); }
            if (다 != 0) { requisito_VALORE(','); verificare_TIPO(espressione_VALORE(), 다); }
            if (라 != 0) { requisito_VALORE(','); verificare_TIPO(espressione_VALORE(), 라); }
            if (마 != 0) { requisito_VALORE(','); verificare_TIPO(espressione_VALORE(), 마); }
            requisito_VALORE(')'); comando(184, esterno_fonti(10, proprietario_VALORE, metodo_VALORE, 서술)); return risultato;
        }
        if (INCLUDI_Word("Integer")) {
            requisito_VALORE('.'); 말요구("parseInt"); requisito_VALORE('('); verificare_TIPO(espressione_VALORE(), 3); requisito_VALORE(')');
            comando(184, esterno_fonti(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Nome = identificatore_VALORE();
        if (ricevere('(')) {
            int FUNZIONE_VALORE = -1;
            for (int numero = 0; numero < metodo_CONTA_NUMERI; numero++) if (이름같음(Nome, metodo_voce_nome[numero])) FUNZIONE_VALORE = numero;
            if (FUNZIONE_VALORE < 0) { errore_VALORE("unknown static method"); return 0; }
            int numero = 0;
            while (!errore && Kind_VALORE() != ')') {
                if (numero >= metodo_argomento_CONTA_NUMERI[FUNZIONE_VALORE]) { errore_VALORE("too many arguments"); break; }
                verificare_TIPO(espressione_VALORE(), metodo_argomento_TIPO[FUNZIONE_VALORE * 16 + numero++]); if (!ricevere(',')) break;
            }
            requisito_VALORE(')'); if (numero != metodo_argomento_CONTA_NUMERI[FUNZIONE_VALORE]) errore_VALORE("argument count mismatch");
            comando(184, fonti(10, Corso_costante, fonti(12, metodo_nome_costante[FUNZIONE_VALORE], metodo_descrittore_costante[FUNZIONE_VALORE])));
            return metodo_Reso[FUNZIONE_VALORE];
        }
        int locale_Scope = TROVA_locale(Nome), TIPO_VALORE = locale_TIPO[locale_Scope]; 지역읽기(locale_Scope);
        while (!errore) {
            if (ricevere('[')) { verificare_TIPO(TIPO_VALORE, 4); verificare_TIPO(espressione_VALORE(), 1); requisito_VALORE(']'); 내보내기(50); TIPO_VALORE = 3; }
            else if (ricevere('.')) {
                if (TIPO_VALORE == 6 || TIPO_VALORE == 7) {
                    String proprietario_VALORE = TIPO_VALORE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (INCLUDI_Word("close")) { requisito_VALORE('('); requisito_VALORE(')'); comando(182, esterno_fonti(10, proprietario_VALORE, "close", "()V")); TIPO_VALORE = 0; }
                    else if (TIPO_VALORE == 6 && INCLUDI_Word("read")) { requisito_VALORE('('); requisito_VALORE(')'); comando(182, esterno_fonti(10, proprietario_VALORE, "read", "()I")); TIPO_VALORE = 1; }
                    else if (TIPO_VALORE == 7 && INCLUDI_Word("write")) { requisito_VALORE('('); verificare_TIPO(espressione_VALORE(), 1); requisito_VALORE(')'); comando(182, esterno_fonti(10, proprietario_VALORE, "write", "(I)V")); TIPO_VALORE = 0; }
                    else { errore_VALORE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TIPO_VALORE == 4) { 내보내기(190); TIPO_VALORE = 1; }
                else { verificare_TIPO(TIPO_VALORE, 3); requisito_VALORE('('); requisito_VALORE(')'); comando(182, esterno_fonti(10, "java/lang/String", "length", "()I")); TIPO_VALORE = 1; }
            } else break;
        }
        return TIPO_VALORE;
    }
    static int 단항() {
        if (++식깊이 > 64) { errore_VALORE("expression nesting too deep"); 식깊이--; return 0; }
        int TIPO_VALORE;
        if (ricevere('!')) { verificare_TIPO(단항(), 2); Confronto_VALORE(153); TIPO_VALORE = 2; }
        else if (ricevere('-')) {
            if (Kind_VALORE() == 257) 수상수(analizzare_intero(posizione++, true));
            else { verificare_TIPO(단항(), 1); 내보내기(116); }
            TIPO_VALORE = 1;
        } else if (ricevere('+')) { verificare_TIPO(단항(), 1); TIPO_VALORE = 1; }
        else TIPO_VALORE = 기본식();
        식깊이--; return TIPO_VALORE;
    }
    static int 곱식() {
        int TIPO_VALORE = 단항();
        while (!errore && (Kind_VALORE() == '*' || Kind_VALORE() == '/' || Kind_VALORE() == '%')) {
            int Codifica_VALORE = Kind_VALORE(); posizione++; verificare_TIPO(TIPO_VALORE, 1); verificare_TIPO(단항(), 1);
            내보내기(Codifica_VALORE == '*' ? 104 : Codifica_VALORE == '/' ? 108 : 112); TIPO_VALORE = 1;
        }
        return TIPO_VALORE;
    }
    static int 합식() {
        int TIPO_VALORE = 곱식();
        while (!errore && (Kind_VALORE() == '+' || Kind_VALORE() == '-')) {
            int Codifica_VALORE = Kind_VALORE(); posizione++; int limite_VALORE = CODICE_ridimensionare, BACK_tipo_valore = 곱식();
            if (Codifica_VALORE == '+' && (TIPO_VALORE == 3 || BACK_tipo_valore == 3)) { 결합(limite_VALORE, TIPO_VALORE, BACK_tipo_valore); TIPO_VALORE = 3; }
            else { verificare_TIPO(TIPO_VALORE, 1); verificare_TIPO(BACK_tipo_valore, 1); 내보내기(Codifica_VALORE == '+' ? 96 : 100); TIPO_VALORE = 1; }
        }
        return TIPO_VALORE;
    }
    static int collegato_fonti(int TIPO_VALORE) {
        if (TIPO_VALORE != 1 && TIPO_VALORE != 2 && TIPO_VALORE != 3 && TIPO_VALORE != 5) errore_VALORE("unsupported concatenation type");
        return esterno_fonti(10, "java/lang/StringBuilder", "append", TIPO_VALORE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TIPO_VALORE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TIPO_VALORE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int limite_VALORE, int frontale_tipo_valore, int BACK_tipo_valore) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 DESTRA CODICE_VALORE 앞에 generare 코드를 삽입한다.
        // DESTRA espressione_VALORE 내부의 peer_VALORE ramo 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODICE_ridimensionare;
        comando(187, fonti(7, Word_costante("java/lang/StringBuilder"), 0)); 내보내기(89);
        comando(183, esterno_fonti(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); comando(182, collegato_fonti(frontale_tipo_valore));
        if (errore) return;
        int durata_VALORE = CODICE_ridimensionare - 끝;
        for (int numero = 0; numero < durata_VALORE; numero++) 삽입코드[numero] = CODICE_VALORE[끝 + numero];
        for (int numero = 끝 - 1; numero >= limite_VALORE; numero--) CODICE_VALORE[numero + durata_VALORE] = CODICE_VALORE[numero];
        for (int numero = 0; numero < durata_VALORE; numero++) CODICE_VALORE[limite_VALORE + numero] = 삽입코드[numero];
        comando(182, collegato_fonti(BACK_tipo_valore)); comando(182, esterno_fonti(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Confronto_espressione() {
        int TIPO_VALORE = 합식();
        while (!errore && (Kind_VALORE() == '<' || Kind_VALORE() == '>' || Kind_VALORE() == 302 || Kind_VALORE() == 303)) {
            int Codifica_VALORE = Kind_VALORE(); posizione++; verificare_TIPO(TIPO_VALORE, 1); verificare_TIPO(합식(), 1);
            Confronto_VALORE(Codifica_VALORE == '<' ? 161 : Codifica_VALORE == '>' ? 163 : Codifica_VALORE == 302 ? 164 : 162); TIPO_VALORE = 2;
        }
        return TIPO_VALORE;
    }
    static int 동등식() {
        int TIPO_VALORE = Confronto_espressione();
        while (!errore && (Kind_VALORE() == 300 || Kind_VALORE() == 301)) {
            int Codifica_VALORE = Kind_VALORE(); posizione++; int BACK_tipo_valore = Confronto_espressione();
            if (TIPO_VALORE == 0 || BACK_tipo_valore == 0) errore_VALORE("void expression");
            if (!(intero_TIPO(TIPO_VALORE) && intero_TIPO(BACK_tipo_valore))) verificare_TIPO(BACK_tipo_valore, TIPO_VALORE);
            Confronto_VALORE((TIPO_VALORE <= 2 || TIPO_VALORE == 5 ? 159 : 165) + (Codifica_VALORE == 301 ? 1 : 0)); TIPO_VALORE = 2;
        }
        return TIPO_VALORE;
    }
    static int AND() {
        int TIPO_VALORE = 동등식();
        while (!errore && ricevere(304)) {
            verificare_TIPO(TIPO_VALORE, 2); int 가 = ramo(153); verificare_TIPO(동등식(), 2); int SECONDO_operando = ramo(153);
            내보내기(4); int 끝 = ramo(167); link_VALORE(가, CODICE_ridimensionare); link_VALORE(SECONDO_operando, CODICE_ridimensionare); 내보내기(3); link_VALORE(끝, CODICE_ridimensionare); TIPO_VALORE = 2;
        }
        return TIPO_VALORE;
    }
    static int espressione_VALORE() {
        int TIPO_VALORE = AND();
        while (!errore && ricevere(305)) {
            verificare_TIPO(TIPO_VALORE, 2); int 가 = ramo(154); verificare_TIPO(AND(), 2); int SECONDO_operando = ramo(154);
            내보내기(3); int 끝 = ramo(167); link_VALORE(가, CODICE_ridimensionare); link_VALORE(SECONDO_operando, CODICE_ridimensionare); 내보내기(4); link_VALORE(끝, CODICE_ridimensionare); TIPO_VALORE = 2;
        }
        return TIPO_VALORE;
    }
    static void lab_VALORE(boolean Consenti_dichiarazione) {
        if (Word_VALORE(posizione, "int") || Word_VALORE(posizione, "boolean") || Word_VALORE(posizione, "String") || Word_VALORE(posizione, "char")
            || Word_VALORE(posizione, "FileInputStream") || Word_VALORE(posizione, "FileOutputStream")) {
            if (!Consenti_dichiarazione) errore_VALORE("declaration not allowed here");
            int TIPO_VALORE = formato_VALORE(), Nome = identificatore_VALORE(); requisito_VALORE('='); verificare_TIPO(espressione_VALORE(), TIPO_VALORE);
            scrivere_locale(Aggiungi_locale(Nome, TIPO_VALORE)); return;
        }
        int Nome = identificatore_VALORE(), locale_Scope = TROVA_locale(Nome);
        if (ricevere('=')) { verificare_TIPO(espressione_VALORE(), locale_TIPO[locale_Scope]); scrivere_locale(locale_Scope); }
        else if (Kind_VALORE() >= 308 && Kind_VALORE() <= 312) {
            int Codifica_VALORE = Kind_VALORE(); posizione++; 지역읽기(locale_Scope); int limite_VALORE = CODICE_ridimensionare, BACK_tipo_valore = espressione_VALORE();
            if (Codifica_VALORE == 308 && locale_TIPO[locale_Scope] == 3) 결합(limite_VALORE, 3, BACK_tipo_valore);
            else {
                verificare_TIPO(locale_TIPO[locale_Scope], 1); verificare_TIPO(BACK_tipo_valore, 1);
                내보내기(Codifica_VALORE == 308 ? 96 : Codifica_VALORE == 309 ? 100 : Codifica_VALORE == 310 ? 104 : Codifica_VALORE == 311 ? 108 : 112);
                if (locale_TIPO[locale_Scope] == 5) 내보내기(146);
            }
            scrivere_locale(locale_Scope);
        }
        else if (Kind_VALORE() == 306 || Kind_VALORE() == 307) {
            verificare_TIPO(locale_TIPO[locale_Scope], 1); 내보내기(132); 내보내기(locale_Scope); 내보내기(Kind_VALORE() == 306 ? 1 : 255); posizione++;
            if (locale_TIPO[locale_Scope] == 5) { 지역읽기(locale_Scope); 내보내기(146); scrivere_locale(locale_Scope); }
        } else errore_VALORE("assignment or postfix increment required");
    }
    static void schermata_output() {
        말요구("System"); requisito_VALORE('.'); 말요구("out"); requisito_VALORE('.');
        boolean 줄바꿈 = INCLUDI_Word("println"); if (!줄바꿈) 말요구("print"); requisito_VALORE('(');
        comando(178, esterno_fonti(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean vuota_argomento = Kind_VALORE() == ')';
        int TIPO_VALORE = vuota_argomento ? 0 : espressione_VALORE(); requisito_VALORE(')'); requisito_VALORE(';');
        String 서술 = TIPO_VALORE == 0 ? "()V" : TIPO_VALORE == 1 ? "(I)V" : TIPO_VALORE == 2 ? "(Z)V" : TIPO_VALORE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TIPO_VALORE == 4 || TIPO_VALORE >= 6 || TIPO_VALORE == 0 && (!줄바꿈 || !vuota_argomento)) errore_VALORE("unsupported print argument");
        comando(182, esterno_fonti(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean istruzione_VALORE() {
        if (errore) return false;
        if (깊이 > 32) { errore_VALORE("statement nesting too deep"); return false; }
        if (ricevere('{')) {
            깊이++; boolean Reso_KR = false;
            while (!errore && Kind_VALORE() != '}') { if (Reso_KR) errore_VALORE("unreachable statement"); Reso_KR = istruzione_VALORE(); }
            requisito_VALORE('}'); for (int numero = 0; numero < locale_CONTA_NUMERI; numero++) if (지역깊이[numero] == 깊이) 지역깊이[numero] = -1;
            깊이--; return Reso_KR;
        }
        if (ricevere(';')) return false;
        if (INCLUDI_Word("return")) {
            int TIPO_VALORE = Kind_VALORE() == ';' ? 0 : espressione_VALORE(); verificare_TIPO(TIPO_VALORE, metodo_Reso[Regolari_metodo]); requisito_VALORE(';');
            내보내기(TIPO_VALORE == 0 ? 177 : TIPO_VALORE <= 2 || TIPO_VALORE == 5 ? 172 : 176); return true;
        }
        if (INCLUDI_Word("if")) {
            requisito_VALORE('('); verificare_TIPO(espressione_VALORE(), 2); requisito_VALORE(')'); int FALSO_VALORE = ramo(153);
            깊이++; boolean 가 = controllo_istruzione(); 깊이--;
            if (INCLUDI_Word("else")) { int 끝 = ramo(167); link_VALORE(FALSO_VALORE, CODICE_ridimensionare); 깊이++; boolean SECONDO_operando = controllo_istruzione(); 깊이--; link_VALORE(끝, CODICE_ridimensionare); return 가 && SECONDO_operando; }
            link_VALORE(FALSO_VALORE, CODICE_ridimensionare); return false;
        }
        if (INCLUDI_Word("while")) {
            int avvia = CODICE_ridimensionare; requisito_VALORE('('); verificare_TIPO(espressione_VALORE(), 2); requisito_VALORE(')'); int 끝 = ramo(153);
            깊이++; controllo_istruzione(); 깊이--; link_VALORE(ramo(167), avvia); link_VALORE(끝, CODICE_ridimensionare); return false;
        }
        if (INCLUDI_Word("for")) {
            깊이++; requisito_VALORE('('); if (Kind_VALORE() != ';') lab_VALORE(true); requisito_VALORE(';');
            int condizione = CODICE_ridimensionare; if (Kind_VALORE() == ';') 내보내기(4); else verificare_TIPO(espressione_VALORE(), 2); requisito_VALORE(';');
            int 끝 = ramo(153), corpo_del_testo = ramo(167), aggiornare = CODICE_ridimensionare;
            if (Kind_VALORE() != ')') lab_VALORE(false); requisito_VALORE(')'); link_VALORE(ramo(167), condizione); link_VALORE(corpo_del_testo, CODICE_ridimensionare);
            controllo_istruzione(); link_VALORE(ramo(167), aggiornare); link_VALORE(끝, CODICE_ridimensionare);
            for (int numero = 0; numero < locale_CONTA_NUMERI; numero++) if (지역깊이[numero] == 깊이) 지역깊이[numero] = -1;
            깊이--; return false;
        }
        if (Word_VALORE(posizione, "System")) { schermata_output(); return false; }
        if (Kind_VALORE() == 256 && posizione + 1 < token_CONTA_NUMERI && (token_Kind[posizione + 1] == '(' || token_Kind[posizione + 1] == '.')) {
            int TIPO_VALORE = espressione_VALORE(); if (TIPO_VALORE != 0) 내보내기(87); requisito_VALORE(';'); return false;
        }
        lab_VALORE(true); requisito_VALORE(';'); return false;
    }
    static boolean controllo_istruzione() {
        if (Word_VALORE(posizione, "int") || Word_VALORE(posizione, "boolean") || Word_VALORE(posizione, "char") || Word_VALORE(posizione, "String")
            || Word_VALORE(posizione, "FileInputStream") || Word_VALORE(posizione, "FileOutputStream")) errore_VALORE("local declaration requires braces");
        return istruzione_VALORE();
    }
    static void 출바(int VALORE) { if (output_ridimensionare == uscitaTesto.length) errore_VALORE("class file too large"); else uscitaTesto[output_ridimensionare++] = VALORE & 255; }
    static void 출짧(int VALORE) { 출바(VALORE >> 8); 출바(VALORE); }
    static void 출정(int VALORE) { 출짧(VALORE >>> 16); 출짧(VALORE); }
    static void scrivere_Corso() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(costante_CONTA_NUMERI);
        for (int numero = 0; numero < costante_ridimensionare; numero++) 출바(costante_VALORE[numero]);
        출짧(0x21); 출짧(Corso_costante); 출짧(padre_costante); 출짧(0); 출짧(0); 출짧(metodo_CONTA_NUMERI);
        for (int numero = 0; numero < metodo_CONTA_NUMERI; numero++) {
            출짧(metodo_accesso[numero]); 출짧(metodo_nome_costante[numero]); 출짧(metodo_descrittore_costante[numero]); 출짧(1); 출짧(CODICE_costante);
            출정(12 + metodo_durata[numero]); 출짧(128); 출짧(함수지역[numero]); 출정(metodo_durata[numero]);
            for (int slot_voce = 0; slot_voce < metodo_durata[numero]; slot_voce++) 출바(CODICE_VALORE[metodo_CODICE[numero] + slot_voce]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int avvia() {
        if (spazio_utente.인수개수() == 1 && 자바도구.같음(spazio_utente.argomenti(0), "-version")) {
            spazio_utente.Scrittura("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (spazio_utente.인수개수() != 1) { spazio_utente.Scrittura("Usage: javac FILE.java\n"); return 2; }
        int nome_ridimensionare = 자바도구.Nome(nome_file_SMS, spazio_utente.argomenti(0));
        if (nome_ridimensionare < 6 || nome_ridimensionare > 62 || nome_file_SMS[nome_ridimensionare - 5] != '.' || nome_file_SMS[nome_ridimensionare - 4] != 'j'
            || nome_file_SMS[nome_ridimensionare - 3] != 'a' || nome_file_SMS[nome_ridimensionare - 2] != 'v' || nome_file_SMS[nome_ridimensionare - 1] != 'a') {
            spazio_utente.Scrittura("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        fonte_ridimensionare = spazio_utente.파일읽기(nome_file_SMS, codiceSorgente);
        if (fonte_ridimensionare < 0) { spazio_utente.Scrittura("javac: cannot read source: "); 자바도구.scrivere_numero(fonte_ridimensionare); spazio_utente.scrivere_carattere_VALORE(10); return 1; }
        fonte_ridimensionare = 자바도구.원문해독(codiceSorgente, fonte_ridimensionare);
        if (fonte_ridimensionare < 0) { spazio_utente.Scrittura("javac error: invalid UTF-8 source\n"); return 1; }
        tagliare_VALORE(); if (!errore) 선언읽기();
        if (!errore) {
            if (token_durata[Corso_token] != nome_ridimensionare - 5) errore_VALORE("class name must match file name");
            for (int numero = 0; numero < nome_ridimensionare - 5; numero++) if (codiceSorgente[token_funzione[Corso_token] + numero] != nome_file_SMS[numero]) errore_VALORE("class name must match file name");
        }
        for (Regolari_metodo = 0; Regolari_metodo < metodo_CONTA_NUMERI && !errore; Regolari_metodo++) {
            posizione = corpo_del_metodo[Regolari_metodo]; metodo_CODICE[Regolari_metodo] = CODICE_ridimensionare; locale_CONTA_NUMERI = 0; 깊이 = 0;
            for (int numero = 0; numero < metodo_argomento_CONTA_NUMERI[Regolari_metodo]; numero++) Aggiungi_locale(metodo_argomento_nome[Regolari_metodo * 16 + numero], metodo_argomento_TIPO[Regolari_metodo * 16 + numero]);
            boolean Reso_KR = istruzione_VALORE();
            if (!Reso_KR && metodo_Reso[Regolari_metodo] != 0) errore_VALORE("missing return");
            // ramo 뒤의 합류 지점은 반드시 effettivo_dati 명령이어야 한다 (버전 49 검증기).
            if (metodo_Reso[Regolari_metodo] == 0) 내보내기(177);
            else { boolean intero = metodo_Reso[Regolari_metodo] <= 2 || metodo_Reso[Regolari_metodo] == 5; 내보내기(intero ? 3 : 1); 내보내기(intero ? 172 : 176); }
            if (posizione != metodo_chiudere[Regolari_metodo]) errore_VALORE("invalid method body");
            함수지역[Regolari_metodo] = locale_CONTA_NUMERI; metodo_durata[Regolari_metodo] = CODICE_ridimensionare - metodo_CODICE[Regolari_metodo];
        }
        if (errore) return 1;
        scrivere_Corso(); if (errore) return 1;
        nome_file_SMS[nome_ridimensionare - 4] = 'c'; nome_file_SMS[nome_ridimensionare - 3] = 'l'; nome_file_SMS[nome_ridimensionare - 2] = 'a';
        nome_file_SMS[nome_ridimensionare - 1] = 's'; nome_file_SMS[nome_ridimensionare] = 's'; nome_file_SMS[nome_ridimensionare + 1] = 0;
        int risultato = spazio_utente.scrivere_File(nome_file_SMS, uscitaTesto, output_ridimensionare);
        if (risultato < 0) { spazio_utente.Scrittura("javac: cannot save class: "); 자바도구.scrivere_numero(risultato); spazio_utente.scrivere_carattere_VALORE(10); return 1; }
        spazio_utente.Scrittura("Compiled: "); for (int numero = 0; nome_file_SMS[numero] != 0; numero++) spazio_utente.scrivere_carattere_VALORE(nome_file_SMS[numero]);
        spazio_utente.Scrittura(" (JVM class version 49)\n"); return 0;
    }
}
