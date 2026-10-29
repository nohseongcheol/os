// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java bron_structuur -> 표준 버전 49 class compiler. */
public final class 자바컴파일러 {
    static int[] broncode = new int[16384], tekstuitvoer = new int[16384], CODE_WAARDE = new int[4096];
    static int[] token_soort = new int[2048], token_functie = new int[2048], token_tijdsduur = new int[2048];
    static int[] constante_WAARDE = new int[4096], constante_VERSCHUIVING = new int[512];
    static int[] 문자 = new int[512], bestandsnaam_sms = new int[64];
    static int[] 삽입코드 = new int[16];
    static int bron_formaat_wijzigen, token_AANTAL, positie, CODE_formaat_wijzigen, constante_formaat_wijzigen, constante_AANTAL = 1, uitvoer_formaat_wijzigen, teken_tijdsduur;
    static boolean fout;
    static int les_token, les_constante, bovenliggend_constante, CODE_constante;
    static int[] methode_invoer_naam = new int[32], methode_Retour = new int[32], methode_argument_AANTAL = new int[32];
    static int[] methode_argument_naam = new int[512], methode_argument_TYPE = new int[512];
    static int[] methode_hoofdtekst = new int[32], methode_beëindigen = new int[32], methode_CODE = new int[32];
    static int[] methode_tijdsduur = new int[32], 함수지역 = new int[32], methode_naam_constante = new int[32], 함수서술 = new int[32];
    static int[] methode_toegang = new int[32];
    static int methode_AANTAL, actueel_methode, lokaal_AANTAL, 깊이, 식깊이;
    static int[] lokaal_naam = new int[128], lokaal_TYPE = new int[128], 지역깊이 = new int[128];

    static void fout_WAARDE(String 이유) {
        if (!fout) {
            gebruikersruimte.Schrijven("javac error: "); gebruikersruimte.Schrijven(이유);
            gebruikersruimte.Schrijven(" at line ");
            int invoerregel = 1, 끝 = positie < token_AANTAL ? token_functie[positie] : bron_formaat_wijzigen;
            for (int nummer = 0; nummer < 끝; nummer++) if (broncode[nummer] == 10) invoerregel++;
            자바도구.schrijven_nummer(invoerregel); gebruikersruimte.schrijven_teken_WAARDE(10);
        }
        fout = true;
    }
    static boolean teken_WAARDE(int WAARDE) { return 문자이름규칙.첫글자(WAARDE); }
    static boolean cijfer_WAARDE(int WAARDE) { return WAARDE >= '0' && WAARDE <= '9'; }
    static boolean 이름같음(int 가, int SECONDE_operand) {
        if (가 < 0 || SECONDE_operand < 0 || 가 >= token_AANTAL || SECONDE_operand >= token_AANTAL || token_tijdsduur[가] != token_tijdsduur[SECONDE_operand]) return false;
        for (int nummer = 0; nummer < token_tijdsduur[가]; nummer++) if (broncode[token_functie[가] + nummer] != broncode[token_functie[SECONDE_operand] + nummer]) return false;
        return true;
    }
    static boolean Word_WAARDE(int token_WAARDE, String Word_sms) {
        if (token_WAARDE < 0 || token_WAARDE >= token_AANTAL || token_tijdsduur[token_WAARDE] != Word_sms.length()) return false;
        for (int nummer = 0; nummer < Word_sms.length(); nummer++) if (broncode[token_functie[token_WAARDE] + nummer] != Word_sms.charAt(nummer)) return false;
        return true;
    }
    static int soort_WAARDE() { return positie < token_AANTAL ? token_soort[positie] : 0; }
    static boolean ontvangen(int WAARDE) { if (soort_WAARDE() != WAARDE) return false; positie++; return true; }
    static void vereiste_WAARDE(int WAARDE) { if (!ontvangen(WAARDE)) fout_WAARDE("unexpected token"); }
    static boolean NEMEN_Word(String Word_sms) { if (!Word_WAARDE(positie, Word_sms)) return false; positie++; return true; }
    static void 말요구(String Word_sms) { if (!NEMEN_Word(Word_sms)) fout_WAARDE(Word_sms); }
    static int id_WAARDE() {
        int resultaat = positie;
        if (soort_WAARDE() != 256) fout_WAARDE("identifier required"); else positie++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int starten = 0;
        for (int nummer = 0; nummer <= 예약어.length(); nummer++) {
            if (nummer == 예약어.length() || 예약어.charAt(nummer) == ' ') {
                boolean 같음 = nummer - starten == token_tijdsduur[resultaat];
                for (int sleuf_invoer = starten; 같음 && sleuf_invoer < nummer; sleuf_invoer++) if (예약어.charAt(sleuf_invoer) != broncode[token_functie[resultaat] + sleuf_invoer - starten]) 같음 = false;
                if (같음) fout_WAARDE("reserved word cannot be an identifier");
                starten = nummer + 1;
            }
        }
        return resultaat;
    }
    static void knippen_WAARDE() {
        int nummer = 0;
        while (nummer < bron_formaat_wijzigen && !fout) {
            int WAARDE = broncode[nummer], starten = nummer, soort_WAARDE = WAARDE;
            if (WAARDE == 32 || WAARDE == 9 || WAARDE == 10 || WAARDE == 13) { nummer++; continue; }
            if (WAARDE == '/' && nummer + 1 < bron_formaat_wijzigen && broncode[nummer + 1] == '/') {
                while (nummer < bron_formaat_wijzigen && broncode[nummer] != 10) nummer++;
                continue;
            }
            if (WAARDE == '/' && nummer + 1 < bron_formaat_wijzigen && broncode[nummer + 1] == '*') {
                nummer += 2;
                while (nummer + 1 < bron_formaat_wijzigen && !(broncode[nummer] == '*' && broncode[nummer + 1] == '/')) nummer++;
                if (nummer + 1 >= bron_formaat_wijzigen) { fout_WAARDE("unterminated comment"); break; }
                nummer += 2; continue;
            }
            if (teken_WAARDE(WAARDE)) { soort_WAARDE = 256; while (nummer < bron_formaat_wijzigen && 문자이름규칙.이어진글자(broncode[nummer])) nummer++; }
            else if (cijfer_WAARDE(WAARDE)) { soort_WAARDE = 257; while (nummer < bron_formaat_wijzigen && cijfer_WAARDE(broncode[nummer])) nummer++; }
            else if (WAARDE == '"' || WAARDE == '\'') {
                soort_WAARDE = WAARDE == '"' ? 258 : 259; nummer++;
                while (nummer < bron_formaat_wijzigen && broncode[nummer] != WAARDE && broncode[nummer] != 10 && broncode[nummer] != 13) {
                    if (broncode[nummer] == '\\') nummer++;
                    nummer++;
                }
                if (nummer >= bron_formaat_wijzigen || broncode[nummer] != WAARDE) { fout_WAARDE("unterminated literal"); break; }
                nummer++;
            } else {
                nummer++;
                if (nummer < bron_formaat_wijzigen) {
                    int Volgende_item = broncode[nummer];
                    if (WAARDE == '=' && Volgende_item == '=') soort_WAARDE = 300;
                    if (WAARDE == '!' && Volgende_item == '=') soort_WAARDE = 301;
                    if (WAARDE == '<' && Volgende_item == '=') soort_WAARDE = 302;
                    if (WAARDE == '>' && Volgende_item == '=') soort_WAARDE = 303;
                    if (WAARDE == '&' && Volgende_item == '&') soort_WAARDE = 304;
                    if (WAARDE == '|' && Volgende_item == '|') soort_WAARDE = 305;
                    if (WAARDE == '+' && Volgende_item == '+') soort_WAARDE = 306;
                    if (WAARDE == '-' && Volgende_item == '-') soort_WAARDE = 307;
                    if (WAARDE == '+' && Volgende_item == '=') soort_WAARDE = 308;
                    if (WAARDE == '-' && Volgende_item == '=') soort_WAARDE = 309;
                    if (WAARDE == '*' && Volgende_item == '=') soort_WAARDE = 310;
                    if (WAARDE == '/' && Volgende_item == '=') soort_WAARDE = 311;
                    if (WAARDE == '%' && Volgende_item == '=') soort_WAARDE = 312;
                    if (soort_WAARDE >= 300) nummer++;
                }
            }
            if (token_AANTAL == token_soort.length - 1) { fout_WAARDE("too many tokens (2047 maximum)"); break; }
            token_soort[token_AANTAL] = soort_WAARDE; token_functie[token_AANTAL] = starten; token_tijdsduur[token_AANTAL++] = nummer - starten;
        }
    }
    static void schrijven_constante_byte(int WAARDE) {
        if (constante_formaat_wijzigen == constante_WAARDE.length) { fout_WAARDE("constant pool too large"); return; }
        constante_WAARDE[constante_formaat_wijzigen++] = WAARDE & 255;
    }
    static void 상짧(int WAARDE) { schrijven_constante_byte(WAARDE >> 8); schrijven_constante_byte(WAARDE); }
    static int register_constante(int starten) {
        for (int nummer = 1; nummer < constante_AANTAL; nummer++) {
            int voorkant_WAARDE = constante_VERSCHUIVING[nummer], tijdsduur_WAARDE = (nummer + 1 < constante_AANTAL ? constante_VERSCHUIVING[nummer + 1] : starten) - voorkant_WAARDE;
            if (tijdsduur_WAARDE != constante_formaat_wijzigen - starten) continue;
            boolean 같음 = true;
            for (int sleuf_invoer = 0; sleuf_invoer < tijdsduur_WAARDE; sleuf_invoer++) if (constante_WAARDE[voorkant_WAARDE + sleuf_invoer] != constante_WAARDE[starten + sleuf_invoer]) 같음 = false;
            if (같음) { constante_formaat_wijzigen = starten; return nummer; }
        }
        if (constante_AANTAL == constante_VERSCHUIVING.length) { fout_WAARDE("too many constants"); return 0; }
        constante_VERSCHUIVING[constante_AANTAL] = starten;
        return constante_AANTAL++;
    }
    static void toevoegen_sms(int WAARDE) {
        if (teken_tijdsduur == 문자.length) { fout_WAARDE("text too long"); return; }
        문자[teken_tijdsduur++] = WAARDE;
    }
    static void toevoegen_Word(String Word_sms) { for (int nummer = 0; nummer < Word_sms.length(); nummer++) toevoegen_sms(Word_sms.charAt(nummer)); }
    static int teken_constante() {
        int starten = constante_formaat_wijzigen; schrijven_constante_byte(1); 상짧(0);
        for (int nummer = 0; nummer < teken_tijdsduur; nummer++) {
            int WAARDE = 문자[nummer];
            if (WAARDE > 0 && WAARDE < 128) schrijven_constante_byte(WAARDE);
            else if (WAARDE < 2048) { schrijven_constante_byte(192 | WAARDE >> 6); schrijven_constante_byte(128 | WAARDE & 63); }
            else { schrijven_constante_byte(224 | WAARDE >> 12); schrijven_constante_byte(128 | WAARDE >> 6 & 63); schrijven_constante_byte(128 | WAARDE & 63); }
        }
        if (fout) return 0;
        int tijdsduur_WAARDE = constante_formaat_wijzigen - starten - 3;
        constante_WAARDE[starten + 1] = tijdsduur_WAARDE >> 8; constante_WAARDE[starten + 2] = tijdsduur_WAARDE & 255;
        return register_constante(starten);
    }
    static int Word_constante(String Word_sms) { teken_tijdsduur = 0; toevoegen_Word(Word_sms); return teken_constante(); }
    static int token_constante(int token_WAARDE) {
        teken_tijdsduur = 0;
        for (int nummer = 0; nummer < token_tijdsduur[token_WAARDE]; nummer++) toevoegen_sms(broncode[token_functie[token_WAARDE] + nummer]);
        return teken_constante();
    }
    static int verwijzen(int soort_WAARDE, int 가, int SECONDE_operand) {
        int starten = constante_formaat_wijzigen; schrijven_constante_byte(soort_WAARDE); 상짧(가);
        if (soort_WAARDE == 9 || soort_WAARDE == 10 || soort_WAARDE == 12) 상짧(SECONDE_operand);
        return register_constante(starten);
    }
    static int extern_verwijzen(int soort_WAARDE, String eigenaar_WAARDE, String Naam, String 서술) {
        int eigenaar_id = verwijzen(7, Word_constante(eigenaar_WAARDE), 0);
        int naam_AANTAL = Word_constante(Naam), opmaak_AANTAL = Word_constante(서술);
        return verwijzen(soort_WAARDE, eigenaar_id, verwijzen(12, naam_AANTAL, opmaak_AANTAL));
    }
    static void 내보내기(int WAARDE) {
        if (CODE_formaat_wijzigen == CODE_WAARDE.length) { fout_WAARDE("bytecode too large"); return; }
        CODE_WAARDE[CODE_formaat_wijzigen++] = WAARDE & 255;
    }
    static void opdracht(int WAARDE, int argumenten) { 내보내기(WAARDE); 내보내기(argumenten >> 8); 내보내기(argumenten); }
    static void 수상수(int WAARDE) {
        if (WAARDE >= -1 && WAARDE <= 5) { 내보내기(WAARDE + 3); return; }
        int starten = constante_formaat_wijzigen; schrijven_constante_byte(3); 상짧(WAARDE >>> 16); 상짧(WAARDE);
        opdracht(19, register_constante(starten));
    }
    static int branch(int opdracht) { int resultaat = CODE_formaat_wijzigen; opdracht(opdracht, 0); return resultaat; }
    static void link_WAARDE(int branch, int doel_object) {
        if (fout) return;
        int 거리 = doel_object - branch;
        if (거리 < -32768 || 거리 > 32767 || branch < 0 || branch + 2 >= CODE_formaat_wijzigen) { fout_WAARDE("invalid branch"); return; }
        CODE_WAARDE[branch + 1] = 거리 >> 8 & 255; CODE_WAARDE[branch + 2] = 거리 & 255;
    }
    static void Vergelijking_WAARDE(int opdracht) {
        int WAAR_WAARDE = branch(opdracht); 내보내기(3); int 끝 = branch(167);
        link_WAARDE(WAAR_WAARDE, CODE_formaat_wijzigen); 내보내기(4); link_WAARDE(끝, CODE_formaat_wijzigen);
    }
    static int opmaak_WAARDE() {
        if (NEMEN_Word("void")) return 0;
        if (NEMEN_Word("int")) return 1;
        if (NEMEN_Word("boolean")) return 2;
        if (NEMEN_Word("char")) return 5;
        if (NEMEN_Word("FileInputStream")) return 6;
        if (NEMEN_Word("FileOutputStream")) return 7;
        if (NEMEN_Word("String")) { if (ontvangen('[')) { vereiste_WAARDE(']'); return 4; } return 3; }
        fout_WAARDE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void Toevoegen_opmaak(int TYPE_WAARDE) {
        if (TYPE_WAARDE == 0) toevoegen_sms('V');
        if (TYPE_WAARDE == 1) toevoegen_sms('I');
        if (TYPE_WAARDE == 2) toevoegen_sms('Z');
        if (TYPE_WAARDE == 3) toevoegen_Word("Ljava/lang/String;");
        if (TYPE_WAARDE == 4) toevoegen_Word("[Ljava/lang/String;");
        if (TYPE_WAARDE == 5) toevoegen_sms('C');
        if (TYPE_WAARDE == 6) toevoegen_Word("Ljava/io/FileInputStream;");
        if (TYPE_WAARDE == 7) toevoegen_Word("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws aangifte. uitzondering Proces_WAARDE_invoer 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = NEMEN_Word("Nederlands");
        if (한국어묶음) { vereiste_WAARDE('.'); 말요구("Eigen"); vereiste_WAARDE('.'); }
        if (!한국어묶음 && (NEMEN_Word("Exception") || NEMEN_Word("IOException"))) return;
        if (NEMEN_Word("uitzondering") || NEMEN_Word("uitvoerbewerking_uitzondering") || NEMEN_Word("I_O_uitzondering") || NEMEN_Word("wachten_TIMEOUT_uitzondering") || NEMEN_Word("ADRES_ZOEKEN_uitzondering") || NEMEN_Word("파일없음예외") || NEMEN_Word("communicatie_uitzondering") || NEMEN_Word("nietig_argument_uitzondering") || NEMEN_Word("nummer_opmaak_fout") || NEMEN_Word("범위예외") || NEMEN_Word("배열범위예외") || NEMEN_Word("문자열범위예외") || NEMEN_Word("LEEG_verwijzen_uitzondering") || NEMEN_Word("산술예외") || NEMEN_Word("Status_uitzondering") || NEMEN_Word("TYPE_Weergeven_uitzondering") || NEMEN_Word("음수배열크기예외") || NEMEN_Word("MATRIX_Store_fout") || NEMEN_Word("thread_Status_uitzondering") || NEMEN_Word("대기중단예외")) return;
        fout_WAARDE("unsupported throws type");
    }
    static void 선언읽기() {
        while (NEMEN_Word("import")) {
            if (Word_WAARDE(positie, "Nederlands")) 예외이름읽기();
            else {
                말요구("java"); vereiste_WAARDE('.'); 말요구("io"); vereiste_WAARDE('.');
                if (!(NEMEN_Word("FileInputStream") || NEMEN_Word("FileOutputStream") || NEMEN_Word("IOException"))) fout_WAARDE("unsupported import");
            }
            vereiste_WAARDE(';');
        }
        NEMEN_Word("public"); NEMEN_Word("final"); 말요구("class"); les_token = id_WAARDE();
        les_constante = verwijzen(7, token_constante(les_token), 0);
        bovenliggend_constante = verwijzen(7, Word_constante("java/lang/Object"), 0); CODE_constante = Word_constante("Code"); vereiste_WAARDE('{');
        while (!fout && soort_WAARDE() != '}') {
            if (methode_AANTAL == 32) { fout_WAARDE("too many methods"); break; }
            int toegang_invoer = NEMEN_Word("public") ? 1 : NEMEN_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTIE_WAARDE = methode_AANTAL++;
            methode_toegang[FUNCTIE_WAARDE] = toegang_invoer | 8;
            methode_Retour[FUNCTIE_WAARDE] = opmaak_WAARDE(); methode_invoer_naam[FUNCTIE_WAARDE] = id_WAARDE(); vereiste_WAARDE('(');
            for (int voorkant_WAARDE = 0; voorkant_WAARDE < FUNCTIE_WAARDE; voorkant_WAARDE++) if (이름같음(methode_invoer_naam[voorkant_WAARDE], methode_invoer_naam[FUNCTIE_WAARDE])) fout_WAARDE("duplicate method (overloading unsupported)");
            while (!fout && soort_WAARDE() != ')') {
                int nummer = methode_argument_AANTAL[FUNCTIE_WAARDE];
                if (nummer == 16) { fout_WAARDE("too many parameters"); break; }
                int TYPE_WAARDE = opmaak_WAARDE(); if (TYPE_WAARDE == 0) fout_WAARDE("void parameter");
                methode_argument_TYPE[FUNCTIE_WAARDE * 16 + nummer] = TYPE_WAARDE; methode_argument_naam[FUNCTIE_WAARDE * 16 + nummer] = id_WAARDE();
                methode_argument_AANTAL[FUNCTIE_WAARDE]++;
                if (!ontvangen(',')) break;
            }
            vereiste_WAARDE(')');
            if (NEMEN_Word("throws")) {
                do { 예외이름읽기(); } while (!fout && ontvangen(','));
            }
            methode_hoofdtekst[FUNCTIE_WAARDE] = positie; vereiste_WAARDE('{');
            int nesting_WAARDE = 1;
            while (positie < token_AANTAL && nesting_WAARDE > 0) {
                if (soort_WAARDE() == '{') nesting_WAARDE++;
                if (soort_WAARDE() == '}') nesting_WAARDE--;
                positie++;
            }
            if (nesting_WAARDE != 0) fout_WAARDE("unclosed method body");
            methode_beëindigen[FUNCTIE_WAARDE] = positie;
            methode_naam_constante[FUNCTIE_WAARDE] = token_constante(methode_invoer_naam[FUNCTIE_WAARDE]);
            teken_tijdsduur = 0; toevoegen_sms('(');
            for (int nummer = 0; nummer < methode_argument_AANTAL[FUNCTIE_WAARDE]; nummer++) Toevoegen_opmaak(methode_argument_TYPE[FUNCTIE_WAARDE * 16 + nummer]);
            toevoegen_sms(')'); Toevoegen_opmaak(methode_Retour[FUNCTIE_WAARDE]); 함수서술[FUNCTIE_WAARDE] = teken_constante();
        }
        vereiste_WAARDE('}'); if (positie != token_AANTAL) fout_WAARDE("extra input after class");
    }
    static int Zoeken_lokaal(int Naam) {
        for (int nummer = lokaal_AANTAL - 1; nummer >= 0; nummer--) if (지역깊이[nummer] >= 0 && 이름같음(lokaal_naam[nummer], Naam)) return nummer;
        fout_WAARDE("unknown variable"); return 0;
    }
    static int Toevoegen_lokaal(int Naam, int TYPE_WAARDE) {
        for (int nummer = 0; nummer < lokaal_AANTAL; nummer++) if (지역깊이[nummer] >= 0 && 이름같음(lokaal_naam[nummer], Naam)) fout_WAARDE("duplicate local variable");
        if (lokaal_AANTAL == 128) { fout_WAARDE("too many locals"); return 0; }
        lokaal_naam[lokaal_AANTAL] = Naam; lokaal_TYPE[lokaal_AANTAL] = TYPE_WAARDE; 지역깊이[lokaal_AANTAL] = 깊이;
        return lokaal_AANTAL++;
    }
    static boolean geheel_getal_TYPE(int TYPE_WAARDE) { return TYPE_WAARDE == 1 || TYPE_WAARDE == 5; }
    static void 지역읽기(int nummer) { 내보내기(lokaal_TYPE[nummer] <= 2 || lokaal_TYPE[nummer] == 5 ? 21 : 25); 내보내기(nummer); }
    static void schrijven_lokaal(int nummer) { 내보내기(lokaal_TYPE[nummer] <= 2 || lokaal_TYPE[nummer] == 5 ? 54 : 58); 내보내기(nummer); }
    static void bevestigen_TYPE(int werkelijk_gegevens, int 기대) { if (werkelijk_gegevens != 기대 && !(werkelijk_gegevens == 5 && 기대 == 1)) fout_WAARDE("type mismatch"); }
    static void 문자읽기(int token_WAARDE) {
        teken_tijdsduur = 0; int starten = token_functie[token_WAARDE] + 1, 끝 = token_functie[token_WAARDE] + token_tijdsduur[token_WAARDE] - 1;
        while (starten < 끝 && !fout) {
            int WAARDE = broncode[starten++];
            if (WAARDE == '\\') {
                if (starten == 끝) { fout_WAARDE("invalid escape"); break; }
                WAARDE = broncode[starten++];
                if (WAARDE == 'n') WAARDE = 10;
                else if (WAARDE == 'r') WAARDE = 13;
                else if (WAARDE == 't') WAARDE = 9;
                else if (WAARDE == 'b') WAARDE = 8;
                else if (WAARDE == 'f') WAARDE = 12;
                else if (WAARDE != '\\' && WAARDE != '"' && WAARDE != '\'') fout_WAARDE("unsupported escape");
            }
            toevoegen_sms(WAARDE);
        }
    }
    static int parseren_geheel_getal(int token_WAARDE, boolean 음수) {
        if (token_tijdsduur[token_WAARDE] > 1 && broncode[token_functie[token_WAARDE]] == '0') fout_WAARDE("octal literals unsupported");
        int WAARDE = 0;
        for (int nummer = 0; nummer < token_tijdsduur[token_WAARDE]; nummer++) {
            int cijfer_item = broncode[token_functie[token_WAARDE] + nummer] - '0';
            if (WAARDE < -214748364 || WAARDE == -214748364 && cijfer_item > (음수 ? 8 : 7)) fout_WAARDE("integer literal out of range");
            WAARDE = WAARDE * 10 - cijfer_item;
        }
        return 음수 ? WAARDE : -WAARDE;
    }
    static int 기본식() {
        if (NEMEN_Word("new")) {
            int TYPE_WAARDE = opmaak_WAARDE();
            if (TYPE_WAARDE != 6 && TYPE_WAARDE != 7) { fout_WAARDE("only file streams supported by new in source"); return 0; }
            String eigenaar_WAARDE = TYPE_WAARDE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            opdracht(187, verwijzen(7, Word_constante(eigenaar_WAARDE), 0)); 내보내기(89);
            vereiste_WAARDE('('); bevestigen_TYPE(expressie_WAARDE(), 3); boolean 이어 = false;
            if (ontvangen(',')) { if (TYPE_WAARDE != 7) fout_WAARDE("input stream constructor arguments"); bevestigen_TYPE(expressie_WAARDE(), 2); 이어 = true; }
            vereiste_WAARDE(')');
            opdracht(183, extern_verwijzen(10, eigenaar_WAARDE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_WAARDE;
        }
        if (ontvangen('(')) { int TYPE_WAARDE = expressie_WAARDE(); vereiste_WAARDE(')'); return TYPE_WAARDE; }
        if (soort_WAARDE() == 257) { 수상수(parseren_geheel_getal(positie++, false)); return 1; }
        if (soort_WAARDE() == 258) { 문자읽기(positie++); opdracht(19, verwijzen(8, teken_constante(), 0)); return 3; }
        if (soort_WAARDE() == 259) { 문자읽기(positie++); if (teken_tijdsduur != 1) fout_WAARDE("character literal length"); 수상수(문자[0]); return 5; }
        if (NEMEN_Word("true")) { 내보내기(4); return 2; }
        if (NEMEN_Word("false")) { 내보내기(3); return 2; }
        if (NEMEN_Word("Nederlands")) {
            vereiste_WAARDE('.'); 말요구("Eigen"); vereiste_WAARDE('.');
            String eigenaar_WAARDE = "", methode_WAARDE = "", 서술 = ""; int 가 = 0, SECONDE_operand = 0, 다 = 0, 라 = 0, 마 = 0, resultaat = 0;
            if (NEMEN_Word("tekstuitvoer")) {
                eigenaar_WAARDE = "Nederlands/Eigen/tekstuitvoer"; vereiste_WAARDE('.');
                if (NEMEN_Word("schrijven_lijn")) { methode_WAARDE = "schrijven_lijn"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (NEMEN_Word("Schrijven")) { methode_WAARDE = "Schrijven"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (NEMEN_Word("schrijven_nummer")) { methode_WAARDE = "schrijven_nummer"; 서술 = "(I)V"; 가 = 1; }
                else fout_WAARDE("unknown Korean output method");
            } else if (NEMEN_Word("문자")) {
                eigenaar_WAARDE = "Nederlands/Eigen/문자"; vereiste_WAARDE('.'); 가 = 3;
                if (NEMEN_Word("tijdsduur_WAARDE")) { methode_WAARDE = "tijdsduur_WAARDE"; 서술 = "(Ljava/lang/String;)I"; resultaat = 1; }
                else if (NEMEN_Word("codepoint_AANTAL")) { methode_WAARDE = "codepoint_AANTAL"; 서술 = "(Ljava/lang/String;)I"; resultaat = 1; }
                else if (NEMEN_Word("parseren_geheel_getal")) { methode_WAARDE = "parseren_geheel_getal"; 서술 = "(Ljava/lang/String;)I"; resultaat = 1; }
                else if (NEMEN_Word("schrijven_geheel_getal_WAARDE")) { methode_WAARDE = "schrijven_geheel_getal_WAARDE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; resultaat = 3; }
                else if (NEMEN_Word("같음")) { methode_WAARDE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; SECONDE_operand = 3; resultaat = 2; }
                else if (NEMEN_Word("plakken_sms")) { methode_WAARDE = "plakken_sms"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; SECONDE_operand = 3; resultaat = 3; }
                else if (NEMEN_Word("knippen_WAARDE")) { methode_WAARDE = "knippen_WAARDE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; SECONDE_operand = 1; 다 = 1; resultaat = 3; }
                else fout_WAARDE("unknown Korean text method");
            } else if (NEMEN_Word("bestand")) {
                eigenaar_WAARDE = "Nederlands/Eigen/bestand"; vereiste_WAARDE('.'); 가 = 3;
                if (NEMEN_Word("Lezen")) { methode_WAARDE = "Lezen"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; resultaat = 3; }
                else if (NEMEN_Word("Schrijven")) { methode_WAARDE = "Schrijven"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; SECONDE_operand = 3; }
                else fout_WAARDE("unknown Korean file method");
            } else if (NEMEN_Word("scherm")) {
                eigenaar_WAARDE = "Nederlands/Eigen/scherm"; vereiste_WAARDE('.');
                if (NEMEN_Word("너비")) { methode_WAARDE = "너비"; 서술 = "()I"; resultaat = 1; }
                else if (NEMEN_Word("hoogte_WAARDE")) { methode_WAARDE = "hoogte_WAARDE"; 서술 = "()I"; resultaat = 1; }
                else if (NEMEN_Word("rechthoek")) { methode_WAARDE = "rechthoek"; 서술 = "(IIIII)V"; 가 = 1; SECONDE_operand = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (NEMEN_Word("wissen_invoer")) { methode_WAARDE = "wissen_invoer"; 서술 = "(I)V"; 가 = 1; }
                else if (NEMEN_Word("기다리기")) { methode_WAARDE = "기다리기"; 서술 = "()V"; }
                else fout_WAARDE("unknown Korean framebuffer method");
            } else fout_WAARDE("unsupported Korean library class");
            vereiste_WAARDE('('); if (가 != 0) bevestigen_TYPE(expressie_WAARDE(), 가);
            if (SECONDE_operand != 0) { vereiste_WAARDE(','); bevestigen_TYPE(expressie_WAARDE(), SECONDE_operand); }
            if (다 != 0) { vereiste_WAARDE(','); bevestigen_TYPE(expressie_WAARDE(), 다); }
            if (라 != 0) { vereiste_WAARDE(','); bevestigen_TYPE(expressie_WAARDE(), 라); }
            if (마 != 0) { vereiste_WAARDE(','); bevestigen_TYPE(expressie_WAARDE(), 마); }
            vereiste_WAARDE(')'); opdracht(184, extern_verwijzen(10, eigenaar_WAARDE, methode_WAARDE, 서술)); return resultaat;
        }
        if (NEMEN_Word("Integer")) {
            vereiste_WAARDE('.'); 말요구("parseInt"); vereiste_WAARDE('('); bevestigen_TYPE(expressie_WAARDE(), 3); vereiste_WAARDE(')');
            opdracht(184, extern_verwijzen(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Naam = id_WAARDE();
        if (ontvangen('(')) {
            int FUNCTIE_WAARDE = -1;
            for (int nummer = 0; nummer < methode_AANTAL; nummer++) if (이름같음(Naam, methode_invoer_naam[nummer])) FUNCTIE_WAARDE = nummer;
            if (FUNCTIE_WAARDE < 0) { fout_WAARDE("unknown static method"); return 0; }
            int nummer = 0;
            while (!fout && soort_WAARDE() != ')') {
                if (nummer >= methode_argument_AANTAL[FUNCTIE_WAARDE]) { fout_WAARDE("too many arguments"); break; }
                bevestigen_TYPE(expressie_WAARDE(), methode_argument_TYPE[FUNCTIE_WAARDE * 16 + nummer++]); if (!ontvangen(',')) break;
            }
            vereiste_WAARDE(')'); if (nummer != methode_argument_AANTAL[FUNCTIE_WAARDE]) fout_WAARDE("argument count mismatch");
            opdracht(184, verwijzen(10, les_constante, verwijzen(12, methode_naam_constante[FUNCTIE_WAARDE], 함수서술[FUNCTIE_WAARDE])));
            return methode_Retour[FUNCTIE_WAARDE];
        }
        int lokaal_scope = Zoeken_lokaal(Naam), TYPE_WAARDE = lokaal_TYPE[lokaal_scope]; 지역읽기(lokaal_scope);
        while (!fout) {
            if (ontvangen('[')) { bevestigen_TYPE(TYPE_WAARDE, 4); bevestigen_TYPE(expressie_WAARDE(), 1); vereiste_WAARDE(']'); 내보내기(50); TYPE_WAARDE = 3; }
            else if (ontvangen('.')) {
                if (TYPE_WAARDE == 6 || TYPE_WAARDE == 7) {
                    String eigenaar_WAARDE = TYPE_WAARDE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (NEMEN_Word("close")) { vereiste_WAARDE('('); vereiste_WAARDE(')'); opdracht(182, extern_verwijzen(10, eigenaar_WAARDE, "close", "()V")); TYPE_WAARDE = 0; }
                    else if (TYPE_WAARDE == 6 && NEMEN_Word("read")) { vereiste_WAARDE('('); vereiste_WAARDE(')'); opdracht(182, extern_verwijzen(10, eigenaar_WAARDE, "read", "()I")); TYPE_WAARDE = 1; }
                    else if (TYPE_WAARDE == 7 && NEMEN_Word("write")) { vereiste_WAARDE('('); bevestigen_TYPE(expressie_WAARDE(), 1); vereiste_WAARDE(')'); opdracht(182, extern_verwijzen(10, eigenaar_WAARDE, "write", "(I)V")); TYPE_WAARDE = 0; }
                    else { fout_WAARDE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_WAARDE == 4) { 내보내기(190); TYPE_WAARDE = 1; }
                else { bevestigen_TYPE(TYPE_WAARDE, 3); vereiste_WAARDE('('); vereiste_WAARDE(')'); opdracht(182, extern_verwijzen(10, "java/lang/String", "length", "()I")); TYPE_WAARDE = 1; }
            } else break;
        }
        return TYPE_WAARDE;
    }
    static int 단항() {
        if (++식깊이 > 64) { fout_WAARDE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_WAARDE;
        if (ontvangen('!')) { bevestigen_TYPE(단항(), 2); Vergelijking_WAARDE(153); TYPE_WAARDE = 2; }
        else if (ontvangen('-')) {
            if (soort_WAARDE() == 257) 수상수(parseren_geheel_getal(positie++, true));
            else { bevestigen_TYPE(단항(), 1); 내보내기(116); }
            TYPE_WAARDE = 1;
        } else if (ontvangen('+')) { bevestigen_TYPE(단항(), 1); TYPE_WAARDE = 1; }
        else TYPE_WAARDE = 기본식();
        식깊이--; return TYPE_WAARDE;
    }
    static int 곱식() {
        int TYPE_WAARDE = 단항();
        while (!fout && (soort_WAARDE() == '*' || soort_WAARDE() == '/' || soort_WAARDE() == '%')) {
            int Encoding_WAARDE = soort_WAARDE(); positie++; bevestigen_TYPE(TYPE_WAARDE, 1); bevestigen_TYPE(단항(), 1);
            내보내기(Encoding_WAARDE == '*' ? 104 : Encoding_WAARDE == '/' ? 108 : 112); TYPE_WAARDE = 1;
        }
        return TYPE_WAARDE;
    }
    static int 합식() {
        int TYPE_WAARDE = 곱식();
        while (!fout && (soort_WAARDE() == '+' || soort_WAARDE() == '-')) {
            int Encoding_WAARDE = soort_WAARDE(); positie++; int grens_WAARDE = CODE_formaat_wijzigen, BACK_waardetype = 곱식();
            if (Encoding_WAARDE == '+' && (TYPE_WAARDE == 3 || BACK_waardetype == 3)) { 결합(grens_WAARDE, TYPE_WAARDE, BACK_waardetype); TYPE_WAARDE = 3; }
            else { bevestigen_TYPE(TYPE_WAARDE, 1); bevestigen_TYPE(BACK_waardetype, 1); 내보내기(Encoding_WAARDE == '+' ? 96 : 100); TYPE_WAARDE = 1; }
        }
        return TYPE_WAARDE;
    }
    static int gekoppeld_verwijzen(int TYPE_WAARDE) {
        if (TYPE_WAARDE != 1 && TYPE_WAARDE != 2 && TYPE_WAARDE != 3 && TYPE_WAARDE != 5) fout_WAARDE("unsupported concatenation type");
        return extern_verwijzen(10, "java/lang/StringBuilder", "append", TYPE_WAARDE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_WAARDE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_WAARDE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int grens_WAARDE, int voorkant_waardetype, int BACK_waardetype) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 recht CODE_WAARDE 앞에 genereren 코드를 삽입한다.
        // recht expressie_WAARDE 내부의 peer_WAARDE branch 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_formaat_wijzigen;
        opdracht(187, verwijzen(7, Word_constante("java/lang/StringBuilder"), 0)); 내보내기(89);
        opdracht(183, extern_verwijzen(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); opdracht(182, gekoppeld_verwijzen(voorkant_waardetype));
        if (fout) return;
        int tijdsduur_WAARDE = CODE_formaat_wijzigen - 끝;
        for (int nummer = 0; nummer < tijdsduur_WAARDE; nummer++) 삽입코드[nummer] = CODE_WAARDE[끝 + nummer];
        for (int nummer = 끝 - 1; nummer >= grens_WAARDE; nummer--) CODE_WAARDE[nummer + tijdsduur_WAARDE] = CODE_WAARDE[nummer];
        for (int nummer = 0; nummer < tijdsduur_WAARDE; nummer++) CODE_WAARDE[grens_WAARDE + nummer] = 삽입코드[nummer];
        opdracht(182, gekoppeld_verwijzen(BACK_waardetype)); opdracht(182, extern_verwijzen(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Vergelijking_expressie() {
        int TYPE_WAARDE = 합식();
        while (!fout && (soort_WAARDE() == '<' || soort_WAARDE() == '>' || soort_WAARDE() == 302 || soort_WAARDE() == 303)) {
            int Encoding_WAARDE = soort_WAARDE(); positie++; bevestigen_TYPE(TYPE_WAARDE, 1); bevestigen_TYPE(합식(), 1);
            Vergelijking_WAARDE(Encoding_WAARDE == '<' ? 161 : Encoding_WAARDE == '>' ? 163 : Encoding_WAARDE == 302 ? 164 : 162); TYPE_WAARDE = 2;
        }
        return TYPE_WAARDE;
    }
    static int 동등식() {
        int TYPE_WAARDE = Vergelijking_expressie();
        while (!fout && (soort_WAARDE() == 300 || soort_WAARDE() == 301)) {
            int Encoding_WAARDE = soort_WAARDE(); positie++; int BACK_waardetype = Vergelijking_expressie();
            if (TYPE_WAARDE == 0 || BACK_waardetype == 0) fout_WAARDE("void expression");
            if (!(geheel_getal_TYPE(TYPE_WAARDE) && geheel_getal_TYPE(BACK_waardetype))) bevestigen_TYPE(BACK_waardetype, TYPE_WAARDE);
            Vergelijking_WAARDE((TYPE_WAARDE <= 2 || TYPE_WAARDE == 5 ? 159 : 165) + (Encoding_WAARDE == 301 ? 1 : 0)); TYPE_WAARDE = 2;
        }
        return TYPE_WAARDE;
    }
    static int EN() {
        int TYPE_WAARDE = 동등식();
        while (!fout && ontvangen(304)) {
            bevestigen_TYPE(TYPE_WAARDE, 2); int 가 = branch(153); bevestigen_TYPE(동등식(), 2); int SECONDE_operand = branch(153);
            내보내기(4); int 끝 = branch(167); link_WAARDE(가, CODE_formaat_wijzigen); link_WAARDE(SECONDE_operand, CODE_formaat_wijzigen); 내보내기(3); link_WAARDE(끝, CODE_formaat_wijzigen); TYPE_WAARDE = 2;
        }
        return TYPE_WAARDE;
    }
    static int expressie_WAARDE() {
        int TYPE_WAARDE = EN();
        while (!fout && ontvangen(305)) {
            bevestigen_TYPE(TYPE_WAARDE, 2); int 가 = branch(154); bevestigen_TYPE(EN(), 2); int SECONDE_operand = branch(154);
            내보내기(3); int 끝 = branch(167); link_WAARDE(가, CODE_formaat_wijzigen); link_WAARDE(SECONDE_operand, CODE_formaat_wijzigen); 내보내기(4); link_WAARDE(끝, CODE_formaat_wijzigen); TYPE_WAARDE = 2;
        }
        return TYPE_WAARDE;
    }
    static void lab_WAARDE(boolean Toestaan_aangifte) {
        if (Word_WAARDE(positie, "int") || Word_WAARDE(positie, "boolean") || Word_WAARDE(positie, "String") || Word_WAARDE(positie, "char")
            || Word_WAARDE(positie, "FileInputStream") || Word_WAARDE(positie, "FileOutputStream")) {
            if (!Toestaan_aangifte) fout_WAARDE("declaration not allowed here");
            int TYPE_WAARDE = opmaak_WAARDE(), Naam = id_WAARDE(); vereiste_WAARDE('='); bevestigen_TYPE(expressie_WAARDE(), TYPE_WAARDE);
            schrijven_lokaal(Toevoegen_lokaal(Naam, TYPE_WAARDE)); return;
        }
        int Naam = id_WAARDE(), lokaal_scope = Zoeken_lokaal(Naam);
        if (ontvangen('=')) { bevestigen_TYPE(expressie_WAARDE(), lokaal_TYPE[lokaal_scope]); schrijven_lokaal(lokaal_scope); }
        else if (soort_WAARDE() >= 308 && soort_WAARDE() <= 312) {
            int Encoding_WAARDE = soort_WAARDE(); positie++; 지역읽기(lokaal_scope); int grens_WAARDE = CODE_formaat_wijzigen, BACK_waardetype = expressie_WAARDE();
            if (Encoding_WAARDE == 308 && lokaal_TYPE[lokaal_scope] == 3) 결합(grens_WAARDE, 3, BACK_waardetype);
            else {
                bevestigen_TYPE(lokaal_TYPE[lokaal_scope], 1); bevestigen_TYPE(BACK_waardetype, 1);
                내보내기(Encoding_WAARDE == 308 ? 96 : Encoding_WAARDE == 309 ? 100 : Encoding_WAARDE == 310 ? 104 : Encoding_WAARDE == 311 ? 108 : 112);
                if (lokaal_TYPE[lokaal_scope] == 5) 내보내기(146);
            }
            schrijven_lokaal(lokaal_scope);
        }
        else if (soort_WAARDE() == 306 || soort_WAARDE() == 307) {
            bevestigen_TYPE(lokaal_TYPE[lokaal_scope], 1); 내보내기(132); 내보내기(lokaal_scope); 내보내기(soort_WAARDE() == 306 ? 1 : 255); positie++;
            if (lokaal_TYPE[lokaal_scope] == 5) { 지역읽기(lokaal_scope); 내보내기(146); schrijven_lokaal(lokaal_scope); }
        } else fout_WAARDE("assignment or postfix increment required");
    }
    static void scherm_uitvoer() {
        말요구("System"); vereiste_WAARDE('.'); 말요구("out"); vereiste_WAARDE('.');
        boolean 줄바꿈 = NEMEN_Word("println"); if (!줄바꿈) 말요구("print"); vereiste_WAARDE('(');
        opdracht(178, extern_verwijzen(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean leeg_argument = soort_WAARDE() == ')';
        int TYPE_WAARDE = leeg_argument ? 0 : expressie_WAARDE(); vereiste_WAARDE(')'); vereiste_WAARDE(';');
        String 서술 = TYPE_WAARDE == 0 ? "()V" : TYPE_WAARDE == 1 ? "(I)V" : TYPE_WAARDE == 2 ? "(Z)V" : TYPE_WAARDE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_WAARDE == 4 || TYPE_WAARDE >= 6 || TYPE_WAARDE == 0 && (!줄바꿈 || !leeg_argument)) fout_WAARDE("unsupported print argument");
        opdracht(182, extern_verwijzen(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean overzicht_WAARDE() {
        if (fout) return false;
        if (깊이 > 32) { fout_WAARDE("statement nesting too deep"); return false; }
        if (ontvangen('{')) {
            깊이++; boolean Retour_HR = false;
            while (!fout && soort_WAARDE() != '}') { if (Retour_HR) fout_WAARDE("unreachable statement"); Retour_HR = overzicht_WAARDE(); }
            vereiste_WAARDE('}'); for (int nummer = 0; nummer < lokaal_AANTAL; nummer++) if (지역깊이[nummer] == 깊이) 지역깊이[nummer] = -1;
            깊이--; return Retour_HR;
        }
        if (ontvangen(';')) return false;
        if (NEMEN_Word("return")) {
            int TYPE_WAARDE = soort_WAARDE() == ';' ? 0 : expressie_WAARDE(); bevestigen_TYPE(TYPE_WAARDE, methode_Retour[actueel_methode]); vereiste_WAARDE(';');
            내보내기(TYPE_WAARDE == 0 ? 177 : TYPE_WAARDE <= 2 || TYPE_WAARDE == 5 ? 172 : 176); return true;
        }
        if (NEMEN_Word("if")) {
            vereiste_WAARDE('('); bevestigen_TYPE(expressie_WAARDE(), 2); vereiste_WAARDE(')'); int ONWAAR_WAARDE = branch(153);
            깊이++; boolean 가 = controle_overzicht(); 깊이--;
            if (NEMEN_Word("else")) { int 끝 = branch(167); link_WAARDE(ONWAAR_WAARDE, CODE_formaat_wijzigen); 깊이++; boolean SECONDE_operand = controle_overzicht(); 깊이--; link_WAARDE(끝, CODE_formaat_wijzigen); return 가 && SECONDE_operand; }
            link_WAARDE(ONWAAR_WAARDE, CODE_formaat_wijzigen); return false;
        }
        if (NEMEN_Word("while")) {
            int starten = CODE_formaat_wijzigen; vereiste_WAARDE('('); bevestigen_TYPE(expressie_WAARDE(), 2); vereiste_WAARDE(')'); int 끝 = branch(153);
            깊이++; controle_overzicht(); 깊이--; link_WAARDE(branch(167), starten); link_WAARDE(끝, CODE_formaat_wijzigen); return false;
        }
        if (NEMEN_Word("for")) {
            깊이++; vereiste_WAARDE('('); if (soort_WAARDE() != ';') lab_WAARDE(true); vereiste_WAARDE(';');
            int toestand = CODE_formaat_wijzigen; if (soort_WAARDE() == ';') 내보내기(4); else bevestigen_TYPE(expressie_WAARDE(), 2); vereiste_WAARDE(';');
            int 끝 = branch(153), hoofdtekst = branch(167), vernieuwen = CODE_formaat_wijzigen;
            if (soort_WAARDE() != ')') lab_WAARDE(false); vereiste_WAARDE(')'); link_WAARDE(branch(167), toestand); link_WAARDE(hoofdtekst, CODE_formaat_wijzigen);
            controle_overzicht(); link_WAARDE(branch(167), vernieuwen); link_WAARDE(끝, CODE_formaat_wijzigen);
            for (int nummer = 0; nummer < lokaal_AANTAL; nummer++) if (지역깊이[nummer] == 깊이) 지역깊이[nummer] = -1;
            깊이--; return false;
        }
        if (Word_WAARDE(positie, "System")) { scherm_uitvoer(); return false; }
        if (soort_WAARDE() == 256 && positie + 1 < token_AANTAL && (token_soort[positie + 1] == '(' || token_soort[positie + 1] == '.')) {
            int TYPE_WAARDE = expressie_WAARDE(); if (TYPE_WAARDE != 0) 내보내기(87); vereiste_WAARDE(';'); return false;
        }
        lab_WAARDE(true); vereiste_WAARDE(';'); return false;
    }
    static boolean controle_overzicht() {
        if (Word_WAARDE(positie, "int") || Word_WAARDE(positie, "boolean") || Word_WAARDE(positie, "char") || Word_WAARDE(positie, "String")
            || Word_WAARDE(positie, "FileInputStream") || Word_WAARDE(positie, "FileOutputStream")) fout_WAARDE("local declaration requires braces");
        return overzicht_WAARDE();
    }
    static void 출바(int WAARDE) { if (uitvoer_formaat_wijzigen == tekstuitvoer.length) fout_WAARDE("class file too large"); else tekstuitvoer[uitvoer_formaat_wijzigen++] = WAARDE & 255; }
    static void 출짧(int WAARDE) { 출바(WAARDE >> 8); 출바(WAARDE); }
    static void 출정(int WAARDE) { 출짧(WAARDE >>> 16); 출짧(WAARDE); }
    static void schrijven_les() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(constante_AANTAL);
        for (int nummer = 0; nummer < constante_formaat_wijzigen; nummer++) 출바(constante_WAARDE[nummer]);
        출짧(0x21); 출짧(les_constante); 출짧(bovenliggend_constante); 출짧(0); 출짧(0); 출짧(methode_AANTAL);
        for (int nummer = 0; nummer < methode_AANTAL; nummer++) {
            출짧(methode_toegang[nummer]); 출짧(methode_naam_constante[nummer]); 출짧(함수서술[nummer]); 출짧(1); 출짧(CODE_constante);
            출정(12 + methode_tijdsduur[nummer]); 출짧(128); 출짧(함수지역[nummer]); 출정(methode_tijdsduur[nummer]);
            for (int sleuf_invoer = 0; sleuf_invoer < methode_tijdsduur[nummer]; sleuf_invoer++) 출바(CODE_WAARDE[methode_CODE[nummer] + sleuf_invoer]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int starten() {
        if (gebruikersruimte.인수개수() == 1 && 자바도구.같음(gebruikersruimte.argumenten(0), "-version")) {
            gebruikersruimte.Schrijven("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (gebruikersruimte.인수개수() != 1) { gebruikersruimte.Schrijven("Usage: javac FILE.java\n"); return 2; }
        int naam_formaat_wijzigen = 자바도구.Naam(bestandsnaam_sms, gebruikersruimte.argumenten(0));
        if (naam_formaat_wijzigen < 6 || naam_formaat_wijzigen > 62 || bestandsnaam_sms[naam_formaat_wijzigen - 5] != '.' || bestandsnaam_sms[naam_formaat_wijzigen - 4] != 'j'
            || bestandsnaam_sms[naam_formaat_wijzigen - 3] != 'a' || bestandsnaam_sms[naam_formaat_wijzigen - 2] != 'v' || bestandsnaam_sms[naam_formaat_wijzigen - 1] != 'a') {
            gebruikersruimte.Schrijven("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        bron_formaat_wijzigen = gebruikersruimte.파일읽기(bestandsnaam_sms, broncode);
        if (bron_formaat_wijzigen < 0) { gebruikersruimte.Schrijven("javac: cannot read source: "); 자바도구.schrijven_nummer(bron_formaat_wijzigen); gebruikersruimte.schrijven_teken_WAARDE(10); return 1; }
        bron_formaat_wijzigen = 자바도구.원문해독(broncode, bron_formaat_wijzigen);
        if (bron_formaat_wijzigen < 0) { gebruikersruimte.Schrijven("javac error: invalid UTF-8 source\n"); return 1; }
        knippen_WAARDE(); if (!fout) 선언읽기();
        if (!fout) {
            if (token_tijdsduur[les_token] != naam_formaat_wijzigen - 5) fout_WAARDE("class name must match file name");
            for (int nummer = 0; nummer < naam_formaat_wijzigen - 5; nummer++) if (broncode[token_functie[les_token] + nummer] != bestandsnaam_sms[nummer]) fout_WAARDE("class name must match file name");
        }
        for (actueel_methode = 0; actueel_methode < methode_AANTAL && !fout; actueel_methode++) {
            positie = methode_hoofdtekst[actueel_methode]; methode_CODE[actueel_methode] = CODE_formaat_wijzigen; lokaal_AANTAL = 0; 깊이 = 0;
            for (int nummer = 0; nummer < methode_argument_AANTAL[actueel_methode]; nummer++) Toevoegen_lokaal(methode_argument_naam[actueel_methode * 16 + nummer], methode_argument_TYPE[actueel_methode * 16 + nummer]);
            boolean Retour_HR = overzicht_WAARDE();
            if (!Retour_HR && methode_Retour[actueel_methode] != 0) fout_WAARDE("missing return");
            // branch 뒤의 합류 지점은 반드시 werkelijk_gegevens 명령이어야 한다 (버전 49 검증기).
            if (methode_Retour[actueel_methode] == 0) 내보내기(177);
            else { boolean geheel_getal = methode_Retour[actueel_methode] <= 2 || methode_Retour[actueel_methode] == 5; 내보내기(geheel_getal ? 3 : 1); 내보내기(geheel_getal ? 172 : 176); }
            if (positie != methode_beëindigen[actueel_methode]) fout_WAARDE("invalid method body");
            함수지역[actueel_methode] = lokaal_AANTAL; methode_tijdsduur[actueel_methode] = CODE_formaat_wijzigen - methode_CODE[actueel_methode];
        }
        if (fout) return 1;
        schrijven_les(); if (fout) return 1;
        bestandsnaam_sms[naam_formaat_wijzigen - 4] = 'c'; bestandsnaam_sms[naam_formaat_wijzigen - 3] = 'l'; bestandsnaam_sms[naam_formaat_wijzigen - 2] = 'a';
        bestandsnaam_sms[naam_formaat_wijzigen - 1] = 's'; bestandsnaam_sms[naam_formaat_wijzigen] = 's'; bestandsnaam_sms[naam_formaat_wijzigen + 1] = 0;
        int resultaat = gebruikersruimte.schrijven_Bestand(bestandsnaam_sms, tekstuitvoer, uitvoer_formaat_wijzigen);
        if (resultaat < 0) { gebruikersruimte.Schrijven("javac: cannot save class: "); 자바도구.schrijven_nummer(resultaat); gebruikersruimte.schrijven_teken_WAARDE(10); return 1; }
        gebruikersruimte.Schrijven("Compiled: "); for (int nummer = 0; bestandsnaam_sms[nummer] != 0; nummer++) gebruikersruimte.schrijven_teken_WAARDE(bestandsnaam_sms[nummer]);
        gebruikersruimte.Schrijven(" (JVM class version 49)\n"); return 0;
    }
}
