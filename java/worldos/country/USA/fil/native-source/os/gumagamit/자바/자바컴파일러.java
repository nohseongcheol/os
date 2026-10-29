// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java pinagmulan_balangkas -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] pinagmulan = new int[16384], 출력 = new int[16384], CODE_VALUE = new int[4096];
    static int[] 토큰종류 = new int[2048], token_posisyon = new int[2048], token_haba = new int[2048];
    static int[] constant_VALUE = new int[4096], constant_OFFSET = new int[512];
    static int[] 문자 = new int[512], file_pangalan_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int pinagmulan_sukat, token_COUNT, posisyon, CODE_sukat, constant_sukat, constant_COUNT = 1, 출력크기, karakter_haba;
    static boolean error;
    static int kategorya_token, kategorya_constant, 부모상수, CODE_constant;
    static int[] pamamaraan_pagpasok_pangalan = new int[32], 함수반환 = new int[32], pamamaraan_argumento_COUNT = new int[32];
    static int[] pamamaraan_argumento_pangalan = new int[512], pamamaraan_argumento_TYPE = new int[512];
    static int[] pamamaraan_katawan = new int[32], pamamaraan_tapusin = new int[32], pamamaraan_CODE = new int[32];
    static int[] pamamaraan_haba = new int[32], 함수지역 = new int[32], pamamaraan_pangalan_constant = new int[32], 함수서술 = new int[32];
    static int[] pamamaraan_access = new int[32];
    static int pamamaraan_COUNT, 현재함수, lokal_COUNT, 깊이, 식깊이;
    static int[] lokal_pangalan = new int[128], lokal_TYPE = new int[128], 지역깊이 = new int[128];

    static void pagpalya_VALUE(String 이유) {
        if (!error) {
            gumagamit.sumulat("javac error: "); gumagamit.sumulat(이유);
            gumagamit.sumulat(" at line ");
            int linya = 1, 끝 = posisyon < token_COUNT ? token_posisyon[posisyon] : pinagmulan_sukat;
            for (int 수 = 0; 수 < 끝; 수++) if (pinagmulan[수] == 10) linya++;
            자바도구.수쓰기(linya); gumagamit.sumulat_karakter_VALUE(10);
        }
        error = true;
    }
    static boolean karakter_VALUE(int VALUE) { return 문자이름규칙.첫글자(VALUE); }
    static boolean digit_VALUE(int VALUE) { return VALUE >= '0' && VALUE <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= token_COUNT || 나 >= token_COUNT || token_haba[가] != token_haba[나]) return false;
        for (int 수 = 0; 수 < token_haba[가]; 수++) if (pinagmulan[token_posisyon[가] + 수] != pinagmulan[token_posisyon[나] + 수]) return false;
        return true;
    }
    static boolean Word_VALUE(int token_VALUE, String Word_SMS) {
        if (token_VALUE < 0 || token_VALUE >= token_COUNT || token_haba[token_VALUE] != Word_SMS.length()) return false;
        for (int 수 = 0; 수 < Word_SMS.length(); 수++) if (pinagmulan[token_posisyon[token_VALUE] + 수] != Word_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return posisyon < token_COUNT ? 토큰종류[posisyon] : 0; }
    static boolean 받기(int VALUE) { if (종류() != VALUE) return false; posisyon++; return true; }
    static void 요구(int VALUE) { if (!받기(VALUE)) pagpalya_VALUE("unexpected token"); }
    static boolean TAKE_Word(String Word_SMS) { if (!Word_VALUE(posisyon, Word_SMS)) return false; posisyon++; return true; }
    static void 말요구(String Word_SMS) { if (!TAKE_Word(Word_SMS)) pagpalya_VALUE(Word_SMS); }
    static int tagakilala_VALUE() {
        int sukat = posisyon;
        if (종류() != 256) pagpalya_VALUE("identifier required"); else posisyon++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int run = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - run == token_haba[sukat];
                for (int espasyo_pagpasok = run; 같음 && espasyo_pagpasok < 수; espasyo_pagpasok++) if (예약어.charAt(espasyo_pagpasok) != pinagmulan[token_posisyon[sukat] + espasyo_pagpasok - run]) 같음 = false;
                if (같음) pagpalya_VALUE("reserved word cannot be an identifier");
                run = 수 + 1;
            }
        }
        return sukat;
    }
    static void I_cut_VALUE() {
        int 수 = 0;
        while (수 < pinagmulan_sukat && !error) {
            int VALUE = pinagmulan[수], run = 수, 종류 = VALUE;
            if (VALUE == 32 || VALUE == 9 || VALUE == 10 || VALUE == 13) { 수++; continue; }
            if (VALUE == '/' && 수 + 1 < pinagmulan_sukat && pinagmulan[수 + 1] == '/') {
                while (수 < pinagmulan_sukat && pinagmulan[수] != 10) 수++;
                continue;
            }
            if (VALUE == '/' && 수 + 1 < pinagmulan_sukat && pinagmulan[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < pinagmulan_sukat && !(pinagmulan[수] == '*' && pinagmulan[수 + 1] == '/')) 수++;
                if (수 + 1 >= pinagmulan_sukat) { pagpalya_VALUE("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (karakter_VALUE(VALUE)) { 종류 = 256; while (수 < pinagmulan_sukat && 문자이름규칙.이어진글자(pinagmulan[수])) 수++; }
            else if (digit_VALUE(VALUE)) { 종류 = 257; while (수 < pinagmulan_sukat && digit_VALUE(pinagmulan[수])) 수++; }
            else if (VALUE == '"' || VALUE == '\'') {
                종류 = VALUE == '"' ? 258 : 259; 수++;
                while (수 < pinagmulan_sukat && pinagmulan[수] != VALUE && pinagmulan[수] != 10 && pinagmulan[수] != 13) {
                    if (pinagmulan[수] == '\\') 수++;
                    수++;
                }
                if (수 >= pinagmulan_sukat || pinagmulan[수] != VALUE) { pagpalya_VALUE("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < pinagmulan_sukat) {
                    int Susunod_item = pinagmulan[수];
                    if (VALUE == '=' && Susunod_item == '=') 종류 = 300;
                    if (VALUE == '!' && Susunod_item == '=') 종류 = 301;
                    if (VALUE == '<' && Susunod_item == '=') 종류 = 302;
                    if (VALUE == '>' && Susunod_item == '=') 종류 = 303;
                    if (VALUE == '&' && Susunod_item == '&') 종류 = 304;
                    if (VALUE == '|' && Susunod_item == '|') 종류 = 305;
                    if (VALUE == '+' && Susunod_item == '+') 종류 = 306;
                    if (VALUE == '-' && Susunod_item == '-') 종류 = 307;
                    if (VALUE == '+' && Susunod_item == '=') 종류 = 308;
                    if (VALUE == '-' && Susunod_item == '=') 종류 = 309;
                    if (VALUE == '*' && Susunod_item == '=') 종류 = 310;
                    if (VALUE == '/' && Susunod_item == '=') 종류 = 311;
                    if (VALUE == '%' && Susunod_item == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (token_COUNT == 토큰종류.length - 1) { pagpalya_VALUE("too many tokens (2047 maximum)"); break; }
            토큰종류[token_COUNT] = 종류; token_posisyon[token_COUNT] = run; token_haba[token_COUNT++] = 수 - run;
        }
    }
    static void sumulat_constant_byte(int VALUE) {
        if (constant_sukat == constant_VALUE.length) { pagpalya_VALUE("constant pool too large"); return; }
        constant_VALUE[constant_sukat++] = VALUE & 255;
    }
    static void 상짧(int VALUE) { sumulat_constant_byte(VALUE >> 8); sumulat_constant_byte(VALUE); }
    static int magrehistro_constant(int run) {
        for (int 수 = 1; 수 < constant_COUNT; 수++) {
            int nasa_harap_VALUE = constant_OFFSET[수], haba_VALUE = (수 + 1 < constant_COUNT ? constant_OFFSET[수 + 1] : run) - nasa_harap_VALUE;
            if (haba_VALUE != constant_sukat - run) continue;
            boolean 같음 = true;
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < haba_VALUE; espasyo_pagpasok++) if (constant_VALUE[nasa_harap_VALUE + espasyo_pagpasok] != constant_VALUE[run + espasyo_pagpasok]) 같음 = false;
            if (같음) { constant_sukat = run; return 수; }
        }
        if (constant_COUNT == constant_OFFSET.length) { pagpalya_VALUE("too many constants"); return 0; }
        constant_OFFSET[constant_COUNT] = run;
        return constant_COUNT++;
    }
    static void 글추가(int VALUE) {
        if (karakter_haba == 문자.length) { pagpalya_VALUE("text too long"); return; }
        문자[karakter_haba++] = VALUE;
    }
    static void 말추가(String Word_SMS) { for (int 수 = 0; 수 < Word_SMS.length(); 수++) 글추가(Word_SMS.charAt(수)); }
    static int karakter_constant() {
        int run = constant_sukat; sumulat_constant_byte(1); 상짧(0);
        for (int 수 = 0; 수 < karakter_haba; 수++) {
            int VALUE = 문자[수];
            if (VALUE > 0 && VALUE < 128) sumulat_constant_byte(VALUE);
            else if (VALUE < 2048) { sumulat_constant_byte(192 | VALUE >> 6); sumulat_constant_byte(128 | VALUE & 63); }
            else { sumulat_constant_byte(224 | VALUE >> 12); sumulat_constant_byte(128 | VALUE >> 6 & 63); sumulat_constant_byte(128 | VALUE & 63); }
        }
        if (error) return 0;
        int haba_VALUE = constant_sukat - run - 3;
        constant_VALUE[run + 1] = haba_VALUE >> 8; constant_VALUE[run + 2] = haba_VALUE & 255;
        return magrehistro_constant(run);
    }
    static int Word_constant(String Word_SMS) { karakter_haba = 0; 말추가(Word_SMS); return karakter_constant(); }
    static int token_constant(int token_VALUE) {
        karakter_haba = 0;
        for (int 수 = 0; 수 < token_haba[token_VALUE]; 수++) 글추가(pinagmulan[token_posisyon[token_VALUE] + 수]);
        return karakter_constant();
    }
    static int Sanggunian(int 종류, int 가, int 나) {
        int run = constant_sukat; sumulat_constant_byte(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return magrehistro_constant(run);
    }
    static int 외부참조(int 종류, String may_ari_VALUE, String pangalan, String 서술) {
        int may_ari_tagakilala = Sanggunian(7, Word_constant(may_ari_VALUE), 0);
        int pangalan_COUNT = Word_constant(pangalan), format_COUNT = Word_constant(서술);
        return Sanggunian(종류, may_ari_tagakilala, Sanggunian(12, pangalan_COUNT, format_COUNT));
    }
    static void 내보내기(int VALUE) {
        if (CODE_sukat == CODE_VALUE.length) { pagpalya_VALUE("bytecode too large"); return; }
        CODE_VALUE[CODE_sukat++] = VALUE & 255;
    }
    static void utos(int VALUE, int 인수) { 내보내기(VALUE); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int VALUE) {
        if (VALUE >= -1 && VALUE <= 5) { 내보내기(VALUE + 3); return; }
        int run = constant_sukat; sumulat_constant_byte(3); 상짧(VALUE >>> 16); 상짧(VALUE);
        utos(19, magrehistro_constant(run));
    }
    static int sanga(int utos) { int sukat = CODE_sukat; utos(utos, 0); return sukat; }
    static void Link_VALUE(int sanga, int target_bagay) {
        if (error) return;
        int 거리 = target_bagay - sanga;
        if (거리 < -32768 || 거리 > 32767 || sanga < 0 || sanga + 2 >= CODE_sukat) { pagpalya_VALUE("invalid branch"); return; }
        CODE_VALUE[sanga + 1] = 거리 >> 8 & 255; CODE_VALUE[sanga + 2] = 거리 & 255;
    }
    static void Paghahambing_VALUE(int utos) {
        int TRUE_VALUE = sanga(utos); 내보내기(3); int 끝 = sanga(167);
        Link_VALUE(TRUE_VALUE, CODE_sukat); 내보내기(4); Link_VALUE(끝, CODE_sukat);
    }
    static int format_VALUE() {
        if (TAKE_Word("void")) return 0;
        if (TAKE_Word("int")) return 1;
        if (TAKE_Word("boolean")) return 2;
        if (TAKE_Word("char")) return 5;
        if (TAKE_Word("FileInputStream")) return 6;
        if (TAKE_Word("FileOutputStream")) return 7;
        if (TAKE_Word("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        pagpalya_VALUE("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void idagdag_format(int TYPE_VALUE) {
        if (TYPE_VALUE == 0) 글추가('V');
        if (TYPE_VALUE == 1) 글추가('I');
        if (TYPE_VALUE == 2) 글추가('Z');
        if (TYPE_VALUE == 3) 말추가("Ljava/lang/String;");
        if (TYPE_VALUE == 4) 말추가("[Ljava/lang/String;");
        if (TYPE_VALUE == 5) 글추가('C');
        if (TYPE_VALUE == 6) 말추가("Ljava/io/FileInputStream;");
        if (TYPE_VALUE == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws declaration. pagbubukod Proseso_VALUE_pagpasok 본문은 host javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = TAKE_Word("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (TAKE_Word("Exception") || TAKE_Word("IOException"))) return;
        if (TAKE_Word("pagbubukod") || TAKE_Word("실행예외") || TAKE_Word("I_O_pagbubukod") || TAKE_Word("maghintay_TIMEOUT_pagbubukod") || TAKE_Word("email_LOOKUP_pagbubukod") || TAKE_Word("파일없음예외") || TAKE_Word("통신예외") || TAKE_Word("hindi_tama_argumento_pagbubukod") || TAKE_Word("숫자형식예외") || TAKE_Word("범위예외") || TAKE_Word("배열범위예외") || TAKE_Word("문자열범위예외") || TAKE_Word("NULL_Sanggunian_pagbubukod") || TAKE_Word("산술예외") || TAKE_Word("katayuan_pagbubukod") || TAKE_Word("TYPE_Cast_pagbubukod") || TAKE_Word("음수배열크기예외") || TAKE_Word("ARRAY_Store_pagpalya") || TAKE_Word("thread_katayuan_pagbubukod") || TAKE_Word("대기중단예외")) return;
        pagpalya_VALUE("unsupported throws type");
    }
    static void 선언읽기() {
        while (TAKE_Word("import")) {
            if (Word_VALUE(posisyon, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(TAKE_Word("FileInputStream") || TAKE_Word("FileOutputStream") || TAKE_Word("IOException"))) pagpalya_VALUE("unsupported import");
            }
            요구(';');
        }
        TAKE_Word("public"); TAKE_Word("final"); 말요구("class"); kategorya_token = tagakilala_VALUE();
        kategorya_constant = Sanggunian(7, token_constant(kategorya_token), 0);
        부모상수 = Sanggunian(7, Word_constant("java/lang/Object"), 0); CODE_constant = Word_constant("Code"); 요구('{');
        while (!error && 종류() != '}') {
            if (pamamaraan_COUNT == 32) { pagpalya_VALUE("too many methods"); break; }
            int access_pagpasok = TAKE_Word("public") ? 1 : TAKE_Word("private") ? 2 : 0; 말요구("static");
            int pormula_VALUE = pamamaraan_COUNT++;
            pamamaraan_access[pormula_VALUE] = access_pagpasok | 8;
            함수반환[pormula_VALUE] = format_VALUE(); pamamaraan_pagpasok_pangalan[pormula_VALUE] = tagakilala_VALUE(); 요구('(');
            for (int nasa_harap_VALUE = 0; nasa_harap_VALUE < pormula_VALUE; nasa_harap_VALUE++) if (이름같음(pamamaraan_pagpasok_pangalan[nasa_harap_VALUE], pamamaraan_pagpasok_pangalan[pormula_VALUE])) pagpalya_VALUE("duplicate method (overloading unsupported)");
            while (!error && 종류() != ')') {
                int 수 = pamamaraan_argumento_COUNT[pormula_VALUE];
                if (수 == 16) { pagpalya_VALUE("too many parameters"); break; }
                int TYPE_VALUE = format_VALUE(); if (TYPE_VALUE == 0) pagpalya_VALUE("void parameter");
                pamamaraan_argumento_TYPE[pormula_VALUE * 16 + 수] = TYPE_VALUE; pamamaraan_argumento_pangalan[pormula_VALUE * 16 + 수] = tagakilala_VALUE();
                pamamaraan_argumento_COUNT[pormula_VALUE]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (TAKE_Word("throws")) {
                do { 예외이름읽기(); } while (!error && 받기(','));
            }
            pamamaraan_katawan[pormula_VALUE] = posisyon; 요구('{');
            int nesting_VALUE = 1;
            while (posisyon < token_COUNT && nesting_VALUE > 0) {
                if (종류() == '{') nesting_VALUE++;
                if (종류() == '}') nesting_VALUE--;
                posisyon++;
            }
            if (nesting_VALUE != 0) pagpalya_VALUE("unclosed method body");
            pamamaraan_tapusin[pormula_VALUE] = posisyon;
            pamamaraan_pangalan_constant[pormula_VALUE] = token_constant(pamamaraan_pagpasok_pangalan[pormula_VALUE]);
            karakter_haba = 0; 글추가('(');
            for (int 수 = 0; 수 < pamamaraan_argumento_COUNT[pormula_VALUE]; 수++) idagdag_format(pamamaraan_argumento_TYPE[pormula_VALUE * 16 + 수]);
            글추가(')'); idagdag_format(함수반환[pormula_VALUE]); 함수서술[pormula_VALUE] = karakter_constant();
        }
        요구('}'); if (posisyon != token_COUNT) pagpalya_VALUE("extra input after class");
    }
    static int FIND_lokal(int pangalan) {
        for (int 수 = lokal_COUNT - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(lokal_pangalan[수], pangalan)) return 수;
        pagpalya_VALUE("unknown variable"); return 0;
    }
    static int idagdag_lokal(int pangalan, int TYPE_VALUE) {
        for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] >= 0 && 이름같음(lokal_pangalan[수], pangalan)) pagpalya_VALUE("duplicate local variable");
        if (lokal_COUNT == 128) { pagpalya_VALUE("too many locals"); return 0; }
        lokal_pangalan[lokal_COUNT] = pangalan; lokal_TYPE[lokal_COUNT] = TYPE_VALUE; 지역깊이[lokal_COUNT] = 깊이;
        return lokal_COUNT++;
    }
    static boolean integer_buong_numero_TYPE(int TYPE_VALUE) { return TYPE_VALUE == 1 || TYPE_VALUE == 5; }
    static void 지역읽기(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 21 : 25); 내보내기(수); }
    static void sumulat_lokal(int 수) { 내보내기(lokal_TYPE[수] <= 2 || lokal_TYPE[수] == 5 ? 54 : 58); 내보내기(수); }
    static void tiyakin_kumpirmahin_TYPE(int totoo_data, int 기대) { if (totoo_data != 기대 && !(totoo_data == 5 && 기대 == 1)) pagpalya_VALUE("type mismatch"); }
    static void 문자읽기(int token_VALUE) {
        karakter_haba = 0; int run = token_posisyon[token_VALUE] + 1, 끝 = token_posisyon[token_VALUE] + token_haba[token_VALUE] - 1;
        while (run < 끝 && !error) {
            int VALUE = pinagmulan[run++];
            if (VALUE == '\\') {
                if (run == 끝) { pagpalya_VALUE("invalid escape"); break; }
                VALUE = pinagmulan[run++];
                if (VALUE == 'n') VALUE = 10;
                else if (VALUE == 'r') VALUE = 13;
                else if (VALUE == 't') VALUE = 9;
                else if (VALUE == 'b') VALUE = 8;
                else if (VALUE == 'f') VALUE = 12;
                else if (VALUE != '\\' && VALUE != '"' && VALUE != '\'') pagpalya_VALUE("unsupported escape");
            }
            글추가(VALUE);
        }
    }
    static int mag_parse_integer_buong_numero(int token_VALUE, boolean 음수) {
        if (token_haba[token_VALUE] > 1 && pinagmulan[token_posisyon[token_VALUE]] == '0') pagpalya_VALUE("octal literals unsupported");
        int VALUE = 0;
        for (int 수 = 0; 수 < token_haba[token_VALUE]; 수++) {
            int digit_item = pinagmulan[token_posisyon[token_VALUE] + 수] - '0';
            if (VALUE < -214748364 || VALUE == -214748364 && digit_item > (음수 ? 8 : 7)) pagpalya_VALUE("integer literal out of range");
            VALUE = VALUE * 10 - digit_item;
        }
        return 음수 ? VALUE : -VALUE;
    }
    static int 기본식() {
        if (TAKE_Word("new")) {
            int TYPE_VALUE = format_VALUE();
            if (TYPE_VALUE != 6 && TYPE_VALUE != 7) { pagpalya_VALUE("only file streams supported by new in source"); return 0; }
            String may_ari_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            utos(187, Sanggunian(7, Word_constant(may_ari_VALUE), 0)); 내보내기(89);
            요구('('); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 3); boolean 이어 = false;
            if (받기(',')) { if (TYPE_VALUE != 7) pagpalya_VALUE("input stream constructor arguments"); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 2); 이어 = true; }
            요구(')');
            utos(183, 외부참조(10, may_ari_VALUE, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return TYPE_VALUE;
        }
        if (받기('(')) { int TYPE_VALUE = expression_VALUE(); 요구(')'); return TYPE_VALUE; }
        if (종류() == 257) { 수상수(mag_parse_integer_buong_numero(posisyon++, false)); return 1; }
        if (종류() == 258) { 문자읽기(posisyon++); utos(19, Sanggunian(8, karakter_constant(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(posisyon++); if (karakter_haba != 1) pagpalya_VALUE("character literal length"); 수상수(문자[0]); return 5; }
        if (TAKE_Word("true")) { 내보내기(4); return 2; }
        if (TAKE_Word("false")) { 내보내기(3); return 2; }
        if (TAKE_Word("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String may_ari_VALUE = "", pamamaraan_VALUE = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, sukat = 0;
            if (TAKE_Word("출력")) {
                may_ari_VALUE = "한국어/자체/출력"; 요구('.');
                if (TAKE_Word("sumulat_linya")) { pamamaraan_VALUE = "sumulat_linya"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("sumulat")) { pamamaraan_VALUE = "sumulat"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (TAKE_Word("수쓰기")) { pamamaraan_VALUE = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else pagpalya_VALUE("unknown Korean output method");
            } else if (TAKE_Word("문자")) {
                may_ari_VALUE = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (TAKE_Word("haba_VALUE")) { pamamaraan_VALUE = "haba_VALUE"; 서술 = "(Ljava/lang/String;)I"; sukat = 1; }
                else if (TAKE_Word("character_code_COUNT")) { pamamaraan_VALUE = "character_code_COUNT"; 서술 = "(Ljava/lang/String;)I"; sukat = 1; }
                else if (TAKE_Word("mag_parse_integer_buong_numero")) { pamamaraan_VALUE = "mag_parse_integer_buong_numero"; 서술 = "(Ljava/lang/String;)I"; sukat = 1; }
                else if (TAKE_Word("sumulat_integer_buong_numero_VALUE")) { pamamaraan_VALUE = "sumulat_integer_buong_numero_VALUE"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; sukat = 3; }
                else if (TAKE_Word("같음")) { pamamaraan_VALUE = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; sukat = 2; }
                else if (TAKE_Word("I_paste_SMS")) { pamamaraan_VALUE = "I_paste_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; sukat = 3; }
                else if (TAKE_Word("I_cut_VALUE")) { pamamaraan_VALUE = "I_cut_VALUE"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; sukat = 3; }
                else pagpalya_VALUE("unknown Korean text method");
            } else if (TAKE_Word("file")) {
                may_ari_VALUE = "한국어/자체/file"; 요구('.'); 가 = 3;
                if (TAKE_Word("읽기")) { pamamaraan_VALUE = "읽기"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; sukat = 3; }
                else if (TAKE_Word("sumulat")) { pamamaraan_VALUE = "sumulat"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else pagpalya_VALUE("unknown Korean file method");
            } else if (TAKE_Word("화면")) {
                may_ari_VALUE = "한국어/자체/화면"; 요구('.');
                if (TAKE_Word("너비")) { pamamaraan_VALUE = "너비"; 서술 = "()I"; sukat = 1; }
                else if (TAKE_Word("높이")) { pamamaraan_VALUE = "높이"; 서술 = "()I"; sukat = 1; }
                else if (TAKE_Word("사각형")) { pamamaraan_VALUE = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (TAKE_Word("burahin_pagpasok")) { pamamaraan_VALUE = "burahin_pagpasok"; 서술 = "(I)V"; 가 = 1; }
                else if (TAKE_Word("기다리기")) { pamamaraan_VALUE = "기다리기"; 서술 = "()V"; }
                else pagpalya_VALUE("unknown Korean framebuffer method");
            } else pagpalya_VALUE("unsupported Korean library class");
            요구('('); if (가 != 0) tiyakin_kumpirmahin_TYPE(expression_VALUE(), 가);
            if (나 != 0) { 요구(','); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 나); }
            if (다 != 0) { 요구(','); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 다); }
            if (라 != 0) { 요구(','); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 라); }
            if (마 != 0) { 요구(','); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 마); }
            요구(')'); utos(184, 외부참조(10, may_ari_VALUE, pamamaraan_VALUE, 서술)); return sukat;
        }
        if (TAKE_Word("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 3); 요구(')');
            utos(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int pangalan = tagakilala_VALUE();
        if (받기('(')) {
            int pormula_VALUE = -1;
            for (int 수 = 0; 수 < pamamaraan_COUNT; 수++) if (이름같음(pangalan, pamamaraan_pagpasok_pangalan[수])) pormula_VALUE = 수;
            if (pormula_VALUE < 0) { pagpalya_VALUE("unknown static method"); return 0; }
            int 수 = 0;
            while (!error && 종류() != ')') {
                if (수 >= pamamaraan_argumento_COUNT[pormula_VALUE]) { pagpalya_VALUE("too many arguments"); break; }
                tiyakin_kumpirmahin_TYPE(expression_VALUE(), pamamaraan_argumento_TYPE[pormula_VALUE * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != pamamaraan_argumento_COUNT[pormula_VALUE]) pagpalya_VALUE("argument count mismatch");
            utos(184, Sanggunian(10, kategorya_constant, Sanggunian(12, pamamaraan_pangalan_constant[pormula_VALUE], 함수서술[pormula_VALUE])));
            return 함수반환[pormula_VALUE];
        }
        int lokal_lawak = FIND_lokal(pangalan), TYPE_VALUE = lokal_TYPE[lokal_lawak]; 지역읽기(lokal_lawak);
        while (!error) {
            if (받기('[')) { tiyakin_kumpirmahin_TYPE(TYPE_VALUE, 4); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 1); 요구(']'); 내보내기(50); TYPE_VALUE = 3; }
            else if (받기('.')) {
                if (TYPE_VALUE == 6 || TYPE_VALUE == 7) {
                    String may_ari_VALUE = TYPE_VALUE == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (TAKE_Word("close")) { 요구('('); 요구(')'); utos(182, 외부참조(10, may_ari_VALUE, "close", "()V")); TYPE_VALUE = 0; }
                    else if (TYPE_VALUE == 6 && TAKE_Word("read")) { 요구('('); 요구(')'); utos(182, 외부참조(10, may_ari_VALUE, "read", "()I")); TYPE_VALUE = 1; }
                    else if (TYPE_VALUE == 7 && TAKE_Word("write")) { 요구('('); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 1); 요구(')'); utos(182, 외부참조(10, may_ari_VALUE, "write", "(I)V")); TYPE_VALUE = 0; }
                    else { pagpalya_VALUE("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (TYPE_VALUE == 4) { 내보내기(190); TYPE_VALUE = 1; }
                else { tiyakin_kumpirmahin_TYPE(TYPE_VALUE, 3); 요구('('); 요구(')'); utos(182, 외부참조(10, "java/lang/String", "length", "()I")); TYPE_VALUE = 1; }
            } else break;
        }
        return TYPE_VALUE;
    }
    static int 단항() {
        if (++식깊이 > 64) { pagpalya_VALUE("expression nesting too deep"); 식깊이--; return 0; }
        int TYPE_VALUE;
        if (받기('!')) { tiyakin_kumpirmahin_TYPE(단항(), 2); Paghahambing_VALUE(153); TYPE_VALUE = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(mag_parse_integer_buong_numero(posisyon++, true));
            else { tiyakin_kumpirmahin_TYPE(단항(), 1); 내보내기(116); }
            TYPE_VALUE = 1;
        } else if (받기('+')) { tiyakin_kumpirmahin_TYPE(단항(), 1); TYPE_VALUE = 1; }
        else TYPE_VALUE = 기본식();
        식깊이--; return TYPE_VALUE;
    }
    static int 곱식() {
        int TYPE_VALUE = 단항();
        while (!error && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int pag_encode_VALUE = 종류(); posisyon++; tiyakin_kumpirmahin_TYPE(TYPE_VALUE, 1); tiyakin_kumpirmahin_TYPE(단항(), 1);
            내보내기(pag_encode_VALUE == '*' ? 104 : pag_encode_VALUE == '/' ? 108 : 112); TYPE_VALUE = 1;
        }
        return TYPE_VALUE;
    }
    static int 합식() {
        int TYPE_VALUE = 곱식();
        while (!error && (종류() == '+' || 종류() == '-')) {
            int pag_encode_VALUE = 종류(); posisyon++; int 경계 = CODE_sukat, Bumalik_VALUE_TYPE = 곱식();
            if (pag_encode_VALUE == '+' && (TYPE_VALUE == 3 || Bumalik_VALUE_TYPE == 3)) { 결합(경계, TYPE_VALUE, Bumalik_VALUE_TYPE); TYPE_VALUE = 3; }
            else { tiyakin_kumpirmahin_TYPE(TYPE_VALUE, 1); tiyakin_kumpirmahin_TYPE(Bumalik_VALUE_TYPE, 1); 내보내기(pag_encode_VALUE == '+' ? 96 : 100); TYPE_VALUE = 1; }
        }
        return TYPE_VALUE;
    }
    static int 붙임참조(int TYPE_VALUE) {
        if (TYPE_VALUE != 1 && TYPE_VALUE != 2 && TYPE_VALUE != 3 && TYPE_VALUE != 5) pagpalya_VALUE("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", TYPE_VALUE == 1 ? "(I)Ljava/lang/StringBuilder;"
            : TYPE_VALUE == 2 ? "(Z)Ljava/lang/StringBuilder;" : TYPE_VALUE == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int nasa_harap_VALUE_TYPE, int Bumalik_VALUE_TYPE) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 RIGHT CODE_VALUE 앞에 mag_generate 코드를 삽입한다.
        // RIGHT expression_VALUE 내부의 peer_VALUE sanga 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = CODE_sukat;
        utos(187, Sanggunian(7, Word_constant("java/lang/StringBuilder"), 0)); 내보내기(89);
        utos(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); utos(182, 붙임참조(nasa_harap_VALUE_TYPE));
        if (error) return;
        int haba_VALUE = CODE_sukat - 끝;
        for (int 수 = 0; 수 < haba_VALUE; 수++) 삽입코드[수] = CODE_VALUE[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) CODE_VALUE[수 + haba_VALUE] = CODE_VALUE[수];
        for (int 수 = 0; 수 < haba_VALUE; 수++) CODE_VALUE[경계 + 수] = 삽입코드[수];
        utos(182, 붙임참조(Bumalik_VALUE_TYPE)); utos(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int Paghahambing_expression() {
        int TYPE_VALUE = 합식();
        while (!error && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int pag_encode_VALUE = 종류(); posisyon++; tiyakin_kumpirmahin_TYPE(TYPE_VALUE, 1); tiyakin_kumpirmahin_TYPE(합식(), 1);
            Paghahambing_VALUE(pag_encode_VALUE == '<' ? 161 : pag_encode_VALUE == '>' ? 163 : pag_encode_VALUE == 302 ? 164 : 162); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 동등식() {
        int TYPE_VALUE = Paghahambing_expression();
        while (!error && (종류() == 300 || 종류() == 301)) {
            int pag_encode_VALUE = 종류(); posisyon++; int Bumalik_VALUE_TYPE = Paghahambing_expression();
            if (TYPE_VALUE == 0 || Bumalik_VALUE_TYPE == 0) pagpalya_VALUE("void expression");
            if (!(integer_buong_numero_TYPE(TYPE_VALUE) && integer_buong_numero_TYPE(Bumalik_VALUE_TYPE))) tiyakin_kumpirmahin_TYPE(Bumalik_VALUE_TYPE, TYPE_VALUE);
            Paghahambing_VALUE((TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 159 : 165) + (pag_encode_VALUE == 301 ? 1 : 0)); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int 논리곱() {
        int TYPE_VALUE = 동등식();
        while (!error && 받기(304)) {
            tiyakin_kumpirmahin_TYPE(TYPE_VALUE, 2); int 가 = sanga(153); tiyakin_kumpirmahin_TYPE(동등식(), 2); int 나 = sanga(153);
            내보내기(4); int 끝 = sanga(167); Link_VALUE(가, CODE_sukat); Link_VALUE(나, CODE_sukat); 내보내기(3); Link_VALUE(끝, CODE_sukat); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static int expression_VALUE() {
        int TYPE_VALUE = 논리곱();
        while (!error && 받기(305)) {
            tiyakin_kumpirmahin_TYPE(TYPE_VALUE, 2); int 가 = sanga(154); tiyakin_kumpirmahin_TYPE(논리곱(), 2); int 나 = sanga(154);
            내보내기(3); int 끝 = sanga(167); Link_VALUE(가, CODE_sukat); Link_VALUE(나, CODE_sukat); 내보내기(4); Link_VALUE(끝, CODE_sukat); TYPE_VALUE = 2;
        }
        return TYPE_VALUE;
    }
    static void takdang_aralin_VALUE(boolean payagan_declaration) {
        if (Word_VALUE(posisyon, "int") || Word_VALUE(posisyon, "boolean") || Word_VALUE(posisyon, "String") || Word_VALUE(posisyon, "char")
            || Word_VALUE(posisyon, "FileInputStream") || Word_VALUE(posisyon, "FileOutputStream")) {
            if (!payagan_declaration) pagpalya_VALUE("declaration not allowed here");
            int TYPE_VALUE = format_VALUE(), pangalan = tagakilala_VALUE(); 요구('='); tiyakin_kumpirmahin_TYPE(expression_VALUE(), TYPE_VALUE);
            sumulat_lokal(idagdag_lokal(pangalan, TYPE_VALUE)); return;
        }
        int pangalan = tagakilala_VALUE(), lokal_lawak = FIND_lokal(pangalan);
        if (받기('=')) { tiyakin_kumpirmahin_TYPE(expression_VALUE(), lokal_TYPE[lokal_lawak]); sumulat_lokal(lokal_lawak); }
        else if (종류() >= 308 && 종류() <= 312) {
            int pag_encode_VALUE = 종류(); posisyon++; 지역읽기(lokal_lawak); int 경계 = CODE_sukat, Bumalik_VALUE_TYPE = expression_VALUE();
            if (pag_encode_VALUE == 308 && lokal_TYPE[lokal_lawak] == 3) 결합(경계, 3, Bumalik_VALUE_TYPE);
            else {
                tiyakin_kumpirmahin_TYPE(lokal_TYPE[lokal_lawak], 1); tiyakin_kumpirmahin_TYPE(Bumalik_VALUE_TYPE, 1);
                내보내기(pag_encode_VALUE == 308 ? 96 : pag_encode_VALUE == 309 ? 100 : pag_encode_VALUE == 310 ? 104 : pag_encode_VALUE == 311 ? 108 : 112);
                if (lokal_TYPE[lokal_lawak] == 5) 내보내기(146);
            }
            sumulat_lokal(lokal_lawak);
        }
        else if (종류() == 306 || 종류() == 307) {
            tiyakin_kumpirmahin_TYPE(lokal_TYPE[lokal_lawak], 1); 내보내기(132); 내보내기(lokal_lawak); 내보내기(종류() == 306 ? 1 : 255); posisyon++;
            if (lokal_TYPE[lokal_lawak] == 5) { 지역읽기(lokal_lawak); 내보내기(146); sumulat_lokal(lokal_lawak); }
        } else pagpalya_VALUE("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = TAKE_Word("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        utos(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean walang_laman_argumento = 종류() == ')';
        int TYPE_VALUE = walang_laman_argumento ? 0 : expression_VALUE(); 요구(')'); 요구(';');
        String 서술 = TYPE_VALUE == 0 ? "()V" : TYPE_VALUE == 1 ? "(I)V" : TYPE_VALUE == 2 ? "(Z)V" : TYPE_VALUE == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (TYPE_VALUE == 4 || TYPE_VALUE >= 6 || TYPE_VALUE == 0 && (!줄바꿈 || !walang_laman_argumento)) pagpalya_VALUE("unsupported print argument");
        utos(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean pahayag_VALUE() {
        if (error) return false;
        if (깊이 > 32) { pagpalya_VALUE("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!error && 종류() != '}') { if (반환) pagpalya_VALUE("unreachable statement"); 반환 = pahayag_VALUE(); }
            요구('}'); for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (TAKE_Word("return")) {
            int TYPE_VALUE = 종류() == ';' ? 0 : expression_VALUE(); tiyakin_kumpirmahin_TYPE(TYPE_VALUE, 함수반환[현재함수]); 요구(';');
            내보내기(TYPE_VALUE == 0 ? 177 : TYPE_VALUE <= 2 || TYPE_VALUE == 5 ? 172 : 176); return true;
        }
        if (TAKE_Word("if")) {
            요구('('); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 2); 요구(')'); int FALSE_VALUE = sanga(153);
            깊이++; boolean 가 = control_pahayag(); 깊이--;
            if (TAKE_Word("else")) { int 끝 = sanga(167); Link_VALUE(FALSE_VALUE, CODE_sukat); 깊이++; boolean 나 = control_pahayag(); 깊이--; Link_VALUE(끝, CODE_sukat); return 가 && 나; }
            Link_VALUE(FALSE_VALUE, CODE_sukat); return false;
        }
        if (TAKE_Word("while")) {
            int run = CODE_sukat; 요구('('); tiyakin_kumpirmahin_TYPE(expression_VALUE(), 2); 요구(')'); int 끝 = sanga(153);
            깊이++; control_pahayag(); 깊이--; Link_VALUE(sanga(167), run); Link_VALUE(끝, CODE_sukat); return false;
        }
        if (TAKE_Word("for")) {
            깊이++; 요구('('); if (종류() != ';') takdang_aralin_VALUE(true); 요구(';');
            int kondisyon = CODE_sukat; if (종류() == ';') 내보내기(4); else tiyakin_kumpirmahin_TYPE(expression_VALUE(), 2); 요구(';');
            int 끝 = sanga(153), teksto_ng_nilalaman = sanga(167), i_refresh = CODE_sukat;
            if (종류() != ')') takdang_aralin_VALUE(false); 요구(')'); Link_VALUE(sanga(167), kondisyon); Link_VALUE(teksto_ng_nilalaman, CODE_sukat);
            control_pahayag(); Link_VALUE(sanga(167), i_refresh); Link_VALUE(끝, CODE_sukat);
            for (int 수 = 0; 수 < lokal_COUNT; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Word_VALUE(posisyon, "System")) { 화면출력(); return false; }
        if (종류() == 256 && posisyon + 1 < token_COUNT && (토큰종류[posisyon + 1] == '(' || 토큰종류[posisyon + 1] == '.')) {
            int TYPE_VALUE = expression_VALUE(); if (TYPE_VALUE != 0) 내보내기(87); 요구(';'); return false;
        }
        takdang_aralin_VALUE(true); 요구(';'); return false;
    }
    static boolean control_pahayag() {
        if (Word_VALUE(posisyon, "int") || Word_VALUE(posisyon, "boolean") || Word_VALUE(posisyon, "char") || Word_VALUE(posisyon, "String")
            || Word_VALUE(posisyon, "FileInputStream") || Word_VALUE(posisyon, "FileOutputStream")) pagpalya_VALUE("local declaration requires braces");
        return pahayag_VALUE();
    }
    static void 출바(int VALUE) { if (출력크기 == 출력.length) pagpalya_VALUE("class file too large"); else 출력[출력크기++] = VALUE & 255; }
    static void 출짧(int VALUE) { 출바(VALUE >> 8); 출바(VALUE); }
    static void 출정(int VALUE) { 출짧(VALUE >>> 16); 출짧(VALUE); }
    static void sumulat_kategorya() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(constant_COUNT);
        for (int 수 = 0; 수 < constant_sukat; 수++) 출바(constant_VALUE[수]);
        출짧(0x21); 출짧(kategorya_constant); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(pamamaraan_COUNT);
        for (int 수 = 0; 수 < pamamaraan_COUNT; 수++) {
            출짧(pamamaraan_access[수]); 출짧(pamamaraan_pangalan_constant[수]); 출짧(함수서술[수]); 출짧(1); 출짧(CODE_constant);
            출정(12 + pamamaraan_haba[수]); 출짧(128); 출짧(함수지역[수]); 출정(pamamaraan_haba[수]);
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < pamamaraan_haba[수]; espasyo_pagpasok++) 출바(CODE_VALUE[pamamaraan_CODE[수] + espasyo_pagpasok]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int run() {
        if (gumagamit.인수개수() == 1 && 자바도구.같음(gumagamit.인수(0), "-version")) {
            gumagamit.sumulat("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (gumagamit.인수개수() != 1) { gumagamit.sumulat("Usage: javac FILE.java\n"); return 2; }
        int pangalan_sukat = 자바도구.pangalan(file_pangalan_SMS, gumagamit.인수(0));
        if (pangalan_sukat < 6 || pangalan_sukat > 62 || file_pangalan_SMS[pangalan_sukat - 5] != '.' || file_pangalan_SMS[pangalan_sukat - 4] != 'j'
            || file_pangalan_SMS[pangalan_sukat - 3] != 'a' || file_pangalan_SMS[pangalan_sukat - 2] != 'v' || file_pangalan_SMS[pangalan_sukat - 1] != 'a') {
            gumagamit.sumulat("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        pinagmulan_sukat = gumagamit.파일읽기(file_pangalan_SMS, pinagmulan);
        if (pinagmulan_sukat < 0) { gumagamit.sumulat("javac: cannot read source: "); 자바도구.수쓰기(pinagmulan_sukat); gumagamit.sumulat_karakter_VALUE(10); return 1; }
        pinagmulan_sukat = 자바도구.원문해독(pinagmulan, pinagmulan_sukat);
        if (pinagmulan_sukat < 0) { gumagamit.sumulat("javac error: invalid UTF-8 source\n"); return 1; }
        I_cut_VALUE(); if (!error) 선언읽기();
        if (!error) {
            if (token_haba[kategorya_token] != pangalan_sukat - 5) pagpalya_VALUE("class name must match file name");
            for (int 수 = 0; 수 < pangalan_sukat - 5; 수++) if (pinagmulan[token_posisyon[kategorya_token] + 수] != file_pangalan_SMS[수]) pagpalya_VALUE("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < pamamaraan_COUNT && !error; 현재함수++) {
            posisyon = pamamaraan_katawan[현재함수]; pamamaraan_CODE[현재함수] = CODE_sukat; lokal_COUNT = 0; 깊이 = 0;
            for (int 수 = 0; 수 < pamamaraan_argumento_COUNT[현재함수]; 수++) idagdag_lokal(pamamaraan_argumento_pangalan[현재함수 * 16 + 수], pamamaraan_argumento_TYPE[현재함수 * 16 + 수]);
            boolean 반환 = pahayag_VALUE();
            if (!반환 && 함수반환[현재함수] != 0) pagpalya_VALUE("missing return");
            // sanga 뒤의 합류 지점은 반드시 totoo_data 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean integer_buong_numero = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(integer_buong_numero ? 3 : 1); 내보내기(integer_buong_numero ? 172 : 176); }
            if (posisyon != pamamaraan_tapusin[현재함수]) pagpalya_VALUE("invalid method body");
            함수지역[현재함수] = lokal_COUNT; pamamaraan_haba[현재함수] = CODE_sukat - pamamaraan_CODE[현재함수];
        }
        if (error) return 1;
        sumulat_kategorya(); if (error) return 1;
        file_pangalan_SMS[pangalan_sukat - 4] = 'c'; file_pangalan_SMS[pangalan_sukat - 3] = 'l'; file_pangalan_SMS[pangalan_sukat - 2] = 'a';
        file_pangalan_SMS[pangalan_sukat - 1] = 's'; file_pangalan_SMS[pangalan_sukat] = 's'; file_pangalan_SMS[pangalan_sukat + 1] = 0;
        int sukat = gumagamit.sumulat_file(file_pangalan_SMS, 출력, 출력크기);
        if (sukat < 0) { gumagamit.sumulat("javac: cannot save class: "); 자바도구.수쓰기(sukat); gumagamit.sumulat_karakter_VALUE(10); return 1; }
        gumagamit.sumulat("Compiled: "); for (int 수 = 0; file_pangalan_SMS[수] != 0; 수++) gumagamit.sumulat_karakter_VALUE(file_pangalan_SMS[수]);
        gumagamit.sumulat(" (JVM class version 49)\n"); return 0;
    }
}
