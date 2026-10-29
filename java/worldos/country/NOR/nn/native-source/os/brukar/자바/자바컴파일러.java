// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java kjelde_tre -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] KJELDE = new int[16384], Utdata = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_plassere = new int[2048], token_lengd = new int[2048];
    static int[] konstant_VALUE = new int[4096], konstant_OFFSET = new int[512];
    static int[] 문자 = new int[512], fil_namn_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int kjelde_endre_storleik, token_COUNT, Posisjon, CODE_endre_storleik, konstant_endre_storleik, konstant_COUNT = 1, 출력크기, teikn_lengd;
    static boolean FEIL;
    static int time_token, time_konstant, forelder_konstant, CODE_konstant;
    static int[] metode_oppføring_namn = new int[32], metode_levere_tilbake = new int[32], metode_argument_COUNT = new int[32];
    static int[] metode_argument_namn = new int[512], metode_argument_TYPE = new int[512];
    static int[] metode_brødtekst = new int[32], metode_avslutte = new int[32], metode_CODE = new int[32];
    static int[] metode_lengd = new int[32], 함수지역 = new int[32], metode_namn_konstant = new int[32], 함수서술 = new int[32];
    static int[] metode_tilgang = new int[32];
    static int metode_COUNT, betalt_metode, lokal_COUNT, 깊이, 식깊이;
    static int[] lokal_namn = new int[128], lokal_TYPE = new int[128], 지역깊이 = new int[128];

    static void feil_VALUE(String 이유) {
        if (!FEIL) {
            brukar.Skriv("javac error: "); brukar.Skriv(이유);
            brukar.Skriv(" at line ");
            int linje = 1, 끝 = Posisjon < token_COUNT ? token_plassere[Posisjon] : kjelde_endre_storleik;
            for (int 수 = 0; 수 < 끝; 수++) if (KJELDE[수] == 10) linje++;
            자바도구.수쓰기(linje); brukar.skrive_teikn_VALUE(10);
        }
        FEIL = true;
    }
    static boolean teikn_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean siffer_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= token_COUNT || 나 >= token_COUNT || token_lengd[가] != token_lengd[나]) return false;
        for (int 수 = 0; 수 < token_lengd[가]; 수++) if (KJELDE[token_plassere[가] + 수] != KJELDE[token_plassere[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_lengd[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (KJELDE[token_plassere[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return Posisjon < token_COUNT ? 토큰종류[Posisjon] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; Posisjon++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) feil_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(Posisjon, Word_SMS)) return false; Posisjon++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) feil_VALUE(Word_SMS); }
    static int identifikator_VALUE() {
        int forretningsmål = Posisjon;
        if (종류() != 256) feil_VALUE("identifier required"); else Posisjon++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Køyr_2 = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Køyr_2 == token_lengd[forretningsmål];
                for (int felt_oppføring = Køyr_2; 같음 && felt_oppføring < 수; felt_oppføring++) if (예약어.charAt(felt_oppføring) != KJELDE[token_plassere[forretningsmål] + felt_oppføring - Køyr_2]) 같음 = false;
                if (같음) feil_VALUE("reserved word cannot be an identifier");
                Køyr_2 = 수 + 1;
            }
        }
        return forretningsmål;
    }
    static void klippe_VALUE() {
        int 수 = 0;
        while (수 < kjelde_endre_storleik && !FEIL) {
            int VALUE = KJELDE[수], Køyr_2 = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < kjelde_endre_storleik && KJELDE[수 + 1] == '/') {
                while (수 < kjelde_endre_storleik && KJELDE[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < kjelde_endre_storleik && KJELDE[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < kjelde_endre_storleik && !(KJELDE[수] == '*' && KJELDE[수 + 1] == '/')) 수++;
                if (수 + 1 >= kjelde_endre_storleik) { feil_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (teikn_VALUE(VALUE)) { 종류 = 256; while (수 < kjelde_endre_storleik && 문자이름규칙.이어진글자(KJELDE[수])) 수++; }
            else if (siffer_VALUE(VALUE)) { 종류 = 257; while (수 < kjelde_endre_storleik && siffer_VALUE(KJELDE[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < kjelde_endre_storleik && KJELDE[수] != VALUE && KJELDE[수] != 10 && KJELDE[수] != 13) {
                    if (KJELDE[수] == '\\') 수++;
                    수++;
                }
                if (수 >= kjelde_endre_storleik || KJELDE[수] != VALUE) { feil_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < kjelde_endre_storleik) {
                    int Neste_vare = KJELDE[수];
                    if (VALUE == '=' && Neste_vare == '=') 종류 = 300;
                    if (VALUE == '!' && Neste_vare == '=') 종류 = 301;
                    if (VALUE == '<' && Neste_vare == '=') 종류 = 302;
                    if (VALUE == '>' && Neste_vare == '=') 종류 = 303;
                    if (VALUE == '&' && Neste_vare == '&') 종류 = 304;
                    if (VALUE == '|' && Neste_vare == '|') 종류 = 305;
                    if (VALUE == '+' && Neste_vare == '+') 종류 = 306;
                    if (VALUE == '-' && Neste_vare == '-') 종류 = 307;
                    if (VALUE == '+' && Neste_vare == '=') 종류 = 308;
                    if (VALUE == '-' && Neste_vare == '=') 종류 = 309;
                    if (VALUE == '*' && Neste_vare == '=') 종류 = 310;
                    if (VALUE == '/' && Neste_vare == '=') 종류 = 311;
                    if (VALUE == '%' && Neste_vare == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { feil_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_plassere[token_COUNT] = Køyr_2; token_lengd[token_COUNT++] = 수 - Køyr_2;
        }
    }
    static void skrive_konstant_byte(int VALUE) {
        if (konstant_endre_storleik == konstant_VALUE.length) { feil_VALUE("constant pool too large"); return; }
        konstant_VALUE[konstant_endre_storleik++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { skrive_konstant_byte(VALUE >> 8); skrive_konstant_byte(VALUE); }
    static int registrere_konstant(int Køyr_2) {
        for (int 수 = 1; 수 < konstant_COUNT; 수++) {
            int 앞 = konstant_OFFSET[수], lengd_VALUE = (수 + 1 < konstant_COUNT ? konstant_OFFSET[수 + 1] : Køyr_2) - 앞;
            if (lengd_VALUE != konstant_endre_storleik - Køyr_2) continue;
            boolean 같음 = true;
            for (int felt_oppføring = 0; felt_oppføring < lengd_VALUE; felt_oppføring++) if (konstant_VALUE[앞 + felt_oppføring] != konstant_VALUE[Køyr_2 + felt_oppføring]) 같음 = false;
            if (같음) { konstant_endre_storleik = Køyr_2; return 수; }
        }
        if (konstant_COUNT == konstant_OFFSET.length) { feil_VALUE("too many constants"); return 0; }
        konstant_OFFSET[konstant_COUNT] = Køyr_2;
        return konstant_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (teikn_lengd == 문자.length) { feil_VALUE("text too long"); return; }
        문자[teikn_lengd++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int teikn_konstant() {
        int Køyr_2 = konstant_endre_storleik; skrive_konstant_byte(1); 상짧(0);
        for (int 수 = 0; 수 < teikn_lengd; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) skrive_konstant_byte(VALUE);
            else if (VALUE < 2048) { skrive_konstant_byte(192 | VALUE >> 6); skrive_konstant_byte(128 | VALUE & 63); }
            else { skrive_konstant_byte(224 | VALUE >> 12); skrive_konstant_byte(128 | VALUE >> 6 & 63); skrive_konstant_byte(128 | VALUE & 63); }
        }
        if (FEIL) return 0;
        int lengd_VALUE = konstant_endre_storleik - Køyr_2 - 3;
        konstant_VALUE[Køyr_2 + 1] = lengd_VALUE >> 8; konstant_VALUE[Køyr_2 + 2] = lengd_VALUE & 255;
        return registrere_konstant(Køyr_2);
    }
    static int Word_konstant(String Word_SMS) { teikn_lengd = 0; 말추가(Word_SMS); return teikn_konstant(); }
    static int token_konstant(int token_VALUE) {
        teikn_lengd = 0;
        for (int 수 = 0; 수 < token_lengd[token_VALUE]; 수++) 글추가(KJELDE[token_plassere[token_VALUE] + 수]);
        return teikn_konstant();
    }
    static int Oppslagsverk(int 종류, int 가, int 나) {
        int Køyr_2 = konstant_endre_storleik; skrive_konstant_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return registrere_konstant(Køyr_2);
    }
    static int ekstern_Oppslagsverk(int 종류, String eigar_VALUE, String Namn, String 서술) {
        int eigar_identifikator = Oppslagsverk(7, Word_konstant(eigar_VALUE), 0);
        int namn_COUNT = Word_konstant(Namn), format_COUNT = Word_konstant(서술);
        return Oppslagsverk(종류, eigar_identifikator, Oppslagsverk(12, namn_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_endre_storleik == CODE_VALUE.length) { feil_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_endre_storleik++] = VALUE & 255;
    }
    static void Kommando(int VALUE, int Argument) { 내보내기(VALUE); 내보내기(Argument >> 8); 내보내기(Argument); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int Køyr_2 = konstant_endre_storleik; skrive_konstant_byte(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        Kommando(19, registrere_konstant(Køyr_2));
    }
    static int grein(int Kommando) { int forretningsmål = CODE_endre_storleik; Kommando(Kommando, 0); return forretningsmål; }
    static void kople_VALUE(int grein, int mål_objekt) {
        if (FEIL) return;
        int 거리 = mål_objekt - grein;
        if (거리 < -32768 || 거리 > 32767 || grein < 0 || grein + 2 >= CODE_endre_storleik) { feil_VALUE("invalid branch"); return; }
        CODE_VALUE[grein + 1] = 거리 >> 8 & 255; CODE_VALUE[grein + 2] = 거리 & 255;
    }
    static void Samanlikning_VALUE(int Kommando) {
        int TRUE_VALUE = grein(Kommando); 내보내기(3); int 끝 = grein(167);
        kople_VALUE(TRUE_VALUE, CODE_endre_storleik); 내보내기(4); kople_VALUE(끝, CODE_endre_storleik);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        feil_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void leggje_til_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws erklæring. unntak Prosess_VALUE_oppføring 본문은 vert javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("unntak") || TAKE_Word("실행예외") || TAKE_Word("I_U_unntak") || TAKE_Word("vent_TIMEOUT_unntak") || TAKE_Word("ADDRESS_LOOKUP_unntak") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("ugyldig_argument_unntak") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_Oppslagsverk_unntak") || TAKE_Word("산술예외") || TAKE_Word("status_unntak") || TAKE_Word("TYPE_strøyme_unntak") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_feil") || TAKE_Word("tråd_status_unntak") || TAKE_Word("대기중단예외")) return;
        feil_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(Posisjon, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) feil_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); time_token = identifikator_VALUE();
        time_konstant = Oppslagsverk(7, token_konstant(time_token), 0);
        forelder_konstant = Oppslagsverk(7, Word_konstant("java/lang/Object"), 0); CODE_konstant = Word_konstant("Code"); 요구('{');
        while (!FEIL && 종류() != '}') {
            if (metode_COUNT == 32) { feil_VALUE("too many methods"); break; }
            int tilgang_oppføring = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int FUNCTION_VALUE = metode_COUNT++;
            metode_tilgang[FUNCTION_VALUE] = tilgang_oppføring | 8;
            metode_levere_tilbake[FUNCTION_VALUE] = format_VALUE(); metode_oppføring_namn[FUNCTION_VALUE] = identifikator_VALUE(); 요구('(');
            for (int 앞 = 0; 앞 < FUNCTION_VALUE; 앞++) if (이름같음(metode_oppføring_namn[앞], metode_oppføring_namn[FUNCTION_VALUE])) feil_VALUE("duplicate method (overloading unsupported)");
            while (!FEIL && 종류() != ')') {
                int 수 = metode_argument_COUNT[FUNCTION_VALUE];
                if (수 == 16) { feil_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) feil_VALUE("void parameter");
                metode_argument_TYPE[FUNCTION_VALUE * 16 + 수] = TYPE_VALUE; metode_argument_namn[FUNCTION_VALUE * 16 + 수] = identifikator_VALUE();
                metode_argument_COUNT[FUNCTION_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!FEIL && 받기(','));
            }
            metode_brødtekst[FUNCTION_VALUE] = Posisjon; 요구('{');
            int 중첩 = 1;
            while (Posisjon < token_COUNT && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                Posisjon++;
            }
            if (중첩 != 0) feil_VALUE("unclosed method body");
            metode_avslutte[FUNCTION_VALUE] = Posisjon;
            metode_namn_konstant[FUNCTION_VALUE] = token_konstant(metode_oppføring_namn[FUNCTION_VALUE]);
            teikn_lengd = 0; 글추가('(');
            for (int 수 = 0; 수 < metode_argument_COUNT[FUNCTION_VALUE]; 수++) leggje_til_format(metode_argument_TYPE[FUNCTION_VALUE * 16 + 수]);
            글추가(')'); leggje_til_format(metode_levere_tilbake[FUNCTION_VALUE]); 함수서술[FUNCTION_VALUE] = teikn_konstant();
        }
        요구('}'); if (Posisjon != token_COUNT) feil_VALUE("extra input after class");
    }
    static int Søk_lokal(int Namn) {
        for (int 수 = lokal_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokal_namn[수], Namn)) return 수;
        feil_VALUE("unknown variable"); return 0;
    }
    static int leggje_til_lokal(int Namn, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokal_namn[수], Namn)) feil_VALUE("duplicate local variable");
        if (lokal_COUNT == 128) { feil_VALUE("too many locals"); return 0; }
        lokal_namn[lokal_COUNT] = Namn; lokal_TYPE[lokal_COUNT] = TYPE_VALUE; 지역깊이[lokal_COUNT] = 깊이;
        return lokal_COUNT++;
    }
    static boolean heiltal_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void skrive_lokal(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void stadfeste_TYPE(int faktisk_data, int 기대) { if (faktisk_data != 기대 && !(faktisk_data == 5 && 기대 == 1)) feil_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        teikn_lengd = 0; int Køyr_2 = token_plassere[token_VALUE] + 1, 끝 = token_plassere[token_VALUE] + token_lengd[token_VALUE] - 1;
        while (Køyr_2 < 끝 && !FEIL) {
            int VALUE = KJELDE[Køyr_2++];
            if (VALUE == '\\') {
                if (Køyr_2 == 끝) { feil_VALUE("invalid escape"); break; }
                VALUE = KJELDE[Køyr_2++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') feil_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int dele_opp_heiltal(int token_VALUE, boolean 음수) {
        if (token_lengd[token_VALUE] > 1 && KJELDE[token_plassere[token_VALUE]] == '0') feil_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_lengd[token_VALUE]; 수++) {
            int siffer_vare = KJELDE[token_plassere[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && siffer_vare > (음수 ? 8 : 7)) feil_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - siffer_vare;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { feil_VALUE("only file streams supported by new in source"); return 0; }
            String eigar_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Kommando(187, Oppslagsverk(7, Word_konstant(eigar_VALUE), 0)); 내보내기(89);
            요구('('); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) feil_VALUE("input stream constructor arguments"); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 2); 이어 = true; }
            요구(')');
            Kommando(183, ekstern_Oppslagsverk(10, eigar_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = uttrykk_VALUE_eb3593ac(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(dele_opp_heiltal(Posisjon++, false)); return 1; }
        if (종류() == 258) { 문자읽기(Posisjon++); Kommando(19, Oppslagsverk(8, teikn_konstant(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(Posisjon++); if (teikn_lengd != 1) feil_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String eigar_VALUE = "", metode_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, forretningsmål = 0;
            if (TAKE_Word("Utdata")) {
                eigar_VALUE = "한국어/자체/Utdata"; 요구('.');
                if (TAKE_Word("skrive_line")) { metode_VALUE = "skrive_line"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("Skriv")) { metode_VALUE = "Skriv"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { metode_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else feil_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                eigar_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("lengd_VALUE")) { metode_VALUE = "lengd_VALUE"; 서술 = "(Ljava/lang/String;)I"; forretningsmål = 1; }
                else if (TAKE_Word("teiknkode_COUNT")) { metode_VALUE = "teiknkode_COUNT"; 서술 = "(Ljava/lang/String;)I"; forretningsmål = 1; }
                else if (TAKE_Word("dele_opp_heiltal")) { metode_VALUE = "dele_opp_heiltal"; 서술 = "(Ljava/lang/String;)I"; forretningsmål = 1; }
                else if (TAKE_Word("skrive_heiltal_VALUE")) { metode_VALUE = "skrive_heiltal_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; forretningsmål = 3; }
                else if (TAKE_Word("같음")) { metode_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; forretningsmål = 2; }
                else if (TAKE_Word("lime_inn_SMS")) { metode_VALUE = "lime_inn_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; forretningsmål = 3; }
                else if (TAKE_Word("klippe_VALUE")) { metode_VALUE = "klippe_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; forretningsmål = 3; }
                else feil_VALUE("unknown Korean text method");
            } else if (TAKE_Word("Fil")) {
                eigar_VALUE = "한국어/자체/Fil"; 요구('.'); 가 = 3;
                if (TAKE_Word("Les")) { metode_VALUE = "Les"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; forretningsmål = 3; }
                else if (TAKE_Word("Skriv")) { metode_VALUE = "Skriv"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else feil_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                eigar_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { metode_VALUE = "너비"; 서술 = "()I"; forretningsmål = 1; }
                else if (TAKE_Word("높이")) { metode_VALUE = "높이"; 서술 = "()I"; forretningsmål = 1; }
                else if (TAKE_Word("사각형")) { metode_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("지우기")) { metode_VALUE = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { metode_VALUE = "기다리기"; 서술 = "()V"; }
                else feil_VALUE("unknown Korean framebuffer method");
            } else feil_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 가);
            if (나 != 0) { 요구(','); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 나); }
            if (다 != 0) { 요구(','); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 다); }
            if (라 != 0) { 요구(','); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 라); }
            if (마 != 0) { 요구(','); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 마); }
            요구(')'); Kommando(184, ekstern_Oppslagsverk(10, eigar_VALUE, metode_VALUE, 서술)); return forretningsmål;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 3); 요구(')');
            Kommando(184, ekstern_Oppslagsverk(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Namn = identifikator_VALUE();
        if (받기('(')) {
            int FUNCTION_VALUE = -1;
            for (int 수 = 0; 수 < metode_COUNT; 수++) if (이름같음(Namn, metode_oppføring_namn[수])) FUNCTION_VALUE = 수;
            if (FUNCTION_VALUE < 0) { feil_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!FEIL && 종류() != ')') {
                if (수 >= metode_argument_COUNT[FUNCTION_VALUE]) { feil_VALUE("too many arguments"); break; }
                stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), metode_argument_TYPE[FUNCTION_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != metode_argument_COUNT[FUNCTION_VALUE]) feil_VALUE("argument count mismatch");
            Kommando(184, Oppslagsverk(10, time_konstant, Oppslagsverk(12, metode_namn_konstant[FUNCTION_VALUE], 함수서술[FUNCTION_VALUE])));
            return metode_levere_tilbake[FUNCTION_VALUE];
        }
        int lokal_område = Søk_lokal(Namn), TYPE_VALUE = lokal_TYPE[lokal_område]; 지역읽기(lokal_område);
        while (!FEIL) {
            if (받기('[')) { stadfeste_TYPE(TYPE_VALUE, 4); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String eigar_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); Kommando(182, ekstern_Oppslagsverk(10, eigar_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); Kommando(182, ekstern_Oppslagsverk(10, eigar_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 1); 요구(')'); Kommando(182, ekstern_Oppslagsverk(10, eigar_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { feil_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { stadfeste_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); Kommando(182, ekstern_Oppslagsverk(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { feil_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { stadfeste_TYPE(단항(), 2); Samanlikning_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(dele_opp_heiltal(Posisjon++, true));
            else { stadfeste_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { stadfeste_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!FEIL && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int koding_VALUE = 종류(); Posisjon++; stadfeste_TYPE(TYPE_VALUE, 1); stadfeste_TYPE(단항(), 1);
            내보내기(koding_VALUE == '*' ? 104 : koding_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!FEIL && (종류() == '+' || 종류() == '-')) {
            int koding_VALUE = 종류(); Posisjon++; int 경계 = CODE_endre_storleik, TILBAKE_VALUE_TYPE = 곱식();
            if (koding_VALUE == '+' && (TYPE_VALUE == 3 || TILBAKE_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, TILBAKE_VALUE_TYPE); TYPE_VALUE = 3; }
            else { stadfeste_TYPE(TYPE_VALUE, 1); stadfeste_TYPE(TILBAKE_VALUE_TYPE, 1); 내보내기(koding_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) feil_VALUE("unsupported concatenation type");
        return ekstern_Oppslagsverk(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int TILBAKE_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 generere 코드를 삽입한다.
        // RIGHT uttrykk_VALUE_eb3593ac 내부의 node_VALUE_6a3b6fa7 grein 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_endre_storleik;
        Kommando(187, Oppslagsverk(7, Word_konstant("java/lang/StringBuilder"), 0)); 내보내기(89);
        Kommando(183, ekstern_Oppslagsverk(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Kommando(182, 붙임참조(앞형));
        if (FEIL) return;
        int lengd_VALUE = CODE_endre_storleik - 끝;
        for (int 수 = 0; 수 < lengd_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + lengd_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < lengd_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        Kommando(182, 붙임참조(TILBAKE_VALUE_TYPE)); Kommando(182, ekstern_Oppslagsverk(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Samanlikning_uttrykk() {
        int TYPE_VALUE = 합식();
        while (!FEIL && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int koding_VALUE = 종류(); Posisjon++; stadfeste_TYPE(TYPE_VALUE, 1); stadfeste_TYPE(합식(), 1);
            Samanlikning_VALUE(koding_VALUE == '<' ? 161 : koding_VALUE == '>' ? 163 : koding_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Samanlikning_uttrykk();
        while (!FEIL && (종류() == 300 || 종류() == 301)) {
            int koding_VALUE = 종류(); Posisjon++; int TILBAKE_VALUE_TYPE = Samanlikning_uttrykk();
            if (TYPE_VALUE == 0 || TILBAKE_VALUE_TYPE == 0) feil_VALUE("void expression");
            if (!(heiltal_TYPE(TYPE_VALUE) && heiltal_TYPE(TILBAKE_VALUE_TYPE))) stadfeste_TYPE(TILBAKE_VALUE_TYPE, TYPE_VALUE);
            Samanlikning_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (koding_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!FEIL && 받기(304)) {
            stadfeste_TYPE(TYPE_VALUE, 2); int 가 = grein(153); stadfeste_TYPE(동등식(), 2); int 나 = grein(153);
            내보내기(4); int 끝 = grein(167); kople_VALUE(가, CODE_endre_storleik); kople_VALUE(나, CODE_endre_storleik); 내보내기(3); kople_VALUE(끝, CODE_endre_storleik); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int uttrykk_VALUE_eb3593ac() {
        int TYPE_VALUE = 논리곱();
        while (!FEIL && 받기(305)) {
            stadfeste_TYPE(TYPE_VALUE, 2); int 가 = grein(154); stadfeste_TYPE(논리곱(), 2); int 나 = grein(154);
            내보내기(3); int 끝 = grein(167); kople_VALUE(가, CODE_endre_storleik); kople_VALUE(나, CODE_endre_storleik); 내보내기(4); kople_VALUE(끝, CODE_endre_storleik); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void oppgåve_VALUE(boolean Tillat_erklæring) {
        if (Word_VALUE(Posisjon, "int") || Word_VALUE(Posisjon, "boolean") || Word_VALUE(Posisjon, "String") || Word_VALUE(Posisjon, "char")
            || Word_VALUE(Posisjon, "FileInputStream") || Word_VALUE(Posisjon, "FileOutputStream")) {
            if (!Tillat_erklæring) feil_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), Namn = identifikator_VALUE(); 요구('='); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), TYPE_VALUE);
            skrive_lokal(leggje_til_lokal(Namn, TYPE_VALUE)); return;
        }
        int Namn = identifikator_VALUE(), lokal_område = Søk_lokal(Namn);
        if (받기('=')) { stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), lokal_TYPE[lokal_område]); skrive_lokal(lokal_område); }
        else if (종류() >= 308 && 종류() <= 312) {
            int koding_VALUE = 종류(); Posisjon++; 지역읽기(lokal_område); int 경계 = CODE_endre_storleik, TILBAKE_VALUE_TYPE = uttrykk_VALUE_eb3593ac();
            if (koding_VALUE == 308 && lokal_TYPE[lokal_område] == 3) 결합(경계, 3, TILBAKE_VALUE_TYPE);
            else {
                stadfeste_TYPE(lokal_TYPE[lokal_område], 1); stadfeste_TYPE(TILBAKE_VALUE_TYPE, 1);
                내보내기(koding_VALUE == 308 ? 96 : koding_VALUE == 309 ? 100 : koding_VALUE == 310 ? 104 : koding_VALUE == 311 ? 108 : 112);
                if (lokal_TYPE[lokal_område] == 5) 내보내기(146);
            }
            skrive_lokal(lokal_område);
        }
        else if (종류() == 306 || 종류() == 307) {
            stadfeste_TYPE(lokal_TYPE[lokal_område], 1); 내보내기(132); 내보내기(lokal_område); 내보내기(종류() == 306 ? 1 : 255); Posisjon++;
            if (lokal_TYPE[lokal_område] == 5) { 지역읽기(lokal_område); 내보내기(146); skrive_lokal(lokal_område); }
        } else feil_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Kommando(178, ekstern_Oppslagsverk(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean tom_argument = 종류() == ')';
        int TYPE_VALUE = tom_argument ? 0 : uttrykk_VALUE_eb3593ac(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !tom_argument)) feil_VALUE("unsupported print argument");
        Kommando(182, ekstern_Oppslagsverk(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean uttrykk_VALUE() {
        if (FEIL) return false;
        if (깊이 > 32) { feil_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean levere_tilbake_forretningsmål = false;
            while (!FEIL && 종류() != '}') { if (levere_tilbake_forretningsmål) feil_VALUE("unreachable statement"); levere_tilbake_forretningsmål = uttrykk_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return levere_tilbake_forretningsmål;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : uttrykk_VALUE_eb3593ac(); stadfeste_TYPE(TYPE_VALUE, metode_levere_tilbake[betalt_metode]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 2); 요구(')'); int FALSE_VALUE = grein(153);
            깊이++; boolean 가 = styring_uttrykk(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = grein(167); kople_VALUE(FALSE_VALUE, CODE_endre_storleik); 깊이++; boolean 나 = styring_uttrykk(); 깊이--; kople_VALUE(끝, CODE_endre_storleik); return 가 && 나; }
            kople_VALUE(FALSE_VALUE, CODE_endre_storleik); return false;
        }
        if (TAKE_Word("while")) {
            int Køyr_2 = CODE_endre_storleik; 요구('('); stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 2); 요구(')'); int 끝 = grein(153);
            깊이++; styring_uttrykk(); 깊이--; kople_VALUE(grein(167), Køyr_2); kople_VALUE(끝, CODE_endre_storleik); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') oppgåve_VALUE(true); 요구(';');
            int tilstand = CODE_endre_storleik; if (종류() == ';') 내보내기(4); else stadfeste_TYPE(uttrykk_VALUE_eb3593ac(), 2); 요구(';');
            int 끝 = grein(153), brødtekst = grein(167), oppdatere = CODE_endre_storleik;
            if (종류() != ')') oppgåve_VALUE(false); 요구(')'); kople_VALUE(grein(167), tilstand); kople_VALUE(brødtekst, CODE_endre_storleik);
            styring_uttrykk(); kople_VALUE(grein(167), oppdatere); kople_VALUE(끝, CODE_endre_storleik);
            for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(Posisjon, "System")) { 화면출력(); return false; }
        if (종류() == 256 && Posisjon + 1 < token_COUNT && (토큰종류[Posisjon + 1] == '(' || 토큰종류[Posisjon + 1] == '.')) {
            int TYPE_VALUE = uttrykk_VALUE_eb3593ac(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        oppgåve_VALUE(true); 요구(';'); return false;
    }
    static boolean styring_uttrykk() {
        if (Word_VALUE(Posisjon, "int") || Word_VALUE(Posisjon, "boolean") || Word_VALUE(Posisjon, "char") || Word_VALUE(Posisjon, "String")
            || Word_VALUE(Posisjon, "FileInputStream") || Word_VALUE(Posisjon, "FileOutputStream")) feil_VALUE("local declaration requires braces");
        return uttrykk_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == Utdata.length) feil_VALUE("class file too large"); else Utdata[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void skrive_time() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(konstant_COUNT);
        for (int 수 = 0; 수 < konstant_endre_storleik; 수++) 출바(konstant_VALUE[수]);
        출짧(0x21); 출짧(time_konstant); 출짧(forelder_konstant); 출짧(0); 출짧(0); 출짧(metode_COUNT);
        for (int 수 = 0; 수 < metode_COUNT; 수++) {
            출짧(metode_tilgang[수]); 출짧(metode_namn_konstant[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_konstant);
            출정(12 + metode_lengd[수]); 출짧(128); 출짧(함수지역[수]); 출정(metode_lengd[수]);
            for (int felt_oppføring = 0; felt_oppføring < metode_lengd[수]; felt_oppføring++) 출바(CODE_VALUE[metode_CODE[수] + felt_oppføring]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Køyr_2() {
        if (brukar.인수개수() == 1 && 자바도구.같음(brukar.Argument(0), "-version")) {
            brukar.Skriv("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (brukar.인수개수() != 1) { brukar.Skriv("Usage: javac FILE.java\n"); return 2; }
        int namn_endre_storleik = 자바도구.Namn(fil_namn_SMS, brukar.Argument(0));
        if (namn_endre_storleik < 6 || namn_endre_storleik > 62 || fil_namn_SMS[namn_endre_storleik - 5] != '.' || fil_namn_SMS[namn_endre_storleik - 4] != 'j'
            || fil_namn_SMS[namn_endre_storleik - 3] != 'a' || fil_namn_SMS[namn_endre_storleik - 2] != 'v' || fil_namn_SMS[namn_endre_storleik - 1] != 'a') {
            brukar.Skriv("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        kjelde_endre_storleik = brukar.파일읽기(fil_namn_SMS, KJELDE);
        if (kjelde_endre_storleik < 0) { brukar.Skriv("javac: cannot read source: "); 자바도구.수쓰기(kjelde_endre_storleik); brukar.skrive_teikn_VALUE(10); return 1; }
        kjelde_endre_storleik = 자바도구.원문해독(KJELDE, kjelde_endre_storleik);
        if (kjelde_endre_storleik < 0) { brukar.Skriv("javac error: invalid UTF-8 source\n"); return 1; }
        klippe_VALUE(); if (!FEIL) 선언읽기();
        if (!FEIL) {
            if (token_lengd[time_token] != namn_endre_storleik - 5) feil_VALUE("class name must match file name");
            for (int 수 = 0; 수 < namn_endre_storleik - 5; 수++) if (KJELDE[token_plassere[time_token] + 수] != fil_namn_SMS[수]) feil_VALUE("class name must match file name");
        }
        for (betalt_metode = 0; betalt_metode < metode_COUNT && !FEIL; betalt_metode++) {
            Posisjon = metode_brødtekst[betalt_metode]; metode_CODE[betalt_metode] = CODE_endre_storleik; lokal_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < metode_argument_COUNT[betalt_metode]; 수++) leggje_til_lokal(metode_argument_namn[betalt_metode * 16 + 수], metode_argument_TYPE[betalt_metode * 16 + 수]);
            boolean levere_tilbake_forretningsmål = uttrykk_VALUE();
            if (!levere_tilbake_forretningsmål && metode_levere_tilbake[betalt_metode] != 0) feil_VALUE("missing return");
            // grein 뒤의 합류 지점은 반드시 faktisk_data 명령이어야 한다 (버전 49 검증기).
            if (metode_levere_tilbake[betalt_metode] == 0) 내보내기(177);
            else { boolean heiltal = metode_levere_tilbake[betalt_metode] <= 2 || metode_levere_tilbake[betalt_metode] == 5; 내보내기(heiltal ? 3 : 1); 내보내기(heiltal ? 172 : 176); }
            if (Posisjon != metode_avslutte[betalt_metode]) feil_VALUE("invalid method body");
            함수지역[betalt_metode] = lokal_COUNT; metode_lengd[betalt_metode] = CODE_endre_storleik - metode_CODE[betalt_metode];
        }
        if (FEIL) return 1;
        skrive_time(); if (FEIL) return 1;
        fil_namn_SMS[namn_endre_storleik - 4] = 'c'; fil_namn_SMS[namn_endre_storleik - 3] = 'l'; fil_namn_SMS[namn_endre_storleik - 2] = 'a';
        fil_namn_SMS[namn_endre_storleik - 1] = 's'; fil_namn_SMS[namn_endre_storleik] = 's'; fil_namn_SMS[namn_endre_storleik + 1] = 0;
        int forretningsmål = brukar.skrive_fil(fil_namn_SMS, Utdata, 출력크기);
        if (forretningsmål < 0) { brukar.Skriv("javac: cannot save class: "); 자바도구.수쓰기(forretningsmål); brukar.skrive_teikn_VALUE(10); return 1; }
        brukar.Skriv("Compiled: "); for (int 수 = 0; fil_namn_SMS[수] != 0; 수++) brukar.skrive_teikn_VALUE(fil_namn_SMS[수]);
        brukar.Skriv(" (JVM class version 49)\n"); return 0;
    }
}
